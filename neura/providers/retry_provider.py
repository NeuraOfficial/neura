# -----------------------------------------------------------------------------
# Copyright [2025] [Krisna Pranav, Neura AI]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import random
from __future__ import annotations
from ..typing import Type, List, CreateResult, Messages, AsyncResult
from .types import BaseProvider, BaseRetryProvider, ProviderType
from .response import ImageResponse, ProviderInfo
from .. import debug
from ..errors import RetryProviderError, RetryNoProviderError

class IterListProvider(BaseRetryProvider):
    def __init__(self, providers: List[Type[BaseProvider]], shuffle: bool = True) -> None:
        self.providers = providers
        self.shuffle = shuffle
        self.working = True
        self.last_provider: Type[BaseProvider] = None

    def create_completion(self, model: str, messages: Messages, stream: bool = False, ignore_stream: bool = False, ignored: list[str] = [], **kwargs,) -> CreateResult:
        exceptions = {}
        started: bool = False

        for provider in self.get_providers(stream and not ignore_stream, ignored):
            self.last_provider = provider
            debug.log(f"Using {provider.__name__} provider")
            
            yield ProviderInfo(**provider.get_dict(), model=model if model else getattr(provider, "default_model"))
            
            try:
                response = provider.get_create_function()(model, messages, stream=stream, **kwargs)
                for chunk in response:
                    if chunk:
                        yield chunk
                        if isinstance(chunk, str) or isinstance(chunk, ImageResponse):
                            started = True
                if started:
                    return
            except Exception as e:
                exceptions[provider.__name__] = e
                debug.log(f"{provider.__name__}: {e.__class__.__name__}: {e}")
                if started:
                    raise e
                yield e

        raise_exceptions(exceptions)

    async def create_async_generator(self, model: str, messages: Messages, stream: bool = True, ignore_stream: bool = False, ignored: list[str] = [], **kwargs) -> AsyncResult:
        exceptions = {}
        started: bool = False

        for provider in self.get_providers(stream and not ignore_stream, ignored):
            self.last_provider = provider
            debug.log(f"Using {provider.__name__} provider")
            
            yield ProviderInfo(**provider.get_dict())
            
            try:
                response = provider.get_async_create_function()(model, messages, stream=stream, **kwargs)
                if hasattr(response, "__aiter__"):
                    async for chunk in response:
                        if chunk:
                            yield chunk
                            if isinstance(chunk, str) or isinstance(chunk, ImageResponse):
                                started = True
                elif response:
                    response = await response
                    if response:
                        yield response
                        started = True
                if started:
                    return
            except Exception as e:
                exceptions[provider.__name__] = e
                debug.log(f"{provider.__name__}: {e.__class__.__name__}: {e}")
                if started:
                    raise e
                yield e

        raise_exceptions(exceptions)

    def get_create_function(self) -> callable:
        return self.create_completion

    def get_async_create_function(self) -> callable:
        return self.create_async_generator

    def get_providers(self, stream: bool, ignored: list[str]) -> list[ProviderType]:
        providers = [p for p in self.providers if (p.supports_stream or not stream) and p.__name__ not in ignored]
        if self.shuffle:
            random.shuffle(providers)
        return providers

class RetryProvider(IterListProvider):
    def __init__(self, providers: List[Type[BaseProvider]], shuffle: bool = True, single_provider_retry: bool = False,max_retries: int = 3,) -> None:
        super().__init__(providers, shuffle)
        self.single_provider_retry = single_provider_retry
        self.max_retries = max_retries

    def create_completion(self, model: str, messages: Messages, stream: bool = False, **kwargs,) -> CreateResult:
        if self.single_provider_retry:
            exceptions = {}
            started: bool = False
            provider = self.providers[0]
            self.last_provider = provider
            
            for attempt in range(self.max_retries):
                try:
                    if debug.logging:
                        print(f"Using {provider.__name__} provider (attempt {attempt + 1})")
                    response = provider.get_create_function()(model, messages, stream=stream, **kwargs)
                    for chunk in response:
                        if isinstance(chunk, str) or isinstance(chunk, ImageResponse):
                            yield chunk
                            started = True
                    if started:
                        return
                except Exception as e:
                    exceptions[provider.__name__] = e
                    if debug.logging:
                        print(f"{provider.__name__}: {e.__class__.__name__}: {e}")
                    if started:
                        raise e
            raise_exceptions(exceptions)
        else:
            yield from super().create_completion(model, messages, stream, **kwargs)

    async def create_async_generator(self, model: str, messages: Messages, stream: bool = True, **kwargs) -> AsyncResult:
        exceptions = {}
        started = False

        if self.single_provider_retry:
            provider = self.providers[0]
            self.last_provider = provider
            for attempt in range(self.max_retries):
                try:
                    debug.log(f"Using {provider.__name__} provider (attempt {attempt + 1})")
                    response = provider.get_async_create_function()(model, messages, stream=stream, **kwargs)
                    if hasattr(response, "__aiter__"):
                        async for chunk in response:
                            if isinstance(chunk, str) or isinstance(chunk, ImageResponse):
                                yield chunk
                                started = True
                    else:
                        response = await response
                        if response:
                            yield response
                            started = True
                    if started:
                        return
                except Exception as e:
                    exceptions[provider.__name__] = e
                    if debug.logging:
                        print(f"{provider.__name__}: {e.__class__.__name__}: {e}")
            raise_exceptions(exceptions)
        else:
            async for chunk in super().create_async_generator(model, messages, stream, **kwargs):
                yield chunk
                
def raise_exceptions(exceptions: dict) -> None:
    if exceptions:
        raise RetryProviderError("RetryProvider failed:\n" + "\n".join([
            f"{p}: {type(exception).__name__}: {exception}" for p, exception in exceptions.items()
        ]))

    raise RetryNoProviderError("No provider found")
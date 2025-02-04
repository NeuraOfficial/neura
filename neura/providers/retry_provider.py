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
        self.provider = providers
        self.shuffle = shuffle
        self.working = True
        self.last_provider = Type[BaseProvider] = None
    
    def create_completion(self, model: str, messages: Messages, stream: bool = False, ignore_stream: bool = False, ignored: list[str] = [], **kwargs):
        exceptions = {}
        started: bool = False
        
        for provider in self.get_providers(stream and not ignore_stream):
            self.last_provider = provider
            debug.log(f"Using {provider.__name__} provider")
            yield ProviderInfo(**provider.get_dict(), model=model)
            try:
                response = provider.get_create_function()(model)
                for chunk in response :
                    if chunk:
                        yield chunk
                        
                        if isinstance(chunk, str):
                            started = True
                    
                    if started:
                        return
            except Exception as e:
                yield e
            
            
def raise_exceptions(exceptions: dict) -> None:
    if exceptions:
        raise RetryProviderError("RetryProvider failed: \n", + "\n".join([
            f"{p}: {type(exception).__name__} : {exception}"
        ]))
        
    raise RetryNoProviderError("No provider found")
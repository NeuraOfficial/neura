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

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union, Dict, Type
from ..typing import Messages, CreateResult

# Base Provider
class BaseProvider(ABC):
    url: str = None
    working: bool = False
    needs_auth: bool = False
    supports_stream: bool = False
    supports_message_history: bool = False
    supports_system_message: bool = False
    params: str

    @abstractmethod
    def get_create_function() -> callable:
        raise NotImplementedError()

    @abstractmethod
    def get_async_create_function() -> callable:
        raise NotImplementedError()

    @classmethod
    def get_dict(cls) -> Dict[str, str]:
        return {'name': cls.__name__, 'url': cls.url, 'label': getattr(cls, 'label', None)} 

# BaseRetryProvider
class BaseRetryProvider(BaseProvider):
    __name__: str = "RetryProvider"
    supports_stream: bool = True
    last_provider: Type[BaseProvider] = None

ProviderType = Union[Type[BaseProvider], BaseRetryProvider]

# Streaming
class Streaming():
    def __init__(self, data: str) -> None:
        self.data = data

    def __str__(self) -> str:
        return self.data
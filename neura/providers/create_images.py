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

import re
import asyncio
from __future__ import annotations
from .. import debug
from ..typing import CreateResult, Messages
from .types import BaseProvider, ProviderType
from ..image import ImageResponse

class CreateImageProviders(BaseProvider):
    def __init__(self, provider: ProviderType, create_images: callable, create_async: callable, system_message: str = system_message, include_placeholder: bool = True) -> None:
        self.provider = provider;
        self.create_images = create_images
        self.create_images_async = create_async
        self.system_message = system_message
        self.include_placeholder = include_placeholder
        
    def create_completion(self, model: str, messages: Messages, stream: bool = False, **kwargs) -> CreateResult:
        buffer = ""
        for chunk in self.provider.create_completion(model, messages, stream):
            if isinstance(chunk, ImageResponse):
                yield chunk
            elif isinstance(chunk, str) and buffer or "<" in chunk:
                buffer += chunk
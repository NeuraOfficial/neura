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

system_message = """
You can generate images, pictures, photos or img with the DALL-E 3 image generator.
To generate an image with a prompt, do this:

<img data-prompt=\"keywords for the image\">

Never use own image links. Don't wrap it in backticks.
It is important to use a only a img tag with a prompt.

<img data-prompt=\"image caption\">
"""

class CreateImagesProvider(BaseProvider):
    def __init__(self, provider: ProviderType, create_images: callable, create_async: callable, system_message: str = system_message, include_placeholder: bool = True) -> None:
        self.provider = provider
        self.create_images = create_images
        self.create_images_async = create_async
        self.system_message = system_message
        self.include_placeholder = include_placeholder
        self.__name__ = provider.__name__
        self.url = provider.url
        self.working = provider.working
        self.supports_stream = provider.supports_stream

    def create_completion(self, model: str, messages: Messages, stream: bool = False, **kwargs) -> CreateResult:
        messages.insert(0, {"role": "system", "content": self.system_message})
        buffer = ""
        for chunk in self.provider.create_completion(model, messages, stream, **kwargs):
            if isinstance(chunk, ImageResponse):
                yield chunk
            elif isinstance(chunk, str) and buffer or "<" in chunk:
                buffer += chunk
                if ">" in buffer:
                    match = re.search(r'<img data-prompt="(.*?)">', buffer)
                    if match:
                        placeholder, prompt = match.group(0), match.group(1)
                        start, append = buffer.split(placeholder, 1)
                        if start:
                            yield start
                        if self.include_placeholder:
                            yield placeholder
                        if debug.logging:
                            print(f"Create images with prompt: {prompt}")
                        yield from self.create_images(prompt)
                        if append:
                            yield append
                    else:
                        yield buffer
                    buffer = ""
            else:
                yield chunk

    async def create_async(self, model: str, messages: Messages, **kwargs) -> str:
        messages.insert(0, {"role": "system", "content": self.system_message})
        response = await self.provider.create_async(model, messages, **kwargs)
        matches = re.findall(r'(<img data-prompt="(.*?)">)', response)
        results = []
        placeholders = []
        
        for placeholder, prompt in matches:
            if placeholder not in placeholders:
                if debug.logging:
                    print(f"Create images with prompt: {prompt}")
                results.append(self.create_images_async(prompt))
                placeholders.append(placeholder)
                
        results = await asyncio.gather(*results)
        
        for idx, result in enumerate(results):
            placeholder = placeholder[idx]
            
            if self.include_placeholder:
                result = placeholder + result
            response = response.replace(placeholder, result)
            
        return response
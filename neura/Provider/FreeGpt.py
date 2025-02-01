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

import time
import hashlib
import random
from __future__ import annotations
from typing import AsyncGenerator, Optional, Dict, Any
from ..typing import Messages
from ..requests import StreamSession, raise_for_status
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..errors import RateLimitError

DOMAINS = [
    "https://s.aifree.site",
    "https://v.aifree.site/",
    "https://al.aifree.site/",
    "https://u4.aifree.site/"
]

RATE_LIMIT_ERROR_MESSAGE = "当前地区当日额度已消耗完"


class FreeGpt(AsyncGeneratorProvider, ProviderModelMixin):
    url = "https://freegptsnav.aifree.site"
    working = True
    supports_message_history = True
    supports_system_message = True
    default_model = 'gemini-1.5-pro'

    @classmethod
    async def create_async_generator(cls, model: str, messages: Messages, proxy: Optional[str] = None, timeout: int = 120, **kwargs: Any) -> AsyncGenerator[str, None]:
        prompt = messages[-1]["content"]
        timestamp = int(time.time())
        data = cls._build_request_data(messages, prompt, timestamp)
        domain = random.choice(DOMAINS)

        async with StreamSession(
            impersonate="chrome",
            timeout=timeout,
            proxies={"all": proxy} if proxy else None
        ) as session:
            async with session.post(f"{domain}/api/generate", json=data) as response:
                await raise_for_status(response)
                
                async for chunk in response.iter_content():
                    chunk_decoded = chunk.decode(errors="ignore")
                    
                    if chunk_decoded == RATE_LIMIT_ERROR_MESSAGE:
                        raise RateLimitError("Rate limit reached")
                    yield chunk_decoded

    @staticmethod
    def _build_request_data(messages: Messages, prompt: str, timestamp: int, secret: str = "") -> Dict[str, Any]:
        return {
            "messages": messages,
            "time": timestamp,
            "pass": None,
            "sign": generate_signature(timestamp, prompt, secret)
        }


def generate_signature(timestamp: int, message: str, secret: str = "") -> str:
    data = f"{timestamp}:{message}:{secret}"
    return hashlib.sha256(data.encode()).hexdigest()
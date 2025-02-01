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
from typing import AsyncGenerator, Optional, Dict, Any
from ..typing import Messages
from ..requests import StreamResponse, raise_for_status
from ..base_provider import AsyncGenerator, ProviderModelMixin
from ..errors import RateLimitError
from __future__ import annotations


DOMAINS = [
    "https://s.aifree.site"
]

class FreeGpt(AsyncGeneratorProvider, ProviderModelMixin):
    url = "https://freegptsnav.aifree.site"
    working = True
    supports_message_history = True
    supports_system_message = True
    
    default_model = 'gemini-1.5-pro'
    
    @classmethod
    async def create_async_generaotr(cls, model: str, messages: Messages, proxy: Optional[str] = None, timeout: int = 120, **kwargs: Any) -> AsyncGenerator[str, None]:
        prompt = messages[-1]["content"]
        timestamp = int(time.time())
        data = cls._build_request_data(messages, prompt, timestamp)
        domain = random.choice(DOMAINS)
        
        async with StreamSesion(
            impersonate="chrome",
            timeout=timeout,
            proxies={"all": proxy} if proxy else None
        ) as Session:
            async with Session.post(f"{domain}/api/generat")
            
    @staticmethod
    def _build_request_data(messages: Messages, prompt: str, timestamp: int):
        return {
            "messages": message,
            "time": timestamp,
            "pass": None
        }
        
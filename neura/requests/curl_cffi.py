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


import json
from __future__ import annotations
from curl_cffi.requests import AsyncSession, Response    
from typing import AsyncGenerator, Any
from functools import partialmethod

try:
    from curl_cffi.requests import CurlMime
    has_curl_mime = True
except ImportError:
    has_curl_mime = False

try:
    from curl_cffi.requests import CurlWsFlag
    has_curl_ws = True
except ImportError:
    has_curl_ws = False

class StreamResponse:
    def __init__(self, inner: Response) -> None:
        self.inner: Response = inner
    
    async def text(self) -> str:
        return await self.inner.atext()

    def raise_for_status(self) -> None:
        self.inner.raise_for_status()
    
    async def json(self, **kwargs) -> Any:
        return json.loads(await self.inner.acontent(), **kwargs)

    def iter_lines(self) -> AsyncGenerator[bytes, None]:
        return self.inner.aiter_lines()

    def iter_content(self) -> AsyncGenerator[bytes, None]:
        return self.inner.aiter_content()
    
    async def __aenter__(self):
        inner: Response = await self.inner
        self.inner = inner
        self.request = inner.request
        self.status: int = inner.status_code
        self.reason: str = inner.reason
        self.ok: bool = inner.ok
        
        return self

    async def __aexit__(self, *args):
        await self.inner.aclose()
        
class StreamSession(AsyncSession):
    def request(self, method: str, url: str, ssl = None, **kwargs) -> StreamResponse: 
        if isinstance(kwargs.get("data"), CurlMime):
            kwargs["multipart"] = kwargs.pop("data")
        
        return StreamResponse(super().request(method, url, stream=True, verify=ssl, **kwargs))
    
    def ws_connect(self, url, *args, **kwargs):
        return WebSocket(self, url, **kwargs)
        
        
        
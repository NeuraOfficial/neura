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
from aiohttp import ClientSession, ClientResponse, ClientTimeout, BaseConnector, FormData
from typing import AsyncIterator, Any, Optional
from .defaults import DEFAULT_HEADERS
from ..errors import MissingRequirementsError

class StreamResponse(ClientResponse):
    async def iter_lines(self) -> AsyncIterator[bytes]:
        async for line in self.content:
            yield line.rstrip(b"\r\n")
    
    async def iter_content(self) -> AsyncIterator[bytes]:
        async for chunk in self.content.iter_any():
            yield chunk
    
    async def json(self, content_type: str = None) -> Any:
        return await super().json(content_type=content_type)
    
class StreamSession(ClientSession):
    def __init__(self, headers: dict = {}, timeout: int = None, connector: BaseConnector = None, proxy: str = None, proxies: dict = {}, impersonate = None, **kwargs):
        if impersonate:
            headers = {
                **DEFAULT_HEADERS,
                **headers
            }
            
        connect = None
        
        if isinstance(timeout, tuple):
            connect, timeout = timeout;
        
        if timeout is not None:
            timeout = ClientTimeout(timeout, connect)
        
        if proxy is None:
            proxy = proxies.get("all", proxies.get("https"))
        
        super().__init__(**kwargs, timeout=timeout, response_class=StreamResponse, headers=headers)
        
        
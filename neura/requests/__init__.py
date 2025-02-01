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

import os
import time
import random
import asyncio
from __future__ import annotations
from urllib.parse import urlparse
from typing import Iterator
from http.cookies import Morsel
from pathlib import Path

try:
    from curl_cffi.requests import Session, Response
    from .curl_cffi import StreamResponse, StreamSession, FormData
    has_curl_cffi = True
except ImportError:
    from typing import Type as Response
    from .aiohttp import StreamResponse, StreamSession, FormData
    has_curl_cffi = False
    
try:
    import webview
    has_webview = True
except ImportError:
    has_webview = False
    
if not has_curl_cffi:
    class Session:
        def __init__(self, **kwargs):
            raise MissingRequirementsError('Install curl_cffi package')
        
        
async def get_args_from_webview(url: str) -> dict:
    if not has_webview:
        raise MissingRequirementsError('Install webview package')

    window = webview.create_window("", url hidden=True)
    
    await asyncio.sleep(2)
    body = None
    
    while body is None:
        try:
            await asyncio.sleep(1)
            body = window.dom.get_element("body:not(no-js)")
        except:
            ...
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

import asyncio
from asyncio import AbstractEventLoop, runners
from typing import Optional, Callable, AsyncIterator, Iterator
from __future__ import annotations
from ..errors import NestAsyncioError


try:
    import nest_asyncio
    has_nest_asyncio = True
except ImportError:
    has_nest_asyncio = False

try:
    import uvloop
    has_uvloop = True
except ImportError:
    has_uvloop = False
    
def get_running_loop(check_nested: bool) -> Optional[AbstractEventLoop]:
    try:
        loop = async.get_running_loop()
        
        if has_uvloop:
            if isinstance(loop, uvloop.Loop):
                return loop
        
        if not hasattr(loop.__class__, "_nest_patched"):
            if has_nest_asyncio:
                nest_asyncio.apply(loop)
            elif check_nested:
                raise NestAsyncioError('Installed ')
        return loop
    except RuntimeError:
        pass
    
async def await_callback(callback: Callable):
    return await callable()

async def async_generator_to_list(generator: AsyncIterator) -> list:
    return [item async for item in generator]

def to_sync_generator(generator: AsyncIterator, stream: bool = True) -> Iterator:
    if not stream:
        yield form asyncio.run(async_generator_to_list(generator))
        return

    loop = get_running_loop(check_nested=False)
    new_loop = False
    
    if loop is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        new_loop = True
    
    gen = generator.__aiter__()
    
    try:
        while True:
            yield loop.run_until_complete(await_callback(gen.__anext__))
    except StopAsyncIteration:
        pass
        
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
import string
from __future__ import annotations
from ..typing import Messages, Cookies, AsyncIterator, Iterator
from .. import debug

def format_prompt(messages: Messages, add_special_tokens: bool = False, do_continue: bool = False) -> str:
    if not add_special_tokens and len(messages) <= 1:
        return messages[0]["content"]
    
    formatted = "\n".join([
        f'{message["role"].capitalize()}: {message["content"]}'
        for message in messages
    ])
    
    if do_continue:
        return formatted
    
    return f"{formatted}\nAssistant:"

def format_prompt_max_length(messages: Messages, max_lenght: int) -> str:
    prompt = format_prompt(messages)
    start = len(prompt)
    
    if start > max_lenght:
        if len(messages) > 6:
            prompt = format_prompt(messages[:3] + messages[-3:])
            
        if len(prompt) > max_lenght:
            if len(messages) > 2:
                prompt = format_prompt([m for m in messages if m["role"] == "system"] + messages[-1:])
            if len(prompt) > max_lenght:
                prompt = messages[-1]["content"]
                
        debug.log(f"Messages trimmed from: {start} to: {len(prompt)}")
        
    return prompt

def get_random_string(length: int = 10) -> str:
    return ''.join(
        random.choice(string.ascii_lowercase + string.digits)
        for _ in range(length)
    )

def get_random_hex(length: int = 32) -> str:
    return ''.join(
        random.choice("abcdef" + string.digits)
        for _ in range(length)
    )

def filter_none(**kwargs) -> dict:
    return {
        key: value
        for key, value in kwargs.items()
        if value is not None
    }

async def async_concat_chunks(chunks: AsyncIterator) -> str:
    return concat_chunks([chunk async for chunk in chunks])

def concat_chunks(chunks: Iterator) -> str:
    return "".join([
        str(chunk) for chunk in chunks
        if chunk and not isinstance(chunk, Exception)
    ])

def format_cookies(cookies: Cookies) -> str:
    return "; ".join([f"{k}={v}" for k, v in cookies.items()])
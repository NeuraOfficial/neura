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
import json
from __future__ import annotations
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from abc import abstractmethod
from inspect import signature, Parameter
from typing import Optional, _GenericAlias
from pathlib import Path

try:
    from types import NoneType
except ImportError:
    NoneType = type(None)

from ..typing import CreateResult, AsyncResult, Messages
from .types import BaseProvider
from .asyncio import get_running_loop, to_sync_generator, to_async_iterator
from .response import BaseConversation, AuthResult
from .helper import concat_chunks, async_concat_chunks
from ..cookies import get_cookies_dir
from ..errors import ModelNotSupportedError, ResponseError, MissingAuthError, NoValidHarFileError
from .. import debug

SAFE_PARAMETERS = [
    "model", "messages", "stream", "timeout",
    "proxy", "images", "response_format",
    "prompt", "negative_prompt", "tools", "conversation",
    "history_disabled", "auto_continue",
    "temperature",  "top_k", "top_p",
    "frequency_penalty", "presence_penalty",
    "max_tokens", "max_new_tokens", "stop",
    "api_key", "api_base", "seed", "width", "height",
    "proof_token", "max_retries", "web_search",
    "guidance_scale", "num_inference_steps", "randomize_seed",
    "safe", "enhance", "private",
]

BASIC_PARAMETERS = {
    "provider": None,
    "model": "",
    "messages": [],
    "stream": False,
    "timeout": 0,
    "response_format": None,
    "max_tokens": None,
    "stop": None,
}

PARAMETER_EXAMPLES = {
    "proxy": "http://user:password@127.0.0.1:3128",
    "temperature": 1,
    "top_k": 1,
    "top_p": 1,
    "frequency_penalty": 1,
    "presence_penalty": 1,
    "messages": [{"role": "system", "content": ""}, {"role": "user", "content": ""}],
    "images": [["data:image/jpeg;base64,...", "filename.jpg"]],
    "response_format": {"type": "json_object"},
    "conversation": {"conversation_id": "550e8400-e29b-11d4-a716-...", "message_id": "550e8400-e29b-11d4-a716-..."},
    "max_new_tokens": 1024,
    "max_tokens": 4096,
    "seed": 42,
    "stop": ["stop1", "stop2"],
    "tools": [],
}
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
from .. import debug
from ..typing import Messages, Cookies, AsyncIterator, Iterator
from __future__ import annotations

def format_prompt(messages: Messages, add_special_tokens: bool = False, do_continue: bool = False) -> str:
    if not add_special_tokens and len(messages) <= 1:
        return messages[0]["context"]
    formatted = "\n".join([
        f'${messages["role"]}'
        for message in messages
    ])
    
    if do_continue:
        return formatted

    return f"{formatted}"
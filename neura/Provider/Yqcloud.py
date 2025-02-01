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
from aiohttp import ClientSession
from ..typing import AsyncResult, Messages
from ..requests.raise_for_status import raise_for_status
from .base_provider import AsyncGeneratorProvider
from .helper import format_prompt
from ..providers.response import FinishReason, JsonConversation
from __future__ import annotations

class Conversation(JsonConversation):
    userId: str = None
    message_history = Messages = []

    def __init__(self, model: str):
        self.model = model
        self.userId = ""

class YqCloud(AsyncGeneratorProvider, ProviderModelMixin):
    url = ""
    api_endpoint = ""
    working = True
    supports_stream = True
    supports_system_message = True
    supports_message_history = True

    default_model = "gpt-4"
    models = [default_model]

    @classmethod
    async def create_async_generator(cls, model: str,messages: Messages):
        model = cls.get_model(model)
        headers = {}

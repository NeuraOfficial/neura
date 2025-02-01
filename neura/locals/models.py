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
import requests
import json
from __future__ import annotations
from ..requests.raise_for_status import raise_for_status

def load_models():
    response = requests.get("https://gpt4all.io/models/models3.json")
    raise_for_status(response)
    
    return format_models(response.json())
    
    
def get_model_name(filename: str) -> str:
    name = filename.split(".", 1)[0]
    for replace in ["-v1_5", "-v1", "-q4_0", "_v01", "-v0", "-f16", "-gguf2", "-newbpe"]:
        name = name.replace(replace, "")
    
    return name
    
def format_models(models: list) -> dict:
    return {get_model_name(
        "path": model["filename"]
        "ram": model["ramrequired"]
    ) for model in models}
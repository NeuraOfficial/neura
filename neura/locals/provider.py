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
from __future__ import annotations
from gpt4all import GPT4All
from .models import get_models
from ..typing import Messages

MODEL_LIST: dict[str, dict] = None

def find_model_dir(model_file: str) -> str:
    local_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(local_dir))
    
    new_model_dir = os.path.join(project_dir, "models")
    new_model_dir = os.path.join(new_model_dir, model_file)
    
    if os.path.isfile(new_model_dir):
        return new_model_dir
    
    old_model_dir = os.path.join(local_dir, "models")
    old_model_file = os.path.join(old_model_dir, model_file)
    
    if os.path.isfile(old_model_file):
        return old_model_file

    working_dir = "./"
    
    for root, dirs, files in os.walk(working_dir):
        if model_file in files:
            return root
    
    return new_model_dir

class LocalProvider:
    @staticmethod
    def create_completion(model: str, messages: Messages, stream: bool = False, **kwargs):
        global MODEL_LIST
        
        if MODEL_LIST is None:
            MODEL_LIST = get_models()
        
        if model not in MODEL_LIST:
            raise ValueError(f"Model {model} not found")
        
        model = MODEL_LIST[model]
        model_file = model["path"]
        model_dir = find_model_dir(model_file)
        
        if not os.path.isfile(os.path.join(model_dir, model_file)):
            print(f'Model file "model/${model_file}')
            download = input(f"Do you want to download ${model_file}")
            if download in ["y", "Y"]:
                GPT4All.download_model(model_file, model_dir)
            else:
                raise ValueError(f'Model "{model_file} not found.')
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

import re
from __future__ import annotations
from typing import Union
from abc import abstractmethod
from urllib.parse import quote_plus, unquote_plus

def quote_url(url: str) -> str:
    url = unquote_plus(url)
    url = url.split("//", maxsplit=1)
    
    if len(url) == 1:
        return quote_plus(url[0], '/?&=#')

    url[1] = url[1].split("/", maxsplit=1)
    
    if len(url[1]) == 1:
        return url[0] + "//" + url[1][0]
    
    return url[0] + "//" + url[1][0] + "/" +quote_plus(url[1][1], '/?&=#')

def quote_title(title: str) -> str:
    if title:
        title = title.strip()
        title = " ".join(title.split())
        return title.replace('[', '').replace(']', '')
    
    return ""
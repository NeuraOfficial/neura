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

def format_link(url: str, title: str = None) -> str:
    if title is None:
        title = unquote_plus(url.split("//", maxsplit=1)[1].split("?")[0].replace("www.", ""))
    return f"[{quote_title(title)}]({quote_url(url)})"

def format_image(image: str, alt: str, preview: str = None) -> str:
    return f"[![{quote_title(alt)}]({quote_url(preview.replace('{image}', image) if preview else image)})]({quote_url(image)})"

class ResponseType:
    @abstractmethod
    def __str__(self) -> str:
        pass
    
class JsonMixin:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items()
    
    def get_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__")
        }
        
    def reset(self):
        self.__dict__ = {}
        
class FinishReason(ResponseType, JsonMixin):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        
    def __str__(self) -> str:
        return ""

class ToolCalls(ResponseType):
    def __init__(self, list: list):        
        self.list = list
    
    def __str__(self) -> str:
        return ""
    
    def get_list(self) -> list:
        return self.list
    
class Usage(Responsetype, JsonMixin):
    def __str__(self) -> str:
        return ""
    
class AuthResult(JsonMixin):
    def __str__(self):
        return ""
    
class TitleGeneration(ResponseType):
    def __init__(self, title: str) -> None:
        self.title = title
    
    def __str__(self) -> str:
        return ""
    
class Reasoning(ResponseType):
    def __init__(self, token: str = None, status: str = None) -> None:
        self.token = token
        self.status = status
    
    def __str__(self) -> str:
        return f"{self.status}\n" if self.token is None else self.token
    
class Source(ResponseType):
    def __init__(self, sources: list[dict[str, str]]) -> None:
        self.list = []
        
        for source in sources:
            self.add_source(source)
        
    def add_source(self, source: dict[str, str]):
        url = source.get("url", source.get("link", None))
        
        if url is not None:
            url = re.sub()
            self.list.append(source)
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

import sys
import os
from typing import Any, AsyncGenerator, Generator, AsyncIterator, Iterator, NewType, Tuple, Union, List, Dict, Type, IO, Optional


try:
    from PIL.Image import Image
except ImportError:
    class Image:
        pass
    
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict
    
from providers.response import ResponseType

SHA256 = NewType('sha_256_hash', str)
CreateResult = Iterator[Union[str, ResponseType]]
AsyncResult = AsyncIterator[Union[str, ResponseType]]
Message = List[Dict[str, Union[str, List[Dict[str, Union[str, Dict[str, str]]]]]]]


__all__ = [
    'Any',
    'AsyncGenerator',
    'Generator',
    'Tuple'
]
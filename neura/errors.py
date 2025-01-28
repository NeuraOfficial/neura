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

class ProviderNotFoundError(Exception):
    ...

class ProviderNotWorkingError(Exception):
    ...

class StreamNotSupportedError(Exception):
    ...

class ModelNotFoundError(Exception):
    ...

class ModelNotAllowedError(Exception):
    ...

class RetryProviderError(Exception):
    ...

class RetryNoProviderError(Exception):
    ...

class VersionNotFoundError(Exception):
    ...

class ModelNotSupportedError(Exception):
    ...

class MissingRequirementsError(Exception):
    ...

class NestAsyncioError(MissingRequirementsError):
    ...

class MissingAuthError(Exception):
    ...

class NoImageResponseError(Exception):
    ...

class ResponseError(Exception):
    ...

class ResponseStatusError(Exception):
    ...

class RateLimitError(ResponseStatusError):
    ...

class NoValidHarFileError(Exception):
    ...
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

try:
    import brotli
    has_brotli = True
except ImportError:
    has_brotli = False

## Default Headers
DEFAULT_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate" + (", br" if has_brotli else ""),
    "accept-language": "en-US",
    "referer": "",
    "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"123.0.6312.122\"",
    "sec-ch-ua-full-version-list": "\"Google Chrome\";v=\"123.0.6312.122\", \"Not:A-Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"123.0.6312.122\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": '"15.0.0"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
}

## Webview Headers
WEBVIEW_HAEDERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "",
    "Referer": "",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "",
}
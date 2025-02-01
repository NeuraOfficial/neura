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
import time
import json

try:
    from platformdirs import user_config_dir
    has_platformdirs = True
except ImportError:
    has_platformdirs = False
    
try:
    from browser_cookie3 import (
        chrome, chromium, opera, opera_gx, brave, edge, vivaldi, firefox, _LinuxPasswordManager, BrowserCookieError
    )

    has_browser_cookie3 = True 
except ImportError:
    has_browser_cookie3 = False
    browsers = []
    
    
class CookiesConfig():
    cookies: Dict[str, Cookies] = {}
    cookies_dict: str = "./har_and_cookies"
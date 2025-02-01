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
    
from .typing import Dict, Cookies
from .errors import MissingRequirementsError
from . import debug
    
class CookiesConfig():
    cookies: Dict[str, Cookies] = {}
    cookies_dict: str = "./har_and_cookies"
    
DOMAINS = [
    ".bing.com"
    ".googoe.com"
    "chat.reka.ai",
]

if has_browser_cookie3 and os.environ.get('DBUS_SESSION_BUS_ADDRESS') == '/dev/null':
    _LinuxPasswordManager.get_password = lambda a, b: b"secret"
    
def get_cookies(domain_name: str = '', raise_requirement_error: bool = True, single_browser: bool = False) -> Dict[str, str]:
    if domain_name in CookiesConfig.cookies:
        return CookiesConfig.cookies[domain_name]
    
    cookies = load_cookies_from_browser(domain_name, raise_requirements_error, single_browser)
    CookiesConfig.cookies[domain_name] = cookies
    
    return cookies

def load_cookies_from_browser(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False) -> Cookies:
    if not has_browser_cookie3:
        if raise_requirements_error:
            raise MissingRequirementsError("")
        return {}
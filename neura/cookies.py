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

def set_cookies(domain_name: str, cookies: Cookies = None) -> None:
    if cookies:
        CookiesConfig.cookies[domain_name] = cookies
    elif domain_name in CookiesConfig.cookies:
        CookiesConfig.cookies.pop(domain_name)

def load_cookies_from_browser(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False) -> Cookies:
    if not has_browser_cookie3:
        if raise_requirements_error:
            raise MissingRequirementsError("")
        
        return {}
    
        for cookie_fn in browsers:
            try:
                cookie_jar = cookie_fn(domain_name=domain_name)
                
                if len(cookie_jar) and debug.logging:
                    print(f"Read cookies from ${cookie_fn.__name__}")
                
                for cookie in cookie_jar:
                    if cookie.name not in cookies:
                        if not cookie.expires or cookie.expires > time.time():
                            cookies[cookie.name] = cookie.value
                
                if single_browser and len(cookie_jar):
                    break
            except BrowserCookieError:
                pass
            except Exception as e:
                if debug.logging:
                    print(f"Error")
                    
def set_cookies_dir(dir: str) -> None:
    CookiesConfig.cookies_dict = dir
    
def get_cookies_dir() -> str:
    return CookiesConfig.cookies_dir

def read_cookie_files(dirPath: str = None):
    dirPath = CookiesConfig.cookies_dict if dirPath is None else dirPath
    
    if not os.access(dirPath, os.R_OK):
        debug.log(f"Read cookies: ${dirPath}")
        return
    
    def get_domain(v: dict) -> str:
        host = [h["value"] for h in v['request']['headers'] if h["name"].lower() in ("host", ":authority")]
        
        if not host:
            return

        host = host.pop()
        
        for d in DOMAINS:
            if d in host:
                return d
    
    harFiles = []
    cookiesFiles = []
    
    for root, _, files in os.walk(dirPath):
        for file in files:
            if file.endswith(".har"):
                harFiles.append(os.path.join(root, file))
            elif file.endswith(".json"):
                cookiesFiles.append(os.path.join(root, file))
                
    CookiesConfig.cookies = {}
    
    for path in harFiles:
        with open(path, 'rb') as file:
            try:
                harFiles = json.load(file)
            except json.JSONDecodeError:
                continue
            
            debug.log(f"Read .har file: ${path}")
            new_cookies = {}
            
            for v in harFiles['log']['entries']:
                domain = get_domain(v)
                
                if domain is None:
                    continue
                    
                v_cookies = {}
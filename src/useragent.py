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
Python module to generate random useragents
'''

from random import randint, choice
from json import load
from os.path import dirname, abspath, join

with open(join(dirname(abspath(__file__)), 'files', 'agents.json'), buffering=(16*1024*1024)) as file:
    agents = load(file)

def getAgent() -> str:
    '''
    Creates the useragent
    '''

    browsers = ['chrome', 'firefox', 'opera', 'edge', 'explorer', 'brave']
    other = ['pyrequests','curl','wget']

    agent = ''
    if randint(0,3) != 1:

        i = randint(0,3)
        if i == 0: agent = f'Mozilla/{choice(agents["mozilla"])}'
        elif i == 1 or i == 2: agent = f'Opera/{choice(agents["operav"])}'
        else: agent = 'Mozilla/5.0'

        browser = choice(browsers)

        if browser != 'explorer':
            agent = f'{agent} ({choice(agents["os"])})'

        if 'Opera' in agent:
            browser = 'opera'
            agent = f'{agent} Presto/{choice(agents["presto"])} Version/{choice(agents["opera"])}'

        else:
            if browser in ['opera', 'firefox']: agent = f'{agent} Gecko/{choice(agents["gecko"])}'
            elif browser == 'explorer': agent = f'{agent} ({choice(agents["os"])} Trident/{str(randint(1, 7))}.0)'
            else: agent = f'{agent} AppleWebKit/{choice(agents["kits"])} (KHTML, like Gecko)'

        if 'Gecko' in agent and browser == 'opera': agent = f'{agent} Opera {choice(agents["opera"])}'
        if browser == 'chrome': agent = f'{agent} Chrome/{choice(agents["chrome"])} Safari/{choice(agents["safari"])}'
        elif browser == 'firefox': agent = f'{agent} Firefox/{choice(agents["firefox"])}'
        elif browser == 'edge': agent = f'{agent} Chrome/{choice(agents["chrome"])} Safari/{choice(agents["safari"])} Edge/{choice(agents["edge"])}'
        elif browser == 'brave': agent = f'{agent} Brave Chrome/{choice(agents["chrome"])} Safari/{choice(agents["safari"])}'
        else: pass

    else:
        agent = {
            'pyrequests': f'python-requests/{choice(agents["pyrequests"])}',
            'curl': f'Curl/{choice(agents["curl"])}',
            'wget': f'Wget/{choice(agents["wget"])}',
            'apt': choice([f'Debian APT-HTTP/{choice(["0","1"])}.{str(randint(1,9))} ({choice(agents["apt"])})', f'Debian APT-HTTP/{choice(["0","1"])}.{str(randint(1,9))} ({choice(agents["apt"])}) non-interactive'])
        }.get(choice(other))

    return agent
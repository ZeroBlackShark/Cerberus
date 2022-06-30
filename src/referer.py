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
Python module to generate random referers
'''

from random import randint, choice
from os.path import dirname, abspath, join

with open(join(dirname(abspath(__file__)), 'files', 'referers.txt'), buffering=(16*1024*1024)) as file:
    referers = file.read().split('\n')

def getReferer() -> str:
    '''
    Creates the random referer
    '''
    
    return choice([
        choice(['http://', 'https://']) +  '.'.join([str(randint(1,255)) for _ in range(4)]), # sadly we can't use utils().genip here, due to circular imports
        choice(referers).rstrip() # pick one from the referers.txt file
    ])
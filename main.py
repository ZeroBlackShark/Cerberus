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
    print('Error, it looks like i\'m missing some modules. Did you try "pip install -r requirements"?')
    print(f'Stacktrace: \n{str(e).rstrip()}')
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
    print('Error, failed to import standard library module.')
    print(f'Stacktrace: \n{str(e).rstrip()}')
    exit()

if sys.version_info[0] < 3 and sys.version_info[1] < 6:
    sys.exit('Error, please run Cerberus with Python 3.6 or higher.') # now that we've import sys, we can exit and print with a single function, awesome!

# import all custom modules from the "src" directory
try:
    from src.utils import * # import all utilities
    from src.core import * # import the "bridge", basically used to store variables editable by all core modules
    from src.database import * # database stuff
    from src.argparser import *
    from src.methods import *
except Exception as e:
    print('Error, failed to import core modules.')
    sys.exit(f'Stacktrace: \n{str(e).rstrip()}')

# initialize colorama
init(autoreset=True) # makes it so i don't need to do Fore.RESET at the end of every print()

utils().print_banner()
if len(sys.argv) <= 1: # no arguments? just show all logs

    print('\n'+utils().table([(row['timestamp'], row['identifier'], row['target'], row['attack_vector'], row['isrunning']) for row in database().get_logs(None)], ['Timestamp', 'ID', 'Target', 'Vector', 'Is running?']))

    print(f'\n\nTo view the commands, try this: python3 {sys.argv[0]} -h')
    print('\nTip: you can easily re-launch an attack by using the ID like this:')
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

    '''
    parser.add_argument('-t',   '--target',         dest = 'target',            metavar='target url', default = None,     help='Target URL (Example: https://google.com or http://fbi.gov)', type=str)
    parser.add_argument('-p',   '--port',           dest = 'port',              default = None,     help='Target port (Leave empty to let the tool decide)', type=str)
    parser.add_argument('-d',   '--duration',       dest = 'duration',          default = 10,       help='Attack duration', type=int)
    parser.add_argument(        '--proxy-file',     dest = 'proxy_file_path',   default = None,     help='File with proxies', type=str)
    parser.add_argument(        '--proxy',          dest = 'proxy',             default = None,     help='Use a proxy when attacking (Example: 127.0.0.1:1337)', type=str)
    parser.add_argument(        '--proxy-type',     dest = 'proxy_type',        default = 'SOCKS5', help='Set the proxy type (HTTP, SOCKS4 or SOCKS5)', type=str)
    parser.add_argument(        '--proxy-user',     dest = 'proxy_user',        default = None,     help='Proxy username', type=str)
    parser.add_argument(        '--proxy-pass',     dest = 'proxy_pass',        default = None,     help='Proxy password', type=str)
    parser.add_argument(        '--proxy-resolve',  dest = 'proxy_resolve',     default = True,     help='Resolve host using proxy (needed for hidden service targets)', action='store_true')
    parser.add_argument('-rt',  '--rotate-proxies', dest = 'rotate_proxies',    default = False,    help='Wether we should rotate proxies (use with --proxy-file)', action='store_true')
    parser.add_argument('-ua',  '--user-agent',     dest = 'useragent',         default = None,     help='User agent to use when attacking, else its dynamic', type=str)
    parser.add_argument('-ref', '--referer',        dest = 'referer',           default = None,     help='Referer to use when attacking, else its dynamic', type=str)
    parser.add_argument('-w',   '--workers',        dest = 'workers',           default = 100,      help='Amount of workers/threads to use when attacking', type=int)
    parser.add_argument('-dbg', '--debug',          dest = 'debug',             default = False,    help='Print info for devs', action='store_true')
    parser.add_argument('-bc',  '--bypass-cache',   dest = 'bypass_cache',      default = False,    help='Try to bypass any caching systems to ensure we hit the main site', action='store_true')
    parser.add_argument('-m',   '--method',         dest = 'method',            default = 'GET',    help='Method to use when attacking (default: GET)', type=str)
    parser.add_argument('-dfw', '--detect-firewall',dest = 'detect_firewall',   default = False,    help='Detect if the target site is protected by a firewall', action='store_true')
    parser.add_argument(        '--http-version',   dest = 'version',           default = '1.1',    help='Set the HTTP protocol version (default: 1.1)', type=str)
    parser.add_argument(        '--scrape-proxies', dest = 'scrape_proxies',    default = False,    help='Wether to scrape a list of proxies first (set the type using `--proxy-type`)', action='store_true')
    parser.add_argument(        '--check-proxies',  dest = 'check_proxies_file',default = None,     help='File with proxies to check', type=str)
    args = vars(parser.parse_args())
    '''

    # add arguments
    parser.add_argument('-t',       '--target-url',      action='store',      dest='target_url',      metavar="target url", type=str,  help="Target url to attack", default=None)
    parser.add_argument('-d',       '--attack-duration', action='store',      dest='duration',        metavar='duration',   type=int,  help='Attack length in seconds', default=100)
    parser.add_argument('-w',       '--workers',         action='store',      dest='workers',         metavar='workers',    type=int,  help='Number of threads/workers to spawn', default=40)
    parser.add_argument('-m',       '--method',          action='store',      dest='method',          metavar='method',     type=str,  help='Attack method/vector to use', default='GET')
    parser.add_argument('-logs',    '--list-logs',       action='store_true', dest='list_logs',                                        help='List all attack logs', default=False)
    parser.add_argument('-running', '--list-running',    action='store_true', dest='list_running',                                     help='List all running attacks', default=False)
    parser.add_argument('-methods', '--list-methods',    action='store_true', dest='list_methods',                                     help='List all the attack methods', default=False)
    parser.add_argument('-bc'       '--bypass-cache',    action='store_true', dest='bypass_cache',                                     help='Try to bypass any caching systems to ensure we hit the main servers', default=False)

    # Parse command line
    args = vars(parser.parse_args())

    if args['list_logs']:
        print('\n'+utils().table([(row['timestamp'], row['identifier'], row['target'], row['attack_vector'], row['bypass_cache'], row['isrunning']) for row in database().get_logs(None)], ['Timestamp', 'ID', 'Target', 'Method', 'Bypass cache?', 'Is running?']))

        print('\n\nTip: you can easily re-launch an attack by using the ID like this:')
        sys.exit(f'python3 {sys.argv[0]} --launch-from-id <attack id here>\n')
    
    if args['list_running']:
        print('\n'+utils().table([(row['timestamp'], row['identifier'], row['target'], row['attack_vector'], row['bypass_cache']) for row in database().get_logs(True)], ['Timestamp', 'ID', 'Target', 'Method', 'Bypass cache?']))

        print('\n\nTip: you can easily re-launch an attack by using the ID like this:')
        sys.exit(f'python3 {sys.argv[0]} --launch-from-id <attack id here>\n')


    if not args['target_url']: # check if the "-t/--target-url" argument has been passed
        sys.exit('\nPlease specify your target.\n')


    attack_method = args['method'].upper()
    if not attack_method in Core.methods.keys(): # if the method does not exist
        sys.exit(f'\nError, method "{attack_method}" does not exist.\n')
    
    print('Current attack configuration:')
    print(f'   - Target: {args["target_url"]}')
    print(f'   - Duration: {utils().Sec2Str(args["duration"])}')
    print(f'   - Workers: {str(args["workers"])}')
    print(f'   - Method/Vector: {args["method"]}')
    print(f'   - Cache bypass? {str(args["bypass_cache"])}')
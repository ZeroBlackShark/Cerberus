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

import re
from random import getrandbits
from binascii import hexlify
from netaddr import IPNetwork
from datetime import datetime, timedelta
from tabulate import tabulate

class utils():
    def   init  (self):
        # pre-compile the regex's, for performance
        self.ipv4regex = re.compile(r'(?m)^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        self.ipv6regex = re.compile(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')
        self.hostregex = re.compile(r'[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}')
        self.urlregex = re.compile(r'(http|https):\/\/([\w\- ]+(?:(?:\.[\w\- ]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?')

    def make_id(self) -> str:
        '''
        Helper function to make attack ID's
        '''

        return hexlify(getrandbits(128).to_bytes(16, 'little')).decode() # make a simple 32 characters long ID
    
    def valid_port(self, port: int) -> bool:
        '''
        Checks if the specified port is valid
        '''

        return port >= 0 and port < 65535 # 0 should be invalid, but since we count that as "random" we'll allow it
    
    def valid_ip(self, ip) -> bool:
        '''
        Checks if the specified IPv4/IPv6 address is valid
        '''

        if bool(self.ipv4regex.match(ip)):
            return True
        else:
            return bool(self.ipv6regex.match(ip))
        
    def cidr2iplist(self, cidrange) -> list:
        '''
        Converts a CID range to a list of IP's
        '''

        return [str(ip) for ip in IPNetwork(cidrange)]

    def unix2posix(self, timestamp) -> str:
        '''
        Converts the specified UNIX timestamp into a POSIX one
        '''

        return datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y, %H:%M:%S')
    
    def posix2unix(self, timestamp) -> float:
        '''
        Converts the specified POSIX timestamp into a UNIX one
        '''

        return datetime.timestamp(datetime.strptime(timestamp, "%m/%d/%Y, %H:%M:%S"))
    
    def table(self, rows, headers) -> str:
        '''
        Creates a nice looking table
        '''

        return tabulate(rows, headers=headers, tablefmt='simple')
    
    def Sec2Str(self, sec, hide=True) -> str: # found it on stackoverflow, cheers Timothy C. Quinn
        '''
        Turns seconds into days, hours, minutes and seconds and puts that into a single string
        '''

        td = timedelta(seconds=sec)
        def __t(t, n):
            if t < n: return (t, 0)
            v = t//n
            return (t -  (v * n), v)
            
        (s, h) = __t(td.seconds, 3600)
        (s, m) = __t(s, 60)    

        result = {
            'days': td.days,
            'hours': h,
            'minutes': m,
            'seconds': s,
        }

        result = ''
        #if td.weeks != 0: result += f'{td.weeks} {"weeks" if td.weeks != 1 else "week"}, '
        if td.days != 0: result += f'{td.days} {"days" if td.days != 1 else "day"}, '
        if h != 0: result += f'{h} {"hours" if h != 1 else "hour"}, '
        if m != 0: result += f'{m} {"minutes" if m != 1 else "minutes"}, '
        
        result += f'{s} {"seconds" if s != 1 else "second"}'

        return result
    
    def print_banner(self) -> None:
        '''
        Prints the banner
        '''

        print(r'''
                                  O*         oo                                  
                                 *@#*       *#@o                                 
                                °@#o@*     *@o#@°                                
                                O#@*#@o   o@#o@##                                
                               .@@#o##@###@##*##@.                               
                                #@##@@#@@@#@@##@#                                
                               .##@@@#@@#@@##@@##°                               
                               .######*###*O@####.                               
                   .°           #@##ooo###oooO#@#.          °                    
                 .o#@           .O@@#*°@#@°°#@@#.          .@O*.                 
             .*oO@@@#. ..*°      *#@@@O#@#o@@##o      °°.  .#@@#O*°.             
          .*#@@@@##@OO##@@O.    .#O#@#@@@@@##@O#°    .O@###oO@#@@@@#O°           
        °o#@@######Oo#@@##@#O°  O@#o###@@@##@OO@O  °o#@#@@@#o######@@@#*.        
       oo@#O##@@@@#O#@##@@#@@O o@#@#O@#####@#O@#@*.O@@#@###@#O#@#@@###@#O*       
      °o°O°###@@@####@@@@@###oo@#@#@O#@@@@@#o#####*o##@@@@@#####@@@#@O°O.o.      
      *#O°o@#@@@@###O@#@@@##o°###@@##OO####O#@#@##O.O##@@@@#O###@@@@#@**O#°      
     .#@#@@#@@@@@@@OO@#@@@@##*#@#@@@@#######@#@@#@#o##@@@@#@O#@@@@@@@#@@#@O      
    o@@#@@@@######O###@@@@#@O*@#@@@@@@@@@@@@#@@@@#@o#@#@@@@##OO#####@@@@@#@#*    
  .#@@@@####@@@@@#o###@@@@#@O°@#@@@@@@######@@@@@##°#@#@@@@###o#@@@@#####@@@@O   
 o@@@#O####@#######@@#@@@@@#@**@#@@@@@@@@@@@@@@@#@**@#@@@@@#@@@#####@@##O###@@#° 
.#@#####Oo°.      .°o@@#@@@###o#@#@@@@@@@@@@@@@#@#o##@@@@@@@o°.     .°*OO####@@#.
  °*oo°              °##@@@@#@#o#@#@@@@@@@@@@@#@#o@@@@@@###°             .*oo**  
                      #@#@#@@#@#o#@#@@@@@@@@@#@O*###@@@@#@#                      
                     °*O@#@####@O°o@##@@@@@##@o.#@#@####@O*.                     
                        O##@@@##@#°o@@#@@@#@@*.#@##@@@@@O                        
                         °.o##@@@@#**#@###@#**#@@@@@#o°°                         
                              °oO#@@O*O@@#o*O@@@#o°.                             
                                  °*oO**O**OO*°.''') # art made using https://image2ascii.com/
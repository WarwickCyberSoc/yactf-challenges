FROM ubuntu:20.04

RUN apt update && apt install -y socat python3 python3-pip && rm -rf /var/lib/apt/lists/*

RUN pip install pycryptodome

RUN mkdir /srv/vuln
ADD xortrick.py /srv/vuln
RUN chmod -R 755 /srv/vuln

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /srv/vuln

CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:'/usr/bin/python3 -u /srv/vuln/xortrick.py',stderr

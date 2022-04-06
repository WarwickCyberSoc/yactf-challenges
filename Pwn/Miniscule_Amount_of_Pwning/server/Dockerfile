FROM ubuntu:20.04

RUN apt update && apt install -y socat && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/vuln
ADD . /srv/vuln
RUN chmod -R 755 /srv/vuln

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /srv/vuln

EXPOSE 5000

CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:/srv/vuln/smallpwn,stderr

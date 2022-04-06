FROM ubuntu:20.04

# don't reuse this dockerfile for anything else, it's cursed

# dpkg --add-architecture i386 && apt update && apt install -y gcc socat libc6:i386 libncurses5:i386 libstdc++6:i386 && cd /mnt && gcc tictacpwn.c -o tictacpwn

RUN dpkg --add-architecture i386

RUN apt update && apt install -y socat libc6:i386 libncurses5:i386 libstdc++6:i386 && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/vuln
ADD tictacpwn /srv/vuln
ADD flag.txt /srv/vuln
RUN chmod -R 755 /srv/vuln

RUN touch /srv/vuln/leaderboard.txt
RUN chmod 755 /srv/vuln/tictacpwn && chmod 666 /srv/vuln/leaderboard.txt && chmod 644 /srv/vuln/flag.txt

RUN useradd -s /bin/bash wmg
USER wmg
WORKDIR /srv/vuln

EXPOSE 5000

CMD socat TCP-LISTEN:5000,fork,reuseaddr EXEC:/srv/vuln/tictacpwn,stderr

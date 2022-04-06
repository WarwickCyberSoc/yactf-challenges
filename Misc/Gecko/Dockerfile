FROM ubuntu:20.04

EXPOSE 4444

RUN apt update \
    && DEBIAN_FRONTEND=noninteractive apt install firefox sudo socat supervisor -y \
    && rm -rf /var/lib/apt/lists/*

RUN useradd gecko && mkdir /home/gecko && chown -R gecko:gecko /home/gecko
COPY files/geckodriver /home/gecko/geckodriver
RUN chown root:root /home/gecko/geckodriver && chmod a+x /home/gecko/geckodriver
COPY files/firefox.sh /usr/lib/firefox/firefox.sh
RUN chmod +x /usr/lib/firefox/firefox.sh

COPY files/flag.txt /flag.txt

COPY ./supervisord.conf /etc/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

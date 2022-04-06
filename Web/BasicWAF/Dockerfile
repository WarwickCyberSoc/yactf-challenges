FROM python:3.9

RUN python3 -m pip install flask supervisor

RUN mkdir /server
COPY ./files/ /server/
RUN chown -R root:root /server/ && chmod -R 655 /server/

COPY ./flag.txt /flag

RUN useradd -s /bin/bash wmg

COPY entrypoint.sh /entrypoint.sh
COPY supervisord.conf /etc/supervisord.conf
RUN chmod +x /entrypoint.sh

EXPOSE 8080

CMD ["/entrypoint.sh"]
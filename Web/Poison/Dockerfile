# docker build -t poison .
# docker run --rm -p1337:80 poison

FROM ubuntu:latest

EXPOSE 80

RUN apt update -y && DEBIAN_FRONTEND=noninteractive apt install php apache2 -y && rm -rf /var/lib/apt/lists/*
RUN echo "ServerName 0.0.0.0" >> /etc/apache2/apache2.conf

COPY ./www /var/www/html
RUN chown -R root:root /var/www/html && chmod -R 655 /var/www/html
RUN chmod a+r /var/log/apache2/
RUN chmod a+r /var/log/apache2/*
RUN chmod a+x /var/log/apache2/
RUN chmod a+x /var/log/apache2/*
RUN rm /var/www/html/index.html

COPY ./flag.txt /flag

EXPOSE 80
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["sh", "/entrypoint.sh"]

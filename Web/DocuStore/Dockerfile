FROM python:3.9

# Install latest chrome dev package and fonts to support major charsets (Chinese, Japanese, Arabic, Hebrew, Thai and a few others)
# Note: this installs the necessary libs to make the bundled version of Chromium that Puppeteer
# installs, work.
RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN cd /tmp \ 
    && wget https://github.com/exiftool/exiftool/archive/refs/tags/12.40.tar.gz -O exiftool.tar.gz \
    && tar -xvf exiftool.tar.gz \
    && cd exiftool-12.40 \
    && perl Makefile.PL \
    && make \
    && make test \
    && make install

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true

# Install Node
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash \
    && apt-get install nodejs -yq

RUN apt update && apt install -y nginx && rm -rf /var/lib/apt/lists/*

COPY ./supervisord.conf /etc/supervisord.conf
COPY ./nginx.conf /etc/nginx/sites-available/default

RUN mkdir /opt/challenge
COPY ./web /opt/challenge/web
COPY ./bot /opt/challenge/bot

RUN cd /opt/challenge/bot && npm ci
RUN pip install supervisor flask uwsgi pyexiftool

RUN chown -R www-data:www-data /opt/challenge/web

EXPOSE 5000

CMD ["/usr/local/bin/supervisord", "--nodaemon", "-c", "/etc/supervisord.conf"]
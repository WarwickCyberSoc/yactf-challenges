# docker build -t super_secure_admin_panel .
# docker run --rm -p1337:80 super_secure_admin_panel

FROM php:7.4-apache

RUN apt-get update && apt-get install -y \
    iproute2 \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) gd

COPY ./challenge /var/www/html
RUN chown -R root:root /var/www/html && chmod -R 655 /var/www/html

COPY ./flag.txt /flag.txt

EXPOSE 80

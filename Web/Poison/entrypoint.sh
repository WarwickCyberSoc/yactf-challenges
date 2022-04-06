#!/bin/ash

mv /flag /flag_`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 5 | head -n 1`

while true
do
apachectl -D FOREGROUND &
echo "" > /var/log/apache2/access.log
sleep 60
done
#!/bin/bash

mv /flag /flag_`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 5 | head -n 1`

supervisord -c /etc/supervisord.conf
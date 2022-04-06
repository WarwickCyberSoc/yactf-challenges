#!/usr/bin/bash
set -e 

cp ./challenge/flag.txt ./flag.txt.bak
echo "WMG{FakeFlag}" > ./challenge/flag.txt
zip -r bloghosters.zip challenge Dockerfile .dockerignore supervisord.conf -x "challenge/bot/node_modules/*" "challenge/web/__pycache__/*" "challenge/web/venv*" "challenge/database.db"
cp ./flag.txt.bak ./challenge/flag.txt 
rm ./flag.txt.bak
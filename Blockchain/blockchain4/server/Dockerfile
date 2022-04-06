# sudo docker build -t blockchain4 .
# sudo docker run -d -p 8000:8000 -p 8545:8545 blockchain4

FROM ubuntu:20.04

RUN apt update && apt install -y software-properties-common && rm -rf /var/lib/apt/lists/*
RUN add-apt-repository -y ppa:ethereum/ethereum && apt update && apt install -y ethereum python3 python3-pip supervisor && rm -rf /var/lib/apt/lists/*
RUN pip3 install py-solc-x requests web3

RUN mkdir /srv/eth
ADD . /srv/eth

RUN useradd -ms /bin/bash wmg
RUN chmod -R 755 /srv/eth
RUN chown -R wmg:wmg /srv/eth
USER wmg

RUN mkdir /srv/eth/net/http
RUN mkdir /srv/eth/net/sealer
RUN mkdir /srv/eth/net/victim
RUN head -c 16 /dev/urandom | base64 > /srv/eth/net/http/password
RUN head -c 16 /dev/urandom | base64 > /srv/eth/net/sealer/password
RUN head -c 16 /dev/urandom | base64 > /srv/eth/net/victim/password
RUN geth account new --lightkdf --datadir /srv/eth/net/http --password /srv/eth/net/http/password
RUN geth account new --lightkdf --datadir /srv/eth/net/sealer --password /srv/eth/net/sealer/password
RUN geth account new --lightkdf --datadir /srv/eth/net/victim --password /srv/eth/net/victim/password
RUN ls /srv/eth/net/http/keystore | cut -d - -f  9 > /srv/eth/net/http/address
RUN ls /srv/eth/net/sealer/keystore | cut -d - -f  9 > /srv/eth/net/sealer/address
RUN ls /srv/eth/net/victim/keystore | cut -d - -f  9 > /srv/eth/net/victim/address
RUN sed -i "s/http_address/$(cat /srv/eth/net/http/address)/g" /srv/eth/net/genesis.json
RUN sed -i "s/sealer_address/$(cat /srv/eth/net/sealer/address)/g" /srv/eth/net/genesis.json
RUN sed -i "s/victim_address/$(cat /srv/eth/net/victim/address)/g" /srv/eth/net/genesis.json
RUN geth init --datadir /srv/eth/net/http /srv/eth/net/genesis.json
RUN geth init --datadir /srv/eth/net/sealer /srv/eth/net/genesis.json
RUN geth init --datadir /srv/eth/net/victim /srv/eth/net/genesis.json

RUN mkdir /srv/eth/net/boot
RUN bootnode -genkey /srv/eth/net/boot/key
RUN bootnode -nodekey /srv/eth/net/boot/key -writeaddress > /srv/eth/net/boot/address

WORKDIR /srv/eth

CMD supervisord -c /srv/eth/supervisord/supervisord.conf

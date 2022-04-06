geth --lightkdf --ethash.cachesinmem 0 --ethash.dagsinmem 0 --cache 64 --bloomfilter.size 64 --datadir /srv/eth/net/sealer --networkid 42 --syncmode full --unlock "$(cat /srv/eth/net/sealer/address)" --password /srv/eth/net/sealer/password --bootnodes "enode://$(cat /srv/eth/net/boot/address)@127.0.0.1:30301" --port 30303 --mine --miner.gasprice 1

from json import dump
from pathlib import Path
from time import sleep

import requests
from solcx import compile_files, install_solc
from web3 import Web3
from web3.middleware import geth_poa_middleware

PROVIDER_URL = "http://localhost:8545"

# Wait for the provider node to start.
while True:
    try:
        if requests.get(PROVIDER_URL).status_code == requests.codes.OK:
            break
    except requests.exceptions.RequestException:
        pass

w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

with next(Path("/srv/eth/net/victim/keystore").iterdir()).open() as f:
    keystore = f.read().strip()

with Path("/srv/eth/net/victim/password").open() as f:
    password = f.read().strip()

account = w3.eth.account.from_key(w3.eth.account.decrypt(keystore, password))

install_solc("0.8.9")
_, compiled = compile_files(
    ["/srv/eth/victim/victim.sol"], solc_version="0.8.9"
).popitem()

with Path("/srv/eth/victim/public/abi.json").open("w") as f:
    dump(compiled["abi"], f)

contract = w3.eth.contract(abi=compiled["abi"], bytecode=compiled["bin"])

transaction = contract.constructor().buildTransaction(
    {
        "chainId": 42,
        "from": account.address,
        "gasPrice": 1,
        "nonce": w3.eth.get_transaction_count(account.address),
    }
)
transaction_signed = account.sign_transaction(transaction)
transaction_hash = w3.eth.sendRawTransaction(transaction_signed.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

with Path("/srv/eth/victim/public/transaction_receipt.json").open("w") as f:
    f.write(w3.toJSON(transaction_receipt))

Blockchain2 = w3.eth.contract(
    abi=compiled["abi"], address=transaction_receipt.contractAddress
)

event_filter = Blockchain2.events.Win.createFilter(fromBlock="latest")

while True:
    for _ in event_filter.get_new_entries():
        with Path("/srv/eth/victim/public/flag.txt").open("w") as f:
            f.write(
                "WMG{fc3d3e706146b2f6a909ad270a7544b97ea7dc1c38b3c793b8c4b3c14691d162}"
            )

        sleep(1)

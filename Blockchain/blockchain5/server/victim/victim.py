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


def transact(function):
    transaction = function.buildTransaction(
        {
            "chainId": 42,
            "from": account.address,
            "gasPrice": 1,
            "nonce": w3.eth.get_transaction_count(account.address),
        }
    )
    transaction_signed = account.sign_transaction(transaction)
    transaction_hash = w3.eth.sendRawTransaction(transaction_signed.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(transaction_hash)


install_solc("0.8.9")
for name, compiled in compile_files(
    [
        "/srv/eth/victim/AbstractStorage.sol",
        "/srv/eth/victim/StorageGet.sol",
        "/srv/eth/victim/StorageSet.sol",
    ],
    solc_version="0.8.9",
).items():
    contract = w3.eth.contract(abi=compiled["abi"], bytecode=compiled["bin"])

    transaction_receipt = transact(contract.constructor())

    if "AbstractStorage" in name:
        with Path("/srv/eth/victim/public/transaction_receipt.json").open("w") as f:
            f.write(w3.toJSON(transaction_receipt))

        abstract_storage_abi = compiled["abi"]
        abstract_storage_address = transaction_receipt.contractAddress

    if "StorageGet" in name:
        storage_get_abi = compiled["abi"]
        storage_get_address = transaction_receipt.contractAddress

    if "StorageSet" in name:
        storage_set_abi = compiled["abi"]
        storage_set_address = transaction_receipt.contractAddress

AbstractStorage = w3.eth.contract(
    abi=abstract_storage_abi
    + [i for i in storage_get_abi + storage_set_abi if i.get("name") in ("get", "set")],
    address=abstract_storage_address,
)

with Path("/srv/eth/victim/public/abi.json").open("w") as f:
    dump(AbstractStorage.abi, f)

# Implements get and set on AbstractStorage using StorageGet and StorageSet.
for signature, address in (
    ("get(uint32)", storage_get_address),
    ("set(uint32,bytes32)", storage_set_address),
):
    transact(
        AbstractStorage.functions.setImplementer(w3.keccak(text=signature)[:4], address)
    )

# Verifies that get and set are correctly implemented.
transact(AbstractStorage.functions.set(42, b"TEST" * 8))
assert AbstractStorage.functions.get(42).call() == b"TEST" * 8

event_filter = w3.eth.filter(
    {"address": abstract_storage_address, "topics": [w3.keccak(text="Win()").hex()]}
)

while True:
    for _ in event_filter.get_new_entries():
        with Path("/srv/eth/victim/public/flag.txt").open("w") as f:
            f.write(
                "WMG{8b00810a34afbbf0a1f5b5eaa12c8ac3910838bc5ab3410cd9ddcf986e7a77a8}"
            )

    sleep(1)

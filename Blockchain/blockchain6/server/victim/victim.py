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


install_solc("0.7.6")
for name, compiled in compile_files(
    ["/srv/eth/victim/Bank.sol", "/srv/eth/victim/BankAccount.sol"],
    solc_version="0.7.6",
).items():
    if "Bank.sol:BankAccount" in name:
        continue

    contract = w3.eth.contract(abi=compiled["abi"], bytecode=compiled["bin"])

    transaction_receipt = transact(contract.constructor())

    if name.endswith("Bank"):
        with Path("/srv/eth/victim/public/bank_abi.json").open("w") as f:
            dump(compiled["abi"], f)

        with Path("/srv/eth/victim/public/bank_transaction_receipt.json").open(
            "w"
        ) as f:
            f.write(w3.toJSON(transaction_receipt))

        bank_abi = compiled["abi"]
        bank_address = transaction_receipt.contractAddress

    if name.endswith("BankAccount"):
        with Path("/srv/eth/victim/public/bank_account_abi.json").open("w") as f:
            dump(compiled["abi"], f)

        with Path("/srv/eth/victim/public/bank_account_transaction_receipt.json").open(
            "w"
        ) as f:
            f.write(w3.toJSON(transaction_receipt))

        bank_account_abi = compiled["abi"]
        bank_account_address = transaction_receipt.contractAddress

Bank = w3.eth.contract(abi=bank_abi, address=bank_address)
BankAccount = w3.eth.contract(abi=bank_account_abi, address=bank_account_address)

transact(Bank.functions.setBalance(BankAccount.address, 1))
transact(BankAccount.functions.authorise("0x42426018276De6979B83ec860B284A2D77c34242"))
transact(BankAccount.functions.deauthorise(account.address))

while True:
    if Bank.functions.getBalance(BankAccount.address).call() > 1000:
        with Path("/srv/eth/victim/public/flag.txt").open("w") as f:
            f.write(
                "WMG{0f418995794fb4e36dc7c51992ee6b6b2c289a29f20ad511e93793195b163acf}"
            )

    sleep(1)

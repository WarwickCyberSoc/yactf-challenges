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

Blockchain1 = w3.eth.contract(
    abi=requests.get((f"{VICTIM_URL}/abi.json")).json(),
    address=requests.get((f"{VICTIM_URL}/transaction_receipt.json")).json()[
        "contractAddress"
    ],
)

print(Blockchain1.functions.flag().call())

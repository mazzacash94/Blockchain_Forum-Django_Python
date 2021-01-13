from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/cb3427bf216548ba96157079ddac0427'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print (f"L'indirizzo è {address}\n La chiave: {privateKey}")
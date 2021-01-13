from web3 import Web3

def sendTransaction(message):

    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/cb3427bf216548ba96157079ddac0427'))
    address = "0xD832b3482624cE9655944ac561Aa3C66089a7c68"
    privateKey = "0x688e8b387cce0f67b4cb92ae9483d489aa105dce226a017813ae39468fe7cba5"
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(

        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')

    ), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)

    return txId
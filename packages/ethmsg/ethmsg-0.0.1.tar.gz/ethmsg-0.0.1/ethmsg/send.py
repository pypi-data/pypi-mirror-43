import os
from pathlib import Path

os.environ["SOLC_BINARY"] = str(Path.home()) + "/.py-solc/solc-v0.4.25/bin/solc"

import json
import web3
from string import Template

from web3 import Web3
from solc import compile_source
from solc import install_solc

def send(endpoint, address, message):
    solcexec = Path(str(Path.home()) + "/.py-solc/solc-v0.4.25/bin/solc")
    if solcexec.is_file() == False:
        install_solc('v0.4.25')
    
    w3 = Web3(Web3.HTTPProvider(endpoint))
    private_key = os.environ["ETH_MSG_PRIVATE_KEY"]
    
    contract_source_code = '''
    pragma solidity ^0.4.21;
    
    contract Message {
      string public message;
    
      function message() public {
        message = '$message';
      }
    }
    '''

    contract_source_code = Template(contract_source_code).substitute({'message': message})
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:Message']
    
    nonce = w3.eth.getTransactionCount(address, 'pending')

    Message = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    
    tx = Message.constructor().buildTransaction({
        'from': address,
        'gas': w3.eth.estimateGas(Message.constructor().buildTransaction({'from': address})),
        'nonce': nonce,
        'gasPrice': w3.eth.gasPrice
    })
    
    signed_txn = w3.eth.account.signTransaction(tx, private_key=private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = w3.eth.waitForTransactionReceipt(tx_hash, 10000)

    print("Message saved to contract:")
    print(w3.eth.getTransactionReceipt(tx_hash)['contractAddress'])

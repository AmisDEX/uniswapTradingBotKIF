from web3 import Web3
from web3 import HTTPProvider
import json
import time
from var import keys
from var import contract_keys
# works
#web3 = Web3(Web3.HTTPProvider(keys["infura_url"]))
web3 = Web3(Web3.HTTPProvider("https://rpc.xdaichain.com"))

# uniswap contract 
uniswap_contract_abi = json.loads(contract_keys["uniswap_abi"])
uniswap_contract_address = Web3.toChecksumAddress(contract_keys["uniswap_address"])
uniswap_contract = web3.eth.contract(address=uniswap_contract_address, abi=uniswap_contract_abi)

# contracts used in path, eth->weth->amis and amis->weth->eth
weth_contract_abi = json.loads(contract_keys["weth_abi"])
weth_contract_address = Web3.toChecksumAddress(contract_keys["weth_token"])
weth_contract = web3.eth.contract(address=weth_contract_address, abi=weth_contract_abi)
amis_contract_abi = json.loads(contract_keys["amis_abi"])
amis_contract_address = Web3.toChecksumAddress(contract_keys["amis_token"])
amis_contract = web3.eth.contract(address=amis_contract_address, abi=amis_contract_abi)

# eth_out: the amount of eth you want to exchange for amis
# slippage: percentage tolerance for tokens in/out
# receiver: the receiving address of the final tokens
### this function turns your eth->weth->amis
def buy_amis(eth_out: int, slippage: float, receiver: str):
    path = [Web3.toChecksumAddress(contract_keys["weth_token"]), Web3.toChecksumAddress(contract_keys["amis_token"])] 
    amountOutMin = int(eth_out * get_price_eth_to_amis() * (1 - slippage) * 1000000000000000000)
    to = receiver
    deadline = web3.eth.getBlock("latest")["timestamp"] + 120 # added 120 seconds from when the transaction was sent
    txn = uniswap_contract.functions.swapExactETHForTokens(amountOutMin=amountOutMin, path=path, to=to, deadline=deadline).buildTransaction({
        'nonce': web3.eth.getTransactionCount(keys["my_account"]),
        'value': web3.toWei(eth_out, 'ether'),
        'gas': keys["gas_limit"],
        'gasPrice':web3.toWei(keys["gas_price"], 'gwei')})
    signed_tx = web3.eth.account.signTransaction(txn, keys["private_key"])
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print("buy successful")
    print("b one amis is worth this much eth: " + str(get_price_amis_to_eth()))
    
# amis_out: the amount of amis you want to exchange for eth
# slippage: percentage tolerance for tokens in/out
# receiver: the receiving address of the final tokens
### this function turns your amis->weth->eth
def sell_amis(amis_out: int, slippage: float, receiver: str):
    amountIn = amis_out
    amountOutMin = int(amis_out * get_price_amis_to_eth() * (1 - slippage) )
    path = [Web3.toChecksumAddress(contract_keys["amis_token"]), Web3.toChecksumAddress(contract_keys["weth_token"])] 
    to = receiver
    deadline = web3.eth.getBlock("latest")["timestamp"] + 20 # added 20 seconds from when the transaction was sent
    txn = uniswap_contract.functions.swapExactTokensForETH(amountIn=amountIn, amountOutMin=amountOutMin, path=path, to=to, deadline=deadline).buildTransaction({
        'nonce': web3.eth.getTransactionCount(keys["my_account"]),
        'value': web3.toWei(0, 'ether'),
        'gas': keys["gas_limit"],
        'gasPrice':web3.toWei(keys["gas_price"], 'gwei')})
    signed_tx = web3.eth.account.signTransaction(txn, keys["private_key"])
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print("sell successful")
    print("s one amis is worth this much eth: " + str(get_price_amis_to_eth()))

def get_price_amis_to_eth():
    univ2_amis_balance = amis_contract.functions.balanceOf(contract_keys["amis_weth_univ2_contract"]).call()
    univ2_weth_balance = weth_contract.functions.balanceOf(contract_keys["amis_weth_univ2_contract"]).call()
    return univ2_weth_balance / univ2_amis_balance

def get_price_eth_to_amis():
    univ2_amis_balance = amis_contract.functions.balanceOf(contract_keys["amis_weth_univ2_contract"]).call()
    univ2_weth_balance = weth_contract.functions.balanceOf(contract_keys["amis_weth_univ2_contract"]).call()
    return univ2_amis_balance / univ2_weth_balance

# lower_bound: the price point to trigger a buy, in terms of amis/eth
# upper_bound: the price point to trigger a sell, in terms of amis/eth
def run(lower_bound, upper_bound, holding=""):
    asset = holding
    while True:
        price = get_price_amis_to_eth()
        time.sleep(1)
        if price < lower_bound and asset != "amis":
            buy_amis((web3.eth.getBalance(keys["my_account"])*keys["percentage_of_eth"])/1000000000000000000, keys["slippage"], keys["receiver_account"])
            asset = "amis"
        elif price > upper_bound and asset != "eth":
            sell_amis(amis_contract.functions.balanceOf(keys["my_account"]).call(), keys["slippage"], keys["receiver_account"])
            asset = "eth"

print("r one amis is worth this much eth: " + str(get_price_amis_to_eth()))
run(0.035, 0.041)

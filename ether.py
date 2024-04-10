import logging
import time
from web3 import Web3

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

ethereum_rpc_url = 'https://sepolia.infura.io/v3/e205d9d8229c428fb246d3b7ccd0174a'  # Replace with your Infura project ID
ethereum_private_key = '4bdcb18e6f8e5fb9f6498bd00f89bf4514c69428b7fca504f67a074bf59fc71e'  # Replace with your Ethereum private key
web3_ethereum = Web3(Web3.HTTPProvider(ethereum_rpc_url))

def get_eth_balance(address: str) -> int:
    balance = web3_ethereum.eth.get_balance(address)
    return balance

def withdraw_all_eth(to_address: str) -> None:
    try:
        sender_account = "0x6b5e9A8d750077eF4B25e187f16b7f07Bc5eF603"  # Replace with the sender account address
        balance = get_eth_balance(sender_account)
        if balance > 0:
            nonce = web3_ethereum.eth.get_transaction_count(sender_account)
            
            # Reduce transaction value
            value_to_send = balance - 1000000000000000  # Example: Sending 0.001 Ether
            
            gas_price = web3_ethereum.eth.gas_price
            if gas_price is None:
                raise ValueError("Gas price is None")
            
            gas_limit = 21000  # Fixed gas limit for simple transactions
            estimated_gas = web3_ethereum.eth.estimate_gas({
                'to': to_address,
                'value': value_to_send,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
            tx_data = {
                'to': to_address,
                'value': value_to_send,
                'gas': estimated_gas,
                'gasPrice': gas_price,
                'nonce': nonce,
            }
            signed_tx = web3_ethereum.eth.account.sign_transaction(tx_data, private_key=ethereum_private_key)
            tx_hash = web3_ethereum.eth.send_raw_transaction(signed_tx.rawTransaction)
            logger.info(f"Withdrawal of Ethereum initiated. Transaction hash: {tx_hash.hex()}")
            check_transaction_status(tx_hash)
        else:
            logger.info("No Ethereum to withdraw.")
    except ValueError as ve:
        logger.error(str(ve))
    except Exception as e:
        logger.error(f"Error: {str(e)}")

def check_transaction_status(tx_hash: str) -> None:
    try:
        receipt = web3_ethereum.eth.wait_for_transaction_receipt(tx_hash)
        block_number = receipt['blockNumber']
        block_hash = receipt['blockHash']
        logger.info(f"Transaction mined in block: {block_number}\nBlock hash: {block_hash}")
    except Exception as e:
        logger.error(f"Error checking transaction status: {str(e)}")

def main() -> None:
    """Run the script."""
    recipient_address = '0xF3AC2253720ff69c34ba27584Cd10e9416001008'  # Replace with recipient address
    while True:
        withdraw_all_eth(recipient_address)
        time.sleep(5)

if __name__ == "__main__":
    main()

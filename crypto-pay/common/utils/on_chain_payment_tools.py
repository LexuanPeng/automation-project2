import json
import math
import logging
from decimal import Decimal
from eth_typing import HexStr
from web3 import Web3
from web3.middleware import geth_poa_middleware

logger = logging.getLogger(__name__)


class OnChainTestPaymentTools:
    decimal_map = {"TUSD": 18, "USDC": 18, "CRO": 8, "TGPB": 18, "ETH": 18, "USDT": 18, "CALVIN": 8}

    # Default for Ethereum Testnet Rinkeby
    def __init__(
        self, infura_url: str = "https://goerli.infura.io/v3/f96dfb6f34b240178fec535afede8296", chain_id: int = 5
    ):
        self.infura_url = infura_url
        self.chain_id = chain_id
        self.http_provider = Web3.HTTPProvider(infura_url)
        self.w3 = Web3(self.http_provider)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        f = open("common/utils/abi.json", mode="r")
        self.ABI = json.load(f)
        f.close()

    def get_balance(self, address: str):
        total_balance = self.w3.eth.get_balance(address)
        total_balance = self.w3.fromWei(total_balance, "ether")
        return total_balance

    def get_token_balance(self, address: str, contract_address: str):
        address = self.w3.toChecksumAddress(address)
        contract_address = self.w3.toChecksumAddress(contract_address)
        contract = self.w3.eth.contract(address=contract_address, abi=self.ABI)

        total_token_balances = contract.functions.balanceOf(address).call()
        total_token_balances = self.w3.fromWei(total_token_balances, "ether")
        token_name = contract.functions.name().call()
        decimal = contract.functions.decimals().call()

        return {total_token_balances, token_name, decimal}

    def on_chain_test_pay_by_eth(self, from_address: str, to_address: str, from_address_pk_key: str, amount: str):
        try:
            gas = self.w3.eth.estimateGas({"from": from_address})
            gas_price = self.w3.eth.gasPrice
            # if self.chain_id == 338:
            #     gas_price += 3100000000000

            right = int(math.pow(10, 18))
            amount = int(Decimal(round(Decimal(amount), 18)) * right)
            txn = {
                "to": to_address,
                "from": from_address,
                "chainId": self.chain_id,
                "value": amount,
                "gas": gas,
                "gasPrice": gas_price,
                "nonce": self.w3.eth.get_transaction_count(from_address),
            }
            logger.info(f"【Ready to on chain test pay by eth from {from_address} to {to_address} by {amount}】: {txn}")

            signed_txn = self.w3.eth.account.sign_transaction(
                txn,
                private_key=HexStr(from_address_pk_key),
            )
            self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tt = self.w3.toHex(self.w3.keccak(signed_txn.rawTransaction))
            rr = self.w3.eth.wait_for_transaction_receipt(tt, timeout=60 * 5, poll_latency=5)
            txn_id = rr["transactionHash"].hex()
            logger.info(f"【On chain test pay by eth from {from_address} to {to_address} by {amount}】{rr}")
            return txn_id
        except Exception as e:
            logger.error(e)
            raise e

    def on_chain_test_pay(
        self,
        from_address: str,
        from_contract_address: str,
        from_address_pk_key: str,
        to_address: str,
        amount: str,
        token_name: str = None,
    ):
        try:
            from_address = self.w3.toChecksumAddress(from_address)
            from_contract_address = self.w3.toChecksumAddress(from_contract_address)
            contract = self.w3.eth.contract(address=from_contract_address, abi=self.ABI)
            if token_name is None:
                token_name = contract.functions.name().call()
            decimal = contract.functions.decimals().call()
            right = int(math.pow(10, decimal))
            amount = int(Decimal(round(Decimal(amount), decimal)) * right)

            transaction = contract.functions.transfer(to_address, amount)
            gas = transaction.estimateGas({"from": from_address})
            gas_price = self.w3.eth.gas_price
            # if self.chain_id == 338:
            #     gas_price += 3100000000000

            txn = transaction.buildTransaction(
                {
                    "chainId": self.chain_id,
                    "gas": gas,
                    "gasPrice": gas_price,
                    "nonce": self.w3.eth.get_transaction_count(from_address),
                }
            )
            logger.info(
                f"【Ready to on chain test pay {token_name} from {from_address} to {to_address} by {amount}】: {txn}"
            )

            signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=HexStr(from_address_pk_key))
            contract.web3.eth.send_raw_transaction(signed_txn.rawTransaction)

            tt = self.w3.toHex(self.w3.keccak(signed_txn.rawTransaction))
            rr = self.w3.eth.wait_for_transaction_receipt(tt, timeout=60 * 5, poll_latency=5)
            txn_id = rr["transactionHash"].hex()
            logger.info(f"【On chain test pay from {from_address} to {to_address} by {amount}】{rr}")
            return txn_id
        except Exception as e:
            logger.error(e)
            raise e

    def get_txn_value(self, txn_id: str, token_name: str = "USDC"):
        try:
            t = self.w3.eth.get_transaction(HexStr(txn_id))

            if token_name == "NoneToken":
                value = int(t["value"])
                value = self.w3.fromWei(value, "ether")
                logger.info(f"【Get transaction by {txn_id} for {token_name}】: {value}")
                return value

            input_data = t["input"]
            contract = self.w3.eth.contract(address=t["to"], abi=self.ABI)
            decimal = contract.functions.decimals().call()
            right = int(math.pow(10, decimal))

            func_params = contract.decode_function_input(input_data)[1]
            value = Decimal(func_params["_value"] / right)
            logger.info(f"【Get token {token_name} transaction by {txn_id} 】:  {value}")
            return value
        except Exception as e:
            logger.warning(f"【We dont' find any transaction by {txn_id} for {token_name}】: {str(e)}")
            return None


def create_eth_account():
    from eth_account import Account
    import secrets

    private_key: str = secrets.token_hex(32)
    address: str = Account.from_key(private_key).address
    account_info = {"address": address, "private_key": private_key}
    logger.info(f"【Your eth account created】: {account_info}")
    return account_info

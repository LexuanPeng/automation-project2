import logging
from decimal import Decimal
from typing import Union

from bit import PrivateKey, PrivateKeyTestnet


logger = logging.getLogger(__name__)


class BtcTools:
    def __init__(self, network="testnet", wif: str = None):
        self.address = None
        self.network = network
        self.pub_key = None

        if wif is not None:
            self.key = self._new_key(wif)
            self.address = self.key.address
        else:
            self.key = None
        self.wif = wif

    def create_account(self):
        self.key = self._new_key()
        self.wif = self.key.to_wif()
        self.address = self.key.address
        self.pub_key = self.key.pub_to_hex()
        account_details = {"wif": self.wif, "address": self.address, "pub_key": self.pub_key}
        logger.info(f"Please save account details {account_details}")
        return account_details, self.key

    def get_balances(self, currency: str = "btc"):
        if self._check():
            return self.key.get_balance(currency)
        return None

    def send(self, to_address: str, currency: str, amount: Union[int, float, str, Decimal], **kwargs):
        if self._check():
            outputs = [(to_address, amount, currency)]
            txn = self.key.send(outputs=outputs, **kwargs)
            logger.info(f"Send {amount} {currency} from {self.address} to {to_address}, txn: {txn}")
            return txn
        return None

    def _check(self):
        if self.wif is None:
            logger.warning("WIF is required key to do all actions in BTC tools, Please make sure WIF was provided")
            return False
        return True

    def _new_key(self, wif: str = None):
        if self.network != "testnet":
            key = PrivateKey(wif)
        else:
            key = PrivateKeyTestnet(wif)
        return key

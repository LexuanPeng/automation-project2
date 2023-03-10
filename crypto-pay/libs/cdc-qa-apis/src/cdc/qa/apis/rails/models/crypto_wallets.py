from typing import List, Optional

from cdc.qa.apis.crypto_pay.models import FrozenBaseModel
from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models.common import Transaction, Wallet
from pydantic import Field


class CryptoWalletsTransactionsQueryParams(FrozenBaseModel):
    count: int = Field()
    currency: Optional[str] = Field()


class CryptoWalletsTransactionsResponse(RailsResponse):
    transactions: List[Transaction] = Field()


class CryptoWalletsShowQueryParams(FrozenBaseModel):
    currency: str = Field()


class CryptoWalletsShowResponse(RailsResponse):
    wallet: Wallet = Field()

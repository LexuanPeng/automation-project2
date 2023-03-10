from typing import List, Optional, Union
from decimal import Decimal
from cdc.qa.apis.exchange.models import ExchangeResponse, ExchangeSignedRequest, FrozenBaseModel
from pydantic import Field


class TransferHistoryDetail(FrozenBaseModel):
    direction: str = Field(description="Transfer direction into or out of Derivatives Wallet E.g. IN or OUT")
    time: int = Field(description="Transfer creation time (Unix timestamp)")
    amount: str = Field(description="Amount transferred")
    status: str = Field(description="Indicates status of the transfer")
    information: str = Field(description="Text description of the transfer in relation to the Spot Wallet")
    currency: str = Field(description="Currency E.g. BTC, USDT")


# private/deriv/get-transfer-history
class DerivGetTransferHistoryRequestParams(FrozenBaseModel):
    direction: str = Field(description="Transfer direction into or out of Derivatives Wallet E.g. IN or OUT")
    currency: Optional[str] = Field(default=None, description="Currency being transferred E.g. BTC or omit for 'all'")
    start_ts: Optional[int] = Field(default=None, description="Start timestamp", ge=0)
    end_ts: Optional[int] = Field(default=None, description="end timestamp", ge=0)
    page_size: Optional[int] = Field(default=None, description="Page size (Default: 20, Max: 200)", ge=0, le=200)
    page: Optional[int] = Field(default=None, description="Page number (0-based)", ge=0)


class DerivGetTransferHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/deriv/get-transfer-history"
    params: DerivGetTransferHistoryRequestParams = Field()


class DerivGetTransferHistoryResult(FrozenBaseModel):
    transfer_list: List[TransferHistoryDetail] = Field()


class DerivGetTransferHistoryResponse(ExchangeResponse):
    result: DerivGetTransferHistoryResult = Field()


# private/deriv/transfer
class DerivTransferRequestParams(FrozenBaseModel):
    currency: str = Field(description="Transfer currency, e.g. BTC, CRO")
    from_side: str = Field(description="SPOT or DERIVATIVES", alias="from")
    to: str = Field(description="SPOT or DERIVATIVES")
    amount: Union[str, int, Decimal] = Field(description="The amount to be transferred")


class DerivTransferRequestBody(ExchangeSignedRequest):
    method: str = "private/deriv/transfer"
    params: DerivTransferRequestParams = Field()


class DerivTransferResponse(ExchangeResponse):
    pass

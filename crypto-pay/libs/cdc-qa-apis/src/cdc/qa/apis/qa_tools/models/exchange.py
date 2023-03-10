from typing import List

from pydantic import Field

from ..base_models import FrozenBaseModel, QAToolResponse, QAToolSignedRequest


class APITransferRequestParams(FrozenBaseModel):
    env: str = Field(description="env: xdev/xsta")
    type: str = Field(description="type: email, spot_uuid")
    transfer_type: str = Field(description="transfer_type: DEBIT/CREDIT")
    value: str = Field(description="email address or spot uuid")
    currencys: List[str] = Field(description="currency list")
    amount: str = Field(description="amount")


class APITransferResponse(QAToolResponse):
    pass


class APITransferRequest(QAToolSignedRequest):
    method: str = "exchange/api_transfer/"
    params: APITransferRequestParams = Field()

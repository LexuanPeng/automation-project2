from pydantic import Field
from typing import List
from cdc.qa.apis.exchange.models import ExchangeResponse, FrozenBaseModel

"""
include API models:
public/margin/get-transfer-currencies
public/margin/get-loan-currencies
"""


class GetTransferCurrenciesResult(FrozenBaseModel):
    transfer_currency_list: List[str] = Field(description="consisting of transfer currencies. E.g. BTC, USDT, CRO.")


class GetTransferCurrenciesResponse(ExchangeResponse):
    result: GetTransferCurrenciesResult = Field(description="Get transfer currencies API result")


class GetLoanCurrenciesResult(FrozenBaseModel):
    loan_currency_list: List[str] = Field(description="consisting of loan currencies. E.g. BTC, USDT, CRO.")


class GetLoanCurrenciesResponse(ExchangeResponse):
    result: GetLoanCurrenciesResult = Field(description="Get loan currencies API result")

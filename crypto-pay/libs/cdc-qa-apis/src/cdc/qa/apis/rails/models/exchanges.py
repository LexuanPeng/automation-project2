from typing import Optional, List

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from pydantic import Field, validator
from .common import Balance, Quotation, Transaction


# --------------------------------- ExchangesQuotation --------------------------------- #
class ExchangesQuotationCreateRequestData(FrozenBaseModel):
    side: str = Field()
    to_amount: Optional[str] = Field()
    from_amount: Optional[str] = Field()
    from_side: str = Field(alias="from")
    to: str = Field()

    @validator("from_side")
    def from_side_must_upper_case(cls, v):
        if not v.isupper():
            v = v.upper()
        return v

    @validator("to")
    def to_must_upper_case(cls, v):
        if not v.isupper():
            v = v.upper()
        return v


class ExchangesQuotationCreateResponse(RailsResponse):
    quotation: Quotation = Field()


# --------------------------------- ExchangesCreate --------------------------------- #
class ExchangesCreateRequestData(RailsEncryptedPasscodeRequest):
    side: str = Field()
    quotation_id: str = Field()


class ExchangesCreateResponse(RailsResponse):
    class Transaction(FrozenBaseModel):
        id: int
        context: str
        nature: str
        kind: str
        description: str
        user_uuid: str
        rate: str
        rate_desc: str
        amount: Balance
        to_amount: Balance
        native_amount: Balance
        native_currency: str
        note: Optional[str]
        status: str
        created_at: str
        updated_at: str
        fee: Balance
        execute_rate: List[Balance]

    transaction: Transaction = Field()


# Transfer fund to exchange
class TransferFundToExchangeRequestData(RailsEncryptedPasscodeRequest):
    currency: str
    amount: str


class TransferFundToExchangeResponse(RailsResponse):
    transaction: Transaction

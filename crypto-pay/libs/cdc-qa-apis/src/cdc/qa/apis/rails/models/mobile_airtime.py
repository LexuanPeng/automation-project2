from typing import Optional, List
from decimal import Decimal
from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from cdc.qa.apis.rails.models.common import Balance, Quotation, Transaction

from pydantic import Field

# --------------------------------- MobileAirtimeTopupAmount --------------------------------- #


class MobileAirtimeRewardInfo(FrozenBaseModel):
    high: str
    low: str
    user: str


class MobileAirtimeTopups(FrozenBaseModel):
    terms_agreed: bool
    reward_info: MobileAirtimeRewardInfo = Field()


class MobileAirtimeAmountOption(FrozenBaseModel):
    local: Balance
    payment: Balance
    popular: bool


class MobileAirtimeCountryOperator(FrozenBaseModel):
    operator_id: int
    operator_name: str
    image_url: str
    country_code: str
    fx_rate: Decimal
    pin: bool
    amount_options: List[MobileAirtimeAmountOption]


class MobileAirtimeTopupAmountRequestData(FrozenBaseModel):
    recipient_phone: str


class MobileAirtimeTopupAmountResponse(RailsResponse):
    topups: MobileAirtimeTopups = Field()
    country_operators: List[MobileAirtimeCountryOperator]


# --------------------------------- MobileAirtimeOrder --------------------------------- #


class MobileAirtimeEstimatedReward(FrozenBaseModel):
    from_currency: str
    currency: str
    rate: str


class MobileAirtimeOrder(FrozenBaseModel):
    id: str
    status: str
    payment_uuid: str
    price: Balance
    to_price: Balance
    estimated_reward: MobileAirtimeEstimatedReward = Field


class MobileAirtimeOrderCreateRequestData(FrozenBaseModel):
    fx_rate: Decimal
    operator_id: int
    local_currency: str
    recipient_phone: str
    local_amount: str
    operator_name: str
    payment_currency: str
    payment_amount: str
    country_code: str


class MobileAirtimeOrderCreateResponse(RailsResponse):
    order: MobileAirtimeOrder = Field()


# --------------------------------- MobileAirtimeQuotation --------------------------------- #


class MobileAirtimeQuotationCreateRequestData(FrozenBaseModel):
    from_currency: str
    order_id: str
    otp: Optional[str]


class MobileAirtimeQuotationCreateResponse(RailsResponse):
    quotation: Quotation


# --------------------------------- MobileAirtimePayment --------------------------------- #


class MobileAirtimePaymentCreateRequestData(RailsEncryptedPasscodeRequest):
    quotation_id: str
    order_id: str


class MobileAirtimePaymentCreateResponse(RailsResponse):
    transaction: Transaction = Field()

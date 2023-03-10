from typing import Optional, Union

from cdc.qa.apis.crypto_pay.models import FrozenBaseModel
from pydantic import Field


class MetaData(FrozenBaseModel):
    customer_name: str = Field(default="Automation")
    customer_email: str = Field(default="automation@auto.com")


# Create payment API
class CreatePaymentRequestData(FrozenBaseModel):
    currency: str
    amount: str
    description: str
    order_id: str
    meta_data: MetaData
    delayed_capture: str = Field(default="false")
    expired_at: str = Field(default="")
    sub_merchant_id: Optional[str]
    whitelist_addresses: Optional[str]
    cancel_url: str = Field(default="https://google.com")


class CreatePaymentResponse(FrozenBaseModel):
    id: str
    amount: Union[str, float]
    amount_refunded: str
    created: int
    crypto_currency: str
    crypto_amount: str
    currency: str
    customer_id: Optional[str]
    data_url: str
    payment_url: str
    return_url: Optional[str]
    cancel_url: Optional[str]
    payment_url: str
    description: str
    live_mode: bool
    metadata: Optional[MetaData]
    order_id: str
    recipient: str
    refunded: bool
    status: str
    qr_code: str
    expired_at: Optional[str]
    sub_merchant_id: Optional[str]

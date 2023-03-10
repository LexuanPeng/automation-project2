from typing import Optional, List
from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from cdc.qa.apis.rails.models.common import Balance, Quotation, Transaction

from pydantic import Field

# --------------------------------- GiftCardBrands --------------------------------- #


class GiftCard(FrozenBaseModel):
    id: str
    name: str
    gift_card_type: str
    min_value: Optional[Balance]
    max_value: Optional[Balance]
    face_value: Optional[Balance]
    image_url: str
    status: str


class GiftCardBrand(FrozenBaseModel):
    class RewardInfo(FrozenBaseModel):
        high: str
        low: str

    id: str
    name: str
    category: str
    popular: bool
    image_url: str
    logo_image_url: str
    disclaimer: Optional[str]
    description: str
    reward_info: RewardInfo
    gift_card_type: Optional[str]
    out_of_stock: bool
    gift_cards: List[GiftCard]


class GiftCardBrandsQueryParams(FrozenBaseModel):
    country: str


class GiftCardBrandsResponse(RailsResponse):
    brands: List[GiftCardBrand]


# --------------------------------- GiftCardOrders --------------------------------- #


class GiftCardOrderRequestData(FrozenBaseModel):
    currency: str
    gift_card_id: str
    price: float
    country: str


class GiftCardOrderResponse(RailsResponse):
    class Order(FrozenBaseModel):
        id: str
        status: str
        gift_card_id: str
        payment_uuid: str
        country: str
        price: Balance
        to_price: Balance

    order: Order = Field()


# --------------------------------- GiftCardPaymentsQuotation --------------------------------- #


class GiftCardPaymentsQuotationRequestData(FrozenBaseModel):
    from_currency: str
    order_id: str
    otp: Optional[str]


class GiftCardPaymentsQuotationResponse(RailsResponse):
    quotation: Quotation = Field()


# --------------------------------- GiftCardPayments --------------------------------- #


class GiftCardPaymentsRequestData(RailsEncryptedPasscodeRequest):
    quotation_id: str
    order_id: str


class GiftCardPaymentsResponse(RailsResponse):
    transaction: Transaction = Field()

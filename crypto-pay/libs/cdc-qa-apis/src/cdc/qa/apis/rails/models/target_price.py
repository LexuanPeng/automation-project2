from typing import List, Optional
from pydantic import Field
from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from cdc.qa.apis.rails.models.common import Balance


# --------------------------------- MarketPrice --------------------------------- #


class MarketPrice(FrozenBaseModel):
    base_currency: Optional[str]
    quote_currency: Optional[str]
    quote_price: str
    timestamp: Optional[int]
    datetime: Optional[str]


class MarketPriceQueryParams(FrozenBaseModel):
    base_currency: str
    quote_currency: str


class MarketPriceResponse(RailsResponse):
    market_price: MarketPrice = Field()


# --------------------------------- OrderQuotation --------------------------------- #


class TargetPriceOrderQuotation(FrozenBaseModel):
    base: Balance
    expire_at: Optional[str]
    market_price: MarketPrice
    quote: Balance
    quote_price: str
    side: str


class TargetPriceOrderQuotationRequestData(FrozenBaseModel):
    side: str
    base_currency: str
    base_amount: str
    quote_currency: str
    quote_price: str


class TargetPriceOrderQuotationResponse(RailsResponse):
    order_quotation: TargetPriceOrderQuotation = Field()
    token: str


# --------------------------------- Order --------------------------------- #


class TargetPriceOrder(FrozenBaseModel):
    base: Balance
    created_at: str
    expire_at: Optional[str]
    external_id: str
    quote: Balance
    quote_price: str
    side: str
    status: str
    user_uuid: str


class TargetPriceOrderCreateRequestData(RailsEncryptedPasscodeRequest):
    external_id: str
    order_quotation_token: str


class TargetPriceOrderCreateResponse(RailsResponse):
    external_id: str


class TargetPriceOrderQueryParams(FrozenBaseModel):
    count: Optional[int]
    state: Optional[str]


class TargetPriceOrderResponse(RailsResponse):
    orders: List[TargetPriceOrder]

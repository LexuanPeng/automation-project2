from datetime import datetime
from decimal import Decimal
from typing import List
from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from cdc.qa.apis.rails.models.common import Balance

from pydantic import Field


class DustConversionOffer(FrozenBaseModel):
    currency: str
    estimated_amount: Decimal


class DustConversionOption(FrozenBaseModel):
    currency: str
    amount: Balance
    offers: List[DustConversionOffer]


class Dust(FrozenBaseModel):
    class DepositAmount(FrozenBaseModel):
        currency: str
        deposit_amount: Decimal

    currency: str
    amount: Balance
    deposit_amount: DepositAmount


class DustConversionOverviewResponse(RailsResponse):
    class ConversionOptions(FrozenBaseModel):
        conversion_options: List[DustConversionOption]

    dust_conversion_overview: ConversionOptions = Field()


class DustConversionOrderRequestData(FrozenBaseModel):
    dust_currencies: List[str] = Field()
    deposit_currency: str = Field()


class DustConversionOrderResponse(RailsResponse):
    class DustConversionOrder(FrozenBaseModel):
        id: str
        deposit_currency: str
        deposit_amount: Balance
        fee: Balance
        dusts: List[Dust]
        countdown: int
        expire_at: datetime

    dust_conversion_order: DustConversionOrder = Field()


class DustConversionCreateRequestData(RailsEncryptedPasscodeRequest):
    order_id: str = Field()


class DustConversionCreateResponse(RailsResponse):
    class DustConversion(FrozenBaseModel):
        id: str
        order_id: str
        deposit_currency: str
        deposit_amount: Balance
        fee: Balance
        dusts: List[Dust]

    dust_conversion: DustConversion = Field()

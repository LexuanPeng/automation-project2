from typing import List, Optional

from cdc.qa.apis.exchange.models import ExchangeResponse, ExchangeSignedRequest, FrozenBaseModel
from pydantic import Field


# private/otc/get-otc-user
class GetOTCUserRequestBody(ExchangeSignedRequest):
    method: str = "private/otc/get-otc-user"
    params: dict = {}


class GetOTCUserResult(FrozenBaseModel):
    account_uuid: str = Field(description="Account uuid")
    requests_per_minute: int = Field(description="Quote requests allowed per minute")
    max_trade_value_usd: str = Field(description="Maximum trade value in USD equivalent")
    min_trade_value_usd: str = Field(description="Minimum trade value in USD equivalent")
    accept_otc_tc_datetime: int = Field(description="Accepted terms and conditions timestamp (milliseconds since the)")


class GetOTCUserResponse(ExchangeResponse):
    result: GetOTCUserResult = Field()


# private/otc/get-instruments
class GetInstrumentsRequestBody(ExchangeSignedRequest):
    method: str = "private/otc/get-instruments"
    params: dict = {}


class OTCInstrumentDetail(FrozenBaseModel):
    instrument_name: str = Field(description="Name of instrument, e.g. BTC_USDT")
    base_currency: str = Field(description="Base currency of instrument, e.g. BTC, ETH")
    quote_currency: str = Field(description="Quote currency of instrument, e.g. USDT, USDC")
    base_currency_decimals: int = Field(description="Base currency decimals of instrument")
    quote_currency_decimals: int = Field(description="Quote currency decimals of instrument")
    base_currency_display_decimals: int = Field(description="Base currency display decimals of instrument")
    quote_currency_display_decimals: int = Field(description="Quote currency display decimals of instrument")
    tradable: bool = Field(description="true or false")


class GetInstrumentsResult(FrozenBaseModel):
    instrument_list: List[OTCInstrumentDetail] = Field()


class GetInstrumentsResponse(ExchangeResponse):
    result: GetInstrumentsResult = Field()


# private/otc/request-quote
class RequestQuoteRequestParams(FrozenBaseModel):
    base_currency: str = Field(description="Base currency, e.g. BTC, ETH")
    quote_currency: str = Field(description="Quote currency, e.g. USDT, USDC")
    base_currency_size: Optional[str] = Field(
        description="base currency size.Either base_currency_size or quote_currency_size"
    )
    quote_currency_size: Optional[str] = Field(
        description="quote currency size.Either base_currency_size or quote_currency_size"
    )
    direction: str = Field(description="BUY, SELL, TWO-WAY (returns price for both buy and sell")


class RequestQuoteRequestBody(ExchangeSignedRequest):
    method: str = "private/otc/request-quote"
    params: RequestQuoteRequestParams = Field(description="get quote params")


class RequestQuoteResult(FrozenBaseModel):
    quote_id: str = Field(description="Quote Id (used to accept quote)")
    quote_status: str = Field(description="- ACTIVE- EXPIRED (due to insufficient funds or below minimum trade value)")
    quote_direction: str = Field(description="BUY or SELL or TWO-WAY")
    base_currency: str = Field(description="Base currency, e.g. BTC, ETH")
    quote_currency: str = Field(description="Quote currency, e.g. USDT, USDC")
    base_currency_size: Optional[str] = Field(description="(optional) Base currency size requested")
    quote_currency_size: Optional[str] = Field(description="(optional) Quote currency size requested")
    quote_buy: str = Field(description="(optional) Price to buy base currency with quote currency")
    quote_buy_quantity: str = Field(description="(optional) Size of base currency to buy")
    quote_buy_value: str = Field(description="(optional) Size of quote currency to buy")
    quote_sell: str = Field(description="(optional) Price to sell base currency for quote currency")
    quote_sell_quantity: str = Field(description="(optional) Size of base currency to sell")
    quote_sell_value: str = Field(description="(optional) Size of quote currency to sell")
    quote_duration: int = Field(description="Quote valid for in seconds")
    quote_time: int = Field(description="Quote requested timestamp (milliseconds since the Unix epoch)")
    quote_expiry_time: int = Field(description="Quote expiry timestamp (milliseconds since the Unix epoch)")
    executable: Optional[bool] = Field(description="True or False")
    non_executable_reason: Optional[str] = Field(description="")


class RequestQuoteResponse(ExchangeResponse):
    result: Optional[RequestQuoteResult] = Field()


class OTCQuoteDetail(FrozenBaseModel):
    quote_id: str = Field(description="Quote Id (used to accept quote)")
    quote_status: str = Field(
        description="""- ACTIVE
                    - REJECTED
                    - EXPIRED
                    - FILLED
                    - PENDING (if PENDING does not resolve to FILLED or REJECTED contact support)"""
    )
    quote_direction: str = Field(description="BUY or SELL or TWO-WAY")
    base_currency: str = Field(description="Base currency, e.g. BTC, ETH")
    quote_currency: str = Field(description="Quote currency, e.g. USDT, USDC")
    base_currency_size: Optional[str] = Field(description="(optional) Base currency size requested")
    quote_currency_size: Optional[str] = Field(description="(optional) Quote currency size requested")
    quote_buy: str = Field(description="(optional) Price to buy base currency with quote currency")
    quote_sell: str = Field(description="(optional) Price to sell base currency for quote currency")
    quote_duration: int = Field(description="Quote valid for in seconds")
    quote_time: int = Field(description="Quote requested timestamp (milliseconds since the Unix epoch)")
    quote_expiry_time: int = Field(description="Quote expiry timestamp (milliseconds since the Unix epoch)")
    trade_direction: Optional[str] = Field(description="BUY or SELL")
    trade_price: Optional[str] = Field(description="Price quote executed at")
    trade_quantity: Optional[str] = Field(description="Traded quantity")
    trade_value: Optional[str] = Field(description="Traded value")
    trade_time: Optional[int] = Field(description="Quote accepted timestamp (milliseconds since the Unix epoch)")


# private/otc/accept-quote
class AcceptQuoteRequestParams(FrozenBaseModel):
    quote_id: str = Field(description="Quote Id from request quote")
    direction: Optional[str] = Field(description="BUY or SELL if requested quote using TWO-WAY")


class AcceptQuoteRequestBody(ExchangeSignedRequest):
    method: str = "private/otc/accept-quote"
    params: AcceptQuoteRequestParams = Field(description="accept quote params")


class AcceptQuoteResponse(ExchangeResponse):
    result: Optional[OTCQuoteDetail] = Field()


# private/otc/get-quote-history
class GetQuoteHistoryRequestParams(FrozenBaseModel):
    base_currency: Optional[str] = Field(description="Base currency, e.g. BTC, ETH or omit for 'all'")
    quote_currency: Optional[str] = Field(description="Quote currency, e.g. USDT, USDC or omit for 'all'")
    start_ts: Optional[int] = Field(description="Default is 24 hours ago from current timestamp")
    end_ts: Optional[int] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetQuoteHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/otc/get-quote-history"
    params: GetQuoteHistoryRequestParams = Field(description="accept quote params")


class GetQuoteHistoryResult(FrozenBaseModel):
    count: int = Field(description="count")
    quote_list: List[OTCQuoteDetail] = Field(description="quote detail")


class GetQuoteHistoryResponse(ExchangeResponse):
    result: GetQuoteHistoryResult = Field()


# private/otc/get-trade-history
class GetTradeHistoryRequestParams(FrozenBaseModel):
    base_currency: Optional[str] = Field(description="Base currency, e.g. BTC, ETH or omit for 'all'")
    quote_currency: Optional[str] = Field(description="Quote currency, e.g. USDT, USDC or omit for 'all'")
    start_ts: Optional[int] = Field(description="Default is 24 hours ago from current timestamp")
    end_ts: Optional[int] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetTradeHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/otc/get-trade-history"
    params: GetTradeHistoryRequestParams = Field(description="accept quote params")


class GetTradeHistoryResult(FrozenBaseModel):
    count: int = Field(description="count")
    trade_list: List[OTCQuoteDetail] = Field(description="quote detail")


class GetTradeHistoryResponse(ExchangeResponse):
    result: GetTradeHistoryResult = Field()

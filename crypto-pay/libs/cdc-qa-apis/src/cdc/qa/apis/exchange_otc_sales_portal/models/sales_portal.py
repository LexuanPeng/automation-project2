from typing import List, Optional

from pydantic import Field

from ..fe_sp_models import FrozenBaseModel, SalesPortalRequest, SalesPortalResponse


# fe-sp-api/get-otc-user
class GetOTCUserRequestParams(FrozenBaseModel):
    account_email: str = Field(description="account email")


class GetOTCUserRequestBody(SalesPortalRequest):
    method: str = "fe-sp-api/get-otc-user"
    params: GetOTCUserRequestParams = Field(description="get otc user params")


class OTCAccountDetail(FrozenBaseModel):
    accept_otc_tc_datetime: int = Field(description="Accepted terms and conditions timestamp (milliseconds since the)")
    account_uuid: str = Field(description="Spot account uuid")
    country_code: Optional[str] = Field()
    disabled: bool = Field(description="If true then user has no permission for OTC")
    email: Optional[str] = Field(description="(Optional) Email of account if institutional email will be blank string")
    label: Optional[str] = Field(description="(Optional) Label if sub account no label is master account")
    master_account_uuid: Optional[str] = Field(description="(Optional) Master account uuid if sub account")
    max_trade_amount_usd: Optional[str] = Field(description="Maximum trade value in USD equivalent")
    min_trade_amount_usd: Optional[str] = Field(description="Minimum trade value in USD equivalent")
    name: Optional[str] = Field(description="Account name")
    preferred_base_currency: Optional[str] = Field(description="User’s default base currency to display if set")
    preferred_quote_currency: Optional[str] = Field(description="User’s default quote currency to display if set")
    requests_per_minute: Optional[int] = Field(description="Number of quotes the user can make, 0 means not set")
    settlement_cycles_list: Optional[List[str]] = Field(description="Array of settlement cycle")
    trade_ahead: Optional[bool] = Field(description="Does user have trade ahead")
    user_tags: Optional[str] = Field()
    user_type: str = Field(description="INSTITUTIONAL or RETAIL")
    vip_tier: str = Field(description="1 | 2 | 3 |CUSTOM | NOT VIP")
    whitelisted: bool = Field(description="If the user can confirm the quote")


class GetOTCUserResult(FrozenBaseModel):
    account_list: List[OTCAccountDetail] = Field()
    count: int = Field(description="count")


class GetOTCUserResponse(SalesPortalResponse):
    result: GetOTCUserResult = Field()


# fe-sp-api/get-instruments
class GetInstrumentsRequestBody(SalesPortalRequest):
    method: str = "fe-sp-api/get-instruments"
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
    released_time: int = Field(description="Timestamp instrument is made tradable to public")


class GetInstrumentsResult(FrozenBaseModel):
    instrument_list: List[OTCInstrumentDetail] = Field()
    count: int = Field(description="count")


class GetInstrumentsResponse(SalesPortalResponse):
    result: GetInstrumentsResult = Field()


# fe-sp-api/get-quote
class SalesMarginTierDetail(FrozenBaseModel):
    quote_buy: str = Field(description="(optional) Price to buy base currency with quote currency")
    quote_buy_quantity: str = Field(description="(optional) Size of base currency to buy")
    quote_buy_value: str = Field(description="(optional) Size of quote currency to buy")
    quote_sell: str = Field(description="(optional) Price to sell base currency for quote currency")
    quote_sell_quantity: str = Field(description="(optional) Size of base currency to sell")
    quote_sell_value: str = Field(description="(optional) Size of quote currency to sell")
    sales_margin: str = Field(description="The margin in decimal format (need to multiply by 10000 to get basis point)")
    user_type: str = Field(description="INSTITUTIONAL | INDIVIDUAL")
    vip_tier: str = Field(description="101 | 102 | 103 |CUSTOM")


class GetQuoteRequestParams(FrozenBaseModel):
    base_currency: str = Field(description="Base currency, e.g. BTC, ETH")
    quote_currency: str = Field(description="Quote currency, e.g. USDT, USDC")
    base_currency_size: Optional[str] = Field(
        description="base currency size.Either base_currency_size or quote_currency_size"
    )
    quote_currency_size: Optional[str] = Field(
        description="quote currency size.Either base_currency_size or quote_currency_size"
    )
    direction: str = Field(description="BUY, SELL, TWO-WAY (returns price for both buy and sell")


class GetQuoteRequestBody(SalesPortalRequest):
    method: str = "fe-sp-api/get-quote"
    params: GetQuoteRequestParams = Field(description="get quote params")


class GetQuoteResult(FrozenBaseModel):
    base_currency: str = Field(description="Base currency, e.g. BTC, ETH")
    base_currency_size: Optional[str] = Field(description="(optional) Base currency size requested")
    client_quote_id: Optional[int] = Field()
    executable: Optional[bool] = Field(description="True or False")
    quote_buy: str = Field(description="(optional) Price to buy base currency with quote currency")
    quote_buy_quantity: str = Field(description="(optional) Size of base currency to buy")
    quote_buy_value: str = Field(description="(optional) Size of quote currency to buy")
    quote_currency: str = Field(description="Quote currency, e.g. USDT, USDC")
    quote_currency_size: Optional[str] = Field(description="(optional) Quote currency size requested")
    quote_direction: str = Field(description="BUY or SELL or TWO-WAY")
    quote_duration: int = Field(description="Quote valid for in seconds")
    quote_expiry_time: int = Field(description="Quote expiry timestamp (milliseconds since the Unix epoch)")
    quote_id: str = Field(description="Quote Id (used to accept quote)")
    quote_sell: str = Field(description="(optional) Price to sell base currency for quote currency")
    quote_sell_quantity: str = Field(description="(optional) Size of base currency to sell")
    quote_sell_value: str = Field(description="(optional) Size of quote currency to sell")
    quote_status: str = Field(description="- ACTIVE- EXPIRED (due to insufficient funds or below minimum trade value)")
    quote_time: int = Field(description="Quote requested timestamp (milliseconds since the Unix epoch)")
    sales_margin_tier_list: List[SalesMarginTierDetail] = Field()
    settlement_time: int = Field(description="Settlement due time")
    trade_ahead: bool = Field(description="Trade ahead")
    non_executable_reason: Optional[str] = Field(description="")


class GetQuoteResponse(SalesPortalResponse):
    result: Optional[GetQuoteResult] = Field()


# fe-sp-api/confirm-quote
class ConfirmQuoteDetail(FrozenBaseModel):
    base_currency: str = Field(description="Base currency, e.g. BTC, ETH")
    base_currency_size: Optional[str] = Field(description="(optional) Base currency size requested")
    client_quote_id: Optional[int] = Field()
    manual_booking: bool = Field()
    quote_buy: str = Field(description="(optional) Price to buy base currency with quote currency")
    quote_buy_raw: str = Field()
    quote_currency: str = Field(description="Quote currency, e.g. USDT, USDC")
    quote_currency_size: Optional[str] = Field(description="(optional) Quote currency size requested")
    quote_direction: str = Field(description="BUY or SELL or TWO-WAY")
    quote_duration: int = Field(description="Quote valid for in seconds")
    quote_expiry_time: int = Field(description="Quote expiry timestamp (milliseconds since the Unix epoch)")
    quote_id: str = Field(description="Quote Id (used to accept quote)")
    quote_sell_raw: str = Field(description="The price to sell without sales margin")
    quote_sell: str = Field(description="(optional) Price to sell base currency for quote currency")
    quote_status: str = Field(
        description="""- ACTIVE
                    - REJECTED
                    - EXPIRED
                    - FILLED
                    - PENDING (if PENDING does not resolve to FILLED or REJECTED contact support)"""
    )
    quote_time: int = Field(description="Quote requested timestamp (milliseconds since the Unix epoch)")
    sales_margin: str = Field(description="Sales margin")
    settlement_time: int = Field(description="Settlement due time")
    trade_ahead: bool = Field(description="Trade ahead")
    trade_direction: Optional[str] = Field(description="BUY or SELL")
    trade_price: Optional[str] = Field(description="Price quote executed at")
    trade_quantity: Optional[str] = Field(description="Traded quantity")
    trade_value: Optional[str] = Field(description="Traded value")
    trade_time: Optional[int] = Field(description="Quote accepted timestamp (milliseconds since the Unix epoch)")
    trade_settled: bool = Field(description="Trade settled")


class ConfirmQuoteRequestParams(FrozenBaseModel):
    quote_id: str = Field(description="Quote Id from request quote")
    quote: str = Field(description="(optional) Price to buy base currency with quote currency")
    sales_margin: str = Field(description="Sales margin")
    direction: Optional[str] = Field(description="BUY or SELL if requested quote using TWO-WAY")


class ConfirmQuoteRequestBody(SalesPortalRequest):
    method: str = "fe-sp-api/confirm-quote"
    params: ConfirmQuoteRequestParams = Field(description="confirm quote params")


class ConfirmQuoteResponse(SalesPortalResponse):
    result: Optional[ConfirmQuoteDetail] = Field()


class OTCQuoteDetail(FrozenBaseModel):
    account_email: str = Field(description="The otc user email")
    account_uuid: str = Field(description="The otc user uuid")
    base_currency: str = Field(description="Base currency, e.g. BTC, ETH")
    base_currency_size: Optional[str] = Field(description="(optional) Base currency size requested")
    manual_booking: bool = Field()
    quote_buy: str = Field(default=None, description="(optional) Price to buy base currency with quote currency")
    quote_buy_raw: Optional[str] = Field(description="The price to buy without sales margin")
    quote_channel: str = Field()
    quote_currency: str = Field(description="Quote currency, e.g. USDT, USDC")
    quote_currency_size: Optional[str] = Field(description="(optional) Quote currency size requested")
    quote_direction: str = Field(description="BUY or SELL or TWO-WAY")
    quote_duration: int = Field(description="Quote valid for in seconds")
    quote_expiry_time: int = Field(
        default=None, description="Quote expiry timestamp " "(milliseconds since the Unix epoch)"
    )
    quote_id: str = Field(description="Quote Id (used to accept quote)")
    quote_provider: str = Field()
    quote_sell_raw: Optional[str] = Field(description="The price to sell without sales margin")
    quote_sell: str = Field(default=None, description="(optional) Price to sell base currency for quote currency")
    quote_status: str = Field(
        description="""- ACTIVE
                    - REJECTED
                    - EXPIRED
                    - FILLED
                    - PENDING (if PENDING does not resolve to FILLED or REJECTED contact support)"""
    )
    quote_time: int = Field(description="Quote requested timestamp (milliseconds since the Unix epoch)")
    sales_email: str = Field(description="The sales user email")
    sales_id: str = Field(description="The sales user id")
    sales_margin: Optional[str] = Field(description="Sales margin")
    settlement_time: Optional[int] = Field(description="When trade is due for settlement")
    trade_ahead: bool = Field(description="Trade ahead")
    trade_direction: Optional[str] = Field(description="BUY or SELL")
    trade_price: Optional[str] = Field(description="Price quote executed at")
    trade_quantity: Optional[str] = Field(description="Traded quantity")
    trade_value: Optional[str] = Field(description="Traded value")
    trade_time: Optional[int] = Field(description="Quote accepted timestamp (milliseconds since the Unix epoch)")
    trade_settled: bool = Field(description="Trade settled")


# fe-sp-api/get-quote-history
class GetQuoteHistoryRequestParams(FrozenBaseModel):
    base_currency: Optional[str] = Field(description="Base currency, e.g. BTC or omit for 'all'")
    quote_currency: Optional[str] = Field(description="Quote currency, e.g. USDT, USDC or omit for 'all'")
    start_ts: Optional[int] = Field(description="Default is 24 hours ago from current timestamp")
    end_ts: Optional[int] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetQuoteHistoryRequestBody(SalesPortalRequest):
    method: str = "fe-sp-api/get-quote-history"
    params: GetQuoteHistoryRequestParams = Field(description="get quote history params")


class GetQuoteHistoryResult(FrozenBaseModel):
    count: int = Field(description="count")
    quote_list: List[OTCQuoteDetail] = Field(description="quote detail")


class GetQuoteHistoryResponse(SalesPortalResponse):
    result: GetQuoteHistoryResult = Field()


# fe-sp-api/get-trade-history
class GetTradeHistoryRequestParams(FrozenBaseModel):
    base_currency: Optional[str] = Field(description="Base currency, e.g. BTC, ETH or omit for 'all'")
    quote_currency: Optional[str] = Field(description="Quote currency, e.g. USDT, USDC or omit for 'all'")
    start_ts: Optional[int] = Field(description="Default is 24 hours ago from current timestamp")
    end_ts: Optional[int] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetTradeHistoryRequestBody(SalesPortalRequest):
    method: str = "fe-sp-api/get-trade-history"
    params: GetTradeHistoryRequestParams = Field(description="get trade history params")


class GetTradeHistoryResult(FrozenBaseModel):
    count: int = Field(description="count")
    trade_list: List[OTCQuoteDetail] = Field(description="quote detail")


class GetTradeHistoryResponse(SalesPortalResponse):
    result: GetTradeHistoryResult = Field()


# fe-sp-api/get-otc-user-balance
class GetOtcUserBalanceRequestBody(SalesPortalRequest):
    method: str = "fe-sp-api/get-otc-user-balance"
    params: dict = {}


class GetOtcUserBalanceResult(FrozenBaseModel):
    balance_list: dict = Field(description="balance detail")


class GetOtcUserBalanceResponse(SalesPortalResponse):
    result: GetOtcUserBalanceResult = Field()


# fe-sp-api/get-exchange-price
class GetExchangePriceRequestParams(FrozenBaseModel):
    symbol: str = Field(description="symbol. e.g: BTC_USDT")


class GetExchangePriceRequestBody(SalesPortalRequest):
    method: str = "fe-sp-api/get-exchange-price"
    params: GetExchangePriceRequestParams = Field()


class GetExchangePriceResult(FrozenBaseModel):
    instrument: str = Field(description="instrument name")
    price: str = Field(description="instrument price")
    timestamp: int = Field(description="timestamp")


class GetExchangePriceResponse(SalesPortalResponse):
    result: GetExchangePriceResult = Field()

from pydantic import Field, validator
from typing import Optional, List, Union
from decimal import Decimal
from ....models import FrozenBaseModel, ExchangeResponse, ExchangeRequest
from ...models import SubscribeResponse, SubscribeRequest


class SubscribeUserOrderInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeUserOrderInstrumentRequest(SubscribeRequest):
    params: SubscribeUserOrderInstrumentRequestParams = Field(...)


class SubscibeUserOrderInstrumentData(FrozenBaseModel):
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="(Optional) Client order ID if included in request")
    create_time: int = Field(description="Order creation time (Unix timestamp)")
    update_time: int = Field(description="Order update time (Unix timestamp)")
    status: str = Field(description="ACTIVE, CANCELED, FILLED, REJECTED or EXPIRED")
    reason: Optional[str] = Field(
        description="Reason code (see 'Response and Reason Codes') -- only for REJECTED orders"
    )
    type: str = Field(description="LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    side: str = Field(description="BUY or SELL")
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    price: Decimal = Field(description="Price specified in the order")
    quantity: Decimal = Field(description="Quantity specified in the order")
    cumulative_quantity: Decimal = Field(description="Cumulative executed quantity (for partially filled orders)", ge=0)
    cumulative_value: Decimal = Field(description="Cumulative executed value (for partially filled orders)", ge=0)
    avg_price: Decimal = Field(description="Average filled price. If none is filled, returns 0", ge=0)
    fee_currency: str = Field(description="Currency used for the fees (e.g. CRO)")
    time_in_force: str = Field(description="GOOD_TILL_CANCEL, FILL_OR_KILL or IMMEDIATE_OR_CANCEL")
    exec_inst: str = Field(description="Empty or POST_ONLY (Limit Orders Only)")
    trigger_price: Optional[Decimal] = Field(description="Used for trigger-related orders")


class OrderDetail(FrozenBaseModel):
    status: str = Field(description="ACTIVE, CANCELED, FILLED, REJECTED or EXPIRED")
    reason: Optional[str] = Field(
        description="Reason code (see 'Response and Reason Codes') -- only for REJECTED orders"
    )
    side: str = Field(description="BUY, SELL")
    price: Decimal = Field(description="Price specified in the order")
    quantity: Decimal = Field(description="Quantity specified in the order")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="(Optional) Client order ID if included in request")
    create_time: int = Field(description="Order creation time (Unix timestamp)")
    update_time: int = Field(description="Order update time (Unix timestamp)")
    type: str = Field(description="LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    cumulative_quantity: Decimal = Field(description="Cumulative executed quantity (for partially filled orders)")
    cumulative_value: Decimal = Field(description="Cumulative executed value (for partially filled orders)")
    avg_price: Decimal = Field(description="Average filled price. If none is filled, returns 0")
    fee_currency: str = Field(description="Currency used for the fees (e.g. CRO)")
    time_in_force: str = Field(description="GOOD_TILL_CANCEL, FILL_OR_KILL, IMMEDIATE_OR_CANCEL")
    exec_inst: str = Field(description="Empty or POST_ONLY (Limit Orders Only)")
    trigger_price: Optional[Decimal] = Field(description="Used for trigger-related orders")


class SubscribeUserOrderInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    subscription: str = Field(description="user.order.{instrument_name} -- even in the all case")
    channel: str = Field(description="user.order")
    data: List[SubscibeUserOrderInstrumentData] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"user.order.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.order", f"channel expect:[user.order] actual:[{v}]!"
        return v


class SubscribeUserOrderInstrumentResponse(SubscribeResponse):
    result: SubscribeUserOrderInstrumentResponseResult = Field()


# private/create-order
class PrivateCreateOrderRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="instrument name e.g. BTC_USDT, etc.")
    side: str = Field(description="BUY, SELL")
    type: str = Field(description="LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    price: str = Field(default=None, description="For LIMIT and STOP_LIMIT orders only: Unit price")
    quantity: str = Field(
        description="For LIMIT Orders, MARKET (SELL), STOP_LOSS (SELL) orders only:Order Quantity to be Sold"
    )
    notional: Optional[Union[str, Decimal]] = Field(
        description="Depends For MARKET (BUY), STOP_LOSS (BUY), TAKE_PROFIT (BUY) orders only: Amount to spend"
    )
    client_oid: Optional[str] = Field(description="Optional Client order ID")
    time_in_force: Optional[str] = Field(
        description="""
        (Limit Orders Only)
        Options are:
        - GOOD_TILL_CANCEL (Default if unspecified)
        - FILL_OR_KILL
        - IMMEDIATE_OR_CANCEL"""
    )
    exec_inst: Optional[str] = Field(description="(Limit Orders Only) Options are: - POST_ONLY - Or leave empty")
    trigger_price: Optional[Union[str, Decimal]] = Field(
        description="Used with STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders. "
        "Dictates when order will be triggered"
    )


class PrivateCreateOrderRequest(ExchangeRequest):
    method: str = "private/create-order"
    params: PrivateCreateOrderRequestParams = Field()


class PrivateCreateOrderResponseResult(FrozenBaseModel):
    order_id: int = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(description="(Optional) if a Client order ID was provided in the request")


class PrivateCreateOrderResponse(ExchangeResponse):
    result: Optional[PrivateCreateOrderResponseResult] = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/create-order"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-order
class PrivateCancelOrderRequestParams(FrozenBaseModel):
    instrument_name: str = Field(default=None, description="instrument name e.g. BTC_USDT, etc.")
    order_id: str = Field(default=None, description="order ID")


class PrivateCancelOrderRequest(ExchangeRequest):
    method: str = "private/cancel-order"
    params: PrivateCancelOrderRequestParams = Field()


class PrivateCancelOrderResponse(ExchangeResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-order"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-all-orders
class PrivateCancelAllOrdersRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="instrument name e.g. BTC_USDT, etc.")


class PrivateCancelAllOrdersRequest(ExchangeRequest):
    method: str = "private/cancel-all-orders"
    params: PrivateCancelAllOrdersRequestParams = Field()


class PrivateCancelAllOrdersResponse(ExchangeResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-all-orders"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-order-history
class PrivateGetOrderHistoryRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="e.g. ETH_CRO, BTC_USDT. Omit for 'all'")
    start_ts: Optional[int] = Field(
        description="Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago"
    )
    end_ts: Optional[int] = Field(description="End timestamp (milliseconds since the Unix epoch) - defaults to 'now'")
    page_size: Optional[int] = Field(description="Page size (Default: 20, max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class PrivateGetOrderHistoryRequest(ExchangeRequest):
    method: str = "private/get-order-history"
    params: PrivateGetOrderHistoryRequestParams = Field()


class PrivateGetOrderHistoryResult(FrozenBaseModel):
    order_list: List[OrderDetail] = Field(description="Order list response")


class PrivateGetOrderHistoryResponse(ExchangeResponse):
    result: PrivateGetOrderHistoryResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-order-history"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-open-orders
class PrivateGetOpenOrdersRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(default=None, description="e.g. BTC_USDT, ETH_CRO, etc.")
    page_size: Optional[int] = Field(default=None, description="page size", ge=0, le=200)
    page: Optional[int] = Field(default=None, description="page number", ge=0)


class PrivateGetOpenOrdersRequest(ExchangeRequest):
    method: str = "private/get-open-orders"
    params: PrivateGetOpenOrdersRequestParams = Field()


class PrivateGetOpenOrdersResult(FrozenBaseModel):
    order_list: List[OrderDetail] = Field()


class PrivateGetOpenOrdersResponse(ExchangeResponse):
    result: PrivateGetOpenOrdersResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-open-orders"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-order-detail
class PrivateGetOrderDetailRequestParams(FrozenBaseModel):
    order_id: str = Field(description="order id")


class PrivateGetOrderDetailRequest(ExchangeRequest):
    method: str = "private/get-order-detail"
    params: PrivateGetOrderDetailRequestParams = Field()


class PrivateGetOrderTradeDetailInfo(FrozenBaseModel):
    side: str = Field(description="BUY, SELL")
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    fee: Decimal = Field(description="Trade fee")
    trade_id: str = Field(description="Trade ID")
    create_time: int = Field(description="Trade creation time")
    traded_price: Decimal = Field(description="Executed trade price")
    traded_quantity: Decimal = Field(description="Executed trade quantity")
    fee_currency: str = Field(description="Currency used for the fees (e.g. CRO)")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="Client OID")
    liquidity_indicator: str = Field()


class PrivateGetOrderDetailResult(FrozenBaseModel):
    trade_list: List[PrivateGetOrderTradeDetailInfo] = Field(description="Get order detail trade_list")
    order_info: OrderDetail = Field(description="Get order detail order_info")


class PrivateGetOrderDetailResponse(ExchangeResponse):
    result: PrivateGetOrderDetailResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-order-detail"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/set-cancel-on-disconnect
class PrivateSetCancelOnDisconnectRequestParams(FrozenBaseModel):
    scope: str = Field(default="CONNECTION")


class PrivateSetCancelOnDisconnectRequest(ExchangeRequest):
    method: str = "private/set-cancel-on-disconnect"
    params: PrivateSetCancelOnDisconnectRequestParams = Field()


class PrivateSetCancelOnDisconnectResponseResult(FrozenBaseModel):
    scope: str = Field(default="CONNECTION")


class PrivateSetCancelOnDisconnectResponse(ExchangeResponse):
    result: PrivateSetCancelOnDisconnectResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/set-cancel-on-disconnect"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-cancel-on-disconnect
class PrivateGetCancelOnDisconnectRequest(ExchangeRequest):
    method: str = "private/get-cancel-on-disconnect"
    params: dict = {}


class PrivateGetCancelOnDisconnectResponseResult(FrozenBaseModel):
    scope: str = Field(default="CONNECTION")


class PrivateGetCancelOnDisconnectResponse(ExchangeResponse):
    result: PrivateGetCancelOnDisconnectResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-cancel-on-disconnect"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/create-order-list
class PrivateCreateOrderListRequestParams(FrozenBaseModel):
    contingency_type: str = Field(description="LIST")
    order_list: List[PrivateCreateOrderRequestParams] = Field(description="Exactly 2 orders")


class PrivateCreateOrderListRequest(ExchangeRequest):
    method: str = "private/create-order-list"
    params: PrivateCreateOrderListRequestParams = Field()


class ResultListDetail(FrozenBaseModel):
    index: int = Field(description="The index of corresponding order request (Start from 0)")
    code: int = Field(description="0 if success")
    message: Optional[str] = Field(description="(Optional) For server or error messages")
    order_id: str = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(
        description="(Optional) if a Client order ID was provided in the request. (Maximum 36 characters)"
    )


class PrivateCreateOrderListResponseResult(FrozenBaseModel):
    result_list: List[ResultListDetail] = Field()


class PrivateCreateOrderListResponse(ExchangeResponse):
    result: PrivateCreateOrderListResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/create-order-list"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-order-list
class OrderListDetail(FrozenBaseModel):
    instrument_name: str = Field(description="instrument_name, e.g., ETH_CRO, BTC_USDT")
    order_id: str = Field(description="Order ID")


class PrivateCancelOrderListRequestParams(FrozenBaseModel):
    order_list: Optional[List[OrderListDetail]] = Field(
        description="For non contingency orders, A list of orders to be cancelled"
    )
    instrument_name: Optional[str] = Field(description="instrument_name")
    contingency_id: Optional[str] = Field(description="ID of the contingency order")


class PrivateCancelOrderListRequest(ExchangeRequest):
    method: str = "private/cancel-order-list"
    params: PrivateCancelOrderListRequestParams = Field()


class PrivateCancelOrderListResponse(ExchangeResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-order-list"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v

from typing import List, Optional, Union
from pydantic import Field, validator

from ...models import SubscribeResponse, SubscribeRequest
from ....models import FrozenBaseModel, ExchangeRequest, ExchangeResponse


class OrderDetail(FrozenBaseModel):
    account_id: str = Field(description="Account ID")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="Client Order ID")
    order_type: str = Field(description="MARKET, LIMIT, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    time_in_force: str = Field(description="time in force, such as GOOD_TILL_CANCEL")
    side: str = Field(description="side, such as BUY, SELL")
    exec_inst: List[str] = Field(description="POST_ONLY, REDUCE_ONLY, LIQUIDATION")
    quantity: str = Field(description="Quantity specified in the order")
    limit_price: Optional[str] = Field(description="Limit price specified in the order")
    order_value: str = Field(description="Order value")
    maker_fee_rate: Optional[str] = Field(description="User's maker fee rate")
    taker_fee_rate: Optional[str] = Field(description="User's taker fee rate")
    avg_price: str = Field(description="Average price")
    cumulative_quantity: str = Field(description="Cumulative executed quantity")
    cumulative_value: str = Field(description="Cumulative executed value")
    cumulative_fee: str = Field(description="Cumulative executed fee")
    status: str = Field(description="Order status:NEW, PENDING, REJECTED,ACTIVE,CANCELED,FILLED,EXPIRED")
    update_user_id: str = Field(description="Updated user")
    order_date: str = Field(description="Order creation date")
    create_time: int = Field(description="Order creation timestamp")
    create_time_ns: str = Field(description="Order creation timestamp (nanosecond)")
    update_time: int = Field(description="Order update timestamp")
    instrument_name: str = Field(description="e.g. BTCUSD-PERP")
    fee_instrument_name: str = Field(description="Currency used for the fees")
    trigger_price: Optional[str] = Field(description="Trigger price")
    trigger_price_type: Optional[str] = Field(description="Trigger price type, such as NULL_VAL")
    contingency_type: Optional[str] = Field(description="such as OCO")
    list_id: Optional[str] = Field(description="ID of the contingency order")


class SubscribeUserOrderRequestParams(FrozenBaseModel):
    channels: List[str] = ["user.order"]


class SubscribeUserOrderRequest(SubscribeRequest):
    params: SubscribeUserOrderRequestParams = SubscribeUserOrderRequestParams()


class SubscribeUserOrderResponseResult(FrozenBaseModel):
    channel: str = "user.order"
    subscription: str = "user.order"
    data: List[OrderDetail] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.order", f"channel expect:[user.order] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v):
        assert v == "user.order", f"subscription expect:[user.order] actual:[{v}]!"
        return v


class SubscribeUserOrderResponse(SubscribeResponse):
    result: SubscribeUserOrderResponseResult = Field(default=None)


# private/create-order
class PrivateCreateOrderRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="instrument name e.g. BTC_USDT, etc.")
    side: str = Field(description="BUY, SELL")
    type: str = Field(description="LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    quantity: str = Field(
        description="For LIMIT Orders, MARKET (SELL), STOP_LOSS (SELL) orders only:Order Quantity to be Sold"
    )
    time_in_force: Optional[str] = Field(
        description="""
        (Limit Orders Only)
        Options are:
        - GOOD_TILL_CANCEL (Default if unspecified)
        - FILL_OR_KILL
        - IMMEDIATE_OR_CANCEL"""
    )
    price: Optional[str] = Field(default=None, description="For LIMIT and STOP_LIMIT orders only: Unit price")
    ref_price: Optional[str] = Field(
        default=None,
        description="Trigger price required for STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT order type",
    )
    client_oid: Optional[str] = Field(description="Client Order ID")
    exec_inst: Optional[List[str]] = Field(description="POST_ONLY or MARGIN_CALL")
    ref_price_type: Optional[str] = Field(
        default=None, description="which price to use for ref_price: MARK_PRICE (default), INDEX_PRICE, LAST_PRICE"
    )
    spot_margin: Optional[str] = Field(default=None, description="SPOT: non-margin order, MARGIN: margin order")


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
    order_id: Optional[Union[int, str]] = Field(default=None, description="Optional Order ID")
    client_oid: Optional[str] = Field(default=None, description="Optional Client Order ID")


class PrivateCancelOrderRequest(ExchangeRequest):
    method: str = "private/cancel-order"
    params: PrivateCancelOrderRequestParams = Field()


class PrivateCancelOrderResult(FrozenBaseModel):
    order_id: int = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(description="(Optional) if a Client order ID was provided in the request")


class PrivateCancelOrderResponse(ExchangeResponse):
    result: PrivateCancelOrderResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-order"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-all-orders
class PrivateCancelAllOrdersRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="instrument name e.g. BTC_USDT, etc.")
    type: Optional[str] = Field(description="e.g. LIMIT, TRIGGER, ALL")


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


# private/get-open-orders
class PrivateGetOpenOrdersRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(default=None, description="e.g. BTCUSD-PERP. Omit for 'all'")
    page_size: Optional[int] = Field(default=None, description="page size", ge=0, le=200)
    page: Optional[int] = Field(default=None, description="page number", ge=0)


class PrivateGetOpenOrdersRequest(ExchangeRequest):
    method: str = "private/get-open-orders"
    params: PrivateGetOpenOrdersRequestParams = Field()


class PrivateGetOpenOrdersResult(FrozenBaseModel):
    data: List[OrderDetail] = Field()


class PrivateGetOpenOrdersResponse(ExchangeResponse):
    result: PrivateGetOpenOrdersResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-open-orders"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/set-cancel-on-disconnect
class PrivateSetCancelOnDisconnectRequestParams(FrozenBaseModel):
    scope: str = Field(default="CONNECTION", description="The ONLY scope supported is CONNECTION")


class PrivateSetCancelOnDisconnectRequest(ExchangeRequest):
    method: str = "private/set-cancel-on-disconnect"
    params: PrivateSetCancelOnDisconnectRequestParams = Field()


class PrivateSetCancelOnDisconnectResponseResult(FrozenBaseModel):
    scope: str = Field(description="The ONLY scope supported is CONNECTION")


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
    scope: str = Field(default="CONNECTION", description="The ONLY scope supported is CONNECTION")


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
    contingency_type: str = Field(description="OCO")
    order_list: List[PrivateCreateOrderRequestParams] = Field(description="Exactly 2 orders")


class PrivateCreateOrderListRequest(ExchangeRequest):
    method: str = "private/create-order-list"
    params: PrivateCreateOrderListRequestParams = Field()


class PrivateCreateOrderListResponseResult(FrozenBaseModel):
    list_id: int = Field(description="List ID")


class PrivateCreateOrderListResponse(ExchangeResponse):
    result: PrivateCreateOrderListResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/create-order-list"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-order-list
class PrivateCancelOrderListRequestParams(FrozenBaseModel):
    contingency_type: str = Field(description="OCO")
    instrument_name: str = Field(description="e.g. BTCUSD-PERP")
    list_id: str = Field(description="List ID")


class PrivateCancelOrderListRequest(ExchangeRequest):
    method: str = "private/cancel-order-list"
    params: PrivateCancelOrderListRequestParams


class PrivateCancelOrderListResponse(ExchangeResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-order-list"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-order-list
class PrivateGetOrderListRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTCUSD-PERP")
    list_id: str = Field(description="List ID")
    contingency_type: str = Field(description="OCO")


class PrivateGetOrderListRequest(ExchangeRequest):
    method: str = "private/get-order-list"
    params: PrivateGetOrderListRequestParams


class PrivateGetOrderListResponseResult(FrozenBaseModel):
    data: List[OrderDetail] = Field()


class PrivateGetOrderListResponse(ExchangeResponse):
    result: PrivateGetOrderListResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-order-list"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v

from typing import List, Optional, Any, Union
from pydantic import Field, validator

from ...models import SubscribeResponse, SubscribeRequest
from ....models import FrozenBaseModel, DerivativesRequest, DerivativesResponse


class OrderDetail(FrozenBaseModel):
    account_id: str
    order_id: str
    client_oid: str
    order_type: str = Field(description="order type, such as LIMIT")
    time_in_force: str = Field(description="time in force, such as GOOD_TILL_CANCEL")
    side: str = Field(description="side, such as BUY, SELL")
    exec_inst: List[str]
    quantity: str = Field(description="order quantity")
    limit_price: str = Field(description="order limit price")
    order_value: str
    maker_fee_rate: str
    taker_fee_rate: str
    avg_price: str
    cumulative_quantity: str
    cumulative_value: str
    cumulative_fee: str
    status: str = Field(description="order status ACTIVE")
    update_user_id: str
    order_date: str
    instrument_name: str
    fee_instrument_name: str
    create_time: int
    create_time_ns: int
    update_time: int


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
    price: str = Field(default=None, description="For LIMIT and STOP_LIMIT orders only: Unit price")
    post_only: bool = Field(default=False, description="POST_ONLY")
    ref_price: Optional[str] = Field(
        default=None,
        description="Trigger price required for STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT order type",
    )
    client_oid: Optional[str] = Field(description="Client Order ID")

    def __init__(self, **data: Any):
        super().__init__(**data)
        if (
            "LIMIT" == self.type.upper()
            or "STOP_LIMIT" == self.type.upper()
            or "TAKE_PROFIT_LIMIT" == self.type.upper()
        ):
            if "LIMIT" == self.type.upper() and self.post_only is True:
                object.__setattr__(self, "exec_inst", ["POST_ONLY"])
        else:
            object.__delattr__(self, "price")
        object.__delattr__(self, "post_only")


class PrivateCreateOrderRequest(DerivativesRequest):
    method: str = "private/create-order"
    params: PrivateCreateOrderRequestParams = Field()


class PrivateCreateOrderResponseResult(FrozenBaseModel):
    order_id: int = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(description="(Optional) if a Client order ID was provided in the request")


class PrivateCreateOrderResponse(DerivativesResponse):
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


class PrivateCancelOrderRequest(DerivativesRequest):
    method: str = "private/cancel-order"
    params: PrivateCancelOrderRequestParams = Field()


class PrivateCancelOrderResult(FrozenBaseModel):
    order_id: int = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(description="(Optional) if a Client order ID was provided in the request")


class PrivateCancelOrderResponse(DerivativesResponse):
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


class PrivateCancelAllOrdersRequest(DerivativesRequest):
    method: str = "private/cancel-all-orders"
    params: PrivateCancelAllOrdersRequestParams = Field()


class PrivateCancelAllOrdersResponse(DerivativesResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-all-orders"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-open-orders
class PrivateGetOpenOrdersRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(default=None, description="e.g. BTC_USDT, ETH_CRO, etc.")
    page_size: Optional[int] = Field(default=None, description="page size", ge=0, le=200)
    page: Optional[int] = Field(default=None, description="page number", ge=0)


class PrivateGetOpenOrdersRequest(DerivativesRequest):
    method: str = "private/get-open-orders"
    params: PrivateGetOpenOrdersRequestParams = Field()


class PrivateGetOpenOrdersResult(FrozenBaseModel):
    data: List[OrderDetail] = Field()


class PrivateGetOpenOrdersResponse(DerivativesResponse):
    result: PrivateGetOpenOrdersResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-open-orders"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/set-cancel-on-disconnect
class PrivateSetCancelOnDisconnectRequestParams(FrozenBaseModel):
    scope: str = Field(default="CONNECTION")


class PrivateSetCancelOnDisconnectRequest(DerivativesRequest):
    method: str = "private/set-cancel-on-disconnect"
    params: PrivateSetCancelOnDisconnectRequestParams = Field()


class PrivateSetCancelOnDisconnectResponseResult(FrozenBaseModel):
    scope: str = Field(default="CONNECTION")


class PrivateSetCancelOnDisconnectResponse(DerivativesResponse):
    result: PrivateSetCancelOnDisconnectResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/set-cancel-on-disconnect"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-cancel-on-disconnect
class PrivateGetCancelOnDisconnectRequest(DerivativesRequest):
    method: str = "private/get-cancel-on-disconnect"
    params: dict = {}


class PrivateGetCancelOnDisconnectResponseResult(FrozenBaseModel):
    scope: str = Field(default="CONNECTION")


class PrivateGetCancelOnDisconnectResponse(DerivativesResponse):
    result: PrivateGetCancelOnDisconnectResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-cancel-on-disconnect"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v

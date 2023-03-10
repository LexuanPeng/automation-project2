from typing import List, Union

from ...ws_base import ExchangeWsService
from ..models.account import PrivateUserBalanceRequest, PrivateUserBalanceResponse
from ..models.positions import (
    PrivateGetPositionsRequest,
    PrivateGetPositionsResponse,
    PrivateGetPositionsRequestParams,
    PrivateClosePositionRequest,
    PrivateClosePositionRequestParams,
    PrivateClosePositionResponse,
)
from ..models.orders import (
    PrivateCreateOrderRequest,
    PrivateCreateOrderRequestParams,
    PrivateCreateOrderResponse,
    PrivateCancelOrderRequest,
    PrivateCancelOrderResponse,
    PrivateCancelOrderRequestParams,
    PrivateCancelAllOrdersRequest,
    PrivateCancelAllOrdersRequestParams,
    PrivateCancelAllOrdersResponse,
    PrivateGetOpenOrdersRequest,
    PrivateGetOpenOrdersRequestParams,
    PrivateGetOpenOrdersResponse,
    PrivateGetCancelOnDisconnectResponse,
    PrivateGetCancelOnDisconnectRequest,
    PrivateSetCancelOnDisconnectRequest,
    PrivateSetCancelOnDisconnectResponse,
    PrivateSetCancelOnDisconnectRequestParams,
    PrivateCreateOrderListRequest,
    PrivateCreateOrderListRequestParams,
    PrivateCreateOrderListResponse,
    PrivateCancelOrderListRequestParams,
    PrivateCancelOrderListRequest,
    PrivateCancelOrderListResponse,
    PrivateGetOrderListRequestParams,
    PrivateGetOrderListRequest,
    PrivateGetOrderListResponse,
)


class UserPrivateService(ExchangeWsService):
    def send_user_balance(self):
        request = PrivateUserBalanceRequest().json(exclude_none=True)
        self.client.send(request)

    def get_user_balance_msgs(self, *args, **kwargs) -> List[PrivateUserBalanceResponse]:
        return list(
            map(
                PrivateUserBalanceResponse.parse_raw,
                self.client.get_messages(method="private/user-balance", *args, **kwargs),
            )
        )

    def send_get_positions(self, instrument_name: str = None):
        if instrument_name is None:
            request = PrivateGetPositionsRequest(params=PrivateGetPositionsRequestParams()).json(exclude_none=True)
        else:
            request = PrivateGetPositionsRequest(
                params=PrivateGetPositionsRequestParams(instrument_name=instrument_name)
            ).json(exclude_none=True)
        self.client.send(request)

    def get_positions_msgs(self, *args, **kwargs) -> List[PrivateGetPositionsResponse]:
        return list(
            map(
                PrivateGetPositionsResponse.parse_raw,
                self.client.get_messages(method="private/get-positions", *args, **kwargs),
            )
        )

    def send_create_order(self, **kwargs):
        request = PrivateCreateOrderRequest(**kwargs).json(exclude_none=True)
        self.client.send(request)

    def get_create_order_msgs(self, *args, **kwargs) -> List[PrivateCreateOrderResponse]:
        return list(
            map(
                PrivateCreateOrderResponse.parse_raw,
                self.client.get_messages(method="private/create-order", *args, **kwargs),
            )
        )

    def send_cancel_order(self, order_id: Union[str, int] = None, client_oid: str = None):
        request = PrivateCancelOrderRequest(
            params=PrivateCancelOrderRequestParams(order_id=order_id, client_oid=client_oid)
        ).json(exclude_none=True)
        self.client.send(request)

    def get_cancel_order_msgs(self, *args, **kwargs) -> List[PrivateCancelOrderResponse]:
        return list(
            map(
                PrivateCancelOrderResponse.parse_raw,
                self.client.get_messages(method="private/cancel-order", *args, **kwargs),
            )
        )

    def send_cancel_all_orders(self, instrument_name: str = None, type: str = None):
        request = PrivateCancelAllOrdersRequest(
            params=PrivateCancelAllOrdersRequestParams(instrument_name=instrument_name, type=type)
        ).json(exclude_none=True)
        self.client.send(request)

    def get_cancel_all_orders_msgs(self, *args, **kwargs) -> List[PrivateCancelAllOrdersResponse]:
        return list(
            map(
                PrivateCancelAllOrdersResponse.parse_raw,
                self.client.get_messages(method="private/cancel-all-orders", *args, **kwargs),
            )
        )

    def send_close_position(self, instrument_name: str, type: str, price: str = None):
        request = PrivateClosePositionRequest(
            params=PrivateClosePositionRequestParams(instrument_name=instrument_name, type=type, price=price)
        ).json(exclude_none=True)
        self.client.send(request)

    def get_close_position_msgs(self, *args, **kwargs) -> List[PrivateClosePositionResponse]:
        return list(
            map(
                PrivateClosePositionResponse.parse_raw,
                self.client.get_messages(method="private/close-position", *args, **kwargs),
            )
        )

    def send_get_open_orders(self, instrument_name: str = None, page_size: int = None, page: int = None):
        request = PrivateGetOpenOrdersRequest(
            params=PrivateGetOpenOrdersRequestParams(instrument_name=instrument_name, page_size=page_size, page=page)
        ).json(exclude_none=True)
        self.client.send(request)

    def get_open_orders_msgs(self, *args, **kwargs) -> List[PrivateGetOpenOrdersResponse]:
        return list(
            map(
                PrivateGetOpenOrdersResponse.parse_raw,
                self.client.get_messages(method="private/get-open-orders", *args, **kwargs),
            )
        )

    def send_set_cancel_on_disconnect(self, scope: str = "CONNECTION"):
        request = PrivateSetCancelOnDisconnectRequest(
            params=PrivateSetCancelOnDisconnectRequestParams(scope=scope)
        ).json(exclude_none=True)
        self.client.send(request)

    def get_set_cancel_on_disconnect_msgs(self, *args, **kwargs) -> List[PrivateSetCancelOnDisconnectResponse]:
        return list(
            map(
                PrivateSetCancelOnDisconnectResponse.parse_raw,
                self.client.get_messages(method="private/set-cancel-on-disconnect", *args, **kwargs),
            )
        )

    def send_get_cancel_on_disconnect(self):
        request = PrivateGetCancelOnDisconnectRequest().json(exclude_none=True)
        self.client.send(request)

    def get_cancel_on_disconnect_msgs(self, *args, **kwargs) -> List[PrivateGetCancelOnDisconnectResponse]:
        return list(
            map(
                PrivateGetCancelOnDisconnectResponse.parse_raw,
                self.client.get_messages(method="private/get-cancel-on-disconnect", *args, **kwargs),
            )
        )

    def send_create_order_list(self, order_list: List[PrivateCreateOrderRequestParams], contingency_type: str = "OCO"):
        request = PrivateCreateOrderListRequest(
            params=PrivateCreateOrderListRequestParams(order_list=order_list, contingency_type=contingency_type)
        ).json(exclude_none=True)
        self.client.send(request)

    def get_create_order_list_msgs(self, *args, **kwargs) -> List[PrivateCreateOrderListResponse]:
        return list(
            map(
                PrivateCreateOrderListResponse.parse_raw,
                self.client.get_messages(method="private/create-order-list", *args, **kwargs),
            )
        )

    def send_cancel_order_list(self, instrument_name: str, list_id: str, contingency_type: str = "OCO"):
        request = PrivateCancelOrderListRequest(
            params=PrivateCancelOrderListRequestParams(
                instrument_name=instrument_name, list_id=list_id, contingency_type=contingency_type
            )
        ).json(exclude_none=True)
        self.client.send(request)

    def get_cancel_order_list_msgs(self, *args, **kwargs) -> List[PrivateCancelOrderListResponse]:
        return list(
            map(
                PrivateCancelOrderListResponse.parse_raw,
                self.client.get_messages(method="private/cancel-order-list", *args, **kwargs),
            )
        )

    def send_get_order_list(self, instrument_name: str, list_id: str, contingency_type: str = "OCO"):
        request = PrivateGetOrderListRequest(
            params=PrivateGetOrderListRequestParams(
                instrument_name=instrument_name,
                list_id=list_id,
                contingency_type=contingency_type,
            )
        ).json(exclude_none=True)
        self.client.send(request)

    def get_get_order_list_msgs(self, *args, **kwargs) -> List[PrivateGetOrderListResponse]:
        return list(
            map(
                PrivateGetOrderListResponse.parse_raw,
                self.client.get_messages(method="private/get-order-list", *args, **kwargs),
            )
        )

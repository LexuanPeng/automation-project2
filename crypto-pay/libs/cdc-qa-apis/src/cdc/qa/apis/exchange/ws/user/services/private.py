from decimal import Decimal
from typing import List, Union

from ...ws_base import ExchangeWsService
from ..models.account import (
    PrivateGetAccountSummaryRequest,
    PrivateGetAccountSummaryRequestParams,
    PrivateGetAccountSummaryResponse,
    PrivateCreateWithdrawalRequest,
    PrivateCreateWithdrawalRequestParams,
    PrivateCreateWithdrawalResponse,
    PrivateGetWithdrawalHistoryRequest,
    PrivateGetWithdrawalHistoryRequestParams,
    PrivateGetWithdrawalHistoryResponse,
)
from ..models.order import (
    PrivateCancelOrderRequest,
    PrivateCancelOrderRequestParams,
    PrivateCancelOrderResponse,
    PrivateCreateOrderRequest,
    PrivateCreateOrderResponse,
    PrivateCancelAllOrdersRequest,
    PrivateCancelAllOrdersRequestParams,
    PrivateCancelAllOrdersResponse,
    PrivateGetOrderHistoryRequest,
    PrivateGetOrderHistoryResponse,
    PrivateGetOrderHistoryRequestParams,
    PrivateGetOpenOrdersRequest,
    PrivateGetOpenOrdersRequestParams,
    PrivateGetOpenOrdersResponse,
    PrivateGetOrderDetailRequest,
    PrivateGetOrderDetailRequestParams,
    PrivateGetOrderDetailResponse,
    PrivateGetCancelOnDisconnectResponse,
    PrivateGetCancelOnDisconnectRequest,
    PrivateSetCancelOnDisconnectRequest,
    PrivateSetCancelOnDisconnectResponse,
    PrivateSetCancelOnDisconnectRequestParams,
    PrivateCreateOrderRequestParams,
    PrivateCreateOrderListRequest,
    PrivateCreateOrderListRequestParams,
    PrivateCreateOrderListResponse,
    PrivateCancelOrderListRequest,
    PrivateCancelOrderListRequestParams,
    PrivateCancelOrderListResponse,
)
from ..models.trade import PrivateGetTradesRequest, PrivateGetTradesRequestParams, PrivateGetTradesResponse


class UserPrivateService(ExchangeWsService):
    def send_get_account_summary(self, currency: str = None):
        if currency is None:
            request = PrivateGetAccountSummaryRequest(params=PrivateGetAccountSummaryRequestParams()).json(
                exclude_none=True
            )
        else:
            request = PrivateGetAccountSummaryRequest(
                params=PrivateGetAccountSummaryRequestParams(currency=currency)
            ).json(exclude_none=True)
        self.client.send(request)

    def get_account_summary_msgs(self, *args, **kwargs) -> List[PrivateGetAccountSummaryResponse]:
        return list(
            map(
                PrivateGetAccountSummaryResponse.parse_raw,
                self.client.get_messages(method="private/get-account-summary", *args, **kwargs),
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

    def send_cancel_order(self, instrument_name: str = None, order_id: Union[str, int] = None):
        request = PrivateCancelOrderRequest(
            params=PrivateCancelOrderRequestParams(instrument_name=instrument_name, order_id=order_id)
        ).json(exclude_none=True)
        self.client.send(request)

    def get_cancel_order_msgs(self, *args, **kwargs) -> List[PrivateCancelOrderResponse]:
        return list(
            map(
                PrivateCancelOrderResponse.parse_raw,
                self.client.get_messages(method="private/cancel-order", *args, **kwargs),
            )
        )

    def send_cancel_all_orders(self, instrument_name: str = None):
        request = PrivateCancelAllOrdersRequest(
            params=PrivateCancelAllOrdersRequestParams(instrument_name=instrument_name)
        ).json(exclude_none=True)
        self.client.send(request)

    def get_cancel_all_orders_msgs(self, *args, **kwargs) -> List[PrivateCancelAllOrdersResponse]:
        return list(
            map(
                PrivateCancelAllOrdersResponse.parse_raw,
                self.client.get_messages(method="private/cancel-all-orders", *args, **kwargs),
            )
        )

    def send_get_order_history(
        self,
        instrument_name: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ):
        params = {
            "instrument_name": instrument_name,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "page_size": page_size,
            "page": page,
        }
        request = PrivateGetOrderHistoryRequest(params=PrivateGetOrderHistoryRequestParams(**params)).json(
            exclude_none=True
        )
        self.client.send(request)

    def get_order_history_msgs(self, *args, **kwargs) -> List[PrivateGetOrderHistoryResponse]:
        return list(
            map(
                PrivateGetOrderHistoryResponse.parse_raw,
                self.client.get_messages(method="private/get-order-history", *args, **kwargs),
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

    def send_get_order_detail(self, order_id: str):
        request = PrivateGetOrderDetailRequest(params=PrivateGetOrderDetailRequestParams(order_id=order_id)).json(
            exclude_none=True
        )
        self.client.send(request)

    def get_order_detail_msgs(self, *args, **kwargs) -> List[PrivateGetOrderDetailResponse]:
        return list(
            map(
                PrivateGetOrderDetailResponse.parse_raw,
                self.client.get_messages(method="private/get-order-detail", *args, **kwargs),
            )
        )

    def send_get_trades(
        self,
        instrument_name: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ):
        params = {
            "instrument_name": instrument_name,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "page_size": page_size,
            "page": page,
        }
        request = PrivateGetTradesRequest(params=PrivateGetTradesRequestParams(**params)).json(exclude_none=True)
        self.client.send(request)

    def get_trades_msgs(self, *args, **kwargs) -> List[PrivateGetTradesResponse]:
        return list(
            map(
                PrivateGetTradesResponse.parse_raw,
                self.client.get_messages(method="private/get-trades", *args, **kwargs),
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

    def send_create_withdrawal(
        self, currency: str, amount: Decimal, address: str, client_wid: str = None, address_tag: str = None
    ):
        """create withdrawal

        Args:
            currency (str): currency name
            amount (Decimal): withdrawal amount
            address (str): address
            client_wid (str, optional): client withdrawal id. Defaults to None.
            address_tag (str, optional): address identifier. Defaults to None.
        """
        params = {
            "client_wid": client_wid,
            "currency": currency,
            "amount": amount,
            "address": address,
            "address_tag": address_tag,
        }
        request = PrivateCreateWithdrawalRequest(params=PrivateCreateWithdrawalRequestParams(**params)).json(
            exclude_none=True
        )
        self.client.send(request)

    def get_create_withdrawal_msgs(self, *args, **kwargs) -> List[PrivateCreateWithdrawalResponse]:
        return list(
            map(
                PrivateCreateWithdrawalResponse.parse_raw,
                self.client.get_messages(method="private/create-withdrawal", *args, **kwargs),
            )
        )

    def send_get_withdrawal_history(
        self,
        currency: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
        status: str = None,
    ):
        """get withdrawal history

        Args:
            currency (str, optional): currency. Defaults to None.
            start_ts (int, optional): start timestamp. Defaults to None.
            end_ts (int, optional): end timestamp. Defaults to None.
            page_size (int, optional): page size. Defaults to None.
            page (int, optional): page number 0-based. Defaults to None.
            status (str, optional): 0 - Pending
                        1 - Processing
                        2 - Rejected
                        3 - Payment In-progress
                        4 - Payment Failed
                        5 - Completed
                        6 - Cancelled. Defaults to None.
        """
        params = {
            "currency": currency,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "page_size": page_size,
            "page": page,
            "status": status,
        }
        request = PrivateGetWithdrawalHistoryRequest(params=PrivateGetWithdrawalHistoryRequestParams(**params)).json(
            exclude_none=True
        )
        self.client.send(request)

    def get_withdrawal_history_msgs(self, *args, **kwargs) -> List[PrivateGetWithdrawalHistoryResponse]:
        return list(
            map(
                PrivateGetWithdrawalHistoryResponse.parse_raw,
                self.client.get_messages(method="private/get-withdrawal-history", *args, **kwargs),
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

    def send_cancel_order_list(self, order_list: list = None, instrument_name: str = None, contingency_id: str = None):
        request = PrivateCancelOrderListRequest(
            params=PrivateCancelOrderListRequestParams(
                order_list=order_list,
                instrument_name=instrument_name,
                contingency_id=contingency_id,
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

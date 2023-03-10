from typing import Union, List

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_oex.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.orders import (
    CancelAllOrdersRequestBody,
    CancelAllOrdersRequestParams,
    CancelAllOrdersResponse,
    CancelOrderRequestBody,
    CancelOrderRequestParams,
    CancelOrderResponse,
    CreateOrderRequestBody,
    CreateOrderRequestParams,
    CreateOrderResponse,
    GetOpenOrdersRequestBody,
    GetOpenOrdersRequestParams,
    GetOpenOrdersResponse,
    GetOrderDetailRequestBody,
    GetOrderDetailRequestParams,
    GetOrderDetailResponse,
    GetOrderHistoryRequestBody,
    GetOrderHistoryRequestParams,
    GetOrderHistoryResponse,
    CreateOrderListRequestBody,
    CreateOrderListRequestParams,
    CreateOrderListResponse,
    CancelOrderListRequestBody,
    CancelOrderListRequestParams,
    CancelOrderListResponse,
    GetOrderListRequestBody,
    GetOrderListRequestParams,
    GetOrderListResponse,
)


class GetOpenOrdersApi(ExchangeRestApi):
    """exchange private gets all open orders for a particular instrument"""

    path = "private/get-open-orders"
    method = HttpMethods.POST
    request_data_type = GetOpenOrdersRequestBody
    response_type = GetOpenOrdersResponse


class CancelOrderApi(ExchangeRestApi):
    """exchange private cancel an existing order"""

    path = "private/cancel-order"
    method = HttpMethods.POST
    request_data_type = CancelOrderRequestBody
    response_type = CancelOrderResponse


class CreateOrderApi(ExchangeRestApi):
    """exchange private create a new BUY or SELL order"""

    path = "private/create-order"
    method = HttpMethods.POST
    request_data_type = CreateOrderRequestBody
    response_type = CreateOrderResponse


class CancelAllOrdersApi(ExchangeRestApi):
    """exchange private cancels all orders for a particular instrument/pair"""

    path = "private/cancel-all-orders"
    method = HttpMethods.POST
    request_data_type = CancelAllOrdersRequestBody
    response_type = CancelAllOrdersResponse


class GetOrderDetailApi(ExchangeRestApi):
    """exchange private gets Order Details for a particular order ID"""

    path = "private/get-order-detail"
    method = HttpMethods.POST
    request_data_type = GetOrderDetailRequestBody
    response_type = GetOrderDetailResponse


class GetOrderHistoryApi(ExchangeRestApi):
    """exchange private gets the order history for a particular instrument"""

    path = "private/get-order-history"
    method = HttpMethods.POST
    request_data_type = GetOrderHistoryRequestBody
    response_type = GetOrderHistoryResponse


class CreateOrderListApi(ExchangeRestApi):
    """exchange private create order list"""

    path = "private/create-order-list"
    method = HttpMethods.POST
    request_data_type = CreateOrderListRequestBody
    response_type = CreateOrderListResponse


class CancelOrderListApi(ExchangeRestApi):
    """exchange private create order list"""

    path = "private/cancel-order-list"
    method = HttpMethods.POST
    request_data_type = CancelOrderListRequestBody
    response_type = CancelOrderListResponse


class GetOrderListApi(ExchangeRestApi):
    """exchange private create order list"""

    path = "private/get-order-list"
    method = HttpMethods.POST
    request_data_type = GetOrderListRequestBody
    response_type = GetOrderListResponse


class OrderService(ExchangeRestService):
    def get_open_orders(
        self,
        instrument_name: str = None,
        system_label: str = None,
    ) -> GetOpenOrdersResponse:
        """request get open orders
        Args:
            instrument_name (str, optional): instrument name, None for allow. Defaults to None.
            system_label:
        Returns:
            response: GetOpenOrdersResponse
        """
        api = GetOpenOrdersApi(host=self.host, _session=self.session)
        payload = GetOpenOrdersRequestBody(
            params=GetOpenOrdersRequestParams(instrument_name=instrument_name, system_label=system_label),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetOpenOrdersResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def cancel_order(
        self,
        order_id: Union[str, int] = None,
        client_oid: str = None,
        system_label: str = None,
    ) -> CancelOrderResponse:
        """request cancel order

        Args:
            order_id (Union[str, int], optional): order_id. Defaults to None.
            client_oid (str, optional): client_oid. Defaults to None.
            system_label:

        Returns:
            CancelOrderResponse: CancelOrderResponse
        """
        api = CancelOrderApi(host=self.host, _session=self.session)
        payload = CancelOrderRequestBody(
            params=CancelOrderRequestParams(order_id=order_id, client_oid=client_oid, system_label=system_label),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CancelOrderResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def create_order(
        self,
        instrument_name: str,
        side: str,
        type: str,
        quantity: str,
        time_in_force: str,
        price: str = None,
        post_only: bool = False,
        ref_price: str = None,
        client_oid: str = None,
        exec_inst: List[str] = None,
        notional: str = None,
        system_label: str = None,
    ) -> CreateOrderResponse:
        """request create order
        Args:
            instrument_name (str): instrumen name
            side (str): side
            type (str): trade type
            quantity (str): quantity
            time_in_force (str): time_in_force
            price (str, optional): price, market no need price. Defaults to None.
            post_only (bool, optional): only for limit. Defaults to False.
            ref_price: only for STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT
            client_oid (str, optional): Client Order ID
            exec_inst: (list, optional): POST_ONLY or MARGIN_CALL or empty
            notional: (str, optional): order value for spot market/stop-loss/take-profit buy order
            system_label: (str, optional): system label

        Returns:
            response: CreateOrderResponse
        """
        api = CreateOrderApi(host=self.host, _session=self.session)
        payload = CreateOrderRequestBody(
            params=CreateOrderRequestParams(
                instrument_name=instrument_name,
                side=side,
                type=type,
                quantity=quantity,
                time_in_force=time_in_force,
                price=price,
                post_only=post_only,
                ref_price=ref_price,
                client_oid=client_oid,
                exec_inst=exec_inst,
                notional=notional,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CreateOrderResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def cancel_all_orders(
        self,
        instrument_name: str = None,
        type: str = None,
        system_label: str = None,
    ) -> CancelAllOrdersResponse:
        """request cancel all orders
        Args:
            instrument_name (str, optional): instrument name. Defaults to None cancel all orders
            type (str, optional): type, e.g. LIMIT, TRIGGER, ALL. Defaults to None
            system_label:
        Returns:
            response: CancelAllOrdersResponse
        """
        api = CancelAllOrdersApi(host=self.host, _session=self.session)
        payload = CancelAllOrdersRequestBody(
            params=CancelAllOrdersRequestParams(instrument_name=instrument_name, type=type, system_label=system_label),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CancelAllOrdersResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_order_detail(
        self,
        order_id: Union[str, int] = None,
        client_oid: str = None,
        system_label: str = None,
    ) -> GetOrderDetailResponse:
        """request get order detail
        Args:
            order_id (Union[str, int], optional): Order ID. string format is highly recommended,
                especially for JavaScript client. If not provided, client_oid must be specified.
            client_oid (str, optional): Client Order ID. If not provided, order_id must be specified.
            system_label: System label
        Returns:
            response: GetOrderDetailResponse
        """
        api = GetOrderDetailApi(host=self.host, _session=self.session)
        payload = GetOrderDetailRequestBody(
            params=GetOrderDetailRequestParams(order_id=order_id, client_oid=client_oid, system_label=system_label),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetOrderDetailResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_order_history(
        self,
        instrument_name: str = None,
        start_time: str = None,
        end_time: str = None,
        limit: int = None,
        system_label: str = None,
    ) -> GetOrderHistoryResponse:
        """request get order history
        Args:
            instrument_name (str, optional): instrument name
            start_time (str, optional): start timestamp as 1622131200000000000
            end_time (str, optional): end timestamp as 1622131200000000000
            limit (int, optional): limit order count. Defaults to None.
            system_label:
        Returns:
            response: GetOrderHistoryResponse
        """
        api = GetOrderHistoryApi(host=self.host, _session=self.session)
        payload = GetOrderHistoryRequestBody(
            params=GetOrderHistoryRequestParams(
                instrument_name=instrument_name,
                start_time=start_time,
                end_time=end_time,
                limit=limit,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetOrderHistoryResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def create_order_list(
        self,
        contingency_type: str,
        order_list: List[CreateOrderRequestParams],
        system_label: str = None,
    ) -> CreateOrderListResponse:
        """request create order list
        Args:
            contingency_type (str): OCO
            order_list (list): Exactly 2 orders
            system_label:

        Returns:
            response: CreateOrderListResponse
        """
        api = CreateOrderListApi(host=self.host, _session=self.session)
        payload = CreateOrderListRequestBody(
            params=CreateOrderListRequestParams(
                contingency_type=contingency_type,
                order_list=order_list,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CreateOrderListResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def cancel_order_list(
        self,
        contingency_type: str,
        list_id: str,
        instrument_name: str,
        system_label: str = None,
    ) -> CancelOrderListResponse:
        """request cancel order list
        Args:
            contingency_type (str): OCO
            list_id (str): list id
            instrument_name (str): instrument name
            system_label:
        Returns:
            response: CancelOrderListResponse
        """
        api = CancelOrderListApi(host=self.host, _session=self.session)
        payload = CancelOrderListRequestBody(
            params=CancelOrderListRequestParams(
                contingency_type=contingency_type,
                list_id=list_id,
                instrument_name=instrument_name,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CancelOrderListResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_order_list(
        self,
        contingency_type: str,
        list_id: str,
        instrument_name: str,
        system_label: str = None,
    ) -> GetOrderListResponse:
        """request cancel order list
        Args:
            contingency_type (str): OCO
            list_id (str): list id
            instrument_name (str): instrument name
            system_label:
        Returns:
            response: GetOrderListResponse
        """
        api = GetOrderListApi(host=self.host, _session=self.session)
        payload = GetOrderListRequestBody(
            params=GetOrderListRequestParams(
                contingency_type=contingency_type,
                list_id=list_id,
                instrument_name=instrument_name,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetOrderListResponse.parse_raw(b=api.call(data=payload).content)

        return response

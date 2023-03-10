from typing import List

from ...ws_base import DerivativesWsService
from ..models.account import SubscribeUserBalanceRequest, SubscribeUserBalanceResponse
from ..models.positions import SubscribeUserPositionsRequest, SubscribeUserPositionsResponse
from ..models.orders import SubscribeUserOrderRequest, SubscribeUserOrderResponse
from ..models.order_instrument import (
    SubscribeUserOrderInstrumentRequest,
    SubscribeUserOrderInstrumentResponse,
    SubscribeUserOrderInstrumentRequestParams,
)
from ..models.trade_instrument import (
    SubscribeUserTradeInstrumentRequest,
    SubscribeUserTradeInstrumentResponse,
    SubscribeUserTradeInstrumentRequestParams,
)


class UserSubscribeService(DerivativesWsService):
    def send_user_positions(self):
        request = SubscribeUserPositionsRequest().json(exclude_none=True)
        self.client.send(request)

    def get_user_positions_msgs(self, *args, **kwargs) -> List[SubscribeUserPositionsResponse]:
        return list(
            map(
                SubscribeUserPositionsResponse.parse_raw,
                self.client.get_subscription_messages(subscription="user.positions", *args, **kwargs),
            )
        )

    def send_user_balance(self):
        request = SubscribeUserBalanceRequest().json(exclude_none=True)
        self.client.send(request)

    def get_user_balance_msgs(self, *args, **kwargs) -> List[SubscribeUserBalanceResponse]:
        return list(
            map(
                SubscribeUserBalanceResponse.parse_raw,
                self.client.get_subscription_messages(subscription="user.balance", *args, **kwargs),
            )
        )

    def send_user_order(self):
        request = SubscribeUserOrderRequest().json(exclude_none=True)
        self.client.send(request)

    def get_user_order_msgs(self, *args, **kwargs) -> List[SubscribeUserOrderResponse]:
        return list(
            map(
                SubscribeUserOrderResponse.parse_raw,
                self.client.get_subscription_messages(subscription="user.order", *args, **kwargs),
            )
        )

    def send_user_order_instrument(self, instrument_name: str):
        request = SubscribeUserOrderInstrumentRequest(
            params=SubscribeUserOrderInstrumentRequestParams(channels=[f"user.order.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_user_order_instrument_msgs(
        self, instrument_name: str, *args, **kwargs
    ) -> List[SubscribeUserOrderInstrumentResponse]:
        return list(
            map(
                SubscribeUserOrderInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"user.order.{instrument_name}", *args, **kwargs),
            )
        )

    def send_user_trade_instrument(self, instrument_name: str):
        request = SubscribeUserTradeInstrumentRequest(
            params=SubscribeUserTradeInstrumentRequestParams(channels=[f"user.trade.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_user_trade_instrument_msgs(
        self, instrument_name: str, *args, **kwargs
    ) -> List[SubscribeUserTradeInstrumentResponse]:
        return list(
            map(
                SubscribeUserTradeInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"user.trade.{instrument_name}", *args, **kwargs),
            )
        )

from typing import List
from ..models.trade import SubscribeUserTradeInstrumentResponse
from ...ws_base import ExchangeWsService
from ..models.account import SubscribeUserBalanceRequest, SubscribeUserBalanceResponse
from ..models.order import (
    SubscribeUserOrderInstrumentRequest,
    SubscribeUserOrderInstrumentRequestParams,
    SubscribeUserOrderInstrumentResponse,
)
from ..models.margin import (
    SubscribeUserMarginOrderInstrumentRequest,
    SubscribeUserMarginOrderInstrumentRequestParams,
    SubscribeUserMarginOrderInstrumentResponse,
    SubscribeUserMarginTradeInstrumentRequest,
    SubscribeUserMarginTradeInstrumentRequestParams,
    SubscribeUserMarginTradeInstrumentResponse,
    SubscribeUserMarginBalanceRequest,
    SubscribeUserMarignBalanceResponse,
)


class UserSubscribeService(ExchangeWsService):
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
        request = SubscribeUserMarginTradeInstrumentRequest(
            params=SubscribeUserMarginTradeInstrumentRequestParams(channels=[f"user.trade.{instrument_name}"])
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

    def send_user_margin_order_instrument(self, instrument_name: str):
        request = SubscribeUserMarginOrderInstrumentRequest(
            params=SubscribeUserMarginOrderInstrumentRequestParams(channels=[f"user.margin.order.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_user_margin_order_instrument_msgs(
        self, instrument_name: str, *args, **kwargs
    ) -> List[SubscribeUserMarginOrderInstrumentResponse]:
        return list(
            map(
                SubscribeUserMarginOrderInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(
                    subscription=f"user.margin.order.{instrument_name}", *args, **kwargs
                ),
            )
        )

    def send_user_margin_trade_instrument(self, instrument_name: str):
        request = SubscribeUserMarginTradeInstrumentRequest(
            params=SubscribeUserMarginTradeInstrumentRequestParams(channels=[f"user.margin.trade.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_user_margin_trade_instrument_msgs(
        self, instrument_name: str, *args, **kwargs
    ) -> List[SubscribeUserMarginTradeInstrumentResponse]:
        return list(
            map(
                SubscribeUserMarginTradeInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(
                    subscription=f"user.margin.trade.{instrument_name}", *args, **kwargs
                ),
            )
        )

    def send_user_margin_balance(self):
        request = SubscribeUserMarginBalanceRequest().json(exclude_none=True)
        self.client.send(request)

    def get_user_margin_balance_msgs(self, *args, **kwargs) -> List[SubscribeUserMarignBalanceResponse]:
        return list(
            map(
                SubscribeUserMarignBalanceResponse.parse_raw,
                self.client.get_subscription_messages(subscription="user.margin.balance", *args, **kwargs),
            )
        )

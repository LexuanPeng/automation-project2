from typing import List

from ...ws_base import DerivativesWsService
from ..models.candlestick import (
    SubscribeCandlestickInstrumentRequest,
    SubscribeCandlestickInstrumentRequestParams,
    SubscribeCandlestickInstrumentResponse,
)
from ..models.instruments import (
    SubscribeMarkInstrumentRequest,
    SubscribeMarkInstrumentRequestParams,
    SubscribeMarkInstrumentResponse,
)
from ..models.order_book import (
    SubscribeBookInstrumentRequest,
    SubscribeBookInstrumentRequestParams,
    SubscribeBookInstrumentResponse,
)
from ..models.ticker import (
    SubscribeTickerInstrumentRequest,
    SubscribeTickerInstrumentRequestParams,
    SubscribeTickerInstrumentResponse,
)
from ..models.trade import (
    SubscribeTradeInstrumentRequest,
    SubscribeTradeInstrumentRequestParams,
    SubscribeTradeInstrumentResponse,
)
from ..models.index_instrument import (
    SubscribeIndexInstrumentRequest,
    SubscribeIndexInstrumentRequestParams,
    SubscribeIndexInstrumentResponse,
)
from ..models.settlement_instrument import (
    SubscribeSettlementInstrumentRequest,
    SubscribeSettlementInstrumentRequestParams,
    SubscribeSettlementInstrumentResponse,
)
from ..models.funding_instrument import (
    SubscribeFundingInstrumentRequest,
    SubscribeFundingInstrumentRequestParams,
    SubscribeFundingInstrumentResponse,
)


class MarketSubscribeService(DerivativesWsService):
    def send_mark_instrument(self, instrument_name: str):
        request = SubscribeMarkInstrumentRequest(
            params=SubscribeMarkInstrumentRequestParams(channels=[f"mark.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_mark_instrument_msgs(self, instrument_name: str, *args, **kwargs) -> List[SubscribeMarkInstrumentResponse]:
        return list(
            map(
                SubscribeMarkInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"mark.{instrument_name}", *args, **kwargs),
            )
        )

    def send_book_instrument(self, instrument_name: str, depth: int = None):
        channel = f"book.{instrument_name}"
        if depth is not None:
            channel += f".{depth}"
        request = SubscribeBookInstrumentRequest(params=SubscribeBookInstrumentRequestParams(channels=[channel])).json(
            exclude_none=True
        )
        self.client.send(request)

    def get_book_instrument_msgs(self, instrument_name: str, depth: int = None, *args, **kwargs):
        subscription = f"book.{instrument_name}"
        if depth is not None:
            subscription += f".{depth}"
        return list(
            map(
                SubscribeBookInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=subscription, *args, **kwargs),
            )
        )

    def send_ticker_instrument(self, instrument_name: str):
        request = SubscribeTickerInstrumentRequest(
            params=SubscribeTickerInstrumentRequestParams(channels=[f"ticker.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_ticker_instrument_msgs(self, instrument_name: str, *args, **kwargs):
        return list(
            map(
                SubscribeTickerInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"ticker.{instrument_name}", *args, **kwargs),
            )
        )

    def send_trade_instrument(self, instrument_name: str):
        request = SubscribeTradeInstrumentRequest(
            params=SubscribeTradeInstrumentRequestParams(channels=[f"trade.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_trade_instrument_msgs(self, instrument_name: str, *args, **kwargs):
        return list(
            map(
                SubscribeTradeInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"trade.{instrument_name}", *args, **kwargs),
            )
        )

    def send_candlestick_instrument(self, instrument_name: str, time_frame: str):
        request = SubscribeCandlestickInstrumentRequest(
            params=SubscribeCandlestickInstrumentRequestParams(channels=[f"candlestick.{time_frame}.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_candlestick_instrument_msgs(self, instrument_name: str, time_frame: str, *args, **kwargs):
        return list(
            map(
                SubscribeCandlestickInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(
                    subscription=f"candlestick.{time_frame}.{instrument_name}", *args, **kwargs
                ),
            )
        )

    def send_index_instrument(self, instrument_name: str):
        request = SubscribeIndexInstrumentRequest(
            params=SubscribeIndexInstrumentRequestParams(channels=[f"index.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_index_instrument_msgs(self, instrument_name: str, *args, **kwargs):
        return list(
            map(
                SubscribeIndexInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"index.{instrument_name}", *args, **kwargs),
            )
        )

    def send_settlement_instrument(self, instrument_name: str):
        request = SubscribeSettlementInstrumentRequest(
            params=SubscribeSettlementInstrumentRequestParams(channels=[f"settlement.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_settlement_instrument_msgs(self, instrument_name: str, *args, **kwargs):
        return list(
            map(
                SubscribeSettlementInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"settlement.{instrument_name}", *args, **kwargs),
            )
        )

    def send_funding_instrument(self, instrument_name: str):
        request = SubscribeFundingInstrumentRequest(
            params=SubscribeFundingInstrumentRequestParams(channels=[f"funding.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_funding_instrument_msgs(self, instrument_name: str, *args, **kwargs):
        return list(
            map(
                SubscribeFundingInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"funding.{instrument_name}", *args, **kwargs),
            )
        )

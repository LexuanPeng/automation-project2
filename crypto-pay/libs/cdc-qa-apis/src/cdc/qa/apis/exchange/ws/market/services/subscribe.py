from typing import List

from ...ws_base import ExchangeWsService
from ..models.instruments import (
    SubscribeBookInstrumentDepthRequest,
    SubscribeBookInstrumentDepthRequestParams,
    SubscribeBookInstrumentDepthResponse,
    SubscribeTickerInstrumentResponse,
    SubscribeTickerInstrumentRequest,
    SubscribeTickerInstrumentRequestParams,
    SubscribeTradeInstrumentResponse,
    SubscribeTradeInstrumentRequestParams,
    SubscribeTradeInstrumentRequest,
    SubscribeCandlestickIntervelInstrumentRequestParams,
    SubscribeCandlestickIntervelInstrumentRequest,
    SubscribeCandlestickIntervelInstrumentResponse,
)


class MarketSubscribeService(ExchangeWsService):
    def send_book_instrument_depth(self, instrument_name: str, depth: int):
        """
        subsrible channels is "book.{instrument_name}.{depth}"
        Args:
            instrument_name:
            depth: Number of bids and asks to return. Allowed values: 10 or 150

        Returns:

        """
        request = SubscribeBookInstrumentDepthRequest(
            params=SubscribeBookInstrumentDepthRequestParams(channels=[f"book.{instrument_name}.{depth}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_book_instrument_depth_msgs(
        self, instrument_name: str, depth: int, *args, **kwargs
    ) -> List[SubscribeBookInstrumentDepthResponse]:
        """
        subsrible channels is "book.{instrument_name}.{depth}"
        Args:
            instrument_name:
            depth: Number of bids and asks to return. Allowed values: 10 or 150
            *args:
            **kwargs:

        Returns:

        """
        return list(
            map(
                SubscribeBookInstrumentDepthResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"book.{instrument_name}.{depth}", *args, **kwargs),
            )
        )

    def send_ticker_instrument(self, instrument_name: str):
        """
        subsrible channels is "trade.{instrument_name}"
        Args:
            instrument_name:

        Returns:

        """
        request = SubscribeTickerInstrumentRequest(
            params=SubscribeTickerInstrumentRequestParams(channels=[f"ticker.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_ticker_instrument_msgs(
        self, instrument_name: str, *args, **kwargs
    ) -> List[SubscribeTickerInstrumentResponse]:
        """
        subsrible channels is "ticker.{instrument_name}"
        Args:
            instrument_name:
            *args:
            **kwargs:

        Returns:

        """
        return list(
            map(
                SubscribeTickerInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"ticker.{instrument_name}", *args, **kwargs),
            )
        )

    def send_trade_instrument(self, instrument_name: str):
        """
        subsrible channels is "trade.{instrument_name}"
        Args:
            instrument_name:

        Returns:

        """
        request = SubscribeTradeInstrumentRequest(
            params=SubscribeTradeInstrumentRequestParams(channels=[f"trade.{instrument_name}"])
        ).json(exclude_none=True)
        self.client.send(request)

    def get_trade_instrument_msgs(
        self, instrument_name: str, *args, **kwargs
    ) -> List[SubscribeTradeInstrumentResponse]:
        """
        subsrible channels is "trade.{instrument_name}"
        Args:
            instrument_name:
            *args:
            **kwargs:

        Returns:

        """
        return list(
            map(
                SubscribeTradeInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(subscription=f"trade.{instrument_name}", *args, **kwargs),
            )
        )

    def send_candlestick_interval_instrument(self, interval: str, instrument_name: str):
        """
        subsrible channels is "candlestick.{interval}.{instrument_name}"
        Args:
            interval:
                1m : one minute
                5m : five minutes
                15m : 15 minutes
                30m: 30 minutes
                1h : one hour
                4h : 4 hours
                6h : 6 hours
                12h : 12 hours
                1D : one day
                7D : one week
                14D : two weeks
                1M : one month
            instrument_name:

        Returns:

        """
        request = SubscribeCandlestickIntervelInstrumentRequest(
            params=SubscribeCandlestickIntervelInstrumentRequestParams(
                channels=[f"candlestick.{interval}.{instrument_name}"]
            )
        ).json(exclude_none=True)
        self.client.send(request)

    def get_candlestick_interval_instrument_msgs(
        self, interval: str, instrument_name: str, *args, **kwargs
    ) -> List[SubscribeCandlestickIntervelInstrumentResponse]:
        """
        subsrible channels is "candlestick.{interval}.{instrument_name}"
        Args:
            interval:
                1m : one minute
                5m : five minutes
                15m : 15 minutes
                30m: 30 minutes
                1h : one hour
                4h : 4 hours
                6h : 6 hours
                12h : 12 hours
                1D : one day
                7D : one week
                14D : two weeks
                1M : one month
            instrument_name:
            *args:
            **kwargs:

        Returns:

        """
        return list(
            map(
                SubscribeCandlestickIntervelInstrumentResponse.parse_raw,
                self.client.get_subscription_messages(
                    subscription=f"candlestick.{interval}.{instrument_name}", *args, **kwargs
                ),
            )
        )

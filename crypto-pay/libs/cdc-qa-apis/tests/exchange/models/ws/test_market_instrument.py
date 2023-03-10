import json
from decimal import Decimal
from cdc.qa.apis.exchange.ws.market.models.instruments import (
    SubscribeBookInstrumentDepthResponse,
    SubscribeTickerInstrumentResponse,
    SubscribeTradeInstrumentResponse,
    SubscribeCandlestickIntervelInstrumentResponse,
)


def test_book_instrument_depth_response_model():
    data = json.dumps(
        {
            "code": 0,
            "method": "subscribe",
            "result": {
                "instrument_name": "ETH_USDT",
                "subscription": "book.ETH_USDT.150",
                "channel": "book",
                "depth": 150,
                "data": [
                    {
                        "bids": [
                            [500.00, 1.00000, 1],
                            [400.00, 983.95593, 1],
                            [301.00, 220.30108, 1],
                            [100.00, 1.00000, 1],
                        ],
                        "asks": [[6000.00, "0.99000", 1]],
                        "t": 1627885939107,
                    }
                ],
            },
        }
    ).encode()
    response = SubscribeBookInstrumentDepthResponse.parse_raw(b=data)
    result_data = response.result.data[0]
    bids = result_data.bids[0]
    asks = result_data.asks[0]
    assert result_data.t == 1627885939107
    assert bids[0] == Decimal("500.00")
    assert bids[1] == Decimal("1.00000")
    assert bids[2] == 1
    assert asks[0] == Decimal("6000.00")
    assert Decimal(asks[1]) == Decimal("0.99000")
    assert asks[2] == 1


def test_ticker_instrument_response_model():
    data = json.dumps(
        {
            "code": 0,
            "method": "subscribe",
            "result": {
                "instrument_name": "BTC_USDT",
                "subscription": "ticker.BTC_USDT",
                "channel": "ticker",
                "data": [
                    {
                        "h": "18761.00",
                        "l": "16990.90",
                        "a": "17014.42",
                        "c": "-0.0172",
                        "b": "16991.31",
                        "bs": "2.99966",
                        "k": "2.99",
                        "ks": "3.12",
                        "i": "BTC_USDT",
                        "v": "0.9008",
                        "vv": "16246.40",
                        "t": 1670344991458,
                    }
                ],
            },
        }
    ).encode()
    response = SubscribeTickerInstrumentResponse.parse_raw(b=data)
    result_data = response.result.data[0]
    assert result_data.h == Decimal("18761.00")
    assert result_data.lowerest_trade == Decimal("16990.90")
    assert result_data.a == Decimal("17014.42")
    assert result_data.c == Decimal("-0.0172")
    assert result_data.b == Decimal("16991.31")
    assert result_data.bs == Decimal("2.99966")
    assert result_data.k == Decimal("2.99")
    assert result_data.ks == Decimal("3.12")
    assert result_data.i == "BTC_USDT"
    assert result_data.v == Decimal("0.9008")
    assert result_data.vv == Decimal("16246.40")
    assert result_data.t == 1670344991458


def test_trade_instrument_response_model():
    data = json.dumps(
        {
            "code": 0,
            "method": "subscribe",
            "result": {
                "instrument_name": "ETH_USDT",
                "subscription": "trade.ETH_USDT",
                "channel": "trade",
                "data": [
                    {
                        "dataTime": 1627875410148,
                        "d": 1679017140259018240,
                        "s": "SELL",
                        "p": 4000.00,
                        "q": 0.91500,
                        "t": 1627875410108,
                        "i": "ETH_USDT",
                    },
                ],
            },
        }
    ).encode()
    response = SubscribeTradeInstrumentResponse.parse_raw(b=data)
    result_data = response.result.data[0]
    assert result_data.dataTime == 1627875410148
    assert result_data.d == 1679017140259018240
    assert result_data.s == "SELL"
    assert result_data.p == Decimal("4000.00")
    assert result_data.q == Decimal("0.91500")
    assert result_data.t == 1627875410108
    assert result_data.i == "ETH_USDT"


def test_candlestick_interval_instrument_response_model():
    data = json.dumps(
        {
            "method": "subscribe",
            "result": {
                "instrument_name": "ETH_CRO",
                "subscription": "candlestick.1m.ETH_CRO",
                "channel": "candlestick",
                "interval": "1m",
                "data": [
                    {
                        "o": "18252.11",
                        "h": "18252.12",
                        "l": "18252.13",
                        "c": "18252.14",
                        "v": "0",
                        "t": 1669762740000,
                        "ut": 1669762760000,
                    },
                ],
            },
        }
    ).encode()
    response = SubscribeCandlestickIntervelInstrumentResponse.parse_raw(b=data)
    result_data = response.result.data[0]
    assert result_data.o == Decimal("18252.11")
    assert result_data.h == Decimal("18252.12")
    assert result_data.c == Decimal("18252.14")
    assert result_data.v == Decimal("0")
    assert result_data.t == 1669762740000
    assert result_data.ut == 1669762760000

import json
from decimal import Decimal
from cdc.qa.apis.exchange.ws.user.models.trade import SubscribeUserTradeInstrumentResponse


def test_user_trade_instrument_response_model():
    data = json.dumps(
        {
            "method": "subscribe",
            "code": 0,
            "result": {
                "instrument_name": "ETH_CRO",
                "subscription": "user.trade.ETH_CRO",
                "channel": "user.trade",
                "data": [
                    {
                        "side": "SELL",
                        "instrument_name": "ETH_CRO",
                        "fee": 0.014,
                        "trade_id": "367107655537806900",
                        "create_time": 1588777459755,
                        "traded_price": 7,
                        "traded_quantity": 1,
                        "fee_currency": "CRO",
                        "order_id": "367107623521528450",
                    }
                ],
            },
        }
    ).encode()
    response = SubscribeUserTradeInstrumentResponse.parse_raw(b=data)
    result = response.result
    data = result.data[0]
    assert data.side == "SELL"
    assert data.fee == Decimal("0.014")
    assert data.trade_id == "367107655537806900"
    assert data.create_time == 1588777459755
    assert data.traded_price == 7
    assert data.traded_quantity == 1
    assert data.fee_currency == "CRO"
    assert data.order_id == "367107623521528450"

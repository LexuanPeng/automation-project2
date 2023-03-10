import json
from decimal import Decimal
from cdc.qa.apis.exchange.ws.user.models.margin import (
    SubscribeUserMarginOrderInstrumentResponse,
    SubscribeUserMarginTradeInstrumentResponse,
    SubscribeUserMarignBalanceResponse,
)


def test_user_margin_order_instrument_response_model():
    data = json.dumps(
        {
            "method": "subscribe",
            "result": {
                "instrument_name": "ETH_CRO",
                "subscription": "user.margin.order.ETH_CRO",
                "channel": "user.margin.order",
                "data": [
                    {
                        "status": "ACTIVE",
                        "side": "BUY",
                        "price": 1,
                        "quantity": 1,
                        "order_id": "366455245775097673",
                        "client_oid": "my_order_0002",
                        "create_time": 1588758017375,
                        "update_time": 1588758017411,
                        "type": "LIMIT",
                        "instrument_name": "ETH_CRO",
                        "cumulative_quantity": 0,
                        "cumulative_value": 0,
                        "avg_price": 0,
                        "fee_currency": "CRO",
                        "time_in_force": "GOOD_TILL_CANCEL",
                        "trigger_price": 0,
                        "exec_inst": "",
                    }
                ],
            },
        }
    )
    response = SubscribeUserMarginOrderInstrumentResponse.parse_raw(b=data)
    result_data = response.result.data[0]
    assert result_data.order_id == "366455245775097673"
    assert result_data.client_oid == "my_order_0002"
    assert result_data.create_time == 1588758017375
    assert result_data.update_time == 1588758017411
    assert result_data.status == "ACTIVE"
    assert result_data.type == "LIMIT"
    assert result_data.side == "BUY"
    assert result_data.instrument_name == "ETH_CRO"
    assert result_data.price == 1
    assert result_data.quantity == 1
    assert result_data.cumulative_quantity == 0
    assert result_data.cumulative_value == 0
    assert result_data.avg_price == 0
    assert result_data.fee_currency == "CRO"
    assert result_data.time_in_force == "GOOD_TILL_CANCEL"
    # assert result_data.exec_inst
    assert result_data.trigger_price == 0


def test_user_margin_trade_instrument_response_model():
    data = json.dumps(
        {
            "method": "subscribe",
            "code": 0,
            "result": {
                "instrument_name": "ETH_CRO",
                "subscription": "user.margin.trade.ETH_CRO",
                "channel": "user.margin.trade",
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
    )
    response = SubscribeUserMarginTradeInstrumentResponse.parse_raw(b=data)
    result_data = response.result.data[0]
    assert result_data.side == "SELL"
    assert result_data.fee == Decimal("0.014")
    assert result_data.trade_id == "367107655537806900"
    assert result_data.create_time == 1588777459755
    assert result_data.traded_price == 7
    assert result_data.traded_quantity == 1
    assert result_data.fee_currency == "CRO"
    assert result_data.order_id == "367107623521528450"


def test_user_margin_balance_response_model():
    data = json.dumps(
        {
            "method": "subscribe",
            "result": {
                "subscription": "user.margin.balance",
                "channel": "user.margin.balance",
                "data": [
                    {
                        "currency": "CRO",
                        "balance": 99999999947.99626,
                        "available": 99999988201.50826,
                        "order": 11746.488,
                        "stake": 0,
                    }
                ],
            },
        }
    ).encode()
    response = SubscribeUserMarignBalanceResponse.parse_raw(b=data)
    result = response.result
    data = result.data[0]
    assert data.currency == "CRO"
    assert data.balance == Decimal("99999999947.99626")
    assert data.available == Decimal("99999988201.50826")
    assert data.order == Decimal("11746.488")
    assert data.stake == 0

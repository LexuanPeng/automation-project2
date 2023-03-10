import json
from cdc.qa.apis.exchange.ws.user.models.order import SubscribeUserOrderInstrumentResponse


def test_user_balance_response_model():
    data = json.dumps(
        {
            "method": "subscribe",
            "result": {
                "instrument_name": "ETH_CRO",
                "subscription": "user.order.ETH_CRO",
                "channel": "user.order",
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
                        "exec_inst": "",
                        "trigger_price": 0,
                    }
                ],
            },
        }
    ).encode()
    response = SubscribeUserOrderInstrumentResponse.parse_raw(b=data)
    result = response.result
    data = result.data[0]
    assert data.status == "ACTIVE"
    assert data.side == "BUY"
    assert data.price == 1
    assert data.quantity == 1
    assert data.order_id == "366455245775097673"
    assert data.create_time == 1588758017375
    assert data.update_time == 1588758017411
    assert data.type == "LIMIT"
    assert data.instrument_name == "ETH_CRO"
    assert data.avg_price == 0
    assert data.cumulative_quantity == 0
    assert data.cumulative_value == 0
    assert data.fee_currency == "CRO"
    assert data.time_in_force == "GOOD_TILL_CANCEL"

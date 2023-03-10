import json
from decimal import Decimal
from cdc.qa.apis.exchange.ws.user.models.account import SubscribeUserBalanceResponse


def test_user_balance_response_model():
    data = json.dumps(
        {
            "method": "subscribe",
            "result": {
                "subscription": "user.balance",
                "channel": "user.balance",
                "data": [
                    {
                        "currency": "CRO",
                        "balance": 99999999947.99626,
                        "available": 99999988201.50826,
                        "order": 11746.488,
                        "stake": 0,
                    }
                ],
                "channel": "user.balance",
            },
        }
    ).encode()
    response = SubscribeUserBalanceResponse.parse_raw(b=data)
    result = response.result
    data = result.data[0]
    assert data.currency == "CRO"
    assert data.balance == Decimal("99999999947.99626")
    assert data.available == Decimal("99999988201.50826")
    assert data.order == Decimal("11746.488")
    assert data.stake == 0

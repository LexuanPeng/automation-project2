from pytest import fixture


@fixture
def mock_get_beta_instruments(requests_mock):
    requests_mock.get(
        "https://dstg-rest-gateway.x.3ona.co/deriv/v1/public/get-beta-instruments",
        json={
            "id": -1,
            "method": "public/get-beta-instruments",
            "code": 0,
            "result": {
                "data": [
                    {
                        "symbol": "BTCUSD-211227-CW43000",
                        "inst_type": "WARRANT",
                        "display_name": "BTCUSD-211227-CW43000",
                        "base_ccy": "BTC",
                        "quote_ccy": "USD_Stable_Coin",
                        "quote_decimals": 3,
                        "quantity_decimals": 0,
                        "price_tick_size": "0.001",
                        "qty_tick_size": "10",
                        "max_leverage": "50",
                        "tradable": False,
                        "expiry_timestamp_ms": 1640592000000,
                        "beta_product": True,
                        "underlying_symbol": "BTCUSD-INDEX",
                        "put_call": "CALL",
                        "strike": "43000",
                        "contract_size": "0.0001",
                    },
                    {
                        "symbol": "BTCUSD-211227-CW47000",
                        "inst_type": "WARRANT",
                        "display_name": "BTCUSD-211227-CW47000",
                        "base_ccy": "BTC",
                        "quote_ccy": "USD_Stable_Coin",
                        "quote_decimals": 3,
                        "quantity_decimals": 0,
                        "price_tick_size": "0.001",
                        "qty_tick_size": "10",
                        "max_leverage": "50",
                        "tradable": False,
                        "expiry_timestamp_ms": 1640592000000,
                        "beta_product": True,
                        "underlying_symbol": "BTCUSD-INDEX",
                        "put_call": "CALL",
                        "strike": "47000",
                        "contract_size": "0.0001",
                    },
                ]
            },
        },
    )

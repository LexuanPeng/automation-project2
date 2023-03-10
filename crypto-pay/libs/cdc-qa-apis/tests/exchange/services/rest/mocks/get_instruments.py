from pytest import fixture


@fixture
def mock_get_instruments(requests_mock):
    requests_mock.get(
        "https://uat-api.3ona.co/v2/public/get-instruments",
        json={
            "id": 1627888779104,
            "method": "public/get-instruments",
            "code": 0,
            "result": {
                "instruments": [
                    {
                        "instrument_name": "SHIB_USDT",
                        "quote_currency": "USDT",
                        "base_currency": "SHIB",
                        "price_decimals": 9,
                        "quantity_decimals": 0,
                        "margin_trading_enabled": False,
                        "margin_trading_enabled_5x": False,
                        "margin_trading_enabled_10x": False,
                        "max_quantity": "10000000000",
                        "min_quantity": "10000",
                        "max_price": "0.1",
                        "min_price": "0.000000001",
                        "last_update_date": 1666239124809,
                        "price_tick_size": "0.000000001",
                        "quantity_tick_size": "10000",
                    },
                ]
            },
        },
    )

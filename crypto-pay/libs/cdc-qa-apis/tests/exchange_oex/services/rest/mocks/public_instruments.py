import pytest


@pytest.fixture()
def mock_get_instruments(requests_mock):
    requests_mock.get(
        "https://dstg-rest-gateway.x.3ona.co/v1/public/get-instruments",
        json={
            "id": -1,
            "method": "public/get-instruments",
            "code": 0,
            "result": {
                "data": [
                    {
                        "symbol": "BTCUSD-221028",
                        "inst_type": "FUTURE",
                        "display_name": "BTCUSD Futures 20221028",
                        "base_ccy": "BTC",
                        "quote_ccy": "USD_Stable_Coin",
                        "quote_decimals": 1,
                        "quantity_decimals": 4,
                        "price_tick_size": "0.1",
                        "qty_tick_size": "0.0001",
                        "max_leverage": "100",
                        "tradable": False,
                        "expiry_timestamp_ms": 1666944000000,
                        "beta_product": False,
                        "underlying_symbol": "BTCUSD-INDEX",
                        "contract_size": "1",
                        "margin_buy_enabled": False,
                        "margin_sell_enabled": False,
                    },
                    {
                        "symbol": "AAVEUSD-PERP",
                        "inst_type": "PERPETUAL_SWAP",
                        "display_name": "AAVEUSD Perpetual",
                        "base_ccy": "AAVE",
                        "quote_ccy": "USD_Stable_Coin",
                        "quote_decimals": 3,
                        "quantity_decimals": 2,
                        "price_tick_size": "0.001",
                        "qty_tick_size": "0.01",
                        "max_leverage": "50",
                        "tradable": True,
                        "expiry_timestamp_ms": 0,
                        "beta_product": False,
                        "underlying_symbol": "AAVEUSD-INDEX",
                        "contract_size": "1",
                        "margin_buy_enabled": False,
                        "margin_sell_enabled": False,
                    },
                ]
            },
        },
    )

from pytest import fixture


@fixture
def mock_get_ticker(requests_mock):
    requests_mock.get(
        "https://uat-api.3ona.co/v2/public/get-ticker",
        json={
            "code": 0,
            "method": "public/get-ticker",
            "result": {
                "data": [
                    {
                        "i": "VET_BTC",
                        "b": 0,
                        "k": 1.0000000000,
                        "a": 0.9000000000,
                        "t": 1623307337246,
                        "v": 1,
                        "h": 0.9000000000,
                        "l": 0.9000000000,
                        "c": 0.0000000000,
                    },
                    {
                        "i": "ZIL_CRO",
                        "b": 0,
                        "k": 0,
                        "a": 10.6383,
                        "t": 1623307328800,
                        "v": 0.00,
                        "h": 10.6383,
                        "l": 0.0000,
                        "c": 10.6382,
                    },
                    {
                        "i": "AUDIO_USDT",
                        "b": 0,
                        "k": 0,
                        "a": 0,
                        "t": 1623307333950,
                        "v": 0.00,
                        "h": 0.0000,
                        "l": 0.0000,
                        "c": 0.0000,
                    },
                    {
                        "i": "SUSHI_USDT",
                        "b": 0,
                        "k": 0,
                        "a": 0,
                        "t": 1623307334613,
                        "v": 0.000,
                        "h": 0.000,
                        "l": 0.000,
                        "c": 0.000,
                    },
                ]
            },
        },
    )


@fixture
def mock_get_ticker_btc_usdt(requests_mock):
    requests_mock.get(
        "https://uat-api.3ona.co/v2/public/get-ticker?instrument_name=BTC_USDT",
        json={
            "code": 0,
            "method": "public/get-ticker",
            "result": {
                "data": [
                    {
                        "i": "BTC_USDT",
                        "h": "19500.00",
                        "l": "13500.00",
                        "a": "16479.40",
                        "v": "5.0910",
                        "vv": "82408.50",
                        "c": "0.1771",
                        "b": "11117.00",
                        "k": "16486.68",
                        "t": 1669184061173,
                    }
                ]
            },
        },
    )

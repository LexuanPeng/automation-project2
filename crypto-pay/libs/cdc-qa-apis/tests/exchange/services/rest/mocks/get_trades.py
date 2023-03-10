from pytest import fixture


@fixture
def mock_get_trades(requests_mock):
    requests_mock.get(
        "https://uat-api.3ona.co/v2/public/get-trades",
        json={
            "code": 0,
            "method": "public/get-trades",
            "result": {
                "data": [
                    {
                        "s": "BUY",
                        "p": 2.96,
                        "q": 16.0,
                        "t": 1591710781946,
                        "i": "ICX_CRO",
                    },
                    {
                        "s": "BUY",
                        "p": 0.007749,
                        "q": 115.0,
                        "t": 1591707701898,
                        "i": "VET_USDT",
                    },
                    {
                        "s": "SELL",
                        "p": 25.676,
                        "q": 0.55,
                        "t": 1591710786154,
                        "i": "XTZ_CRO",
                    },
                    {
                        "s": "SELL",
                        "p": 2.9016,
                        "q": 0.6,
                        "t": 1591710783298,
                        "i": "XTZ_USDT",
                    },
                    {
                        "s": "SELL",
                        "p": 2.7662,
                        "q": 0.58,
                        "t": 1591710784498,
                        "i": "EOS_USDT",
                    },
                    {
                        "s": "SELL",
                        "p": 243.21,
                        "q": 0.01647,
                        "t": 1591710784698,
                        "i": "ETH_USDT",
                    },
                    {
                        "s": "SELL",
                        "p": 253.06,
                        "q": 0.00516,
                        "t": 1591710786598,
                        "i": "BCH_USDT",
                    },
                ],
            },
        },
    )

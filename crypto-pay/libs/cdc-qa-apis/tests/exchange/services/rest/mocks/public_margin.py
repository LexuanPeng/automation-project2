from pytest import fixture


@fixture
def mock_margin_get_transfer_currencies(requests_mock):
    requests_mock.get(
        "https://uat-api.3ona.co/v2/public/margin/get-transfer-currencies",
        json={
            "id": -1,
            "method": "public/margin/get-transfer-currencies",
            "code": 0,
            "result": {
                "transfer_currency_list": [
                    "BTC",
                    "USDT",
                    "CRO",
                    "USDC",
                    "ETH",
                    "ADA",
                    "VET",
                    "DOGE",
                    "DOT",
                    "UNI",
                    "LINK",
                    "ENJ",
                    "YFI",
                    "1INCH",
                    "KSM",
                    "ALGO",
                    "LTC",
                    "MATIC",
                    "XRP",
                    "XLM",
                    "EGLD",
                    "SHIB",
                    "CHZ",
                    "PAXG",
                    "RLY",
                    "AXS",
                    "SLP",
                    "LUNA",
                ]
            },
        },
    )


@fixture
def mock_margin_get_loan_currencies(requests_mock):
    requests_mock.get(
        "https://uat-api.3ona.co/v2/public/margin/get-loan-currencies",
        json={
            "id": -1,
            "method": "public/margin/get-loan-currencies",
            "code": 0,
            "result": {
                "loan_currency_list": [
                    "BTC",
                    "USDT",
                    "CRO",
                    "USDC",
                    "ETH",
                    "ADA",
                    "VET",
                    "DOGE",
                    "DOT",
                    "UNI",
                    "LINK",
                    "ENJ",
                    "YFI",
                    "1INCH",
                    "KSM",
                    "ALGO",
                    "LTC",
                    "MATIC",
                    "XRP",
                    "XLM",
                    "EGLD",
                    "SHIB",
                    "CHZ",
                    "PAXG",
                    "RLY",
                    "AXS",
                    "SLP",
                    "LUNA",
                ],
                "margin_enabled_pairs": [
                    "LTC_BTC",
                    "DOGE_USDT",
                    "SHIB_USDT",
                    "BOSON_USDT",
                    "VET_USDT",
                    "ALGO_USDT",
                    "UNI_USDT",
                    "DOGE_BTC",
                    "VET_USDC",
                    "DOT_USDT",
                    "EGLD_USDT",
                    "XRP_BTC",
                    "CHZ_USDT",
                    "MATIC_USDT",
                    "ADA_BTC",
                    "PAXG_USDT",
                    "DOT_BTC",
                    "YFI_USDT",
                    "CRO_USDT",
                    "ADA_USDC",
                    "RLY_USDT",
                    "AXS_USDT",
                    "DOT_USDC",
                    "ADA_USDT",
                    "CRO_BTC",
                    "LINK_BTC",
                    "VET_BTC",
                    "SLP_USDT",
                    "LUNA_USDT",
                    "BTC_USDT",
                    "KSM_USDT",
                    "LTC_USDT",
                    "BTC_USDC",
                    "ETH_USDT",
                    "LINK_USDT",
                    "1INCH_USDT",
                    "ETH_USDC",
                    "ETH_BTC",
                    "ENJ_USDT",
                    "XLM_BTC",
                ],
            },
        },
    )

from pytest import fixture


@fixture
def mock_add_staking(requests_mock):
    requests_mock.post(
        "https://xdev4-www.3ona.co/fe-ex-api/finance/add_staking?symbol=CRO&amount=5000",
        json={"code": "0", "msg": "Success", "data": None},
    )


@fixture
def mock_remove_staking(requests_mock):
    requests_mock.post(
        "https://xdev4-www.3ona.co/fe-ex-api/finance/remove_staking", json={"code": "0", "msg": "Success", "data": None}
    )


@fixture
def mock_fee_rates(requests_mock):
    requests_mock.get(
        "https://xdev4-www.3ona.co/fe-ex-api/finance/fee_rates",
        json={
            "code": "0",
            "msg": "Success",
            "data": {"maker_rate": 0, "taker_rate": 0, "is_discounted_fee": True, "is_vip": False, "tier": 5},
        },
    )


@fixture
def mock_get_charge_address(requests_mock):
    requests_mock.post(
        "https://xdev4-www.3ona.co/fe-ex-api/finance/get_charge_address",
        json={
            "code": "0",
            "msg": "Success",
            "data": {"addressStr": "address", "addressQRCode": "address_qr_code"},
        },
    )


@fixture
def mock_account_balance(requests_mock):
    requests_mock.get(
        "https://xdev4-www.3ona.co/fe-ex-api/finance/v5/account_balance",
        json={
            "code": "0",
            "msg": "Success",
            "data": {
                "total_balance_in_btc": 780147508.6151825,
                "total_balance_in_usd": 44731590753096.73,
                "symbols": {
                    "1INCH": {
                        "available_balance": "199999998.987",
                        "btc_equivalent": "3474.91707522",
                        "deposit_open": 0,
                        "in_order_balance": "0",
                        "is_fiat": 0,
                        "open_order_balance": "0",
                        "sort": 67,
                        "stake_balance": "0",
                        "supercharger_balance": "0",
                        "syndicate_balance": "0",
                        "total_balance": "199999998.987",
                        "usd_equivalent": "199242536.56286546",
                        "withdraw_open": 0,
                    },
                    "AAA": {
                        "available_balance": "0",
                        "btc_equivalent": "0",
                        "deposit_open": 1,
                        "in_order_balance": "0",
                        "is_fiat": 0,
                        "open_order_balance": "0",
                        "sort": 35,
                        "stake_balance": "0",
                        "supercharger_balance": "0",
                        "syndicate_balance": "0",
                        "total_balance": "0",
                        "usd_equivalent": "0",
                        "withdraw_open": 1,
                    },
                },
            },
        },
    )

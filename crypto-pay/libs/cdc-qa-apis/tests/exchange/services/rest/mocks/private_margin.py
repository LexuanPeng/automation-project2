from pytest import fixture


@fixture
def mock_margin_get_user_config(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-user-config",
        json={
            "id": 5276345,
            "method": "private/margin/get-user-config",
            "code": 0,
            "result": {
                "stake_amount": 50000000,
                "currency_configs": [
                    {
                        "currency": "ENJ",
                        "hourly_rate": 0.00000417,
                        "max_borrow_limit": 2000000,
                        "min_borrow_limit": 100,
                    }
                ],
            },
        },
    )


@fixture
def mock_margin_get_account_summary(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-account-summary",
        json={
            "id": 5276345,
            "method": "private/margin/get-account-summary",
            "code": 0,
            "result": {
                "accounts": [
                    {
                        "balance": 200.0022,
                        "available": 200.0022,
                        "order": 0,
                        "borrowed": 0.00019372,
                        "position": 200.00200628,
                        "positionHomeCurrency": 4691247.05930368,
                        "positionBtc": 200.00200628,
                        "lastPriceHomeCurrency": 23456,
                        "lastPriceBtc": 1,
                        "currency": "BTC",
                        "accrued_interest": 0,
                        "liquidation_price": 0,
                    },
                    {
                        "balance": 1095.989158,
                        "available": 1095.989158,
                        "order": 0,
                        "borrowed": 0,
                        "position": 1095.989158,
                        "positionHomeCurrency": 1095.989158,
                        "positionBtc": 0.04672201,
                        "lastPriceHomeCurrency": 1,
                        "lastPriceBtc": 0.00004263,
                        "currency": "USDT",
                        "accrued_interest": 0,
                        "liquidation_price": 0,
                    },
                ],
                "is_liquidating": False,
                "total_balance": 4692748.437311466,
                "total_balance_btc": 200.06601455,
                "equity_value": 4692743.893415146,
                "equity_value_btc": 200.06582083,
                "total_borrowed": 4.54389632,
                "total_borrowed_btc": 0.00019372,
                "total_accrued_interest": 0,
                "total_accrued_interest_btc": 0,
                "margin_ratio": 1032758.69,
                "margin_score": "GOOD",
                "currency": "USDT",
            },
        },
    )


@fixture
def mock_margin_transfer(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/transfer",
        json={"id": 5276345, "method": "private/margin/transfer", "code": 0},
    )


@fixture
def mock_margin_borrow(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/borrow",
        json={"id": 5276345, "method": "private/margin/borrow", "code": 0},
    )


@fixture
def mock_margin_repay(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/repay",
        json={"id": 5276345, "method": "private/margin/repay", "code": 0},
    )


@fixture
def mock_margin_get_transfer_history(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-transfer-history",
        json={
            "id": 5276345,
            "method": "private/margin/get-transfer-history",
            "code": 0,
            "result": {
                "transfer_list": [
                    {
                        "direction": "IN",
                        "time": 1627527955482,
                        "amount": 100,
                        "status": "COMPLETED",
                        "information": "From Spot Wallet",
                        "currency": "BTC",
                    },
                    {
                        "direction": "IN",
                        "time": 1627525052837,
                        "amount": 1000,
                        "status": "COMPLETED",
                        "information": "From Spot Wallet",
                        "currency": "USDT",
                    },
                ]
            },
        },
    )


@fixture
def mock_margin_get_borrow_history(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-borrow-history",
        json={
            "id": 5276345,
            "method": "private/margin/get-borrow-history",
            "code": 0,
            "result": {
                "borrow_list": [
                    {
                        "loan_id": "1667358632666702944",
                        "currency": "BTC",
                        "loan_amount": 2,
                        "borrow_time": 1627527959506,
                        "status": "ACTIVE",
                    }
                ]
            },
        },
    )


@fixture
def mock_margin_get_interest_history(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-interest-history",
        json={
            "id": 5276345,
            "method": "private/margin/get-interest-history",
            "code": 0,
            "result": {
                "list": [
                    {
                        "loan_id": "1667358632666702944",
                        "currency": "BTC",
                        "interest": 0,
                        "time": 1627538759506,
                        "stake_amount": 50000000,
                        "interest_rate": 0.00000334,
                    }
                ]
            },
        },
    )


@fixture
def mock_margin_get_repay_history(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-repay-history",
        json={
            "id": 5276345,
            "method": "private/margin/get-repay-history",
            "code": 0,
            "result": {
                "repay_list": [
                    {
                        "repay_id": "1667358655209851328",
                        "currency": "BTC",
                        "repay_amount": 2,
                        "repay_time": 1627527960178,
                        "status": "CONFIRMED",
                        "outstanding_debt": 0.00019372,
                        "principal_repayment": 1.99999332,
                        "outstanding_principal": 0.00019372,
                        "interest_repayment": 0.00000668,
                        "outstanding_interest": 0,
                        "repay_source": "Normal",
                    }
                ]
            },
        },
    )


@fixture
def mock_margin_get_liquidation_history(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-liquidation-history",
        json={
            "id": 5276345,
            "method": "private/margin/get-liquidation-history",
            "code": 0,
            "result": {
                "list": [
                    {
                        "time": 1627554526102,
                        "liquidation_status": "COMPLETED",
                        "email_status": 1,
                        "margin_level": "NORMAL",
                        "message": "Your Margin Wallet has been liquidated because your Margin Score "
                        "dropped to or below 1.1.",
                        "message_code": 2,
                    }
                ]
            },
        },
    )


@fixture
def mock_margin_get_liquidation_orders(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-liquidation-orders",
        json={
            "id": -1,
            # "method": "/private/get-order-history",
            "method": "private/margin/get-liquidation-orders",
            "code": 0,
            "result": {
                "order_list": [
                    {
                        "status": "FILLED",
                        "side": "SELL",
                        "price": 0.0,
                        "quantity": 0.0747,
                        "order_id": "1668250027295669696",
                        "client_oid": "LQ: 1627554524101",
                        "create_time": 1627554525137,
                        "update_time": 1627554525213,
                        "type": "MARKET",
                        "instrument_name": "ETH_USDT",
                        "avg_price": 400.0,
                        "cumulative_quantity": 0.0747,
                        "cumulative_value": 29.88,
                        "fee_currency": "USDT",
                        "exec_inst": "",
                        "time_in_force": "GOOD_TILL_CANCEL",
                    }
                ]
            },
        },
    )


@fixture
def mock_margin_create_order(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/create-order",
        json={
            "id": 5276345,
            "method": "private/margin/create-order",
            "code": 0,
            "result": {"order_id": "1667855088105953856"},
        },
    )


@fixture
def mock_margin_cancel_order(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/cancel-order",
        json={"id": 5276345, "method": "private/margin/cancel-order", "code": 0},
    )


@fixture
def mock_margin_cancel_all_orders(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/cancel-all-orders",
        json={"id": 5276345, "method": "private/margin/cancel-all-orders", "code": 0},
    )


@fixture
def mock_margin_get_order_history(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-order-history",
        json={
            "id": 5276345,
            "method": "private/margin/get-order-history",
            "code": 0,
            "result": {
                "order_list": [
                    {
                        "status": "FILLED",
                        "side": "BUY",
                        "price": 200000.00,
                        "quantity": 0.002000,
                        "order_id": "1664980974402252544",
                        "client_oid": "",
                        "create_time": 1627457099768,
                        "update_time": 1627457099831,
                        "type": "LIMIT",
                        "instrument_name": "BTC_USDT",
                        "avg_price": 200000.00000000,
                        "cumulative_quantity": 0.002000,
                        "cumulative_value": 400.00000000,
                        "fee_currency": "CRO",
                        "exec_inst": "",
                        "time_in_force": "GOOD_TILL_CANCEL",
                    }
                ]
            },
        },
    )


@fixture
def mock_margin_get_open_orders(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-open-orders",
        json={
            "id": 5276345,
            "method": "private/margin/get-open-orders",
            "code": 0,
            "result": {
                "count": 2,
                "order_list": [
                    {
                        "status": "ACTIVE",
                        "side": "BUY",
                        "price": 13.770,
                        "quantity": 5.000,
                        "order_id": "1650488516770762784",
                        "client_oid": "",
                        "create_time": 1627025190874,
                        "update_time": 1627025190928,
                        "type": "LIMIT",
                        "instrument_name": "DOT_USDC",
                        "avg_price": 0e-8,
                        "cumulative_quantity": 0.000,
                        "cumulative_value": 0e-8,
                        "fee_currency": "CRO",
                        "exec_inst": "",
                        "time_in_force": "GOOD_TILL_CANCEL",
                    }
                ],
            },
        },
    )


@fixture
def mock_margin_get_order_detail(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-order-detail",
        json={
            "id": 5276345,
            "method": "private/margin/get-order-detail",
            "code": 0,
            "result": {
                "trade_list": [
                    {
                        "side": "BUY",
                        "fee": 8.00000000,
                        "trade_id": "1664980976500418080",
                        "instrument_name": "BTC_USDT",
                        "create_time": 1627457099831,
                        "traded_price": 200000.00,
                        "traded_quantity": 0.002000,
                        "fee_currency": "CRO",
                        "order_id": "1664980974402252544",
                        "client_oid": "",
                        "liquidity_indicator": "TAKER",
                    }
                ],
                "order_info": {
                    "status": "FILLED",
                    "side": "BUY",
                    "price": 200000.00,
                    "quantity": 0.002000,
                    "order_id": "1664980974402252544",
                    "client_oid": "",
                    "create_time": 1627457099768,
                    "update_time": 1627457099831,
                    "type": "LIMIT",
                    "instrument_name": "BTC_USDT",
                    "avg_price": 200000.00000000,
                    "cumulative_quantity": 0.002000,
                    "cumulative_value": 400.00000000,
                    "fee_currency": "CRO",
                    "exec_inst": "",
                    "time_in_force": "GOOD_TILL_CANCEL",
                },
            },
        },
    )


@fixture
def mock_margin_get_trades(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-trades",
        json={
            "id": 5276345,
            "method": "private/margin/get-trades",
            "code": 0,
            "result": {
                "trade_list": [
                    {
                        "side": "BUY",
                        "fee": 0.80000000,
                        "trade_id": "1665401749164103488",
                        "instrument_name": "BTC_USDT",
                        "create_time": 1627469639833,
                        "traded_price": 20000.00,
                        "traded_quantity": 0.000200,
                        "fee_currency": "CRO",
                        "order_id": "1665401746210855264",
                        "client_oid": "",
                        "liquidity_indicator": "TAKER",
                    }
                ]
            },
        },
    )


@fixture
def mock_get_margin_trading_user(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/get-margin-trading-user",
        json={
            "id": 5276345,
            "method": "private/margin/get-margin-trading-user",
            "code": 0,
            "result": {"margin_leverage": 5},
        },
    )


@fixture
def mock_adjust_margin_leverage(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/margin/adjust-margin-leverage",
        json={"id": 5276345, "method": "private/margin/adjust-margin-leverage", "code": 0},
    )

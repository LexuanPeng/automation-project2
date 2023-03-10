from pytest import fixture


@fixture
def mock_sub_account_get_balance(requests_mock):
    requests_mock.post(
        "https://dstg-rest-gateway.x.3ona.co/deriv/v1/private/get-subaccount-balances",
        json={
            "id": 12,
            "method": "private/get-subaccount-balances",
            "code": 0,
            "result": {
                "data": [
                    {
                        "total_available_balance": "29.00783000",
                        "total_margin_balance": "29.00783000",
                        "total_initial_margin": "0.00000000",
                        "total_maintenance_margin": "0.00000000",
                        "total_position_cost": "0.00000000",
                        "total_cash_balance": "30.27140000",
                        "total_collateral_value": "29.00783000",
                        "total_session_unrealized_pnl": "0.00000000",
                        "instrument_name": "USD_Stable_Coin",
                        "total_session_realized_pnl": "0.00000000",
                        "position_balances": [
                            {
                                "quantity": "30.00000000",
                                "collateral_weight": "0.950000",
                                "collateral_amount": "24.00783000",
                                "market_value": "25.27140000",
                                "max_withdrawal_balance": "30.00000000",
                                "instrument_name": "CRO",
                            },
                            {
                                "quantity": "5.00000000",
                                "collateral_weight": "1.000000",
                                "collateral_amount": "5.00000000",
                                "market_value": "5.00000000",
                                "max_withdrawal_balance": "5.00000000",
                                "instrument_name": "USD_Stable_Coin",
                            },
                        ],
                        "total_effective_leverage": "0.000000",
                        "position_limit": "3000000.00000000",
                        "used_position_limit": "0.00000000",
                        "account": "8ed53e70-86d7-4d3b-a9dc-5e0755ac6714",
                        "is_liquidating": False,
                    }
                ]
            },
        },
    )

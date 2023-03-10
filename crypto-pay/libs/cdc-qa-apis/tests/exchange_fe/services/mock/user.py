from pytest import fixture


@fixture
def mock_update_fee_coin_open(requests_mock):
    requests_mock.post(
        "https://xdev4-www.3ona.co/fe-ex-api/user/update_fee_coin_open",
        json={"code": "0", "msg": "Success", "data": None},
    )


@fixture
def mock_staking_info(requests_mock):
    requests_mock.get(
        "https://xdev4-www.3ona.co/fe-ex-api/user/staking_info",
        json={
            "code": "0",
            "msg": "Success",
            "data": {
                "staked_before": True,
                "staking_currency": "CRO",
                "dynamic_coin_bonus_remaining_days": "0",
                "can_unstake": False,
                "trading_volume_tier": "5",
                "open_reward_session": False,
                "can_unstake_in_days": 180,
                "deposit_bonus_period": "30",
                "dynamic_coin_bonus_amount": "0",
                "uuid": "ec8716ba-ceab-4b62-a1cd-96421e76d0d6",
                "staking_delta_to_tier_2": "-50015000",
                "staking_amount": "50025000.00000000",
                "min_staking_days": 180,
                "user_created_duration": "485",
                "past_trading_volume": "407356.0000000000040000",
                "id": 1000000734,
                "total_deposit_bonus": "0",
            },
        },
    )


@fixture
def mock_withdrawal_info(requests_mock):
    requests_mock.get(
        "https://xdev4-www.3ona.co/fe-ex-api/user/withdrawal_info",
        json={
            "code": "0",
            "msg": "Succeed",
            "data": {
                "userTier": 2,
                "last24hAmountInUsd": "0.0",
                "24hLimitAmount": "200.0",
                "24hLimitCurrency": "BTC",
                "last24hAmountInBtc": "0.0",
            },
        },
    )

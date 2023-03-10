from decimal import Decimal
from .mock.user import *  # noqa


def test_update_fee_coin_open(service, mock_update_fee_coin_open):
    response = service.user.update_fee_coin_open(0)
    assert int(response.code) == 0
    assert response.msg == "Success"


def test_get_staking_info(service, mock_staking_info):
    response = service.user.staking_info()
    data = response.data
    assert not data.can_unstake
    assert data.can_unstake_in_days == 180
    assert data.past_trading_volume == "407356.0000000000040000"
    assert data.trading_volume_tier == "5"


def test_get_withdrawal_info(service, mock_withdrawal_info):
    response = service.user.withdrawal_info()
    assert response.code == "0"
    assert response.msg == "Succeed"
    data = response.data
    assert data.LimitAmount24h == Decimal("200.0")
    assert data.LimitCurrency24h == "BTC"
    assert data.last24hAmountInBtc == Decimal("0")
    assert data.last24hAmountInUsd == Decimal("0")
    assert data.userTier == 2

from decimal import Decimal
from .mock.common import *  # noqa


def test_get_user_info(service, mock_get_user_info):
    response = service.common.user_info()
    assert response.code == "0"
    assert response.msg == "Success"
    data = response.data
    assert data.marginAccountStatus == 1
    assert data.email == "evelyn.wang+sz01@crypto.com"
    assert data.isEligibleForMarginFeature
    assert data.userTier == 2


def test_supported_coins(service, mock_supported_coins):
    response = service.common.supported_coins()
    assert response.code == "0"
    assert response.msg == "Success"
    data = response.data
    assert data.lastUpdatedAt
    assert data.symbols.AGLD.networks[0].network == "ETH"
    assert data.symbols.AGLD.networks[0].withdrawalFees is None
    assert len(data.symbols.MATIC.networks) == 3
    assert data.symbols.MATIC.networks[0].address_max_length == 256
    assert data.symbols.MATIC.networks[0].minWithdrawalAmount == Decimal("40")

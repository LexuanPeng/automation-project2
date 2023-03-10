from decimal import Decimal
from .mock.finance import *  # noqa


def test_add_staking(service, mock_add_staking):
    response = service.finance.add_staking("CRO", add_amount=5000, total_amount=5000)
    assert response.code == "0"
    assert response.data is None


def test_remove_staking(service, mock_remove_staking):
    response = service.finance.remove_staking("CRO", 5000)
    assert response.code == "0"
    assert response.data is None


def test_get_fee_rates(service, mock_fee_rates):
    response = service.finance.fee_rates()
    data = response.data
    assert response.code == "0"
    assert not data.is_vip
    assert data.maker_rate == 0
    assert data.taker_rate == 0
    assert data.tier == 5


def test_get_charge_address(service, mock_get_charge_address):
    response = service.finance.get_charge_address("CRO", "ERC20")
    data = response.data
    assert response.code == "0"
    assert data.addressStr == "address"
    assert data.addressQRCode == "address_qr_code"


def test_account_balance(service, mock_account_balance):
    response = service.finance.v5_account_balance()
    data = response.data
    print(response)
    assert response.code == "0"
    assert data.total_balance_in_usd == Decimal("44731590753096.73")
    assert data.total_balance_in_btc == Decimal("780147508.6151825")
    assert data.symbols.AAA.deposit_open

from cdc.qa.apis import exchange
from .mocks import *  # noqa
import pytest


@pytest.fixture
def sub_account_service():
    service = exchange.rest.private.SubAccountService(api_key="", secret_key="", host="https://uat-api.3ona.co/v2/")
    return service


def test_get_sub_accounts(mock_sub_account_get_accounts, sub_account_service):
    response = sub_account_service.get_sub_accounts()
    sub_account_list = response.result.sub_account_list
    assert len(sub_account_list) == 1
    account = sub_account_list[0]
    assert account.uuid == "1"
    assert account.master_account_uuid == "2"
    assert account.margin_account_uuid == "3"
    assert account.label == "evelyn01"
    assert account.enabled
    assert account.tradable
    assert account.margin_access == "DEFAULT"
    assert account.derivatives_access == "DISABLED"
    assert not account.suspended
    assert not account.terminated


def test_sub_account_get_transfer_history(mock_get_sub_account_trade_history, sub_account_service):
    response = sub_account_service.get_transfer_history(sub_account_uuid="1", direction="IN")
    transfer_list = response.result.transfer_list
    assert len(transfer_list) == 1
    transfer_info = transfer_list[0]
    assert transfer_info.direction == "IN"
    assert transfer_info.amount == 10000


def test_sub_account_transfer(mock_sub_account_transfer, sub_account_service):
    response = sub_account_service.transfer(
        currency="AAVE",
        transfer_from="MASTER",
        from_wallet="SPOT",
        sub_account_uuid="1",
        to="SUBACCOUNT",
        to_wallet="SPOT",
        amount="1000",
    )
    assert response.code == 0

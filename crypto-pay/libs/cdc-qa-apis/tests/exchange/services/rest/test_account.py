import pytest
from cdc.qa.apis import exchange
from cdc.qa.apis.exchange.rest.private.models.account import DepositAddressStatus

from .mocks import *  # noqa


@pytest.fixture
def account_service():
    service = exchange.rest.private.AccountService(api_key="", secret_key="", host="https://uat-api.3ona.co/v2/")
    return service


def test_get_deposit_address(account_service, mock_get_deposit_address):
    response = account_service.get_deposit_address()
    address_list = response.result.deposit_address_list
    assert len(address_list) == 2
    account = address_list[0]
    assert account.id == 12345
    assert account.currency == "CRO"
    assert account.address == "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    assert account.network == "CRO"
    assert account.status == DepositAddressStatus.ACTIVE

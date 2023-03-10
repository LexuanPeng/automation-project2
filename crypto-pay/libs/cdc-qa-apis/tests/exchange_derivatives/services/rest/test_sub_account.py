from cdc.qa.apis import exchange_derivatives
from .mocks import *  # noqa
import pytest


@pytest.fixture
def sub_account_service():
    service = exchange_derivatives.rest.private.AccountService(
        api_key="", secret_key="", host="https://dstg-rest-gateway.x.3ona.co/deriv/v1/"
    )
    return service


def test_get_sub_accounts(mock_sub_account_get_balance, sub_account_service):
    response = sub_account_service.get_subaccount_balances()
    get_subaccount_balances_list = response.result.data
    assert len(get_subaccount_balances_list) == 1
    balance = get_subaccount_balances_list[0]
    assert balance.total_available_balance == "29.00783000"
    assert balance.total_maintenance_margin == "0.00000000"
    assert type(balance.position_balances) == list
    assert balance.position_balances[0].instrument_name == "CRO"
    assert balance.position_balances[1].instrument_name == "USD_Stable_Coin"
    assert not balance.is_liquidating

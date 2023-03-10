from cdc.qa.apis import exchange
from .mocks import *  # noqa


def test_rest_public_get_transfer_currencies(mock_margin_get_transfer_currencies):

    api = exchange.rest.public.MarginService(api_key="", secret_key="", host="https://uat-api.3ona.co/v2/")
    result = api.get_transfer_currencies().result
    transfer_currency_list = result.transfer_currency_list
    assert transfer_currency_list[0] == "BTC"
    assert transfer_currency_list[1] == "USDT"


def test_rest_public_get_loan_currencies(mock_margin_get_loan_currencies):

    api = exchange.rest.public.MarginService(api_key="", secret_key="", host="https://uat-api.3ona.co/v2/")
    result = api.get_loan_currencies().result
    loan_currency_list = result.loan_currency_list
    assert loan_currency_list[0] == "BTC"
    assert loan_currency_list[1] == "USDT"

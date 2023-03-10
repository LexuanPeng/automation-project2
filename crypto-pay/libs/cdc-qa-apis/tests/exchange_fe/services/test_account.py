from .mock.account import *  # noqa


def test_create_margin_account_when_margin_account_be_created(
    service, mock_create_margin_account_when_margin_account_be_created
):
    response = service.account.create_margin_account()
    assert response.code == "101152"
    assert response.data is None
    assert response.msg == "Margin account has been created."


def test_create_margin_account_success(service, mock_create_margin_account_success):
    response = service.account.create_margin_account()
    assert response.code == "0"
    assert response.msg == "Success"
    assert response.data.category == "margin"

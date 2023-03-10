from pytest import fixture


@fixture
def mock_create_margin_account_when_margin_account_be_created(requests_mock):
    requests_mock.post(
        "https://xdev4-www.3ona.co/fe-ex-api/create-margin-account",
        json={"code": "101152", "msg": "Margin account has been created.", "data": None},
    )


@fixture
def mock_create_margin_account_success(requests_mock):
    requests_mock.post(
        "https://xdev4-www.3ona.co/fe-ex-api/create-margin-account",
        json={"code": "0", "msg": "Success", "data": {"category": "margin"}},
    )

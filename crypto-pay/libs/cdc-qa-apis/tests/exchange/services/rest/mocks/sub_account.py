from pytest import fixture


@fixture
def mock_sub_account_get_accounts(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/subaccount/get-sub-accounts",
        json={
            "id": 5276345,
            "method": "private/subaccount/get-sub-accounts",
            "code": 0,
            "result": {
                "sub_account_list": [
                    {
                        "uuid": "1",
                        "master_account_uuid": "2",
                        "margin_account_uuid": "3",
                        "label": "evelyn01",
                        "enabled": True,
                        "tradable": True,
                        "name": "",
                        "email": "",
                        "mobile_number": "",
                        "country_code": "",
                        "address": "",
                        "margin_access": "DEFAULT",
                        "derivatives_access": "DISABLED",
                        "create_time": 1636612807087,
                        "update_time": 1636612807087,
                        "two_fa_enabled": True,
                        "kyc_level": "ADVANCED",
                        "suspended": False,
                        "terminated": False,
                    }
                ]
            },
        },
    )


@fixture
def mock_get_sub_account_trade_history(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/subaccount/get-transfer-history",
        json={
            "id": 5276345,
            "method": "private/subaccount/get-transfer-history",
            "code": 0,
            "result": {
                "transfer_list": [
                    {
                        "direction": "IN",
                        "time": 1636625613514,
                        "amount": 10000,
                        "status": "COMPLETED",
                        "information": "From Master SPOT Wallet",
                        "from": "MASTER",
                        "from_wallet": "SPOT",
                        "to": "SUBACCOUNT",
                        "to_wallet": "SPOT",
                        "sub_account_uuid": "1",
                        "currency": "CRO",
                        "sub_account_label": "evelyn01",
                    }
                ]
            },
        },
    )


@fixture
def mock_sub_account_transfer(requests_mock):
    requests_mock.post("https://uat-api.3ona.co/v2/private/subaccount/transfer", json={"id": 0, "code": 0})

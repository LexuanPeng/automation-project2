from pytest import fixture


@fixture
def mock_get_deposit_address(requests_mock):
    requests_mock.post(
        "https://uat-api.3ona.co/v2/private/get-deposit-address",
        json={
            "id": 11,
            "method": "private/get-deposit-address",
            "code": 0,
            "result": {
                "deposit_address_list": [
                    {
                        "currency": "CRO",
                        "create_time": 1615886328000,
                        "id": "12345",
                        "address": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                        "status": "1",
                        "network": "CRO",
                    },
                    {
                        "currency": "CRO",
                        "create_time": 1615886332000,
                        "id": "12346",
                        "address": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
                        "status": "1",
                        "network": "ETH",
                    },
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

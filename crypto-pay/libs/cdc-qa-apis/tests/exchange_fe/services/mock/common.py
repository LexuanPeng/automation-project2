from pytest import fixture


@fixture
def mock_get_user_info(requests_mock):
    requests_mock.post(
        "https://xdev4-www.3ona.co/fe-ex-api/common/user_info",
        json={
            "code": "0",
            "msg": "Success",
            "data": {
                "googleStatus": 1,
                "sysSoftStakingOpen": 1,
                "zeroTradingFeeDuration": 0,
                "mobileNumber": "+48****3676",
                "feeCoinRate": "100.00",
                "isEnabledWithdrawalApi": 1,
                "uuid": "ec8716ba-ceab-4b62-a1cd-96421e76d0d6",
                "fee_coin_open": "1",
                "lastLoginIp": "208.127.160.212",
                "userTier": 2,
                "accountStatus": 0,
                "isOpenMobileCheck": 0,
                "userTierReinforcementEnabled": True,
                "countryCode": "POL",
                "derivativeAccountStatus": 1,
                "email": "evelyn.wang+sz01@crypto.com",
                "nickName": "Evelyn wang",
                "useSoftStakingOpen": 1,
                "walletAppStatus": 0,
                "isEnabledCroMainnet": 1,
                "myMarket": [],
                "useFeeCoinOpen": 0,
                "zeroTradingFeeActiveDays": 90,
                "marginAccountStatus": 1,
                "isEligibleForMarginFeature": True,
                "lastLoginTime": "1629258780000",
                "feeCoin": "CRO",
                "phoneCountryCode": "POL",
                "isEnabledZeroTradingFee": 0,
                "userAccount": "e****@crypto.com",
                "isEnabledDerivativeBetaProduct": 0,
                "userType": 1,
                "authLevel": 2,
                "isEligibleForDerivativeFeature": True,
            },
        },
    )


@fixture
def mock_supported_coins(requests_mock):
    requests_mock.get(
        "https://xdev4-www.3ona.co/fe-ex-api/common/supported_coins",
        text="""{
    "code": "0",
    "msg": "Success",
    "data": {
        "lastUpdatedAt": 1637564282000,
        "symbols": {
             "AGLD": {
                "withdrawal_decimals": 8,
                "fullName": "Adventure Gold",
                "networks": [
                    {
                        "minWithdrawalAmount": "1",
                        "withdraw_open": 0,
                        "deposit_open": 0,
                        "withdrawalFees": null,
                        "confirmation": 12,
                        "is_public_release": 1,
                        "is_xapp_released": 1,
                        "network": "ETH"
                    }
                ]
            },
            "MATIC": {
                "withdrawal_decimals": 8,
                "fullName": "MATIC",
                "networks": [
                    {
                        "minWithdrawalAmount": "40",
                        "address_type": null,
                        "withdraw_open": 0,
                        "deposit_open": 0,
                        "withdrawalFees": "20",
                        "confirmation": 12,
                        "is_xapp_released": 1,
                        "is_public_release": 1,
                        "address_max_length": 256,
                        "address_pattern": null,
                        "networkDisplayName": "ERC20",
                        "network": "ETH"
                    },
                    {
                        "minWithdrawalAmount": "40",
                        "address_type": null,
                        "withdraw_open": 0,
                        "deposit_open": 0,
                        "withdrawalFees": "20",
                        "confirmation": 12,
                        "is_xapp_released": 1,
                        "is_public_release": 1,
                        "address_max_length": 256,
                        "address_pattern": null,
                        "networkDisplayName": "BEP20",
                        "network": "BNB"
                    },
                    {
                        "minWithdrawalAmount": "0.16",
                        "address_type": null,
                        "withdraw_open": 0,
                        "deposit_open": 0,
                        "withdrawalFees": "0.08",
                        "confirmation": 12,
                        "is_xapp_released": 1,
                        "is_public_release": 1,
                        "address_max_length": 256,
                        "address_pattern": null,
                        "networkDisplayName": "Polygon",
                        "network": "MATIC"
                    }
                ]
            }
                }
            }
        }""",
    )

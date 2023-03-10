from pytest import fixture


@fixture
def mock_authenticate_by_email(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "authenticateByEmail": {
                    "lastLoginAt": "2022-10-25T10:47:17.186Z",
                    "requiredSteps": ["EmailOtp"],
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9AlZGVLk5Jc5D3HgzAFIpU-z4r5j8Z2F8Nex6ZVWXhBA",
                    "unauthorizedMe": {
                        "email": "example@crypto.com",
                        "name": "atr",
                        "username": "k6-example",
                        "uuid": "a99da057-29ae-46cd-bd6f-88ca68e09c6d",
                        "__typename": "UnauthorizedMeV2",
                    },
                    "__typename": "PreAuthV2",
                }
            }
        },
    )


@fixture
def mock_authenticate(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "authenticate": {
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhOTlkYTA1Ny0yOWFlLTQ2Y2QtYmQ2Zi04OGNhNj",
                    "me": {
                        "uuid": "a99da057-29ae-46cd-bd6f-88ca68e09c6d",
                        "email": "k6-qiangfu@crypto.com",
                        "clientOtpEnabled": False,
                        "__typename": "UnauthorizedMe",
                    },
                    "__typename": "PreAuth",
                }
            }
        },
    )


@fixture
def mock_prepare_otp(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql", json={"data": {"prepareOtp": {"success": True, "__typename": "Otp"}}}
    )


@fixture
def mock_continue_authentication(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "continueAuthentication": {
                    "__typename": "AuthV2",
                    "me": {
                        "uuid": "a99da057-29ae-46cd-bd6f-88ca68e09c6d",
                        "verified": False,
                        "id": "k6-qiangfu",
                        "bio": None,
                        "displayName": None,
                        "instagramUsername": None,
                        "facebookUsername": None,
                        "twitterUsername": None,
                        "countryCode": "GBR",
                        "phoneNumber": "+447488800085",
                        "isPhoneNumberVerified": True,
                        "isPriceAlertLimitReached": False,
                        "username": "k6-qiangfu",
                        "name": "atr",
                        "avatar": None,
                        "cover": None,
                        "segmentUserId": "ca590a4e-69ae-451c-859c-854c1f3c3f3f",
                        "subscribed": False,
                        "primaryFee": 4000,
                        "email": "k6-nft-load-test+qiangfu@crypto.com",
                        "confirmedAt": "2022-09-15T02:44:22.399Z",
                        "connectedCRO": True,
                        "disablePayout": False,
                        "mainAppStatus": "KYC_APPROVED",
                        "creationPayoutBlockExpiredAt": "2022-10-15T00:00:00.000Z",
                        "creationWithdrawalBlockExpiredAt": "2022-10-15T00:00:00.000Z",
                        "isCreationPayoutBlocked": False,
                        "isCreationWithdrawalBlocked": False,
                        "isEmailMismatch": False,
                        "croUserUUID": "b3b7df95-7f2b-4447-b408-fe7d1fe00112",
                        "weeklyUsedCreditCardBalanceDecimal": {
                            "drops": "0.00",
                            "marketplace": "0.00",
                            "__typename": "WeeklyUsedCreditCardBalance",
                        },
                        "croWalletAddress": "tcro1k7hsy88nwl7k64yqk75nckq90plgk87r03dr2r",
                        "offerBlockUntil": "2022-10-29T04:11:00.465Z",
                        "creatorConfig": {
                            "canCreateAsset": True,
                            "defaultRoyaltiesRate": "10.00",
                            "maxCategoriesPerAsset": 2,
                            "maxEditionsPerAsset": 10,
                            "maxAssetsPerWeek": 50,
                            "marketplacePrimaryFeeRate": "1.99",
                            "__typename": "CreatorConfig",
                        },
                        "antiPhishingCode": "lo",
                        "clientOtpEnabled": False,
                        "addressWhitelistingEnabled": False,
                        "newWhitelistAddressLockEnabled": False,
                        "securityChangeWithdrawalLocked": False,
                        "clientOtpEnabledAt": None,
                        "userMFAConfig": None,
                        "featureFlags": [],
                        "tmxProfileSessionId": "cfbda6aa3cd160e84049a69fcea3dfc6",
                        "registrationCompleted": True,
                        "utmId": "9982031d1578784e76d79a80720df0cd",
                        "__typename": "Me",
                    },
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhOTlkYTA1Ny0yOWFlLTQ2Y2QtYzazPY4",
                }
            }
        },
    )


@fixture
def mock_auth_with_otp(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "authenticateWithOtp": {
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhOTlkYTA1Ny0yOWFlLTQ2Y2QtYmQ2Zi04OGNhNc",
                    "me": {
                        "uuid": "a99da057-29ae-46cd-bd6f-88ca68e09c6d",
                        "verified": False,
                        "id": "k6-qiangfu",
                        "bio": None,
                        "displayName": None,
                        "instagramUsername": None,
                        "facebookUsername": None,
                        "twitterUsername": None,
                        "countryCode": "USA",
                        "phoneNumber": "16416705118",
                        "isPhoneNumberVerified": True,
                        "username": "k6-qiangfu",
                        "name": "atr",
                        "avatar": None,
                        "cover": None,
                        "segmentUserId": "ca590a4e-69ae-451c-859c-854c1f3c3f3f",
                        "subscribed": False,
                        "primaryFee": 4000,
                        "email": "k6-qiangfu@crypto.com",
                        "confirmedAt": "2022-09-15T02:44:22.399Z",
                        "connectedCRO": True,
                        "disablePayout": False,
                        "mainAppStatus": "NO_ACCOUNT",
                        "creationPayoutBlockExpiredAt": "2022-10-15T00:00:00.000Z",
                        "creationWithdrawalBlockExpiredAt": "2022-10-15T00:00:00.000Z",
                        "isCreationPayoutBlocked": False,
                        "isCreationWithdrawalBlocked": False,
                        "isEmailMismatch": False,
                        "croUserUUID": "b3b7df95-7f2b-4447-b408-fe7d1fe00112",
                        "weeklyUsedCreditCardBalanceDecimal": {
                            "drops": "0.00",
                            "marketplace": "0.00",
                            "__typename": "WeeklyUsedCreditCardBalance",
                        },
                        "croWalletAddress": "tcro1k7hsy88nwl7k64yqk75nckq90plgk87r03dr2r",
                        "offerBlockUntil": None,
                        "creatorConfig": {
                            "canCreateAsset": True,
                            "defaultRoyaltiesRate": "10.00",
                            "maxCategoriesPerAsset": 2,
                            "maxEditionsPerAsset": 10,
                            "maxAssetsPerWeek": 50,
                            "marketplacePrimaryFeeRate": "1.99",
                            "__typename": "CreatorConfig",
                        },
                        "antiPhishingCode": "lo",
                        "clientOtpEnabled": False,
                        "addressWhitelistingEnabled": False,
                        "newWhitelistAddressLockEnabled": False,
                        "securityChangeWithdrawalLocked": False,
                        "clientOtpEnabledAt": None,
                        "userMFAConfig": None,
                        "featureFlags": [],
                        "tmxProfileSessionId": "61dfd889013aba61178b2d17eb95de79",
                        "__typename": "Me",
                    },
                    "lastLoginAt": "2022-10-24T10:41:46.916Z",
                    "__typename": "Auth",
                }
            }
        },
    )


@fixture
def mock_request_qrcode_login(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "requestQrCodeLogin": {
                    "encodedQr": "nft-login|1|0|https://asta-user-core-authnz-api.3ona.co/v1/public/scan|UIU_WvXg-MzU",
                    "sessionId": "UIU_Wkx6GcPWthLNlRI3MnEOuw7D7ERF8EKzM31JTlERELQef_vXg-MWzbh12H1U",
                    "status": "PENDING",
                    "__typename": "RequestQrCodeLogin",
                }
            }
        },
    )


@fixture
def mock_get_qrcode_login_status(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={"data": {"qrCodeLoginStatus": {"status": "PENDING", "__typename": "QrCodeLoginStatus"}}},
    )


@fixture
def mock_authenticate_by_qrcode(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "authenticateByQrCode": {
                    "__typename": "AuthV2",
                    "me": {
                        "uuid": "8d120e1c-74d1-4a94-90dd-4410784f4f4e",
                        "verified": True,
                        "id": "atest",
                        "bio": None,
                        "displayName": None,
                        "instagramUsername": None,
                        "facebookUsername": None,
                        "twitterUsername": None,
                        "countryCode": "HK",
                        "phoneNumber": "+85237175444",
                        "isPhoneNumberVerified": True,
                        "isPriceAlertLimitReached": False,
                        "username": "atest",
                        "name": "Qiang Fu",
                        "avatar": {
                            "url": "https://vsta-nft-images.3ona.co/0c369f04-2bba-456e-bafd-2a7c530516f3/original.jpeg",
                            "__typename": "Attachment",
                        },
                        "cover": {
                            "url": "https://vsta-nft-images.3ona.co/15608c64-fab9-482c-af40-f3081df4be4b/original.jpeg",
                            "__typename": "Attachment",
                        },
                        "segmentUserId": "aa462130-8b55-42bc-99ba-95033e193640",
                        "subscribed": False,
                        "primaryFee": 0,
                        "email": "qiang.fu@crypto.com",
                        "confirmedAt": "2022-08-08T03:01:36.475Z",
                        "connectedCRO": True,
                        "disablePayout": False,
                        "mainAppStatus": "KYC_APPROVED",
                        "creationPayoutBlockExpiredAt": None,
                        "creationWithdrawalBlockExpiredAt": None,
                        "isCreationPayoutBlocked": False,
                        "isCreationWithdrawalBlocked": False,
                        "isEmailMismatch": False,
                        "croUserUUID": "aa462130-8b55-42bc-99ba-95033e193640",
                        "weeklyUsedCreditCardBalanceDecimal": {
                            "drops": "0.00",
                            "marketplace": "0.00",
                            "__typename": "WeeklyUsedCreditCardBalance",
                        },
                        "croWalletAddress": "tcro1fxtdv63qxdyc5vxhg79s9uae2lqejhtd7286xr",
                        "offerBlockUntil": "2022-10-29T04:11:00.465Z",
                        "creatorConfig": {
                            "canCreateAsset": True,
                            "defaultRoyaltiesRate": "10.00",
                            "maxCategoriesPerAsset": 2,
                            "maxEditionsPerAsset": 10,
                            "maxAssetsPerWeek": 50,
                            "marketplacePrimaryFeeRate": "0.00",
                            "__typename": "CreatorConfig",
                        },
                        "antiPhishingCode": None,
                        "clientOtpEnabled": False,
                        "addressWhitelistingEnabled": False,
                        "newWhitelistAddressLockEnabled": False,
                        "securityChangeWithdrawalLocked": False,
                        "clientOtpEnabledAt": None,
                        "userMFAConfig": None,
                        "featureFlags": [],
                        "tmxProfileSessionId": "3cd2a93d7e88757e29641261d90ca679",
                        "registrationCompleted": True,
                        "utmId": "c0d8a1fc2c5bff9097dab782f50a18e2",
                        "__typename": "Me",
                    },
                    "token": "eyJhbGciOiJIUzI1NiIsdCI6MTY2ODA2MDQyMCwiZXhwIjoxNjY4MTQ2ODIwfQ.CO5L38zazSLfkZEfEul_jk",
                }
            }
        },
    )


@fixture
def mock_logout(requests_mock):
    requests_mock.post(url="https://3ona.co/nft-api/graphql", json={"data": {"logout": None}})

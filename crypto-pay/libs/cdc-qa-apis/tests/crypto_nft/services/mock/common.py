from pytest import fixture


@fixture
def mock_get_credit_cards(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "creditCards": [
                    {
                        "firstSixDigits": "411111",
                        "lastFourDigits": "1111",
                        "isExpired": False,
                        "cardType": "visa",
                        "uuid": "1a984964-3d15-4e63-a8ce-319c9d949519",
                        "createdAt": "2022-09-27T08:06:49.613Z",
                        "__typename": "CreditCard",
                    }
                ]
            }
        },
    )


@fixture
def mock_create_ixo_payment(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={"data": {"createIXOPayment": {"id": "aa859db2-8450-4054-9ad9-b198cc7b94c0", "__typename": "IXOPayment"}}},
    )


@fixture
def mock_preauth_ixo_payment(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "preauthIXOPayment": {
                    "preauthRedirectUrl": "https://cryptocom.paymentsandbox.cloud/redirect/6164de5bbda3f=",
                    "preauthReturnType": "REDIRECT",
                    "status": "preauthorizing",
                    "__typename": "IXOPayment",
                }
            }
        },
    )


@fixture
def mock_capture_ixo_payment(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "captureIXOPayment": {
                    "preauthRedirectUrl": "https://cryptocom.paymentsandbox.cloud/redirect/6164deMGMyZGY3O",
                    "status": "capturing",
                    "checkout": {
                        "listingMode": "sale",
                        "listing": {"source": "CDC_NFT", "__typename": "Listing"},
                        "__typename": "Checkout",
                    },
                    "__typename": "IXOPayment",
                }
            }
        },
    )


@fixture
def mock_paid_checkouts(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "paidCheckouts": [
                    {
                        "id": "c4c605d2-2f2f-46ae-b6b0-35a17b2304fd",
                        "amountDecimal": "10000.00",
                        "currency": "USD",
                        "asset": {
                            "id": "7850f5ff3a1c48a1d858d5d33a14d4be",
                            "name": "NFT AT 09191755",
                            "copies": 10,
                            "cover": {
                                "url": "https://vsta-nft-images.3ona.co/80df2244-5707-4460/original.jpg",
                                "__typename": "Attachment",
                            },
                            "collectiblePerPack": None,
                            "kind": "COLLECTIBLE",
                            "isExternalNft": False,
                            "__typename": "Asset",
                        },
                        "edition": {
                            "id": "cb0c0cade3460b3a47ecd0bc49754e55",
                            "index": 1,
                            "owner": {
                                "id": "k6-qiang016",
                                "uuid": "57bfaba4-a065-4c96-9204-f0dc2dc8fda0",
                                "isCreator": True,
                                "__typename": "User",
                            },
                            "__typename": "Edition",
                        },
                        "listing": {
                            "id": "834445",
                            "mode": "sale",
                            "primary": True,
                            "source": "CDC_NFT",
                            "externalUser": None,
                            "__typename": "Listing",
                        },
                        "cartQuantity": 0,
                        "paidAt": "2022-09-20T02:21:58.966Z",
                        "seller": {
                            "username": "k6-qiang016",
                            "isCreator": True,
                            "uuid": "57bfaba4-a065-4c96-9204-f0dc2dc8fda0",
                            "displayName": None,
                            "__typename": "User",
                        },
                        "gateway": "accountpay",
                        "__typename": "Checkout",
                    },
                    {
                        "id": "1d0ac04f-2462-4d52-a202-ca11d250ccbf",
                        "amountDecimal": "500.00",
                        "currency": "USD",
                        "asset": {
                            "id": "58043988538f2b9a6e110f0e9a35daff",
                            "name": "app integration open edition asset",
                            "copies": 88,
                            "cover": {
                                "url": "https://vsta-nft-images.3ona.co/db915580-9938/original.jpeg",
                                "__typename": "Attachment",
                            },
                            "collectiblePerPack": None,
                            "kind": "OPEN_COLLECTIBLE",
                            "isExternalNft": False,
                            "__typename": "Asset",
                        },
                        "edition": {
                            "id": "4a772f2deea13691632881e03acb8845",
                            "index": 54,
                            "owner": {
                                "id": "k6-qiangfu",
                                "uuid": "a99da057-29ae-46cd-bd6f-88ca68e09c6d",
                                "isCreator": True,
                                "__typename": "User",
                            },
                            "__typename": "Edition",
                        },
                        "listing": {
                            "id": "834148",
                            "mode": "sale",
                            "primary": False,
                            "source": "CDC_NFT",
                            "externalUser": None,
                            "__typename": "Listing",
                        },
                        "cartQuantity": 0,
                        "paidAt": "2022-09-16T07:27:10.464Z",
                        "seller": {
                            "username": "amuletregression",
                            "isCreator": False,
                            "uuid": "24ec3dc0-6103-4453-804c-c2c2f688eb2d",
                            "displayName": None,
                            "__typename": "User",
                        },
                        "gateway": "accountpay",
                        "__typename": "Checkout",
                    },
                ],
                "countPaidCheckouts": 15,
            }
        },
    )


@fixture
def mock_get_categories(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "categories": [
                        {"id": "1", "name": "Art", "unselectable": False, "__typename": "Category"},
                        {"id": "2", "name": "Celebrities", "unselectable": False, "__typename": "Category"},
                    ],
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_create_attachment(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "createAttachment": {
                    "id": "ee9d1778-e144-4ab9-8218-0baf6a0b4a11",
                    "url": "https://vsta-nft-images.3ona.co/ee9d1778-e144-4ab9-8218-0baf6a0b4a11/original.jpg",
                    "coverUrl": None,
                    "__typename": "Attachment",
                }
            }
        },
    )


@fixture
def mock_place_bid_mutation(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "createCheckout": {
                    "id": "3584633f-378c-4d73-b0bb-3c8510253832",
                    "bidPriceDecimal": "100.00",
                    "__typename": "Checkout",
                }
            }
        },
    )


@fixture
def mock_get_bidding_history(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "bids": [
                        {
                            "id": "fe1fc252-4a5d-46cc-a3d3-2a8bf5cf959b",
                            "createdAt": "2022-12-26T02:05:48.751Z",
                            "edition": {"id": "59a8177afb8713bdc3b07b31efdf71f0", "__typename": "Edition"},
                            "priceDecimal": "2.00",
                            "listing": {"priceDecimal": "2.00", "currency": "USD", "__typename": "Listing"},
                            "buyer": {
                                "uuid": "a99da057-29ae-46cd-bd6f-88ca68e09c6d",
                                "id": "k6-qiangfu",
                                "username": "k6-qiangfu",
                                "displayName": None,
                                "isCreator": True,
                                "avatar": {
                                    "url": "https://dfsgjflvxpujn.cloudfront.net/63b044ee-2a24/original.jpg",
                                    "__typename": "Attachment",
                                },
                                "isCreationWithdrawalBlocked": False,
                                "creationWithdrawalBlockExpiredAt": None,
                                "verified": False,
                                "__typename": "User",
                            },
                            "__typename": "Bid",
                        }
                    ],
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_delete_credit_card(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {"deleteCreditCard": {"uuid": "1a984964-3d15-4e63-a8ce-319c9d949519", "__typename": "CreditCard"}}
        },
    )


@fixture
def mock_get_top_collectibles(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "topCollectibles": [
                        {
                            "id": "c4dbb995a39557a6f96335380e93140a",
                            "name": "Solcol # 1",
                            "copies": 1,
                            "copiesInCirculation": 1,
                            "main": {
                                "url": "https://vsta-nft-images.3ona.co/2780a0ff/original.png",
                                "__typename": "Attachment",
                            },
                            "cover": {
                                "url": "https://vsta-nft-images.3ona.co/2b5ea80f/original.png",
                                "__typename": "Attachment",
                            },
                            "collection": {
                                "logo": {
                                    "url": "https://vsta-nft-images.3ona.co/d98bd0d7/original.jpg",
                                    "__typename": "Attachment",
                                },
                                "id": "e204e7b207a56751d7fdf57a3ce38905",
                                "name": "SoL collection",
                                "verified": True,
                                "__typename": "Collection",
                            },
                            "drop": None,
                            "primaryListingsCount": 0,
                            "secondaryListingsCount": 1,
                            "primarySalesCount": 0,
                            "latestPurchasedEdition": {
                                "id": "884b7c3453e501d76fc2e07e0d0c50cf",
                                "priceUSD": "300.00",
                                "__typename": "LastPurchasedEdition",
                            },
                            "totalSalesDecimal": "300.00",
                            "defaultListing": {
                                "id": "5614513",
                                "editionId": "884b7c3453e501d76fc2e07e0d0c50cf",
                                "priceDecimal": "400.00",
                                "mode": "sale",
                                "auctionHasBids": False,
                                "salePriceDecimalUSD": "400.00",
                                "currency": "USD",
                                "source": "CDC_NFT",
                                "seller": {
                                    "id": "jelly2",
                                    "uuid": "7fe0e704-8c37-4551-b086-6679a45008f7",
                                    "__typename": "User",
                                },
                                "__typename": "Listing",
                            },
                            "defaultAuctionListing": None,
                            "defaultSaleListing": {
                                "id": "5614513",
                                "editionId": "884b7c3453e501d76fc2e07e0d0c50cf",
                                "priceDecimal": "400.00",
                                "mode": "sale",
                                "salePriceDecimalUSD": "400.00",
                                "currency": "USD",
                                "source": "CDC_NFT",
                                "seller": {
                                    "id": "jelly2",
                                    "uuid": "7fe0e704-8c37-4551-b086-6679a45008f7",
                                    "__typename": "User",
                                },
                                "__typename": "Listing",
                            },
                            "defaultSecondaryListing": {
                                "id": "5614513",
                                "editionId": "884b7c3453e501d76fc2e07e0d0c50cf",
                                "priceDecimal": "400.00",
                                "mode": "sale",
                                "auctionHasBids": False,
                                "currency": "USD",
                                "salePriceDecimalUSD": "400.00",
                                "source": "CDC_NFT",
                                "seller": {
                                    "id": "jelly2",
                                    "uuid": "7fe0e704-8c37-4551-b086-6679a45008f7",
                                    "__typename": "User",
                                },
                                "__typename": "Listing",
                            },
                            "defaultSecondaryAuctionListing": None,
                            "defaultSecondarySaleListing": {
                                "id": "5614513",
                                "editionId": "884b7c3453e501d76fc2e07e0d0c50cf",
                                "priceDecimal": "400.00",
                                "mode": "sale",
                                "currency": "USD",
                                "salePriceDecimalUSD": "400.00",
                                "source": "CDC_NFT",
                                "seller": {
                                    "id": "jelly2",
                                    "uuid": "7fe0e704-8c37-4551-b086-6679a45008f7",
                                    "__typename": "User",
                                },
                                "__typename": "Listing",
                            },
                            "likes": 0,
                            "recentLikes": 0,
                            "views": 3,
                            "recentViews": 2,
                            "isCurated": False,
                            "isSoulbound": False,
                            "defaultEditionId": "884b7c3453e501d76fc2e07e0d0c50cf",
                            "externalNftMetadata": {
                                "network": "SOL",
                                "isSuspicious": False,
                                "__typename": "ExternalNftMetadata",
                            },
                            "__typename": "Asset",
                        }
                    ]
                }
            }
        },
    )


@fixture
def mock_checkout_amount(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={"data": {"checkout": {"amountDecimal": "3.00", "__typename": "Checkout"}}},
    )

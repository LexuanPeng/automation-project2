from pytest import fixture


@fixture
def mock_get_asset_by_id(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "asset": {
                        "id": "0100d37437298b18f4111667e0be7dc9",
                        "name": "testkittiespack",
                        "collectiblePerPack": 1,
                        "maxItemsPerCheckout": 5,
                        "copies": 10000,
                        "copiesInCirculation": 3,
                        "description": "test",
                        "categories": [],
                        "creator": {
                            "uuid": "573c2d41-d5dc-4259-bdab-92df232b192b",
                            "id": "alex_yeung_stg1",
                            "username": "alex_yeung_stg1",
                            "displayName": None,
                            "isCreator": True,
                            "avatar": None,
                            "isCreationWithdrawalBlocked": False,
                            "creationWithdrawalBlockExpiredAt": None,
                            "verified": True,
                            "__typename": "User",
                        },
                        "main": None,
                        "cover": {
                            "url": "https://dfsgjflvxpujn.cloudfront.net/892dd7a5-3b44-497a-b0a8-95fd50ac/original.png",
                            "__typename": "Attachment",
                        },
                        "royaltiesRateDecimal": "0",
                        "primaryListingsCount": 9997,
                        "secondaryListingsCount": 0,
                        "primarySalesCount": 9997,
                        "isAssetWithdrawableOnChain": True,
                        "drop": {
                            "id": "ceef6e72d97b904f40f9988c37abb8df",
                            "startAt": "2021-12-16T08:00:00.000Z",
                            "endAt": "2023-02-27T16:00:00.000Z",
                            "premiumDropConfig": None,
                            "creator": {
                                "uuid": "573c2d41-d5dc-4259-bdab-92df232b192b",
                                "id": "alex_yeung_stg1",
                                "username": "alex_yeung_stg1",
                                "displayName": None,
                                "isCreator": True,
                                "avatar": None,
                                "isCreationWithdrawalBlocked": False,
                                "creationWithdrawalBlockExpiredAt": None,
                                "verified": True,
                                "__typename": "User",
                            },
                            "__typename": "Drop",
                        },
                        "defaultPrimaryListing": {
                            "id": "496923",
                            "editionId": "62990b4dfe67b60d3e32a4127ae3d73f",
                            "priceDecimal": "10.00",
                            "mode": "sale",
                            "auctionHasBids": False,
                            "primary": True,
                            "source": "CDC_NFT",
                            "salePriceDecimalUSD": "10.00",
                            "currency": "USD",
                            "externalUser": None,
                            "__typename": "Listing",
                        },
                        "kind": "PACK",
                        "pack": None,
                        "likes": 0,
                        "views": 2,
                        "auctionMaxEndDate": None,
                        "remark": None,
                        "isOwnerExternal": False,
                        "isCurated": True,
                        "collection": {
                            "totalSupply": 0,
                            "enableExternalRarity": False,
                            "enableInternalRarity": True,
                            "defaultRarityType": "OFFICIAL",
                            "logo": {
                                "url": "https://dfsgjflvxpujn.cloudfront.net/f2dfb081-a628-4eff-9039-b45f/original.png",
                                "__typename": "Attachment",
                            },
                            "id": "ef46b9cca7848bf5b9b5e2ef0c4aac12",
                            "name": "testkitties",
                            "verified": False,
                            "rarityMetadata": None,
                            "metrics": {
                                "items": 2,
                                "minSaleListingPriceDecimal": "0.00",
                                "__typename": "CollectionMetrics",
                            },
                            "__typename": "Collection",
                        },
                        "denomId": None,
                        "defaultEditionId": "9ebf54b1e7fa51b584659f8a79d02c4e",
                        "defaultAuctionListing": None,
                        "defaultSaleListing": {
                            "editionId": "62990b4dfe67b60d3e32a4127ae3d73f",
                            "priceDecimal": "10.00",
                            "mode": "sale",
                            "salePriceDecimalUSD": "10.00",
                            "currency": "USD",
                            "__typename": "Listing",
                        },
                        "defaultListing": {
                            "editionId": "62990b4dfe67b60d3e32a4127ae3d73f",
                            "priceDecimal": "10.00",
                            "mode": "sale",
                            "auctionHasBids": False,
                            "salePriceDecimalUSD": "10.00",
                            "currency": "USD",
                            "__typename": "Listing",
                        },
                        "defaultSecondaryAuctionListing": None,
                        "defaultSecondarySaleListing": None,
                        "isExternalNft": False,
                        "isLiked": False,
                        "externalNftMetadata": None,
                        "crossChainCreator": None,
                        "isOwnerOnly": False,
                        "rarityScore": "0.000000000000000000",
                        "defaultRarityRank": "3",
                        "externalRarityScore": "0.000000000000000000",
                        "externalRarityRank": "0",
                        "priceAlert": None,
                        "__typename": "Asset",
                    },
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_create_checkout(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={"data": {"createCheckout": {"id": "bf7dca1a-63da-403c-8e24-145d8ce53acc", "__typename": "Checkout"}}},
    )


@fixture
def mock_create_and_capture_account_payment(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "createAndCaptureAccountPayment": {
                    "id": "e2db9fb0-8950-44a7-9d8f-2c4519dfaf10",
                    "status": "captured",
                    "__typename": "AccountPayment",
                }
            }
        },
    )


@fixture
def mock_get_drops(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "drops": [
                        {
                            "id": "12013205d823385a3b1cbd7afa48b0e5",
                            "name": "Zeus Integration Testing Asset 1",
                            "cover": {
                                "url": "https://vsta-nft-images.3ona.co/618ef07e-4955-450a-b848/original.jpeg",
                                "__typename": "Attachment",
                            },
                            "creator": {
                                "uuid": "dbc9c0d9-027a-415a-bf49-d4fb1713d10f",
                                "username": "cynthiacreator1",
                                "displayName": None,
                                "avatar": None,
                                "verified": True,
                                "__typename": "User",
                            },
                            "creatorInfo": "Zeus Integration Testing Drop",
                            "description": "Zeus Integration Testing Drop",
                            "startAt": "2021-08-31T16:00:00.000Z",
                            "endAt": "2023-01-31T18:30:00.000Z",
                            "video": None,
                            "isPublicReadOnly": False,
                            "premiumDropConfig": None,
                            "dropStatus": "LIVE",
                            "__typename": "Drop",
                        }
                    ],
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_get_drop(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "drop": {
                        "id": "912f5bc886e405334540f7966880a35a",
                        "name": "test-1109-016",
                        "cover": {
                            "url": "https://vsta-nft-images.3ona.co/eaebd186/original.webp",
                            "__typename": "Attachment",
                        },
                        "creator": {
                            "uuid": "e0826b34-fe26-4c46-91a8-9d4a6ca5c90e",
                            "id": "harry",
                            "displayName": None,
                            "username": "harry",
                            "bio": None,
                            "avatar": None,
                            "instagramUsername": None,
                            "facebookUsername": None,
                            "twitterUsername": None,
                            "verified": True,
                            "__typename": "User",
                        },
                        "creatorInfo": "test-1109-010",
                        "description": "test-1109-010",
                        "startAt": "2022-11-11T09:53:50.481Z",
                        "endAt": "2022-11-25T09:53:53.851Z",
                        "showCollectible": True,
                        "video": None,
                        "whatInsideDescription": "test-1109-010",
                        "termsAndConditions": "test-1109-010",
                        "dropStatus": "LIVE",
                        "isPublicReadOnly": True,
                        "premiumDropConfig": None,
                        "__typename": "Drop",
                    },
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_get_drop_assets_query(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "assets": [
                        {
                            "id": "7b34ca37977c56aa666219bcd8e27b2d",
                            "name": "Pack AT 0930005",
                            "description": "13123",
                            "copies": 9000,
                            "copiesInCirculation": 26,
                            "collectiblePerPack": 1,
                            "createdAt": "2022-09-30T10:05:14.553Z",
                            "collection": {
                                "logo": {
                                    "url": "https://vsta-nft-images.3ona.co/a26df34e/original.jpeg",
                                    "__typename": "Attachment",
                                },
                                "id": "085507432cb8136b13630640520db6d4",
                                "name": "AT Collection",
                                "verified": False,
                                "__typename": "Collection",
                            },
                            "cover": {
                                "url": "https://vsta-nft-images.3ona.co/01b25648/original.jpg",
                                "__typename": "Attachment",
                            },
                            "main": None,
                            "drop": {
                                "id": "de3525f34dd868113f0150c1d4cebe51",
                                "endAt": "2026-09-29T16:00:00.000Z",
                                "__typename": "Drop",
                            },
                            "kind": "PACK",
                            "primaryListingsCount": 8974,
                            "secondaryListingsCount": 0,
                            "primarySalesCount": 8974,
                            "defaultPrimaryListing": {
                                "editionId": "4012877615527b6e1905014867dce696",
                                "priceDecimal": "1.00",
                                "mode": "sale",
                                "auctionHasBids": False,
                                "auctionCloseAt": None,
                                "primary": True,
                                "salePriceDecimalUSD": "1.00",
                                "currency": "USD",
                                "seller": {"id": "k6-nftcreator", "__typename": "User"},
                                "__typename": "Listing",
                            },
                            "isExternalNft": False,
                            "externalNftMetadata": None,
                            "isCurated": True,
                            "__typename": "Asset",
                        }
                    ],
                    "__typename": "Public",
                }
            }
        },
    )

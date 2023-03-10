from pytest import fixture


@fixture
def mock_get_profile_assets_total(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={"data": {"public": {"profileLikedAssetsTotal": 8, "__typename": "Public"}}},
    )


@fixture
def mock_get_user_private_assets_total(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql", json={"data": {"collectedEditionsTotal": 103, "createdAssetsTotal": 11}}
    )


@fixture
def mock_get_profile_collections(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "profileCollections": [
                        {
                            "id": "45bfb5918b57d3ff93e7925a5165d00c",
                            "name": "1231",
                            "logo": {
                                "url": "https://vsta-nft-images.3ona.co/3976b002/original.jpg",
                                "__typename": "Attachment",
                            },
                            "banner": {
                                "url": "https://vsta-nft-images.3ona.co/8a3362db/original.jpg",
                                "__typename": "Attachment",
                            },
                            "verified": False,
                            "metrics": {"items": 0, "__typename": "CollectionMetrics"},
                            "__typename": "Collection",
                        },
                        {
                            "id": "b0604d98abd467306bc85a058ba50beb",
                            "name": "AT Collection",
                            "logo": {
                                "url": "https://vsta-nft-images.3ona.co/055ac989/original.jpg",
                                "__typename": "Attachment",
                            },
                            "banner": {
                                "url": "https://vsta-nft-images.3ona.co/7ebf1dd7/original.jpg",
                                "__typename": "Attachment",
                            },
                            "verified": False,
                            "metrics": {"items": 9, "__typename": "CollectionMetrics"},
                            "__typename": "Collection",
                        },
                    ],
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_live_and_incoming_drops(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "drops": [
                        {
                            "id": "912f5bc886e405334540f7966880a35a",
                            "name": "test-1109-016",
                            "description": "test-1109-010",
                            "cover": {
                                "url": "https://vsta-nft-images.3ona.co/eaebd186/original.webp",
                                "__typename": "Attachment",
                            },
                            "creator": {"displayName": None, "username": "harry", "avatar": None, "__typename": "User"},
                            "startAt": "2022-11-11T09:53:50.481Z",
                            "endAt": "2022-11-25T09:53:53.851Z",
                            "dropStatus": "LIVE",
                            "isPublicReadOnly": True,
                            "premiumDropConfig": None,
                            "__typename": "Drop",
                        },
                        {
                            "id": "2d6029aa8b36960a6432b109f499cd56",
                            "name": "Dont touch plz - Automation drop",
                            "description": "Dont touch plz - Automation drop",
                            "cover": {
                                "url": "https://vsta-nft-images.3ona.co/268a57ff/original.png",
                                "__typename": "Attachment",
                            },
                            "creator": {
                                "displayName": "testaccaDisplay",
                                "username": "testacca",
                                "avatar": None,
                                "__typename": "User",
                            },
                            "startAt": "2022-01-13T16:00:00.000Z",
                            "endAt": "2022-11-18T16:00:00.000Z",
                            "dropStatus": "LIVE",
                            "isPublicReadOnly": False,
                            "premiumDropConfig": None,
                            "__typename": "Drop",
                        },
                    ],
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_user_metrics(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {"userMetrics": {"likes": 0, "views": 10, "created": 0, "minted": 0, "__typename": "UserMetrics"}}
        },
    )


@fixture
def mock_user(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "user": {
                        "uuid": "a99da057-29ae-46cd-bd6f-88ca68e09c6d",
                        "verified": False,
                        "id": "k6-qiangfu",
                        "username": "k6-qiangfu",
                        "bio": None,
                        "displayName": None,
                        "instagramUsername": None,
                        "facebookUsername": None,
                        "twitterUsername": None,
                        "isCreator": True,
                        "canCreateAsset": True,
                        "croWalletAddress": "tcro1k7hsy88nwl7k64yqk75nckq90plgk87r03dr2r",
                        "avatar": None,
                        "cover": None,
                        "__typename": "User",
                    },
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_get_users_create_assets(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "creations": [
                    {
                        "id": "b3de4d2af999e1bcc23be7dd1e35a8c7",
                        "name": "12123123",
                        "description": "123123",
                        "copies": 10,
                        "copiesInCirculation": 10,
                        "collectiblePerPack": None,
                        "createdAt": "2022-11-02T10:45:01.428Z",
                        "collection": {
                            "logo": {
                                "url": "https://vsta-nft-images.3ona.co/055ac989-2854-41de/original.jpg",
                                "__typename": "Attachment",
                            },
                            "id": "b0604d98abd467306bc85a058ba50beb",
                            "name": "AT Collection",
                            "verified": False,
                            "__typename": "Collection",
                        },
                        "main": {
                            "url": "https://vsta-nft-images.3ona.co/e4ad668a-8d97-4ed6/original.jpg",
                            "__typename": "Attachment",
                        },
                        "cover": {
                            "url": "https://vsta-nft-images.3ona.co/716a5509-9290-49bb/original.jpg",
                            "__typename": "Attachment",
                        },
                        "drop": None,
                        "kind": "COLLECTIBLE",
                        "defaultEditionId": "8bd3b603f5eeeb35227d272b7d881a27",
                        "defaultOwnerEdition": {"id": "8bd3b603f5eeeb35227d272b7d881a27", "__typename": "Edition"},
                        "defaultPrimaryListing": None,
                        "primaryListingsCount": 0,
                        "secondaryListingsCount": 0,
                        "isCurated": False,
                        "isExternalNft": False,
                        "externalNftMetadata": None,
                        "__typename": "Asset",
                    },
                    {
                        "id": "8b7e87864350b59f0f52ad05da8d83ce",
                        "name": "NFT AT 09201009",
                        "description": "NFT AT 09201009",
                        "copies": 10,
                        "copiesInCirculation": 10,
                        "collectiblePerPack": None,
                        "createdAt": "2022-09-20T02:15:00.895Z",
                        "collection": {
                            "logo": {
                                "url": "https://vsta-nft-images.3ona.co/055ac989-2854-41de/original.jpg",
                                "__typename": "Attachment",
                            },
                            "id": "b0604d98abd467306bc85a058ba50beb",
                            "name": "AT Collection",
                            "verified": False,
                            "__typename": "Collection",
                        },
                        "main": {
                            "url": "https://vsta-nft-images.3ona.co/ad9ddc99-5413-4601/original.jpg",
                            "__typename": "Attachment",
                        },
                        "cover": {
                            "url": "https://vsta-nft-images.3ona.co/72d14fab-b830-4292/original.jpg",
                            "__typename": "Attachment",
                        },
                        "drop": None,
                        "kind": "COLLECTIBLE",
                        "defaultEditionId": "fb6ba6d3515a2a2abdc168643898b501",
                        "defaultOwnerEdition": {"id": "2bfc65bb321ca54ce01ee32d45a56599", "__typename": "Edition"},
                        "defaultPrimaryListing": {
                            "editionId": "2bfc65bb321ca54ce01ee32d45a56599",
                            "priceDecimal": "100.00",
                            "mode": "sale",
                            "auctionHasBids": False,
                            "auctionCloseAt": None,
                            "primary": True,
                            "salePriceDecimalUSD": "100.00",
                            "currency": "USD",
                            "seller": {"id": "k6-qiangfu", "__typename": "User"},
                            "__typename": "Listing",
                        },
                        "primaryListingsCount": 1,
                        "secondaryListingsCount": 0,
                        "isCurated": False,
                        "isExternalNft": False,
                        "externalNftMetadata": None,
                        "__typename": "Asset",
                    },
                ]
            }
        },
    )


@fixture
def mock_get_user_created_collections(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "createdCollections": [
                    {
                        "id": "b0604d98abd467306bc85a058ba50beb",
                        "name": "AT Collection",
                        "logo": {
                            "url": "https://vsta-nft-images.3ona.co/055ac989-2854-41de/original.jpg",
                            "__typename": "Attachment",
                        },
                        "banner": {
                            "url": "https://vsta-nft-images.3ona.co/7ebf1dd7-1523-418c/original.jpg",
                            "__typename": "Attachment",
                        },
                        "verified": False,
                        "metrics": {"items": 9, "__typename": "CollectionMetrics"},
                        "__typename": "Collection",
                    }
                ]
            }
        },
    )


@fixture
def mock_get_my_metrics(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {"myMetrics": {"likes": 7, "views": 26, "created": 11, "minted": 110, "__typename": "UserMetrics"}}
        },
    )


@fixture
def mock_complete_profile(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "completeProfile": {
                    "email": "k6-nft-load-test+api12246@crypto.com",
                    "name": "qweqwr",
                    "username": "k6-nft-load-t804",
                    "uuid": "652a11c5-821d-45c3-a588-d17225a07b05",
                    "__typename": "UnauthorizedMeV2",
                }
            }
        },
    )


@fixture
def mock_update_profile(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "updateProfile": {
                    "id": "k6-qiangfu",
                    "bio": "testdeo",
                    "name": "atr",
                    "username": "k6-qiangfu",
                    "displayName": None,
                    "instagramUsername": "at1",
                    "facebookUsername": "at2",
                    "twitterUsername": "at3",
                    "avatar": {
                        "url": "https://dfsgjflvxpujn.cloudfront.net/63b044ee-2a24/original.jpg",
                        "__typename": "Attachment",
                    },
                    "cover": None,
                    "__typename": "Me",
                }
            }
        },
    )


@fixture
def mock_get_unopened_packs(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "packs": [
                    {
                        "id": "0b5500d190d50fcf55497804c0cf3de9",
                        "asset": {
                            "collectiblePerPack": 1,
                            "name": "Pack AT 2022121906",
                            "cover": {
                                "url": "https://dfsgjflvxpujn.cloudfront.net/c99df592/original.jpg",
                                "__typename": "Attachment",
                            },
                            "drop": {"endAt": "2032-12-18T16:00:00.000Z", "__typename": "Drop"},
                            "likes": 0,
                            "views": 1,
                            "__typename": "Asset",
                        },
                        "__typename": "Edition",
                    }
                ]
            }
        },
    )


@fixture
def mock_get_pack(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "edition": {
                        "id": "711e8a59bac61c5deb2ef39e62f48c1a",
                        "asset": {
                            "collectiblePerPack": 1,
                            "name": "pack1230",
                            "cover": {
                                "url": "https://dfsgjflvxpujn.cloudfront.net/23004d43/original.png",
                                "__typename": "Attachment",
                            },
                            "likes": 0,
                            "views": 2,
                            "__typename": "Asset",
                        },
                        "__typename": "Edition",
                    },
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_open_pack(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "openPack": [
                    {
                        "id": "9abddf9dd9e0985efc5cd4b72fd91d61",
                        "index": 5,
                        "asset": {
                            "id": "c6ad29218cab47c240d030f1d4cf8c3a",
                            "name": "name3",
                            "copies": 20,
                            "creator": {
                                "displayName": "jelly",
                                "username": "jellyli",
                                "uuid": "04030ce9-3162-4d1c-9bac-7bfe011019aa",
                                "avatar": {
                                    "url": "https://dfsgjflvxpujn.cloudfront.net/9f438216/original.jpeg",
                                    "__typename": "Attachment",
                                },
                                "__typename": "User",
                            },
                            "cover": {
                                "url": "https://dfsgjflvxpujn.cloudfront.net/9c682e51/original.png",
                                "__typename": "Attachment",
                            },
                            "main": {
                                "url": "https://dfsgjflvxpujn.cloudfront.net/9c682e51/original.png",
                                "__typename": "Attachment",
                            },
                            "likes": 0,
                            "views": 1,
                            "__typename": "Asset",
                        },
                        "__typename": "Edition",
                    }
                ]
            }
        },
    )


@fixture
def mock_get_profile_assets(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "profileAssets": [
                        {
                            "id": "58043988538f2b9a6e110f0e9a35daff",
                            "name": "app integration open edition asset",
                            "copies": 96,
                            "copiesInCirculation": 96,
                            "main": {
                                "url": "https://dfsgjflvxpujn.cloudfront.net/9efdff40/original.jpeg",
                                "__typename": "Attachment",
                            },
                            "cover": {
                                "url": "https://dfsgjflvxpujn.cloudfront.net/db915580/original.jpeg",
                                "__typename": "Attachment",
                            },
                            "primaryListingsCount": 0,
                            "secondaryListingsCount": 0,
                            "isCurated": True,
                            "isSoulbound": False,
                            "isExternalNft": False,
                            "__typename": "Asset",
                            "drop": {"id": "4e607f03637ced60d07cb5dd5a24c82f", "__typename": "Drop"},
                            "primarySalesCount": 0,
                            "totalSalesDecimal": "20355",
                            "collection": None,
                            "defaultListing": None,
                            "defaultAuctionListing": None,
                            "defaultSaleListing": None,
                            "defaultSecondaryListing": None,
                            "defaultSecondaryAuctionListing": None,
                            "defaultSecondarySaleListing": None,
                            "defaultPrimaryListing": {
                                "id": "688453",
                                "editionId": "a2f44660239ddcde28b01bff7ba56469",
                                "priceDecimal": "100.00",
                                "auctionMinPriceDecimal": "0.00",
                                "auctionCloseAt": "2022-06-15T23:59:59.000Z",
                                "mode": "sale",
                                "salePriceDecimalUSD": "100.00",
                                "auctionHasBids": False,
                                "currency": "USD",
                                "seller": {
                                    "id": "testacca",
                                    "uuid": "7634a766-ee86-4eb5-b724-82dad9c54afc",
                                    "__typename": "User",
                                },
                                "__typename": "Listing",
                                "primary": True,
                                "source": "CDC_NFT",
                                "externalUser": None,
                            },
                            "rarityScore": "0.000000000000000000",
                            "rarityRank": "0",
                            "externalRarityScore": "0.000000000000000000",
                            "externalRarityRank": "0",
                            "defaultEditionId": "a2f44660239ddcde28b01bff7ba56469",
                            "externalNftMetadata": None,
                            "ownerEditionsTotal": 96,
                            "latestPurchasedEdition": {
                                "id": "a34ca6937d5b1700e27b1fccd42ff7f4",
                                "priceUSD": "100.00",
                                "__typename": "LastPurchasedEdition",
                            },
                        }
                    ],
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_create_collection(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "createCollection": {
                    "id": "0742253133c13cd651de3c9f2b509f95",
                    "creator": {"id": "k6-qiangfu", "__typename": "User"},
                    "name": "asdate",
                    "description": "asdasd",
                    "logo": {
                        "id": "f4154b57-da07-4b7c-bcf1-e0c0eeef022d",
                        "url": "https://vsta-nft-images.3ona.co/f4154b57-da07-4b7c-bcf1-e0c0eeef022d/original.jpg",
                        "__typename": "Attachment",
                    },
                    "banner": {
                        "id": "4023fbe6-2943-4766-ab72-30a0644c1968",
                        "url": "https://vsta-nft-images.3ona.co/4023fbe6-2943-4766-ab72-30a0644c1968/original.png",
                        "__typename": "Attachment",
                    },
                    "blocked": False,
                    "categories": ["1", "2"],
                    "__typename": "Collection",
                }
            }
        },
    )

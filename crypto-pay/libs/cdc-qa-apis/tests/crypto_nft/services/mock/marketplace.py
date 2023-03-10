from pytest import fixture


@fixture
def mock_get_marketplace_assets(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "assets": [
                        {
                            "id": "ca6cd496e8e6878aa104a23f15b9f6c8",
                            "name": "0822 test name",
                            "copies": 10,
                            "copiesInCirculation": 10,
                            "main": {
                                "url": "https://dfsgjflvxpujn.cloudfront.net/db712b0a-2662-4df0-8cab/original.jpeg",
                                "__typename": "Attachment",
                            },
                            "collection": None,
                            "cover": {
                                "url": "https://dfsgjflvxpujn.cloudfront.net/1896b9eb-9d09-49a3-852c/original.jpeg",
                                "__typename": "Attachment",
                            },
                            "defaultListing": {
                                "id": "898980",
                                "editionId": "339691d925bb650ba885a0b89e6f4862",
                                "priceDecimal": "1.00",
                                "mode": "sale",
                                "auctionHasBids": False,
                                "salePriceDecimalUSD": "1.00",
                                "currency": "USD",
                                "seller": {
                                    "id": "jasonwei",
                                    "uuid": "983d2cd6-09cc-4080-9d2b-396ed69b89db",
                                    "__typename": "User",
                                },
                                "__typename": "Listing",
                            },
                            "defaultAuctionListing": None,
                            "defaultSaleListing": {
                                "id": "898980",
                                "editionId": "339691d925bb650ba885a0b89e6f4862",
                                "priceDecimal": "1.00",
                                "mode": "sale",
                                "salePriceDecimalUSD": "1.00",
                                "currency": "USD",
                                "seller": {
                                    "id": "jasonwei",
                                    "uuid": "983d2cd6-09cc-4080-9d2b-396ed69b89db",
                                    "__typename": "User",
                                },
                                "__typename": "Listing",
                            },
                            "defaultPrimaryListing": {
                                "id": "898980",
                                "editionId": "339691d925bb650ba885a0b89e6f4862",
                                "priceDecimal": "1.00",
                                "mode": "sale",
                                "auctionHasBids": False,
                                "primary": True,
                                "salePriceDecimalUSD": "1.00",
                                "currency": "USD",
                                "seller": {
                                    "id": "jasonwei",
                                    "uuid": "983d2cd6-09cc-4080-9d2b-396ed69b89db",
                                    "__typename": "User",
                                },
                                "__typename": "Listing",
                            },
                            "defaultSecondaryListing": None,
                            "defaultSecondaryAuctionListing": None,
                            "defaultSecondarySaleListing": None,
                            "isCurated": False,
                            "externalNftMetadata": None,
                            "secondaryListingsCount": 0,
                            "primaryListingsCount": 2,
                            "isExternalNft": False,
                            "__typename": "Asset",
                        },
                    ],
                    "__typename": "Public",
                }
            }
        },
    )

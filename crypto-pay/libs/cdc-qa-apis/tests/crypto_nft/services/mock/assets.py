from pytest import fixture


@fixture
def mock_get_next_available_open_listing_edition(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "getNextAvailableOpenListingEdition": {
                    "editionId": "a3e53cbfdd7e5633cdc9d50ee8b9a7a3",
                    "assetId": "496562129e905b506e11b95632c9b467",
                    "__typename": "NextAvailableListing",
                }
            }
        },
    )


@fixture
def mock_get_edition_by_asset_id(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "public": {
                    "edition": {
                        "id": "339691d925bb650ba885a0b89e6f4862",
                        "assetId": "ca6cd496e8e6878aa104a23f15b9f6c8",
                        "index": 9,
                        "listing": {
                            "id": "898980",
                            "price": None,
                            "currency": "USD",
                            "primary": True,
                            "auctionCloseAt": None,
                            "auctionHasBids": False,
                            "auctionMinPriceDecimal": "0.00",
                            "expiredAt": None,
                            "priceDecimal": "1.00",
                            "mode": "sale",
                            "isCancellable": True,
                            "status": "open",
                            "source": "CDC_NFT",
                            "salePriceDecimalUSD": "1.00",
                            "externalUser": None,
                            "seller": {"uuid": "983d2cd6-09cc-4080-9d2b-396ed69b89db", "__typename": "User"},
                            "__typename": "Listing",
                        },
                        "primaryListing": {
                            "id": "898980",
                            "price": None,
                            "currency": "USD",
                            "primary": True,
                            "auctionCloseAt": None,
                            "auctionHasBids": False,
                            "auctionMinPriceDecimal": "0.00",
                            "expiredAt": None,
                            "priceDecimal": "1.00",
                            "mode": "sale",
                            "isCancellable": True,
                            "status": "open",
                            "source": "CDC_NFT",
                            "salePriceDecimalUSD": "1.00",
                            "externalUser": None,
                            "seller": {"uuid": "983d2cd6-09cc-4080-9d2b-396ed69b89db", "__typename": "User"},
                            "__typename": "Listing",
                        },
                        "owner": {
                            "uuid": "983d2cd6-09cc-4080-9d2b-396ed69b89db",
                            "id": "jasonwei",
                            "username": "jasonwei",
                            "displayName": None,
                            "avatar": None,
                            "croWalletAddress": "tcro18s3dhh6q6nuvq40s0upx0u3kj5xzmx07k4l8mc",
                            "isCreator": True,
                            "verified": True,
                            "__typename": "User",
                        },
                        "ownership": {"primary": True, "__typename": "Ownership"},
                        "chainMintStatus": "minted",
                        "chainTransferStatus": None,
                        "chainWithdrawStatus": None,
                        "acceptedOffer": None,
                        "minOfferAmountDecimal": None,
                        "mintTime": "2022-08-22T06:28:13.823Z",
                        "__typename": "Edition",
                    },
                    "__typename": "Public",
                }
            }
        },
    )


@fixture
def mock_edition_price_quote(requests_mock):
    requests_mock.post(
        url="https://3ona.co/nft-api/graphql",
        json={
            "data": {
                "editionPriceQuote": {
                    "createdAt": "2022-12-06T09:25:28.708Z",
                    "priceUSD": "2.00",
                    "validMs": 300000,
                    "__typename": "EditionPriceQuote",
                }
            }
        },
    )

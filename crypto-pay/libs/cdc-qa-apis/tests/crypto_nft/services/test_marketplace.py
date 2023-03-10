import pytest
from .mock.marketplace import *  # noqa
from cdc.qa.apis import crypto_nft as nft


@pytest.fixture
def mp_service():
    service = nft.GqlServices().marketplace
    return service


def test_get_marketplace_assets(mp_service, mock_get_marketplace_assets):
    params = {
        "categories": [],
        "first": 36,
        "skip": 0,
        "cacheId": "getMarketplaceAssetsQuery-2ec291059e0e5f139cab98dc49ce3eda0d075b1c",
        "audience": "MARKETPLACE",
        "listingTypes": [],
        "collections": [],
        "curation": [],
    }
    where = {
        "creatorName": None,
        "assetName": None,
        "description": None,
        "minPrice": None,
        "maxPrice": None,
        "buyNow": False,
        "auction": False,
        "chains": ["CRO"],
    }
    sort = [{"order": "ASC", "field": "price"}]
    resp = mp_service.get_marketplace_assets(params=params, where=where, sort=sort)
    assert resp.data.public.assets[0].id == "ca6cd496e8e6878aa104a23f15b9f6c8"

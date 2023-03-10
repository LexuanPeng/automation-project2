import pytest
from .mock.assets import *  # noqa
from cdc.qa.apis import crypto_nft as nft


@pytest.fixture
def assets_service():
    service = nft.GqlServices().assets
    return service


def test_get_next_available_open_listing_edition(assets_service, mock_get_next_available_open_listing_edition):
    resp = assets_service.get_next_available_open_listing_edition(a_id="496562129e905b506e11b95632c9b467")
    assert resp.data.getNextAvailableOpenListingEdition.editionId == "a3e53cbfdd7e5633cdc9d50ee8b9a7a3"
    assert resp.data.getNextAvailableOpenListingEdition.assetId == "496562129e905b506e11b95632c9b467"


def test_get_edition_by_asset_id(assets_service, mock_get_edition_by_asset_id):
    resp = assets_service.get_edition_by_asset_id(e_id="1234", c_id="getEditionById-1234-undefined-undefined")
    assert resp.data.public.edition.id == "339691d925bb650ba885a0b89e6f4862"
    assert resp.data.public.edition.assetId == "ca6cd496e8e6878aa104a23f15b9f6c8"


def test_edition_price_quote(assets_service, mock_edition_price_quote):
    resp = assets_service.edition_price_quote(e_id="496562129e905b506e11b95632c9b467")
    assert resp.data.editionPriceQuote.validMs == 300000

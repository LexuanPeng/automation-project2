import pytest
from .mock.drops import *  # noqa
from cdc.qa.apis import crypto_nft as nft


@pytest.fixture
def drops_service():
    service = nft.GqlServices().drops
    return service


# def test_create_chekcout(drops_service, mock_create_checkout):
#     response = drops_service.create_checkout("listing_id", "kind", 1)
#     assert response.data.createCheckout.id == "bf7dca1a-63da-403c-8e24-145d8ce53acc"
#
#
# def test_create_and_capture_account_payment(drops_service, mock_create_and_capture_account_payment):
#     response = drops_service.create_and_capture_account_payment("checkout_id")
#     assert response.data.createAndCaptureAccountPayment.id == "e2db9fb0-8950-44a7-9d8f-2c4519dfaf10"


def test_get_drops(drops_service, mock_get_drops):
    response = drops_service.get_drops(
        params={"cacheId": "cacheId", "dropStatuses": ["Upcoming"], "withDropStatusField": True},
        end_at={"gt": "2023-01-31T18:30:00.000Z"},
        sort=[{"field": "field", "order": "order"}],
    )
    assert response.data.public.drops[0].id == "12013205d823385a3b1cbd7afa48b0e5"
    assert response.data.public.drops[0].creator.username == "cynthiacreator1"


def test_get_drop(drops_service, mock_get_drop):
    response = drops_service.get_drop(drop_id="1asdad", cacheId="asdasd")
    assert response.data.public.drop.id == "912f5bc886e405334540f7966880a35a"
    assert response.data.public.drop.creator.id == "harry"
    assert response.data.public.drop.cover.url == "https://vsta-nft-images.3ona.co/eaebd186/original.webp"
    assert response.data.public.drop.isPublicReadOnly is True


def test_get_drop_assets_query(drops_service, mock_get_drop_assets_query):
    response = drops_service.get_drop_asset_query(asset_id="asset_id", cacheId="cacheId")
    assert response.data.public.assets[0].id == "7b34ca37977c56aa666219bcd8e27b2d"

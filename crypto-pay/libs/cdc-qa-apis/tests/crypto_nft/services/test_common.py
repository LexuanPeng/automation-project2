import pytest

from cdc.qa.apis import crypto_nft as nft
from .mock.common import *  # noqa


@pytest.fixture
def common_service():
    service = nft.GqlServices().common
    return service


def test_get_credit_cards(common_service, mock_get_credit_cards):
    resp = common_service.get_credit_cards()
    assert resp.data.creditCards[0].firstSixDigits == "411111"
    assert resp.data.creditCards[0].lastFourDigits == "1111"
    assert resp.data.creditCards[0].isExpired is False
    assert resp.data.creditCards[0].cardType == "visa"
    assert resp.data.creditCards[0].uuid == "1a984964-3d15-4e63-a8ce-319c9d949519"


def test_create_ixo_payment(common_service, mock_create_ixo_payment):
    resp = common_service.create_ixo_payment(
        params={
            "cardFirstSixDigits": "411111",
            "cardLastFourDigits": "1111",
            "checkoutId": "7ae0e250-ec25-4d5a-b837-30917a989496",
        }
    )
    assert resp.data.createIXOPayment.id == "aa859db2-8450-4054-9ad9-b198cc7b94c0"


def test_preauth_ixo_payment(common_service, mock_preauth_ixo_payment):
    resp = common_service.preauth_ixo_payment(
        params={
            "withRegister": False,
            "checkoutId": "7ae0e250-ec25-4d5a-b837-30917a989496",
            "paymentId": "aa859db2-8450-4054-9ad9-b198cc7b94c0",
            "transactionToken": "ix::325053900a0ef16aeda781ee72e2",
        }
    )
    assert resp.data.preauthIXOPayment.preauthReturnType == "REDIRECT"
    assert resp.data.preauthIXOPayment.status == "preauthorizing"


def test_capture_ixo_payment(common_service, mock_capture_ixo_payment):
    resp = common_service.capture_ixo_payment(
        params={
            "checkoutId": "7ae0e250-ec25-4d5a-b837-30917a989496",
            "paymentId": "aa859db2-8450-4054-9ad9-b198cc7b94c0",
        }
    )
    assert resp.data.captureIXOPayment.status == "capturing"
    assert resp.data.captureIXOPayment.checkout.listingMode == "sale"


def test_paid_checkouts(common_service, mock_paid_checkouts):
    resp = common_service.paid_checkouts(params={"first": 20, "skip": 0})
    assert resp.data.paidCheckouts[0].id == "c4c605d2-2f2f-46ae-b6b0-35a17b2304fd"
    assert resp.data.paidCheckouts[0].asset.id == "7850f5ff3a1c48a1d858d5d33a14d4be"
    assert resp.data.paidCheckouts[0].edition.id == "cb0c0cade3460b3a47ecd0bc49754e55"
    assert resp.data.paidCheckouts[0].edition.owner.id == "k6-qiang016"
    assert resp.data.paidCheckouts[0].listing.mode == "sale"
    assert resp.data.paidCheckouts[0].seller.isCreator is True


def test_get_categories(common_service, mock_get_categories):
    resp = common_service.get_categories(params={})
    assert resp.data.public.categories[0].id == "1"
    assert resp.data.public.categories[0].name == "Art"
    assert resp.data.public.categories[1].id == "2"


# def test_create_attachment(common_service, mock_create_attachment):
#     from pathlib import Path
#
#     img_file = Path.cwd() / "tests" / "crypto_nft" / "services" / "__init__.py"
#     resp = common_service.create_attachment(nature="asset-main", file=("__init__.py", open(img_file, "rb"), "file"))
#     assert resp.data.createAttachment.id == "ee9d1778-e144-4ab9-8218-0baf6a0b4a11"


def test_place_bid_mutation(common_service, mock_place_bid_mutation):
    resp = common_service.place_bid_mutation(listing_id="lid", bid_price="100.00")
    assert resp.data.createCheckout.bidPriceDecimal == "100.00"


def test_get_bidding_history(common_service, mock_get_bidding_history):
    resp = common_service.get_bidding_history(listing_id="str123")
    assert resp.data.public.bids[0].id is not None


def test_delete_credit_card(common_service, mock_delete_credit_card):
    resp = common_service.delete_credit_card(card_id="123str")
    assert resp.data.deleteCreditCard.uuid == "1a984964-3d15-4e63-a8ce-319c9d949519"


def test_get_top_collectibles(common_service, mock_get_top_collectibles):
    resp = common_service.get_top_collectibles(
        params={
            "topCollectiblesFilter": "LATEST_7_DAYS",
            "topCollectiblesFilterBy": "VOLUME",
            "cacheId": "getTopCollectiblesQuery-TopCollectibleBlock-VOLUME-LATEST_7_DAYS-12",
            "page": 1,
            "pageSize": 12,
        }
    )
    assert resp.data.public.topCollectibles[0].id == "c4dbb995a39557a6f96335380e93140a"


def test_checkout_amount(common_service, mock_checkout_amount):
    resp = common_service.checkout_amount(c_id="test")
    assert resp.data.checkout.amountDecimal == "3.00"

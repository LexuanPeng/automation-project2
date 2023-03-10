import pytest

from cdc.qa.apis import crypto_nft as nft
from .mock.profile import *  # noqa


@pytest.fixture
def profile_service():
    service = nft.GqlServices().profile
    return service


def test_get_user_private_assets_total(profile_service, mock_get_user_private_assets_total):
    response = profile_service.get_user_private_assets_total()
    assert response.data.collectedEditionsTotal == 103
    assert response.data.createdAssetsTotal == 11


def test_get_profile_collections(profile_service, mock_get_profile_collections):
    param = {"creatorId": "k6", "sort": {"field": "createdAt", "order": "DESC"}}
    response = profile_service.get_profile_collections(param=param)
    assert response.data.public.profileCollections[0].id == "45bfb5918b57d3ff93e7925a5165d00c"
    assert response.data.public.profileCollections[0].name == "1231"
    assert response.data.public.profileCollections[1].name == "AT Collection"
    assert response.data.public.profileCollections[0].metrics.items == 0


def test_live_and_incoming_drops(profile_service, mock_live_and_incoming_drops):
    drop_status = ["LIVE", "UPCOMING", "SOLD_OUT"]
    end_at = {"gt": "2022-11-14T23:27:32.330Z"}
    response = profile_service.live_and_incoming_drops(drop_status=drop_status, endAt=end_at)
    assert response.data.public.drops[0].id == "912f5bc886e405334540f7966880a35a"
    assert response.data.public.drops[0].creator.username == "harry"
    assert response.data.public.drops[0].dropStatus == "LIVE"
    assert response.data.public.drops[0].isPublicReadOnly is True


def test_user_metrics(profile_service, mock_user_metrics):
    response = profile_service.user_metrics(uid="str123")
    assert response.data.userMetrics.likes == 0
    assert response.data.userMetrics.views == 10


def test_user(profile_service, mock_user):
    response = profile_service.user(uid="k6-example", cache_id="cid")
    assert response.data.public.user.uuid == "a99da057-29ae-46cd-bd6f-88ca68e09c6d"
    assert response.data.public.user.id == "k6-qiangfu"


def test_get_my_metrics(profile_service, mock_get_my_metrics):
    resp = profile_service.get_my_metrics()
    assert resp.data.myMetrics.likes == 7


def test_get_user_created_assets(profile_service, mock_get_users_create_assets):
    resp = profile_service.get_user_created_assets(
        params={
            "first": 36,
            "skip": 0,
            "listingTypes": [],
            "collections": [],
            "curation": [],
            "categories": [],
            "sort": [{"order": "DESC", "field": "createdAt"}],
        }
    )
    assert resp.data.creations[0].id == "b3de4d2af999e1bcc23be7dd1e35a8c7"
    assert resp.data.creations[0].defaultOwnerEdition.id == "8bd3b603f5eeeb35227d272b7d881a27"


def test_get_user_created_collections(profile_service, mock_get_user_created_collections):
    resp = profile_service.get_user_created_collections(
        params={
            "search": "",
            "first": 10,
            "sort": {"field": "totalSalesDecimalInLast1Day", "order": "DESC"},
            "withStats": False,
            "isSortFieldZeroLast": False,
            "verifiedOnly": False,
            "verifiedFirst": False,
            "assetCreatorId": "k6-qiangfu",
        }
    )
    assert resp.data.createdCollections[0].id == "b0604d98abd467306bc85a058ba50beb"
    assert resp.data.createdCollections[0].metrics.items == 9


def test_complete_profile(profile_service, mock_complete_profile):
    resp = profile_service.complete_profile(name="qweqwr", username="k6-nft-load-t804")
    assert resp.data.completeProfile.email == "k6-nft-load-test+api12246@crypto.com"
    assert resp.data.completeProfile.name == "qweqwr"
    assert resp.data.completeProfile.username == "k6-nft-load-t804"
    assert resp.data.completeProfile.uuid == "652a11c5-821d-45c3-a588-d17225a07b05"


def test_update_pforfile(profile_service, mock_update_profile):
    params = {
        "bio": "testdeo",
        "name": "atr",
        "username": "k6-qiangfu",
        "displayName": None,
        "instagramUsername": "at1",
        "facebookUsername": "at2",
        "twitterUsername": "at3",
    }
    resp = profile_service.update_profile(params)
    assert resp.data.updateProfile.id == "k6-qiangfu"


def test_get_unopened_packs(profile_service, mock_get_unopened_packs):
    resp = profile_service.get_unopened_packs(first=20, skip=0)
    assert resp.data.packs[0].id == "0b5500d190d50fcf55497804c0cf3de9"


def test_get_pack(profile_service, mock_get_pack):
    resp = profile_service.get_pack(edition_id="str123", owner_id="str456", cache_id="str789")
    assert resp.data.public.edition.id == "711e8a59bac61c5deb2ef39e62f48c1a"


def test_open_pack(profile_service, mock_open_pack):
    resp = profile_service.open_pack(edition_id="str123")
    assert resp.data.openPack[0].id == "9abddf9dd9e0985efc5cd4b72fd91d61"


def test_create_collection(profile_service, mock_create_collection):
    resp = profile_service.create_collection(
        params={
            "bannerId": "4023fbe6-2943-4766-ab72-30a0644c1968",
            "logoId": "f4154b57-da07-4b7c-bcf1-e0c0eeef022d",
            "categories": ["1", "2"],
            "name": "asdate",
            "description": "asdasd",
        }
    )
    assert resp.data.createCollection.id == "0742253133c13cd651de3c9f2b509f95"

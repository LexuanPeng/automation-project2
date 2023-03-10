from cdc.qa.apis.crypto_nft.models import NFTRestApi, NFTClientService, profile
from .tools import compare_dict


class GetProfileAssetsTotalApi(NFTRestApi):
    response_type = profile.GetProfileAssetsTotalResoponse


class GetUserPrivateAssetsTotalApi(NFTRestApi):
    response_type = profile.GerUserPrivateAssetsTotalResoponse


class GetProfileCollectionsApi(NFTRestApi):
    response_type = profile.GetProfileCollectionsResponse


class LiveAndIncomingDropsApi(NFTRestApi):
    response_type = profile.LiveAndIncomingDropsResponse


class UserMetricsApi(NFTRestApi):
    response_type = profile.UserMetricsResponse


class UserApi(NFTRestApi):
    response_type = profile.UserResponse


class GetMyMetricsApi(NFTRestApi):
    response_type = profile.GetMyMetricsResponse


class GetUserCreatedAssetsApi(NFTRestApi):
    response_type = profile.GetUserCreatedAssetsResponse


class GetUserCreatedCollectionsApi(NFTRestApi):
    response_type = profile.GetUserCreatedCollectionsResponse


class CompleteProfileApi(NFTRestApi):
    response_type = profile.CompleteProfileResponse


class UpdateProfileApi(NFTRestApi):
    response_type = profile.UpdateProfileResponse


class GetUnopenedPacksApi(NFTRestApi):
    response_type = profile.GetUnopenedPacksResponse


class GetPackApi(NFTRestApi):
    response_type = profile.GetPackResponse


class OpenPackApi(NFTRestApi):
    response_type = profile.OpenPackResponse


class GetProfileAssetsApi(NFTRestApi):
    response_type = profile.GetProfileAssetsResponse


class UpdateCollectionApi(NFTRestApi):
    response_type = profile.UpdateCollectionResponse


class CreateCollectionApi(NFTRestApi):
    response_type = profile.CreateCollectionResponse


class ProfileService(NFTClientService):
    def get_profile_assets_total(self, use_id: str, cacheId: str) -> profile.GetProfileAssetsTotalResoponse:
        api = GetProfileAssetsTotalApi(host=self.host, _session=self.session, nft_token=None)
        request = profile.GetProfileAssetsTotalRequest(
            variables=profile.GetProfileAssetsTotalRequest.Variables(userId=use_id, cacheId=cacheId)
        )
        return profile.GetProfileAssetsTotalResoponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_user_private_assets_total(self) -> profile.GerUserPrivateAssetsTotalResoponse:
        api = GetUserPrivateAssetsTotalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.GetUserPrivateAssetsTotalRequest()
        return profile.GerUserPrivateAssetsTotalResoponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_profile_collections(self, param: dict) -> profile.GetProfileCollectionsResponse:
        api = GetProfileCollectionsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.GetProfileCollectionsRequest(
            variables=profile.GetProfileCollectionsRequest.Variables(**param)
        )
        request = compare_dict(params_dict=param, request_dict=request.dict())
        return profile.GetProfileCollectionsResponse.parse_raw(b=api.call(json=request).content)

    def live_and_incoming_drops(self, drop_status: list, endAt: dict) -> profile.LiveAndIncomingDropsResponse:
        api = LiveAndIncomingDropsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.LiveAndIncomingDropsRequest(
            variables=profile.LiveAndIncomingDropsRequest.Variables(dropStatuses=drop_status, endAt=endAt)
        )
        return profile.LiveAndIncomingDropsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def user_metrics(self, uid: str) -> profile.UserMetricsResponse:
        api = UserMetricsApi(host=self.host, _session=self.session, nft_token=None)
        request = profile.UserMetricsRequest(variables=profile.UserMetricsRequest.Variables(id=uid))
        return profile.UserMetricsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def user(self, uid: str, cache_id: str) -> profile.UserResponse:
        api = UserApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.UserRequest(variables=profile.UserRequest.Variables(id=uid, cacheId=cache_id))
        return profile.UserResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_my_metrics(self) -> profile.GetMyMetricsResponse:
        api = GetMyMetricsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.GetMyMetricsRequest()
        return profile.GetMyMetricsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_user_created_assets(self, params: dict, token: str = None) -> profile.GetUserCreatedAssetsResponse:
        api = GetUserCreatedAssetsApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = profile.GetUserCreatedAssetsRequest(
            variables=profile.GetUserCreatedAssetsRequest.Variables(**params)
        ).dict()
        request = compare_dict(params_dict=params, request_dict=request)
        return profile.GetUserCreatedAssetsResponse.parse_raw(b=api.call(json=request).content)

    def get_user_created_collections(self, params: dict) -> profile.GetUserCreatedCollectionsResponse:
        api = GetUserCreatedCollectionsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.GetUserCreatedCollectionsRequest(
            variables=profile.GetUserCreatedCollectionsRequest.Variables(**params)
        )
        return profile.GetUserCreatedCollectionsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def complete_profile(self, name: str, username: str, token: str = None):
        api = CompleteProfileApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if token is None else token
        )
        request = profile.CompleteProfileRequest(
            variables=profile.CompleteProfileRequest.Variables(name=name, username=username)
        )
        return profile.CompleteProfileResponse.parse_raw(b=api.call(json=request.dict()).content)

    def update_profile(self, params: dict) -> profile.UpdateProfileResponse:
        api = UpdateProfileApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.UpdateProfileRequest(variables=profile.UpdateProfileRequest.Variables(**params))
        request = compare_dict(params_dict=params, request_dict=request.dict())
        return profile.UpdateProfileResponse.parse_raw(b=api.call(json=request).content)

    def get_unopened_packs(self, first: int, skip: int) -> profile.GetUnopenedPacksResponse:
        api = GetUnopenedPacksApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.GetUnopenedPacksRequest(
            variables=profile.GetUnopenedPacksRequest.Variables(first=first, skip=skip)
        )
        return profile.GetUnopenedPacksResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_pack(self, edition_id: str, owner_id: str, cache_id: str) -> profile.GetPackResponse:
        api = GetPackApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.GetPackRequest(
            variables=profile.GetPackRequest.Variables(editionId=edition_id, ownerId=owner_id, cacheId=cache_id)
        )
        return profile.GetPackResponse.parse_raw(b=api.call(json=request.dict()).content)

    def open_pack(self, edition_id: str) -> profile.OpenPackResponse:
        api = OpenPackApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.OpenPackRequest(variables=profile.OpenPackRequest.Variables(editionId=edition_id))
        return profile.OpenPackResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_profile_assets(self, params: dict) -> profile.GetProfileAssetsResponse:
        api = GetProfileAssetsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.GetProfileAssetsRequest(variables=profile.GetProfileAssetsRequest.Variables(**params))
        return profile.GetProfileAssetsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def update_collection(self, params: dict) -> profile.UpdateCollectionResponse:
        api = UpdateCollectionApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.UpdateCollectionRequest(variables=profile.UpdateCollectionRequest.Variables(**params))
        return profile.UpdateCollectionResponse.parse_raw(b=api.call(json=request.dict()).content)

    def create_collection(self, params: dict) -> profile.CreateCollectionResponse:
        api = CreateCollectionApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = profile.CreateCollectionRequest(variables=profile.CreateCollectionRequest.Variables(**params))
        return profile.CreateCollectionResponse.parse_raw(b=api.call(json=request.dict()).content)

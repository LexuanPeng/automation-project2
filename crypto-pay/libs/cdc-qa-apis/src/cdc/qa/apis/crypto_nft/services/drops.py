from typing import List

from cdc.qa.apis.crypto_nft.models import NFTRestApi, NFTClientService, drops


class GetDropsApi(NFTRestApi):
    response_type = drops.GetDropsResponse


class GetDropApi(NFTRestApi):
    response_type = drops.GetDropResponse


class GetDropAssetsQueryApi(NFTRestApi):
    response_type = drops.GetDropAssetsQueryResponse


class DropsService(NFTClientService):
    def get_drops(self, params: dict, end_at: dict, sort: List) -> drops.GetDropsResponse:
        api = GetDropsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = drops.GetDropsRequest(
            variables=drops.GetDropsRequest.Variables(
                **params,
                endAt=drops.GetDropsRequest.Variables.EndAt(**end_at),
                sort=sort
                # sort=drops.GetDropsRequest.Variables.SortBy(sort)
            )
        )
        return drops.GetDropsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_drop(self, drop_id: str, cacheId: str) -> drops.GetDropResponse:
        api = GetDropApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = drops.GetDropRequest(variables=drops.GetDropRequest.Variables(id=drop_id, cacheId=cacheId))
        return drops.GetDropResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_drop_asset_query(self, asset_id: str, cacheId: str) -> drops.GetDropAssetsQueryResponse:
        api = GetDropAssetsQueryApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = drops.GetDropAssetsQueryRequest(
            variables=drops.GetDropAssetsQueryRequest.Variables(id=asset_id, cacheId=cacheId)
        )
        return drops.GetDropAssetsQueryResponse.parse_raw(b=api.call(json=request.dict()).content)

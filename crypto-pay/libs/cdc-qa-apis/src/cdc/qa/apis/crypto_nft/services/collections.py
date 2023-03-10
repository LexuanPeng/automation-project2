from cdc.qa.apis.crypto_nft.models import NFTRestApi, NFTClientService, collections


class GetCollectionsPageApi(NFTRestApi):
    response_type = collections.GetCollectionsPageResponse


class CollectionsService(NFTClientService):
    def get_collections_page(self, sort: dict, params: dict) -> collections.GetCollectionsPageResponse:
        api = GetCollectionsPageApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = collections.GetCollectionsPageRequest(
            variables=collections.GetCollectionsPageRequest.Variables(sort=sort, **params)
        )
        return collections.GetCollectionsPageResponse.parse_raw(b=api.call(json=request.dict()).content)

from .tools import compare_dict
from cdc.qa.apis.crypto_nft.models import NFTRestApi, NFTClientService, assets


class IncreaseAssetViewsApi(NFTRestApi):
    response_type = assets.IncreaseAssetViewsResponse


class GetAssetMinPriceApi(NFTRestApi):
    response_type = assets.GetAssetMinPriceResponse


class GetAssetByIdApi(NFTRestApi):
    response_type = assets.GetAssetByIdResponse


class GetEditionsByAssetIdApi(NFTRestApi):
    response_type = assets.GetEditionsByAssetIdResponse


class GetUserAssetsQueryApi(NFTRestApi):
    response_type = assets.GetUserAssetsQueryResponse


class GetNextAvailableOpenListingEditionApi(NFTRestApi):
    response_type = assets.GetNextAvailableOpenListingEditionResponse


class GetEditionByAssetIdApi(NFTRestApi):
    response_type = assets.GetEditionByAssetIdResponse


class EditionPriceQuoteApi(NFTRestApi):
    response_type = assets.EditionPriceQuoteResponse


class GetAssetsApi(NFTRestApi):
    response_type = assets.GetAssetsResponse


class GetAssetsInPackApi(NFTRestApi):
    response_type = assets.GetAssetsInPackResponse


class GetAssetListingsByIdApi(NFTRestApi):
    response_type = assets.GetAssetListingsByIdResponse


class GetAssetDetailByIdApi(NFTRestApi):
    response_type = assets.GetAssetDetailByIdResponse


class AssetsService(NFTClientService):
    def increase_asset_views(self, asset_id: str) -> assets.IncreaseAssetViewsResponse:
        api = IncreaseAssetViewsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = assets.IncreaseAssetViewsRequest(
            variables=assets.IncreaseAssetViewsRequest.Variables(assetId=asset_id)
        )
        return assets.IncreaseAssetViewsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_asset_min_price(self, edition_id: str, asset_id: str, token: str = None) -> assets.GetAssetMinPriceResponse:
        api = GetAssetMinPriceApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = assets.GetAssetMinPriceRequest(
            variables=assets.GetAssetMinPriceRequest.Variables(editionId=edition_id, assetId=asset_id)
        )
        return assets.GetAssetMinPriceResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_asset_by_asset_id(self, id: str, cache_id: str, token: str = None) -> assets.GetAssetByIdResponse:
        api = GetAssetByIdApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = assets.GetAssetByIdRequest(variables=assets.GetAssetByIdRequest.Variables(id=id, cacheId=cache_id))
        return assets.GetAssetByIdResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_editions_by_asset_id(self, params: dict, token: str = None) -> assets.GetEditionsByAssetIdResponse:
        api = GetEditionsByAssetIdApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request: dict = assets.GetEditionsByAssetIdRequest(
            variables=assets.GetEditionsByAssetIdRequest.Variables(**params)
        ).dict()
        request = compare_dict(params, request)
        return assets.GetEditionsByAssetIdResponse.parse_raw(b=api.call(json=request).content)

    def get_user_assets_query(self, params: dict, token: str = None) -> assets.GetUserAssetsQueryResponse:
        api = GetUserAssetsQueryApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = assets.GetUserAssetsQueryRequest(
            variables=assets.GetUserAssetsQueryRequest.Variables(**params)
        ).dict()
        request = compare_dict(params, request)
        return assets.GetUserAssetsQueryResponse.parse_raw(b=api.call(json=request).content)

    def get_next_available_open_listing_edition(self, a_id: str) -> assets.GetNextAvailableOpenListingEditionResponse:
        api = GetNextAvailableOpenListingEditionApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = assets.GetNextAvailableOpenListingEditionRequest(
            variables=assets.GetNextAvailableOpenListingEditionRequest.Variables(assetId=a_id)
        )
        return assets.GetNextAvailableOpenListingEditionResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_edition_by_asset_id(self, e_id: str, c_id: str) -> assets.GetEditionByAssetIdResponse:
        api = GetEditionByAssetIdApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = assets.GetEditionByAssetIdRequest(
            variables=assets.GetEditionByAssetIdRequest.Variables(editionId=e_id, cacheId=c_id)
        )
        return assets.GetEditionByAssetIdResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edition_price_quote(self, e_id: str) -> assets.EditionPriceQuoteResponse:
        api = EditionPriceQuoteApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = assets.EditionPriceQuoteRequest(variables=assets.EditionPriceQuoteRequest.Variables(editionId=e_id))
        return assets.EditionPriceQuoteResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_assets(self, params: dict, sort: dict, token: str = None) -> assets.GetAssetsResponse:
        api = GetAssetsApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request: dict = assets.GetAssetsRequest(
            variables=assets.GetAssetsRequest.Variables(**params, sort=assets.GetAssetsRequest.Variables.SortBy(**sort))
        ).dict()
        request = compare_dict(params, request)
        return assets.GetAssetsResponse.parse_raw(b=api.call(json=request).content)

    def get_assets_in_pack(self, drop_id: str, pack_id: str, cache_id: str) -> assets.GetAssetsInPackResponse:
        api = GetAssetsInPackApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = assets.GetAssetsInPackRequest(
            variables=assets.GetAssetsInPackRequest.Variables(dropId=drop_id, packId=pack_id, cacheId=cache_id)
        )
        return assets.GetAssetsInPackResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_asset_listings_by_id(self, id: str, cache_id: str) -> assets.GetAssetListingsByIdResponse:
        api = GetAssetListingsByIdApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = assets.GetAssetListingsByIdRequest(
            variables=assets.GetAssetListingsByIdRequest.Variables(id=id, cacheId=cache_id)
        )
        return assets.GetAssetListingsByIdResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_asset_detail_by_id(self, id: str, cache_id: str) -> assets.GetAssetDetailByIdResponse:
        api = GetAssetDetailByIdApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = assets.GetAssetDetailByIdRequest(
            variables=assets.GetAssetDetailByIdRequest.Variables(id=id, cacheId=cache_id)
        )
        return assets.GetAssetDetailByIdResponse.parse_raw(b=api.call(json=request.dict()).content)

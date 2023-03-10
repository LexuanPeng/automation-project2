from cdc.qa.apis.crypto_nft.models import NFTRestApi, NFTClientService, marketplace


class GetMarketplaceAssetsApi(NFTRestApi):
    response_type = marketplace.GetMartketplaceAssetsResponse


class CanUserCreateListingApi(NFTRestApi):
    response_type = marketplace.CanUserCreateListingResponse


class CreateListingApi(NFTRestApi):
    response_type = marketplace.CreateListingResponse


class CreateAuctionListingApi(NFTRestApi):
    response_type = marketplace.CreateAuctionListingResponse


class GetSearchPreviewResultsApi(NFTRestApi):
    response_type = marketplace.GetSearchPreviewResultsResponse


class CancelListingApi(NFTRestApi):
    response_type = marketplace.CancelListingResponse


class MarketplaceService(NFTClientService):
    def get_marketplace_assets(
        self, where: dict, sort: list, params: dict
    ) -> marketplace.GetMartketplaceAssetsResponse:
        api = GetMarketplaceAssetsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = marketplace.GetMartketplaceAssetsRequest(
            variables=marketplace.GetMartketplaceAssetsRequest.Variables(
                where=marketplace.GetMartketplaceAssetsRequest.Variables.Where(**where), sort=sort, **params
            )
        )
        return marketplace.GetMartketplaceAssetsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def can_user_create_listing(
        self, can_user_create_listing_id: str, token: str = None
    ) -> marketplace.CanUserCreateListingResponse:
        api = CanUserCreateListingApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = marketplace.CanUserCreateListingRequest(
            variables=marketplace.CanUserCreateListingRequest.Variables(
                canUserCreateListingId=can_user_create_listing_id
            )
        )
        return marketplace.CanUserCreateListingResponse.parse_raw(b=api.call(json=request.dict()).content)

    def create_listing(
        self, edition_id: str, price_decimal: str, mode: str, token: str = None
    ) -> marketplace.CreateListingResponse:
        api = CreateListingApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = marketplace.CreateListingRequest(
            variables=marketplace.CreateListingRequest.Variables(
                editionId=edition_id, priceDecimal=price_decimal, mode=mode
            )
        )
        return marketplace.CreateListingResponse.parse_raw(b=api.call(json=request.dict()).content)

    def create_auction_listing(
        self, edition_id: str, auction_close_at: str, auction_min_price_decimal: str, mode: str, token: str = None
    ) -> marketplace.CreateAuctionListingResponse:
        api = CreateAuctionListingApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = marketplace.CreateAuctionListingRequest(
            variables=marketplace.CreateAuctionListingRequest.Variables(
                editionId=edition_id,
                auctionCloseAt=auction_close_at,
                auctionMinPriceDecimal=auction_min_price_decimal,
                mode=mode,
            )
        )
        return marketplace.CreateAuctionListingResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_search_preview_results(
        self, key_word: str, token: str = None
    ) -> marketplace.GetSearchPreviewResultsResponse:
        api = GetSearchPreviewResultsApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = marketplace.GetSearchPreviewResultsRequest(
            variables=marketplace.GetSearchPreviewResultsRequest.Variables(keyWord=key_word)
        )
        return marketplace.GetSearchPreviewResultsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def cancel_listing(self, id: str, token: str = None) -> marketplace.CancelListingResponse:
        api = CancelListingApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = marketplace.CancelListingRequest(variables=marketplace.CancelListingRequest.Variables(id=id))
        return marketplace.CancelListingResponse.parse_raw(b=api.call(json=request.dict()).content)

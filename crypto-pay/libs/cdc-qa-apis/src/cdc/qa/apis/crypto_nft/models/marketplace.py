from pydantic import Field
from typing import List, Union, Optional

from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import GqlRequest, GqlResponse, FrozenBaseModel
from .models import AssetModel, IdModel, URLModel, MetricsModel


class GetMartketplaceAssetsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        categories: list = Field()
        first: int = Field()
        skip: int = Field()
        cacheId: str = Field(description="getMartketplaceAssetsQuery-{id}")
        audience: str = Field(default="MARKETPLACE")
        listingTypes: list = Field()
        collections: list = Field()
        curation: list = Field()

        class Where(FrozenBaseModel):
            creatorName: Optional[Union[str, None]] = Field(description="creator name")
            assetName: Optional[Union[str, None]] = Field(description="asset name")
            description: Optional[Union[str, None]] = Field(description="description")
            minPrice: Optional[Union[str, None]] = Field(description="min price")
            maxPrice: Optional[Union[str, None]] = Field(description="max price")
            buyNow: Optional[bool] = Field(description="buy now")
            auction: Optional[bool] = Field(description="auction")
            chains: Optional[list] = Field(description="chains")

        class Sort(FrozenBaseModel):
            order: str = Field()
            field: str = Field()

        where: Where = Field()
        sort: List[Sort] = Field()

    operationName: str = Field(default="GetMarketplaceAssets")
    query: str = graphql.marketplace.GetMarketplaceAssets
    variables: Variables = Field()


class GetMartketplaceAssetsResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            assets: List[AssetModel] = Field()

        public: Public = Field()

    data: Data = Field()


class CanUserCreateListingRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        canUserCreateListingId: str = Field()

    operationName: str = Field(default="canUserCreateListing")
    query: str = graphql.marketplace.canUserCreateListing
    variables: Variables = Field()


class CanUserCreateListingResponse(GqlResponse):
    class CanUserCreateListingData(FrozenBaseModel):
        canUserCreateListing: bool = Field()

    data: CanUserCreateListingData = Field()


class CreateListingRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        editionId: str = Field()
        priceDecimal: str = Field()
        mode: str = Field()

    operationName: str = Field(default="CreateListing")
    query: str = graphql.marketplace.CreateListing
    variables: Variables = Field()


class CreateListingResponse(GqlResponse):
    class CreateListingData(FrozenBaseModel):
        createListing: IdModel = Field()

    data: CreateListingData = Field()


class CreateAuctionListingRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        editionId: str = Field()
        auctionCloseAt: str = Field()
        auctionMinPriceDecimal: str = Field()
        mode: str = Field()

    operationName: str = Field(default="CreateAuctionListing")
    query: str = graphql.marketplace.CreateAuctionListing
    variables: Variables = Field()


class CreateAuctionListingResponse(GqlResponse):
    class CreateAuctionListingData(FrozenBaseModel):
        createListing: IdModel = Field()

    data: CreateAuctionListingData = Field()


class GetSearchPreviewResultsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        keyWord: str = Field()

    operationName: str = Field(default="getSearchPreviewResults")
    query: str = graphql.marketplace.getSearchPreviewResults
    variables: Variables = Field()


class GetSearchPreviewResultsResponse(GqlResponse):
    class GetSearchPreviewResultsData(FrozenBaseModel):
        class Public(FrozenBaseModel):
            class DropDown(FrozenBaseModel):
                class Collections(FrozenBaseModel):
                    id: str = Field()
                    logo: URLModel = Field()
                    name: str = Field()
                    verified: str = Field()
                    metrics: MetricsModel = Field()
                    __typename: str = Field()

                collectibles: list = Field()
                collections: List[Collections] = Field()
                users: list = Field()
                __typename: str = Field()

            dropDown: DropDown = Field()
            __typename: str = Field()

        public: Public = Field()

    data: GetSearchPreviewResultsData = Field()


class CancelListingRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()

    operationName: str = Field(default="cancelListing")
    query: str = graphql.marketplace.cancelListing
    variables: Variables = Field()


class CancelListingResponse(GqlResponse):
    class CancelListingData(FrozenBaseModel):
        cancelListing: IdModel = Field()

    data: CancelListingData = Field()

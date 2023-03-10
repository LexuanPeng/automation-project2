from typing import List, Union, Optional

from pydantic import Field
from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import GqlRequest, FrozenBaseModel, GqlResponse
from .models import NextAvailableListingModel, EditionModel, AssetModel


class GetNextAvailableOpenListingEditionRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        assetId: str = Field()

    operationName: str = Field(default="getNextAvailableOpenListingEdition")
    query: str = graphql.assets.getNextAvailableOpenListingEdition
    variables: Variables = Field()


class GetNextAvailableOpenListingEditionResponse(GqlResponse):
    class Data(FrozenBaseModel):
        getNextAvailableOpenListingEdition: NextAvailableListingModel = Field()

    data: Data = Field()


class IncreaseAssetViewsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        assetId: str = Field()

    operationName: str = Field(default="increaseAssetViews")
    query: str = graphql.assets.increaseAssetViews
    variables: Variables = Field()


class IncreaseAssetViewsResponse(GqlResponse):
    class IncreaseAssetViewsData(FrozenBaseModel):
        class IncreaseAssetViews(FrozenBaseModel):
            id: str = Field()
            views: int = Field()
            __typename: str = Field()

        increaseAssetViews: IncreaseAssetViews = Field()

    data: IncreaseAssetViewsData = Field()


class GetAssetMinPriceRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        editionId: str = Field()
        assetId: str = Field()

    operationName: str = Field(default="GetAssetMinPrice")
    query: str = graphql.assets.GetAssetMinPrice
    variables: Variables = Field()


class GetAssetMinPriceResponse(GqlResponse):
    class GetAssetMinPriceData(FrozenBaseModel):
        assetMinPrice: str = Field()

    data: GetAssetMinPriceData = Field()


class GetAssetByIdRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()
        cacheId: str = Field()

    operationName: str = Field(default="GetAssetById")
    query: str = graphql.assets.GetAssetById
    variables: Variables = Field()


class GetAssetByIdResponse(GqlResponse):
    class GetAssetByIdData(FrozenBaseModel):
        class Public(FrozenBaseModel):
            asset: AssetModel = Field()
            __typename: str = Field()

        public: Public = Field()

    data: GetAssetByIdData = Field()


class GetEditionsByAssetIdRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        assetId: Optional[str] = Field()
        cacheId: Optional[str] = Field()
        ownerId: Optional[str] = Field()
        first: Optional[int] = Field()
        skip: Optional[int] = Field()
        ownerId: Optional[str] = Field()
        primary: Optional[bool] = Field()
        hasListing: Optional[bool] = Field()
        sort: Optional[list] = Field()
        mode: Optional[str] = Field()
        editionIndex: Optional[str] = Field()
        isDropLast: Optional[bool] = Field()
        excludeOwnerId: Optional[str] = Field()

    operationName: str = Field(default="getEditionsByAssetId")
    query: str = graphql.assets.getEditionsByAssetId
    variables: Variables = Field()


class GetEditionsByAssetIdResponse(GqlResponse):
    class GetEditionsByAssetIdData(FrozenBaseModel):
        class Public(FrozenBaseModel):
            class Editions(FrozenBaseModel):
                totalCount: int = Field()
                editions: List[EditionModel] = Field()
                __typename: str = Field()

            editions: Editions = Field()
            __typename: str = Field()

        public: Public = Field()

    data: GetEditionsByAssetIdData = Field()


class GetUserAssetsQueryRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        skipCount: bool = Field()
        creatorId: Optional[str] = Field()
        hasSecondaryListing: Optional[bool] = Field()
        first: int = Field()
        skip: int = Field()
        assetIds: Optional[list] = Field()
        where: Optional[dict] = Field()
        sort: list = Field()
        listingTypes: Optional[list] = Field()
        collections: Optional[list] = Field()
        curation: Optional[list] = Field()
        categories: Optional[list] = Field()

    operationName: str = Field(default="GetUserAssetsQuery")
    query: str = graphql.assets.GetUserAssetsQuery
    variables: Variables = Field()


class GetUserAssetsQueryResponse(GqlResponse):
    class GetUserAssetsQueryData(FrozenBaseModel):
        assets: List[AssetModel] = Field()

    data: GetUserAssetsQueryData = Field()


class GetEditionByAssetIdRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        editionId: str = Field()
        cacheId: str = Field()

    operationName: str = Field(default="getEditionByAssetId")
    query: str = graphql.assets.getEditionByAssetId
    variables: Variables = Field()


class GetEditionByAssetIdResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            edition: EditionModel = Field()

        public: Public = Field()

    data: Data = Field()


class EditionPriceQuoteRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        editionId: str = Field()

    operationName: str = Field(default="editionPriceQuote")
    query: str = graphql.assets.editionPriceQuote
    variables: Variables = Field()


class EditionPriceQuoteResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class EditionPriceQuote(FrozenBaseModel):
            createdAt: Optional[Union[str, None]] = Field()
            priceUSD: str = Field()
            validMs: int = Field()
            __typename: str = Field()

        editionPriceQuote: EditionPriceQuote = Field()

    data: Data = Field()


class GetAssetsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        class SortBy(FrozenBaseModel):
            field: str = Field()
            order: str = Field()

        collectionId: str = Field()
        first: int = Field()
        skip: int = Field()
        cacheId: str = Field()
        sort: SortBy = Field()
        listingTypes: Optional[Union[list, None]] = Field()

    operationName: str = Field(default="GetAssets")
    query: str = graphql.assets.GetAssets
    variables: Variables = Field()


class GetAssetsResponse(GqlResponse):
    class GetAssetsData(FrozenBaseModel):
        class Public(FrozenBaseModel):
            assets: List[AssetModel] = Field()
            __typename: str = Field()

        public: Public = Field()

    data: GetAssetsData = Field()


class GetAssetsInPackRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        dropId: str = Field()
        packId: str = Field()
        cacheId: str = Field()

    operationName: str = Field(default="GetAssetsInPack")
    query: str = graphql.assets.GetAssetsInPack
    variables: Variables = Field()


class GetAssetsInPackResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            assets: List[AssetModel] = Field()

        public: Public = Field()

    data: Data = Field()


class GetAssetListingsByIdRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()
        cacheId: str = Field()

    operationName: str = Field(default="GetAssetListingsById")
    query: str = graphql.assets.GetAssetListingsById
    variables: Variables = Field()


class GetAssetListingsByIdResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            asset: AssetModel = Field()

        public: Public = Field()

    data: Data = Field()


class GetAssetDetailByIdRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()
        cacheId: str = Field()

    operationName: str = Field(default="GetAssetDetailById")
    query: str = graphql.assets.GetAssetDetailById
    variables: Variables = Field()


class GetAssetDetailByIdResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            asset: AssetModel = Field()
            __typename: str = Field()

        public: Public = Field()

    data: Data = Field()

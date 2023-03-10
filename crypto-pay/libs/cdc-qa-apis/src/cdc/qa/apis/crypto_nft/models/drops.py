from pydantic import Field
from datetime import datetime
from typing import List, Union, Optional

from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import GqlRequest, GqlResponse, FrozenBaseModel
from .models import DropModel, AssetModel, DropModel


class GetDropsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        cacheId: str = Field()
        dropStatuses: Optional[list] = Field()
        withDropStatusField: bool = Field()
        first: Optional[int] = Field()
        skip: Optional[int] = Field()

        class EndAt(FrozenBaseModel):
            lte: Optional[Union[str, datetime]] = Field()
            gt: Optional[Union[str, datetime]] = Field()

        class SortBy(FrozenBaseModel):
            field: Optional[str] = Field()
            order: Optional[str] = Field()

        endAt: EndAt = Field()
        sort: List[dict] = Field()

    operationName: str = Field(default="GetDrops")
    query: str = graphql.drops.GetDrops
    variables: Variables = Field()


class GetDropsResponse(GqlResponse):
    class GetDropsData(FrozenBaseModel):
        class Public(FrozenBaseModel):
            __typename: str = Field()

            drops: List[DropModel] = Field()

        public: Public = Field()

    data: GetDropsData = Field()


class GetDropRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field(description="drop id")
        cacheId: str = Field(description="cache id: select-drop-{drop id}-en")

    operationName: str = Field(default="Drop")
    query: str = graphql.drops.GetDrop
    variables: Variables = Field()


class GetDropResponse(GqlResponse):
    class GetDropData(FrozenBaseModel):
        class Public(FrozenBaseModel):
            drop: DropModel = Field()

        public: Public = Field()

    data: GetDropData = Field()


class GetDropAssetsQueryRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field(description="drop id")
        cacheId: str = Field(description="cache id: getDropAsset-{drop id}")

    operationName: str = Field(default="GetDropAssetsQuery")
    query: str = graphql.drops.GetDropAssetsQuery
    variables: Variables = Field()


class GetDropAssetsQueryResponse(GqlResponse):
    class GetDropAssetsQueryData(FrozenBaseModel):
        class Public(FrozenBaseModel):
            assets: List[Optional[AssetModel]]

        public: Public = Field()

    data: GetDropAssetsQueryData = Field()

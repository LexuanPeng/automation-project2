from pydantic import Field
from typing import List

from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import GqlRequest, GqlResponse, FrozenBaseModel
from .models import CollectionModel


class GetCollectionsPageRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        first: int = Field(default=100)
        skip: int = Field(default=0)
        isSortFieldZeroLast: bool = Field(default=True)
        timeRange: list = Field(default="ONE_DAY")
        verifiedOnly: bool = Field(default=True)
        hideEmpty: bool = Field(default=True)
        withStats: bool = Field(default=True)
        cacheId: str = Field(
            default="getCollectionsPageQuery-ab5171fc8a7511e2b72d3877a5de7605e3ecad28",
            description="getCollectionsPageQuery-{id}",
        )

        class Sort(FrozenBaseModel):
            order: str = Field()
            field: str = Field()

        sort: Sort = Field()

    operationName: str = Field(default="GetCollectionsPage")
    query: str = graphql.collections.GetCollectionsPage
    variables: Variables = Field()


class GetCollectionsPageResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            collections: List[CollectionModel] = Field()

        public: Public = Field()

    data: Data = Field()

from typing import List, Union

from pydantic import Field
from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import GqlRequest, FrozenBaseModel, GqlResponse
from cdc.qa.apis.crypto_nft.models.models import CollectionModel, PriceAlertModel, AssetModel


class CreatePriceAlertRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        input: dict = Field()

    operationName: str = Field(default="createPriceAlert")
    query: str = graphql.user_behavior.createPriceAlert
    variables: Variables = Field()


class CreatePriceAlertResponse(GqlResponse):
    class CreatePriceAlertData(FrozenBaseModel):
        createPriceAlert: PriceAlertModel = Field()

    data: CreatePriceAlertData = Field()


class GetPriceAlertsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        target: str = Field()
        first: int = Field()
        skip: int = Field()

    operationName: str = Field(default="getPriceAlerts")
    query: str = graphql.user_behavior.getPriceAlerts
    variables: Variables = Field()


class GetPriceAlertsResponse(GqlResponse):
    class GetPriceAlertsData(FrozenBaseModel):
        class PriceAlerts(FrozenBaseModel):
            asset: Union[AssetModel, None] = Field()
            collection: Union[CollectionModel, None] = Field()
            enabled: bool = Field()
            frequency: str = Field()
            id: str = Field()
            price: str = Field()
            target: str = Field()
            type: str = Field()
            __typename: str = Field()

        priceAlerts: List[PriceAlerts] = Field()
        priceAlertCount: int = Field()

    data: GetPriceAlertsData = Field()


class GetPriceAlertCountsRequest(GqlRequest):
    operationName: str = Field(default="getPriceAlertCounts")
    query: str = graphql.user_behavior.getPriceAlertCounts


class GetPriceAlertCountsResponse(GqlResponse):
    class GetPriceAlertCountsData(FrozenBaseModel):
        collectionAlerts: int = Field()
        collectibleAlerts: int = Field()

    data: GetPriceAlertCountsData = Field()


class DeletePriceAlertRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        class Input(FrozenBaseModel):
            id: str = Field()

        input: Input = Field()

    operationName: str = Field(default="deletePriceAlert")
    query: str = graphql.user_behavior.deletePriceAlert
    variables: Variables = Field()


class DeletePriceAlertResponse(GqlResponse):
    class DeletePriceAlertData(FrozenBaseModel):
        deletePriceAlert: PriceAlertModel = Field()

    data: DeletePriceAlertData = Field()

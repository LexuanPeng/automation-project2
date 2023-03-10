from typing import List, Union

from pydantic import Field
from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import GqlRequest, FrozenBaseModel, GqlResponse
from .models import IdUrlModel, URLModel


class GetCollectionsByCreatorRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        creatorId: str = Field()
        first: int = Field()

    operationName: str = Field(default="getCollectionsByCreator")
    query: str = graphql.create_nft.getCollectionsByCreator
    variables: Variables = Field()


class GetCollectionsByCreatorResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            class Collections(FrozenBaseModel):
                class Creator(FrozenBaseModel):
                    id: str = Field()
                    __typename: str = Field()

                id: str = Field()
                creator: Creator = Field()
                name: str = Field()
                description: Union[str, None] = Field()
                logo: IdUrlModel = Field()
                banner: IdUrlModel = Field()
                blocked: bool = Field()
                categories: list = Field()
                verified: bool = Field()
                __typename: str = Field()

            collections: List[Collections] = Field()

        public: Public = Field()

    data: Data = Field()


class GetCreatorWeeklyCreateStatusRequest(GqlRequest):
    operationName: str = Field(default="GetCreatorWeeklyCreateStatus")
    query: str = graphql.create_nft.GetCreatorWeeklyCreateStatus


class GetCreatorWeeklyCreateStatusResponse(GqlResponse):
    class GetCreatorWeeklyCreateStatusData(FrozenBaseModel):
        class CreatorWeeklyCreateStatus(FrozenBaseModel):
            hasReachedWeeklyLimit: bool = Field()
            __typename: str = Field()

        creatorWeeklyCreateStatus: CreatorWeeklyCreateStatus = Field()

    data: GetCreatorWeeklyCreateStatusData = Field()


class GetAttachmentRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()

    operationName: str = Field(default="GetAttachment")
    query: str = graphql.create_nft.GetAttachment
    variables: Variables = Field()


class GetAttachmentResponse(GqlResponse):
    class GetAttachmentData(FrozenBaseModel):
        class Attachment(FrozenBaseModel):
            class ContentModeration(FrozenBaseModel):
                status: str = Field()
                expiredAt: str = Field()
                __typename: str = Field()

            id: str = Field()
            url: str = Field()
            coverUrl: Union[str, None] = Field()
            contentModeration: ContentModeration = Field()
            __typename: str = Field()

        attachment: Attachment = Field()

    data: GetAttachmentData = Field()


class CreateAssetRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        description: str = Field()
        mainId: str = Field()
        name: str = Field()
        categories: list = Field()
        attributes: list = Field()
        collectionId: str = Field()
        copies: int = Field()
        network: str = Field()

    operationName: str = Field(default="CreateAsset")
    query: str = graphql.create_nft.CreateAsset
    variables: Variables = Field()


class CreateAssetResponse(GqlResponse):
    class CreateAssetData(FrozenBaseModel):
        class CreateAsset(FrozenBaseModel):
            uuid: str = Field()
            __typename: str = Field()

        createAsset: CreateAsset = Field()

    data: CreateAssetData = Field()


class CheckoutAssetRecordRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        assetCreateRecordId: str = Field()
        kind: str = Field()

    operationName: str = Field(default="checkoutAssetRecord")
    query: str = graphql.create_nft.checkoutAssetRecord
    variables: Variables = Field()


class CheckoutAssetRecordResponse(GqlResponse):
    class CheckoutAssetRecordData(FrozenBaseModel):
        class CreateCheckout(FrozenBaseModel):
            id: str = Field()
            asset: Union[str, None] = Field()
            amountDecimal: str = Field()
            __typename: str = Field()

        createCheckout: CreateCheckout = Field()

    data: CheckoutAssetRecordData = Field()


class GetCreatorApplicationStatusRequest(GqlRequest):
    operationName: str = Field(default="GetCreatorApplicationStatus")
    query: str = graphql.create_nft.GetCreatorApplicationStatus


class GetCreatorApplicationStatusResponse(GqlResponse):
    class GetCreatorApplicationStatusData(FrozenBaseModel):
        class CreatorApplicationStatus(FrozenBaseModel):
            status: str = Field()
            statusUpdatedAt: Union[str, None] = Field()
            __typename: str = Field()

        creatorApplicationStatus: CreatorApplicationStatus = Field()

    data: GetCreatorApplicationStatusData = Field()


class MintHistoryRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        first: int = Field()
        skip: int = Field()

    operationName: str = Field(default="mintHistory")
    query: str = graphql.create_nft.mintHistory
    variables: Variables = Field()


class MintHistoryResponse(GqlResponse):
    class MintHistoryData(FrozenBaseModel):
        class MintHistory(FrozenBaseModel):
            id: str = Field()
            name: str = Field()
            copies: int = Field()
            cover: URLModel = Field()
            createdAt: str = Field()
            network: str = Field()
            walletAddress: str = Field()
            checkoutId: Union[str, None] = Field()
            gateway: Union[str, None] = Field()
            mintFee: Union[str, None] = Field()
            __typename: str = Field()

        mintHistory: List[MintHistory] = Field()
        countMintHistory: int = Field()

    data: MintHistoryData = Field()


class GetCrossChainMintFeeQuoteRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        assetCreateRecordId: str = Field()

    operationName: str = Field(default="getCrossChainMintFeeQuote")
    query: str = graphql.create_nft.getCrossChainMintFeeQuote
    variables: Variables = Field()


class GetCrossChainMintFeeQuoteResponse(GqlResponse):
    class GetCrossChainMintFeeQuoteData(FrozenBaseModel):
        class CrossChainMintFeeQuote(FrozenBaseModel):
            mintFeeUSD: str = Field()
            assetCreateRecordId: str = Field()
            createdAt: str = Field()
            expiredAt: str = Field()
            validMs: int = Field()
            __typename: str = Field()

        crossChainMintFeeQuote: CrossChainMintFeeQuote = Field()

    data: GetCrossChainMintFeeQuoteData = Field()

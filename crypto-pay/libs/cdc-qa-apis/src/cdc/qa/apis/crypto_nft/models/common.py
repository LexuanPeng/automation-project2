from typing import List, Optional, Union

from pydantic import Field
from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import GqlRequest, FrozenBaseModel, GqlResponse
from .models import (
    CreditCardModel,
    PaidCheckoutModel,
    CategoryModel,
    MeModel,
    CollectionModel,
    BidModel,
    UuidModel,
    AssetModel,
)


class GetBrandsRequest(GqlRequest):
    operationName: str = Field(default="GetBrands")
    query: str = graphql.common.GetBrands


class GetBrandsResponse(GqlResponse):
    class GetBrandsData(FrozenBaseModel):
        class Public(FrozenBaseModel):
            class Brands(FrozenBaseModel):
                id: str = Field()
                username: str = Field()
                name: str = Field()
                __typename: str = Field()

            brands: List[Brands] = Field()

        public: Public = Field()

    data: GetBrandsData = Field()


class GetPlatformFeeRequest(GqlRequest):
    operationName: str = Field(default="GetPlatformFee")
    query: str = graphql.common.getPlatformFee


class GetPlatformFeeResponse(GqlResponse):
    class GetPlatformFeeData(FrozenBaseModel):
        class PlatformFee(FrozenBaseModel):
            isEnabled: bool = Field()
            minFee: str = Field()
            __typename: str = Field()

        platformFee: PlatformFee = Field()

    data: GetPlatformFeeData = Field()


class CreateCheckoutRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        listingId: Optional[str] = Field()
        offerId: Optional[str] = Field()
        kind: str = Field()
        quantity: Optional[int] = Field(default=1)

    operationName: str = Field(default="CreateCheckout")
    query: str = graphql.common.CreateCheckout
    variables: Variables = Field()


class CreateCheckoutResponse(GqlResponse):
    class CreateCheckoutData(FrozenBaseModel):
        class CreateCheckout(FrozenBaseModel):
            id: str = Field()
            __typename: str = Field()

        createCheckout: CreateCheckout = Field()

    data: CreateCheckoutData = Field()


class CreateAndCaptureAccountPaymentRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        checkoutId: str = Field()

    operationName: str = Field(default="CreateAndCaptureAccountPayment")
    query: str = graphql.common.CreateAndCaptureAccountPayment
    variables: Variables = Field()


class CreateAndCaptureAccountPaymentResponse(GqlResponse):
    class CreateAndCaptureAccountPaymentData(FrozenBaseModel):
        class CreateAndCaptureAccountPayment(FrozenBaseModel):
            id: str = Field()
            status: str = Field()
            __typename: str = Field()

        createAndCaptureAccountPayment: CreateAndCaptureAccountPayment = Field()

    data: CreateAndCaptureAccountPaymentData = Field()


class CheckoutRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()

    operationName: str = Field(default="Checkout")
    query: str = graphql.common.Checkout
    variables: Variables = Field()


class CheckoutResponse(GqlResponse):
    class CheckoutData(FrozenBaseModel):
        class Checkout(FrozenBaseModel):
            class Asset(FrozenBaseModel):
                class Cover(FrozenBaseModel):
                    url: str = Field()
                    __typename: str = Field()

                class Collection(FrozenBaseModel):
                    name: str = Field()
                    __typename: str = Field()

                id: str = Field()
                name: str = Field()
                copies: int = Field()
                cover: Cover = Field()
                collectiblePerPack: Union[str, None] = Field()
                kind: str = Field()
                isExternalNft: bool = Field()
                collection: Union[Collection, None] = Field()
                __typename: str = Field()

            class Edition(FrozenBaseModel):
                id: str = Field()
                index: int = Field()
                __typename: str = Field()

            class Listing(FrozenBaseModel):
                id: str = Field()
                mode: str = Field()
                primary: bool = Field()
                source: str = Field()
                __typename: str = Field()

            class Seller(FrozenBaseModel):
                username: str = Field()
                isCreator: bool = Field()
                uuid: str = Field()
                displayName: Union[str, None] = Field()
                __typename: str = Field()

            class AssetCreateRecord(FrozenBaseModel):
                class Main(FrozenBaseModel):
                    coverUrl: str = Field()
                    __typename: str = Field()

                class Collection(FrozenBaseModel):
                    name: str = Field()
                    id: str = Field()
                    __typename: str = Field()

                id: str = Field()
                name: str = Field()
                copies: int = Field()
                main: Main = Field()
                collection: Collection = Field()
                network: str = Field()
                __typename: str = Field()

            id: str = Field()
            amountDecimal: str = Field()
            currency: str = Field()
            asset: Union[Asset, None] = Field()
            edition: Union[Edition, None] = Field()
            listing: Union[Listing, None] = Field()
            cartQuantity: int = Field()
            listingMode: str = Field()
            paidAt: Optional[Union[str, None]] = Field()
            seller: Union[Seller, None] = Field()
            kind: str = Field()
            assetCreateRecord: Union[AssetCreateRecord, None] = Field()
            __typename: str = Field()

        checkout: Checkout = Field()

    data: CheckoutData = Field()


class GetCroMintFeeRequest(GqlRequest):
    operationName: str = Field(default="GetCroMintFee")
    query: str = graphql.common.GetCroMintFee


class GetCroMintFeeResponse(GqlResponse):
    class GetCroMintFeeData(FrozenBaseModel):
        class Me(FrozenBaseModel):
            class CreatorConfig(FrozenBaseModel):
                canMintFree: bool = Field()
                hasMinted: bool = Field()
                __typename: str = Field()

            class CroMintFeeConfig(FrozenBaseModel):
                isEnabled: bool = Field()
                fee: str = Field()
                defaultFee: str = Field()
                __typename: str = Field()

            creatorConfig: CreatorConfig = Field()
            croMintFeeConfig: CroMintFeeConfig = Field()
            __typename: str = Field()

        me: Me = Field()

    data: GetCroMintFeeData = Field()


class GetUserCardTierRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()

    operationName: str = Field(default="getUserCardTier")
    query: str = graphql.common.getUserCardTier
    variables: Variables = Field()


class GetUserCardTierResponse(GqlResponse):
    class GetUserCardTierData(FrozenBaseModel):
        class GetUserCardTier(FrozenBaseModel):
            status: str = Field()
            cardName: str = Field()
            __typename: str = Field()

        getUserCardTier: GetUserCardTier = Field()

    data: GetUserCardTierData = Field()


class GetMeRequest(GqlRequest):
    operationName: str = Field(default="getMe")
    query: str = graphql.common.getMe


class GetMeResponse(GqlResponse):
    class GetMeData(FrozenBaseModel):
        me: MeModel = Field()

    data: GetMeData = Field()


class GetUserCardStakeRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()

    operationName: str = Field(default="getUserCardStake")
    query: str = graphql.common.getUserCardStake
    variables: Variables = Field()


class GetUserCardStakeResponse(GqlResponse):
    class GetUserCardStakeData(FrozenBaseModel):
        class GetUserCardStake(FrozenBaseModel):
            stakingType: str = Field()
            planId: str = Field()
            __typename: str = Field()

        getUserCardStake: GetUserCardStake = Field()

    data: GetUserCardStakeData = Field()


class GetCreditCardsRequest(GqlRequest):
    operationName: str = Field(default="getCreditCards")
    query: str = graphql.common.getCreditCards


class GetCreditCardsResponse(GqlResponse):
    class Data(FrozenBaseModel):
        creditCards: List[CreditCardModel] = Field()

    data: Data = Field()


class CreateIXOPaymentRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        cardFirstSixDigits: str = Field()
        cardLastFourDigits: str = Field()
        checkoutId: str = Field()

    operationName: str = Field(default="createIXOPayment")
    query: str = graphql.common.createIXOPayment
    variables: Variables = Field()


class CreateIXOPaymentResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class CreateIXOPayment(FrozenBaseModel):
            id: str = Field()
            __typename: str = Field()

        createIXOPayment: CreateIXOPayment = Field()

    data: Data = Field()


class PreauthIXOPaymentRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        withRegister: bool = Field()
        checkoutId: str = Field()
        paymentId: str = Field()
        transactionToken: str = Field()

    operationName: str = Field(default="preauthIXOPayment")
    query: str = graphql.common.preauthIXOPayment
    variables: Variables = Field()


class PreauthIXOPaymentResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class PreauthIXOPayment(FrozenBaseModel):
            preauthRedirectUrl: str = Field()
            preauthReturnType: str = Field()
            status: str = Field()
            __typename: str = Field()

        preauthIXOPayment: PreauthIXOPayment = Field()

    data: Data = Field()


class CaptureIXOPaymentRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        checkoutId: str = Field()
        paymentId: str = Field()

    operationName: str = Field(default="captureIXOPayment")
    query: str = graphql.common.captureIXOPayment
    variables: Variables = Field()


class CaptureIXOPaymentResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class CaptureIXOPayment(FrozenBaseModel):
            preauthRedirectUrl: str = Field()
            status: str = Field()
            __typename: str = Field()

            class Checkout(FrozenBaseModel):
                listingMode: str = Field()
                __typename: str = Field()

                class Listing(FrozenBaseModel):
                    source: str = Field()
                    __typename: str = Field()

                listing: Listing = Field()

            checkout: Checkout = Field()

        captureIXOPayment: CaptureIXOPayment = Field()

    data: Data = Field()


class PaidCheckoutsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        first: int = Field()
        skip: int = Field()

    operationName: str = Field(default="paidCheckouts")
    query: str = graphql.common.paidCheckouts
    variables: Variables = Field()


class PaidCheckoutsResponse(GqlResponse):
    class Data(FrozenBaseModel):
        paidCheckouts: List[PaidCheckoutModel] = Field()
        countPaidCheckouts: int = Field()

    data: Data = Field()


class GetCategoriesRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        first: Optional[int] = Field()
        skip: Optional[int] = Field()

    operationName: str = Field(default="getCategories")
    query: str = graphql.common.getCategories
    variables: Variables = Field()


class GetCategoriesResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            categories: List[CategoryModel] = Field()
            __typename: str = Field()

        public: Public = Field()

    data: Data = Field()


class CreateAttachmentResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class CreateAttachment(FrozenBaseModel):
            id: str = Field()
            url: str = Field()
            coverUrl: Union[str, None] = Field()
            __typename: str = Field()

        createAttachment: CreateAttachment = Field()

    data: Data = Field()


class PlaceBidMutationRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        listingId: str = Field()
        bidPriceDecimal: str = Field()

    operationName: str = Field(default="PlaceBidMutation")
    query: str = graphql.common.PlaceBidMutation
    variables: Variables = Field()


class PlaceBidMutationResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class CreateCheckout(FrozenBaseModel):
            id: str = Field()
            bidPriceDecimal: str = Field()
            __typename: str = Field()

        createCheckout: CreateCheckout = Field()

    data: Data = Field()


class GetCollectionRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        collectionId: str = Field()

    operationName: str = Field(default="GetCollection")
    query: str = graphql.common.GetCollection
    variables: Variables = Field()


class GetCollectionResponse(GqlResponse):
    class GetCollectionData(FrozenBaseModel):
        class Public(FrozenBaseModel):
            collection: CollectionModel = Field()
            __typename: str = Field()

        public: Public = Field()

    data: GetCollectionData = Field()


class GetBiddingHistoryRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        listingId: str = Field()

    operationName: str = Field(default="getBiddingHistory")
    query: str = graphql.common.getBiddingHistory
    variables: Variables = Field()


class GetBiddingHistoryResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            bids: Optional[List[BidModel]] = Field()

        public: Public = Field()

    data: Data = Field()


class DeleteCreditCardRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        cardId: str = Field()

    operationName: str = Field(default="deleteCreditCard")
    query: str = graphql.common.deleteCreditCard
    variables: Variables = Field()


class DeleteCreditCardResponse(GqlResponse):
    class Data(FrozenBaseModel):
        deleteCreditCard: UuidModel = Field()

    data: Data = Field()


class GetTopCollectiblesRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        topCollectiblesFilter: str = Field()
        topCollectiblesFilterBy: str = Field()
        cacheId: str = Field()
        page: int = Field()
        pageSize: int = Field()

    operationName: str = Field(default="getTopCollectibles")
    variables: Variables = Field()
    query: str = graphql.common.GetTopCollectibles


class GetTopCollectiblesResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            topCollectibles: List[AssetModel] = Field()

        public: Public = Field()

    data: Data = Field()


class CheckoutAmountRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()

    operationName = Field(default="CheckoutAmount")
    query: str = graphql.common.CheckoutAmount
    variables: Variables = Field()


class CheckoutAmountResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class CheckoutAmount(FrozenBaseModel):
            amountDecimal: str = Field()
            __typename: str = Field()

        checkout: CheckoutAmount = Field()

    data: Data = Field()

from typing import List, Union

from pydantic import Field
from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import GqlRequest, FrozenBaseModel, GqlResponse


class CreateOfferRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        editionId: str = Field()
        amountDecimal: str = Field()

    operationName: str = Field(default="createOffer")
    query: str = graphql.offers.createOffer
    variables: Variables = Field()


class CreateOfferResponse(GqlResponse):
    class CreateOfferData(FrozenBaseModel):
        class CreateOffer(FrozenBaseModel):
            id: str = Field()
            __typename: str = Field()

        createOffer: CreateOffer = Field()

    data: CreateOfferData = Field()


class GetOfferRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        offerId: str = Field()

    operationName: str = Field(default="getOffer")
    query: str = graphql.offers.getOffer
    variables: Variables = Field()


class GetOfferResponse(GqlResponse):
    class GetOfferData(FrozenBaseModel):
        class Offer(FrozenBaseModel):
            class Asset(FrozenBaseModel):
                class Cover(FrozenBaseModel):
                    url: str = Field()
                    __typename: str = Field()

                class Main(FrozenBaseModel):
                    url: str = Field()
                    __typename: str = Field()

                id: str = Field()
                blocked: bool = Field()
                name: str = Field()
                copies: int = Field()
                cover: Cover = Field()
                main: Main = Field()
                kind: str = Field()
                royaltiesRateDecimal: str = Field()
                isCurated: bool = Field()
                copiesInCirculation: int = Field()
                isExternalNft: bool = Field()
                __typename: str = Field()

            class User(FrozenBaseModel):
                uuid: str = Field()
                id: str = Field()
                username: str = Field()
                displayName: str = Field()
                isCreator: bool = Field()
                avatar: str = Field()
                isCreationWithdrawalBlocked: bool = Field()
                creationWithdrawalBlockExpiredAt: str = Field()
                verified: bool = Field()
                __typename: str = Field()

            class ToUser(FrozenBaseModel):
                uuid: str = Field()
                id: str = Field()
                username: str = Field()
                displayName: str = Field()
                isCreator: bool = Field()
                avatar: str = Field()
                isCreationWithdrawalBlocked: bool = Field()
                creationWithdrawalBlockExpiredAt: str = Field()
                verified: bool = Field()
                __typename: str = Field()

            class Edition(FrozenBaseModel):
                id: str = Field()
                index: int = Field()
                __typename: str = Field()

            id: str = Field()
            amountDecimal: str = Field()
            createdAt: str = Field()
            asset: Asset = Field()
            user: User = Field()
            toUser: ToUser = Field()
            edition: Edition = Field()
            status: str = Field()
            minServiceFeeDecimal: str = Field()
            __typename: str = Field()

        offer: Offer = Field()

    data: GetOfferData = Field()


class GetOffersMadeRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        first: int = Field()
        skip: int = Field()

    operationName: str = Field(default="getOffersMade")
    query: str = graphql.offers.getOffersMade
    variables: Variables = Field()


class GetOffersMadeResponse(GqlResponse):
    class GetOffersMadeData(FrozenBaseModel):
        class OffersMade(FrozenBaseModel):
            class Asset(FrozenBaseModel):
                class Cover(FrozenBaseModel):
                    url: str = Field()
                    __typename: str = Field()

                id: str = Field()
                name: str = Field()
                copies: int = Field()
                cover: Cover = Field()
                kind: str = Field()
                copiesInCirculation: int = Field()
                isExternalNft: bool = Field()
                __typename: str = Field()

            class Edition(FrozenBaseModel):
                id: str = Field()
                index: int = Field()
                acceptedOffer: Union[str, None] = Field()
                __typename: str = Field()

            class User(FrozenBaseModel):
                uuid: str = Field()
                id: str = Field()
                username: str = Field()
                displayName: Union[str, None] = Field()
                isCreator: bool = Field()
                avatar: Union[str, None] = Field()
                isCreationWithdrawalBlocked: bool = Field()
                creationWithdrawalBlockExpiredAt: Union[str, None] = Field()
                verified: bool = Field()
                __typename: str = Field()

            class ToUser(FrozenBaseModel):
                uuid: str = Field()
                id: str = Field()
                username: str = Field()
                displayName: Union[str, None] = Field()
                isCreator: bool = Field()
                avatar: Union[str, None] = Field()
                isCreationWithdrawalBlocked: bool = Field()
                creationWithdrawalBlockExpiredAt: Union[str, None] = Field()
                verified: bool = Field()
                __typename: str = Field()

            id: str = Field()
            amountDecimal: str = Field()
            createdAt: str = Field()
            asset: Asset = Field()
            edition: Edition = Field()
            user: User = Field()
            toUser: ToUser = Field()
            status: str = Field()
            __typename: str = Field()

        offersMade: List[OffersMade] = Field()
        countOffersMade: int = Field()

    data: GetOffersMadeData = Field()


class GetOffersRecievedRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        first: int = Field()
        skip: int = Field()

    operationName: str = Field(default="getOffersRecieved")
    query: str = graphql.offers.getOffersRecieved
    variables: Variables = Field()


class GetOffersRecievedResponse(GqlResponse):
    class GetOffersRecievedData(FrozenBaseModel):
        class OffersRecieved(FrozenBaseModel):
            class Asset(FrozenBaseModel):
                class Cover(FrozenBaseModel):
                    url: str = Field()
                    __typename: str = Field()

                id: str = Field()
                name: str = Field()
                copies: int = Field()
                cover: Cover = Field()
                kind: str = Field()
                copiesInCirculation: int = Field()
                isExternalNft: bool = Field()
                __typename: str = Field()

            class Edition(FrozenBaseModel):
                id: str = Field()
                index: int = Field()
                acceptedOffer: Union[str, None] = Field()
                __typename: str = Field()

            class User(FrozenBaseModel):
                uuid: str = Field()
                id: str = Field()
                username: str = Field()
                displayName: Union[str, None] = Field()
                isCreator: bool = Field()
                avatar: Union[str, None] = Field()
                isCreationWithdrawalBlocked: bool = Field()
                creationWithdrawalBlockExpiredAt: Union[str, None] = Field()
                verified: bool = Field()
                __typename: str = Field()

            class ToUser(FrozenBaseModel):
                uuid: str = Field()
                id: str = Field()
                username: str = Field()
                displayName: Union[str, None] = Field()
                isCreator: bool = Field()
                avatar: Union[str, None] = Field()
                isCreationWithdrawalBlocked: bool = Field()
                creationWithdrawalBlockExpiredAt: Union[str, None] = Field()
                verified: bool = Field()
                __typename: str = Field()

            id: str = Field()
            amountDecimal: str = Field()
            createdAt: str = Field()
            asset: Asset = Field()
            edition: Edition = Field()
            user: User = Field()
            toUser: ToUser = Field()
            status: str = Field()
            __typename: str = Field()

        offersRecieved: List[OffersRecieved] = Field()
        countOffersReceived: int = Field()

    data: GetOffersRecievedData = Field()


class AcceptOfferRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()

    operationName: str = Field(default="acceptOffer")
    query: str = graphql.offers.acceptOffer
    variables: Variables = Field()


class AcceptOfferResponse(GqlResponse):
    class AcceptOfferData(FrozenBaseModel):
        class AcceptOffer(FrozenBaseModel):
            id: str = Field()
            __typename: str = Field()

        acceptOffer: AcceptOffer = Field()

    data: AcceptOfferData = Field()


class GetMyWalletsRequest(GqlRequest):
    operationName: str = Field(default="getMyWallets")
    query: str = graphql.offers.getMyWallets


class GetMyWalletsResponse(GqlResponse):
    class GetMyWalletsData(FrozenBaseModel):
        class Wallets(FrozenBaseModel):
            network: str = Field()
            address: str = Field()
            status: str = Field()
            __typename: str = Field()

        wallets: List[Wallets] = Field()

    data: GetMyWalletsData = Field()


class AccountBalanceQueryRequest(GqlRequest):
    operationName: str = Field(default="accountBalanceQuery")
    query: str = graphql.offers.accountBalanceQuery


class AccountBalanceQueryResponse(GqlResponse):
    class AccountBalanceQueryData(FrozenBaseModel):
        class AccountBalance(FrozenBaseModel):
            amountDecimal: str = Field()
            currency: str = Field()
            __typename: str = Field()

        accountBalance: AccountBalance = Field()

    data: AccountBalanceQueryData = Field()


class RejectOfferRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()

    operationName: str = Field(default="rejectOffer")
    query: str = graphql.offers.rejectOffer
    variables: Variables = Field()


class RejectOfferResponse(GqlResponse):
    class RejectOfferData(FrozenBaseModel):
        class RejectOffer(FrozenBaseModel):
            id: str = Field()
            __typename: str = Field()

        rejectOffer: RejectOffer = Field()

    data: RejectOfferData = Field()

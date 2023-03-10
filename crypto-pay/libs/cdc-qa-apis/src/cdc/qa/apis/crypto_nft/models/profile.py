from typing import Optional, List

from pydantic import Field

from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import GqlRequest, GqlResponse, FrozenBaseModel
from .models import (
    DropModel,
    DatetimeAtModel,
    UserModel,
    UserMetricsModel,
    ProfileCollectionsModel,
    CreationModel,
    CreatedCollectionModel,
    UnauthorizedMeV2Model,
    MeModel,
    PackModel,
    EditionModel,
    OpenPackModel,
    AssetModel,
    IdModel,
    IdUrlModel,
)


class GetProfileAssetsTotalRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        userId: str = Field(description="user id")
        cacheId: str = Field(description="cache ID")

    operationName: str = Field(default="GetProfileAssetsTotal")
    query: str = graphql.profile.GetProfileAssetsTotal
    variables: Variables = Field()


class GetProfileAssetsTotalResoponse(GqlResponse):
    class GetProfileAssetsTotalData(FrozenBaseModel):
        class Public(FrozenBaseModel):
            collectedEditionsTotal: int = Field(description="collected editions total")
            profileCreatedAssetsTotal: int = Field(description="profile created assets total")
            profileLikedAssetsTotal: int = Field(description="profile liked total")
            __typename: str = Field()

        public: Public = Field()

    data: GetProfileAssetsTotalData = Field()


class GetUserPrivateAssetsTotalRequest(GqlRequest):
    operationName: str = Field(default="GetUserPrivateAssetsTotal")
    query: str = graphql.profile.GetUserPrivateAssetsTotal


class GerUserPrivateAssetsTotalResoponse(GqlResponse):
    class GetUserPrivateAssetsTotalData(FrozenBaseModel):
        collectedEditionsTotal: int = Field(description="collected number")
        createdAssetsTotal: int = Field(description="created number")

    data: GetUserPrivateAssetsTotalData = Field()


class GetProfileCollectionsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        search: Optional[str] = Field(description="search")
        first: Optional[int] = Field(description="first page size")
        skip: Optional[int] = Field()
        collectionIds: Optional[List[str]] = Field()
        isSortFieldZeroLast: Optional[bool] = Field()
        verifiedOnly: Optional[bool] = Field()
        verifiedFirst: Optional[bool] = Field()
        creatorId: str = Field()
        assetOwnerId: Optional[str] = Field()
        assetCreatorId: Optional[str] = Field()
        assetLikedById: Optional[str] = Field()
        sort: Optional[dict] = Field()

    operationName: str = Field(default="GetProfileCollections")
    query: str = graphql.profile.GetProfileCollections
    variables: Variables = Field()


class GetProfileCollectionsResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            profileCollections: Optional[List[ProfileCollectionsModel]] = Field()

        public: Public = Field()

    data: Data = Field()


class LiveAndIncomingDropsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        dropStatuses: list = Field()
        endAt: DatetimeAtModel = Field()

    operationName: str = Field(default="LiveAndIncomingDrops")
    query: str = graphql.profile.LiveAndIncomingDrops
    variables: Variables = Field()


class LiveAndIncomingDropsResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            drops: Optional[List[DropModel]] = Field()

        public: Public = Field()

    data: Data = Field()


class UserMetricsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()

    operationName: str = Field(default="UserMetrics")
    query: str = graphql.profile.UserMetrics
    variables: Variables = Field()


class UserMetricsResponse(GqlResponse):
    class Data(FrozenBaseModel):
        userMetrics: UserMetricsModel = Field()

    data: Data = Field()


class UserRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field(description="user id")
        cacheId: str = Field(description="cache id")

    operationName: str = Field(default="User")
    query: str = graphql.profile.User
    variables: Variables = Field()


class UserResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            user: UserModel = Field()

        public: Public = Field()

    data: Data = Field()


class GetMyMetricsRequest(GqlRequest):
    operationName: str = Field(default="getMyMetrics")
    query: str = graphql.profile.getMyMetrics


class GetMyMetricsResponse(GqlResponse):
    class Data(FrozenBaseModel):
        myMetrics: UserMetricsModel = Field()

    data: Data = Field()


class GetUserCreatedAssetsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        first: int = Field()
        skip: int = Field(default=0)
        kinds: Optional[List] = Field()
        listingTypes: Optional[List] = Field()
        collections: Optional[List] = Field()
        curation: Optional[List] = Field()
        categories: Optional[List] = Field()
        sort: Optional[List] = Field()
        dropId: Optional[str] = Field()

    operationName: str = Field(default="getUserCreatedAssets")
    query: str = graphql.profile.getUserCreatedAssets
    variables: Variables = Field()


class GetUserCreatedAssetsResponse(GqlResponse):
    class Data(FrozenBaseModel):
        creations: List[CreationModel] = Field()

    data: Data = Field()


class GetUserCreatedCollectionsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        search: str = Field()
        first: int = Field()
        withStats: bool = Field()
        isSortFieldZeroLast: bool = Field()
        verifiedOnly: bool = Field()
        verifiedFirst: bool = Field()
        assetCreatorId: str = Field()

        class SortModel(FrozenBaseModel):
            order: str = Field()
            field: str = Field()

        sort: SortModel = Field()

    operationName: str = Field(default="GetUserCreatedCollections")
    query: str = graphql.profile.GetUserCreatedCollections
    variables: Variables = Field()


class GetUserCreatedCollectionsResponse(GqlResponse):
    class Data(FrozenBaseModel):
        createdCollections: List[CreatedCollectionModel] = Field()

    data: Data = Field()


class CompleteProfileRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        name: str = Field()
        username: str = Field()

    operationName: str = Field(default="completeProfile")
    query: str = graphql.profile.completeProfile
    variables: Variables = Field()


class CompleteProfileResponse(GqlResponse):
    class Data(FrozenBaseModel):
        completeProfile: UnauthorizedMeV2Model = Field()

    data: Data = Field()


class UpdateProfileRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        bio: Optional[str] = Field()
        name: Optional[str] = Field()
        username: Optional[str] = Field()
        displayName: Optional[str] = Field()
        instagramUsername: Optional[str] = Field()
        facebookUsername: Optional[str] = Field()
        twitterUsername: Optional[str] = Field()
        coverId: Optional[str] = Field()
        avatarId: Optional[str] = Field()

    operationName: str = Field(default="UpdateProfile")
    query: str = graphql.profile.UpdateProfile
    variables: Variables = Field()


class UpdateProfileResponse(GqlResponse):
    class Data(FrozenBaseModel):
        updateProfile: MeModel = Field()

    data: Data = Field()


class GetUnopenedPacksRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        first: int = Field(default=20)
        skip: int = Field(default=0)

    operationName: str = Field(default="GetUnopenedPacks")
    query: str = graphql.profile.GetUnopenedPacks
    variables: Variables = Field()


class GetUnopenedPacksResponse(GqlResponse):
    class Data(FrozenBaseModel):
        packs: List[PackModel] = Field()

    data: Data = Field()


class GetPackRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        editionId: str = Field()
        ownerId: str = Field()
        cacheId: str = Field()

    operationName: str = Field(default="GetPack")
    query: str = graphql.profile.GetPack
    variables: Variables = Field()


class GetPackResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            edition: EditionModel = Field()

        public: Public = Field()
        __typename: str = Field()

    data: Data = Field()


class OpenPackRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        editionId: str = Field()

    operationName: str = Field(default="OpenPack")
    query: str = graphql.profile.OpenPack
    variables: Variables = Field()


class OpenPackResponse(GqlResponse):
    class Data(FrozenBaseModel):
        openPack: List[OpenPackModel] = Field()

    data: Data = Field()


class GetProfileAssetsRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        categories: List = Field()
        first: int = Field(default=36)
        skip: int = Field(default=0)
        cacheId: str = Field()
        sort: List = Field()
        listingTypes: List = Field()
        collections: List = Field()
        curation: List = Field()
        likedById: str = Field()

    operationName: str = Field(default="GetProfileAssets")
    query: str = graphql.profile.GetProfileAssets
    variables: Variables = Field()


class GetProfileAssetsResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class Public(FrozenBaseModel):
            profileAssets: List[AssetModel] = Field
            __typename: str = Field()

        public: Public = Field()

    data: Data = Field()


class UpdateCollectionRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        id: str = Field()
        categories: List = Field()
        name: str = Field()
        description: str = Field()

    operationName: str = Field(default="updateCollection")
    query = graphql.profile.updateCollection
    variables: Variables = Field()


class UpdateCollectionResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class UpdateCollection(FrozenBaseModel):
            id: str = Field()
            creator: IdModel = Field()
            name: str = Field()
            description: str = Field()
            logo: IdUrlModel = Field()
            banner: IdUrlModel = Field()
            blocked: bool = Field()
            categories: List = Field()

        updateCollection: UpdateCollection = Field()

    data: Data = Field()


class CreateCollectionRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        bannerId: str = Field()
        logoId: str = Field()
        categories: List = Field()
        name: str = Field()
        description: str = Field()

    operationName = Field(default="createCollection")
    variables: Variables = Field()
    query = graphql.profile.createCollection


class CreateCollectionResponse(GqlResponse):
    class Data(FrozenBaseModel):
        createCollection: CreatedCollectionModel = Field()

    data: Data = Field()

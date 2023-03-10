from datetime import datetime
from typing import Union, Optional

from pydantic import Field

from cdc.qa.apis.crypto_nft.models import FrozenBaseModel


class URLModel(FrozenBaseModel):
    url: str = Field(description="url")
    __typename: str = Field()


class IdModel(FrozenBaseModel):
    id: str = Field(description="id")
    __typename: str = Field()


class IdUrlModel(FrozenBaseModel):
    id: Optional[str] = Field(description="id")
    url: Optional[str] = Field(description="url")
    __typename: str = Field()


class MetricsModel(FrozenBaseModel):
    items: int = Field(description="items")
    minAuctionListingPriceDecimal: Optional[str] = Field()
    minSaleListingPriceDecimal: Optional[str] = Field()
    owners: Optional[int] = Field()
    totalSalesDecimal: Optional[str] = Field()
    statisticSource: Optional[Union[list, None]] = Field()
    totalSalesCount: Optional[int] = Field()
    __typename: str = Field()


class UuidModel(FrozenBaseModel):
    uuid: str = Field(description="uuid")
    __typename: str = Field()


class OwnerShipModel(FrozenBaseModel):
    primary: str = Field()

    __typename: str = Field()


class AcceptedOfferModel(FrozenBaseModel):
    id: str = Field()
    user: Optional[IdModel] = Field()


class OwnerModel(FrozenBaseModel):
    id: str = Field()
    uuid: str = Field()
    isCreator: bool = Field()
    username: Optional[str] = Field()
    displayName: Optional[str] = Field()
    avatar: Optional[URLModel] = Field()
    croWalletAddress: Optional[str] = Field()
    verified: Optional[bool] = Field()
    __typename: str = Field()


class ExternalNftMetadataModel(FrozenBaseModel):
    chainCollection: Optional[dict] = Field()
    chainCollectionId: Optional[str] = Field(description="chain chainCollectionId")
    creator: Optional[dict] = Field()
    creatorAddress: Optional[str] = Field()
    network: Optional[str] = Field()
    tokenId: Optional[str] = Field()


class ExternalUserModel(FrozenBaseModel):
    address: Optional[str] = Field()
    avatar: Optional[URLModel] = Field()
    username: Optional[str] = Field()


class SellerModel(FrozenBaseModel):
    id: Optional[str] = Field(description="seller ID")
    uuid: Optional[str] = Field(description="seller uuid")
    username: Optional[str] = Field()
    isCreator: Optional[bool] = Field()
    displayName: Optional[Union[str, None]]
    __typename: str = Field()


class PriceAlertModel(FrozenBaseModel):
    id: Optional[str] = Field(description="price alert ID")
    enabled: Optional[bool] = Field()
    frequency: Optional[str] = Field()
    price: Optional[str] = Field()
    target: Optional[str] = Field()
    type: Optional[str] = Field()
    __typename: str = Field()


class PrimaryListingModel(FrozenBaseModel):
    id: str = Field()
    price: Union[str, None] = Field()
    currency: str = Field()
    primary: bool = Field()
    auctionCloseAt: Union[str, None] = Field()
    auctionHasBids: bool = Field()
    auctionMinPriceDecimal: str = Field()
    expiredAt: Union[str, None] = Field()
    priceDecimal: str = Field()
    mode: str = Field()
    isCancellable: bool = Field()
    status: str = Field()
    source: str = Field()
    salePriceDecimalUSD: str = Field()
    externalUser: Union[ExternalUserModel, None] = Field()
    seller: SellerModel = Field()
    __typename: str = Field()


class ListingModel(FrozenBaseModel):
    id: Optional[str] = Field()
    editionId: Optional[str] = Field()
    mode: str = Field()
    primary: Optional[bool] = Field()
    source: Optional[str] = Field()
    price: Optional[Union[str, None]] = Field()
    currency: Optional[str] = Field()
    auctionCloseAt: Optional[Union[str, None]] = Field()
    auctionHasBids: Optional[bool] = Field()
    auctionMinPriceDecimal: Optional[str] = Field()
    expiredAt: Optional[Union[str, None]] = Field()
    priceDecimal: Optional[str] = Field()
    isCancellable: Optional[str] = Field()
    status: Optional[str] = Field()
    salePriceDecimalUSD: Optional[str] = Field()
    externalUser: Union[ExternalUserModel, None] = Field()
    seller: Union[UuidModel, None] = Field()
    __typename: str = Field()


class MeModel(FrozenBaseModel):
    uuid: Optional[str] = Field(description="user uuid")
    verified: Optional[bool] = Field(description="is verified")
    id: Optional[str] = Field(description="user id")
    bio: Optional[Union[str, None]] = Field(description="user bio")
    displayName: Optional[Union[str, None]] = Field(description="user display name")
    instagramUsername: Optional[Union[str, None]] = Field(description="user Instagram username")
    facebookUsername: Optional[Union[str, None]] = Field(description="user Facebook username")
    twitterUsername: Optional[Union[str, None]] = Field(description="user Twitter username")
    countryCode: Optional[Union[str, None]] = Field(description="country code")
    phoneNumber: Optional[Union[str, None]] = Field(description="user phone number")
    isPhoneNumberVerified: Optional[bool] = Field(description="use")
    username: Optional[str] = Field(description="user username")
    name: Optional[Union[str, None]] = Field(description="the user name")
    segmentUserId: Optional[str] = Field(description="user segmentUserId")
    subscribed: Optional[bool] = Field(description="is subscribed")
    primaryFee: Optional[Union[int, float]] = Field(description="primary fee")
    email: Optional[str] = Field(description="user email")
    confirmedAt: Optional[Union[datetime, None]] = Field(description="confirmed datetime")
    connectedCRO: Optional[bool] = Field(description="is connected CRO")
    disablePayout: Optional[bool] = Field(description="is disable Payout")
    mainAppStatus: Optional[str] = Field(description="main app status")
    creationPayoutBlockExpiredAt: Optional[Union[datetime, None]] = Field(
        description="create payout block expired datetime"
    )
    creationWithdrawalBlockExpiredAt: Optional[Union[datetime, None]] = Field(
        description="CreateWithdrawalBlockExpiredDatetime"
    )
    isCreationPayoutBlocked: Optional[bool] = Field(description="is creation payout blocked")
    isCreationWithdrawalBlocked: Optional[bool] = Field(description="is creation withdrawal blocked")
    isEmailMismatch: Optional[bool] = Field(description="is email mismatch")
    croUserUUID: Optional[Union[str, None]] = Field(description="cro user uuid")
    croWalletAddress: Optional[str] = Field(description="cro wallet address")
    offerBlockUntil: Optional[Union[str, None]] = Field()
    antiPhishingCode: Optional[Union[str, None]] = Field()
    clientOtpEnabled: Optional[bool] = Field(description="2FA status")
    addressWhitelistingEnabled: Optional[bool] = Field()
    newWhitelistAddressLockEnabled: Optional[bool] = Field()
    securityChangeWithdrawalLocked: Optional[bool] = Field()
    clientOtpEnabledAt: Optional[Union[datetime, None]] = Field(description="2FA start datetime")
    featureFlags: Optional[list] = Field()
    tmxProfileSessionId: Optional[str] = Field()
    __typename: str = Field()

    class WeeklyUsedCreditCardBalanceDecimal(FrozenBaseModel):
        drops: str = Field()
        marketplace: str = Field()
        __typename: str = Field()

    class CreatorConfig(FrozenBaseModel):
        canCreateAsset: bool = Field(description="can create asset?")
        defaultRoyaltiesRate: str = Field(description="default royalties rate")
        maxCategoriesPerAsset: int = Field(description="Max Categories Per Asset")
        maxEditionsPerAsset: int = Field(description="Max Editions Per Asset")
        maxAssetsPerWeek: int = Field(description="Max Assets Per Week")
        marketplacePrimaryFeeRate: str = Field(description="Marketplace Primary Fee Rate")
        __typename: str = Field()

    class UserMFAConfig(FrozenBaseModel):
        __typename: str = Field()

    weeklyUsedCreditCardBalanceDecimal: Optional[WeeklyUsedCreditCardBalanceDecimal] = Field()
    creatorConfig: Optional[Union[CreatorConfig, None]] = Field()
    avatar: Optional[Union[URLModel, None]] = Field()
    cover: Optional[Union[URLModel, None]] = Field()
    userMFAConfig: Optional[Union[UserMFAConfig, None]] = Field()


class CreatorModel(FrozenBaseModel):
    uuid: Optional[str] = Field()
    id: Optional[str] = Field()
    displayName: Optional[Union[str, None]] = Field()
    username: Optional[str] = Field()
    isCreator: Optional[bool] = Field()
    bio: Optional[Union[str, None]] = Field()
    avatar: Optional[Union[URLModel, None]] = Field()
    isCreationWithdrawalBlocked: Optional[bool] = Field()
    creationWithdrawalBlockExpiredAt: Optional[Union[str, None]] = Field()
    instagramUsername: Optional[Union[str, None]] = Field()
    facebookUsername: Optional[Union[str, None]] = Field()
    twitterUsername: Optional[Union[str, None]] = Field()
    verified: Optional[bool] = Field()
    __typename: str = Field()


class DropModel(FrozenBaseModel):
    id: str = Field()
    name: Optional[str] = Field()
    creatorInfo: Optional[Union[str, None]] = Field()
    description: Optional[str] = Field()
    startAt: Optional[str] = Field()
    endAt: Optional[str] = Field()
    showCollectible: Optional[bool] = Field()
    whatInsideDescription: Optional[str] = Field()
    termsAndConditions: Optional[str] = Field()
    isPublicReadOnly: Optional[bool] = Field()
    dropStatus: Optional[str] = Field()
    __typename: str = Field()

    class PremiumDropConfig(FrozenBaseModel):
        id: Optional[str] = Field()
        endAt: Optional[str] = Field()
        startAt: Optional[str] = Field()
        type: Optional[str] = Field()
        description: Optional[str] = Field()
        title: Optional[str] = Field()
        __typename: str = Field()

    cover: Optional[Union[URLModel, None]] = Field()
    video: Optional[Union[URLModel, None]] = Field()
    creator: Optional[Union[CreatorModel, None]] = Field()
    premiumDropConfig: Union[PremiumDropConfig, None] = Field()


class StatsModel(FrozenBaseModel):
    floorPriceDecimal: Optional[str] = Field()
    allDayBuyerCount: Optional[int] = Field()
    oneDayBuyerCount: Optional[int] = Field()
    oneDayFloorPriceDecimal: Optional[str] = Field()
    oneDayFloorPriceDecimalChange: Optional[str] = Field()
    oneDayVolumeDecimal: Optional[str] = Field()
    oneDayVolumeDecimalChange: Optional[str] = Field()
    sevenDayBuyerCount: Optional[int] = Field()
    sevenDayFloorPriceDecimal: Optional[str] = Field()
    sevenDayFloorPriceDecimalChange: Optional[str] = Field()
    sevenDayVolumeDecimal: Optional[str] = Field()
    sevenDayVolumeDecimalChange: Optional[str] = Field()
    thirtyDayBuyerCount: Optional[int] = Field()
    thirtyDayFloorPriceDecimal: Optional[str] = Field()
    thirtyDayFloorPriceDecimalChange: Optional[str] = Field()
    thirtyDayVolumeDecimal: Optional[str] = Field()
    thirtyDayVolumeDecimalChange: Optional[str] = Field()
    __typename: str = Field()


class CollectionModel(FrozenBaseModel):
    id: str = Field(description="Collection ID")
    name: str = Field(description="Collection Name")
    description: Optional[str] = Field()
    categories: Optional[list] = Field()
    banner: Optional[URLModel] = Field()
    logo: URLModel = Field()
    creator: Optional[CreatorModel] = Field()
    aggregatedAttributes: Optional[Union[list, None]] = Field()
    metrics: Optional[MetricsModel] = Field()
    network: Optional[str] = Field()
    verified: bool = Field()
    instagramUsername: Optional[Union[str, None]] = Field()
    twitterUsername: Optional[Union[str, None]] = Field()
    websiteUrl: Optional[Union[str, None]] = Field()
    discordUsername: Optional[Union[str, None]] = Field()
    enableInternalRarity: Optional[bool] = Field()
    enableExternalRarity: Optional[bool] = Field()
    enableOfficialRarity: Optional[bool] = Field()
    defaultRarityType: Optional[Union[str, None]] = Field()
    priceAlert: Optional[Union[PriceAlertModel, None]] = Field()
    watched: Optional[bool] = Field()
    stats: Optional[StatsModel] = Field()
    __typename: str = Field()


class DefaultPrimaryListingModel(FrozenBaseModel):
    editionId: str = Field(description="edition Id")
    priceDecimal: str = Field(description="Price")
    mode: str = Field(description="mode: sale")
    auctionHasBids: bool = Field()
    auctionCloseAt: Union[datetime, None] = Field()
    primary: bool = Field()
    salePriceDecimalUSD: str = Field()
    currency: str = Field()
    seller: Optional[SellerModel] = Field()
    __typename: str = Field()


class EditionModel(FrozenBaseModel):
    id: str = Field()
    assetId: Optional[str] = Field()
    index: Optional[int] = Field()
    chainMintStatus: Optional[str] = Field()
    chainTransferStatus: Optional[str] = Field()
    chainWithdrawStatus: Optional[str] = Field()
    minOfferAmountDecimal: Optional[str] = Field()
    mintTime: Optional[str] = Field()
    acceptedOffer: Optional[Union[AcceptedOfferModel, None]] = Field()
    listing: Optional[Union[ListingModel, None]] = Field()
    primaryListing: Optional[Union[PrimaryListingModel, None]] = Field()
    owner: Optional[OwnerModel] = Field()
    ownership: Optional[OwnerShipModel] = Field()
    __typename: str = Field()


class AssetModel(FrozenBaseModel):
    id: Optional[str] = Field(description="asset id")
    name: Optional[str] = Field()
    description: Optional[str] = Field(description="asset description")
    copies: Optional[int] = Field()
    copiesInCirculation: Optional[int] = Field()
    collectiblePerPack: Optional[Union[int, None]] = Field()
    maxItemsPerCheckout: Optional[Union[str, None]] = Field()
    categories: Optional[list] = Field()
    creator: Optional[CreatorModel] = Field()
    createAt: Union[str, datetime, None] = Field()
    cover: Union[URLModel, None] = Field()
    royaltiesRateDecimal: Optional[str] = Field()
    main: Union[URLModel, None] = Field()
    kind: Optional[str] = Field()
    pack: Optional[Union[dict, None]] = Field()
    likes: Optional[int] = Field()
    views: Optional[int] = Field()
    auctionMaxEndDate: Optional[Union[str, None]] = Field()
    remark: Optional[Union[str, None]] = Field()
    isOwnerExternal: Optional[bool] = Field()
    defaultEditionId: Optional[str] = Field()
    defaultOwnerEdition: Optional[Union[EditionModel, None]] = Field()
    defaultOwnerSaleEdition: Optional[Union[EditionModel, None]] = Field()
    defaultOwnerAuctionEdition: Optional[Union[EditionModel, None]] = Field()
    defaultListing: Optional[ListingModel] = Field()
    defaultAuctionListing: Optional[Union[ListingModel, None]] = Field()
    defaultSaleListing: Optional[Union[ListingModel, None]] = Field()
    defaultPrimaryListing: Optional[DefaultPrimaryListingModel] = Field()
    defaultSecondaryListing: Optional[Union[ListingModel, None]] = Field()
    defaultSecondaryAuctionListing: Optional[Union[ListingModel, None]] = Field()
    defaultSecondarySaleListing: Optional[Union[ListingModel, None]] = Field()
    rarityScore: Optional[str] = Field()
    defaultRarityRank: Optional[str] = Field()
    externalRarityScore: Optional[str] = Field()
    externalRarityRank: Optional[str] = Field()
    primaryListingsCount: Optional[int] = Field()
    secondaryListingsCount: Optional[int] = Field()
    primarySalesCount: Optional[int] = Field()
    isAssetWithdrawableOnChain: Optional[bool] = Field()
    totalSalesDecimal: Optional[str] = Field()
    isExternalNft: Optional[bool] = Field()
    isLiked: Optional[bool] = Field()
    externalNftMetadata: Union[ExternalNftMetadataModel, None] = Field()
    crossChainCreator: Optional[Union[dict, None]] = Field()
    isOwnerOnly: Optional[bool] = Field()
    isCurated: Optional[bool] = Field()
    isSoulbound: Optional[bool] = Field()
    ownerEditionsTotal: Optional[int] = Field()
    ownerEditionsForSale: Optional[int] = Field()
    __typename: str = Field()
    collection: Optional[CollectionModel] = Field()
    denomId: Optional[str] = Field()
    priceAlert: Optional[Union[PriceAlertModel, None]]
    isCrossChainSelfMint: Optional[bool] = Field()

    class Drop(FrozenBaseModel):
        id: Optional[str] = Field(description="drop id")
        endAt: Optional[datetime] = Field()

    drop: Optional[Drop] = Field()


class DatetimeAtModel(FrozenBaseModel):
    lte: Optional[Union[str, datetime]] = Field()
    gt: Optional[Union[str, datetime]] = Field()


class PackModel(FrozenBaseModel):
    id: str = Field()
    asset: AssetModel = Field()
    __typename: str = Field()


class UserModel(FrozenBaseModel):
    uuid: str = Field(description="user uuid")
    verified: bool = Field(description="is verified")
    id: str = Field(description="user id")
    username: str = Field(description="username")
    bio: Union[str, None] = Field(description="bio")
    displayName: Union[str, None] = Field(description="display name")
    instagramUsername: Union[str, None] = Field()
    facebookUsername: Union[str, None] = Field()
    twitterUsername: Union[str, None] = Field()
    isCreator: bool = Field()
    canCreateAsset: bool = Field()
    croWalletAddress: str = Field()
    avatar: Union[URLModel, None] = Field()
    cover: Union[URLModel, None] = Field()
    __typename: str = Field()


class SortModel(FrozenBaseModel):
    field: str = Field()
    order: str = Field()


class UserMetricsModel(FrozenBaseModel):
    likes: int = Field()
    views: int = Field()
    created: int = Field()
    minted: int = Field()
    __typename: str = Field()


class ProfileCollectionsModel(FrozenBaseModel):
    id: str = Field(description="collection id")
    name: str = Field(description="collection name")
    logo: URLModel = Field()
    banner: URLModel = Field()
    verified: bool = Field()
    __typename: str = Field()

    class Metrics(FrozenBaseModel):
        items: int = Field()
        __typename: str = Field()

    metrics: Metrics = Field()


class UnauthorizedMeModel(FrozenBaseModel):
    uuid: str = Field()
    email: str = Field()
    clientOtpEnabled: Optional[bool] = Field()
    registrationCompleted: Optional[bool] = Field()
    name: Union[str, None] = Field()
    username: Union[str, None] = Field()
    __typename: str = Field()


class UnauthorizedMeV2Model(FrozenBaseModel):
    uuid: str = Field()
    email: str = Field()
    name: str = Field()
    username: str = Field()
    __typename: str = Field()


class CreationModel(FrozenBaseModel):
    id: str = Field(description="creation id")
    name: str = Field(description="creation name")
    description: str = Field()
    copies: int = Field()
    copiesInCirculation: int = Field()
    collectiblePerPack: Union[int, None] = Field()
    createdAt: str = Field()
    collection: Optional[Union[CollectionModel, None]] = Field()
    main: URLModel = Field()
    cover: Union[URLModel, None] = Field()
    drop: Union[DropModel, None] = Field()
    kind: str = Field()
    defaultEditionId: Union[str, None] = Field()
    defaultOwnerEdition: Union[IdModel, None] = Field()
    defaultPrimaryListing: Optional[Union[DefaultPrimaryListingModel, None]] = Field()
    primaryListingsCount: int = Field(description="primary list count")
    secondaryListingsCount: int = Field(description="secondary listings count")
    isCurated: bool = Field()
    isExternalNft: bool = Field()
    externalNftMetadata: Union[ExternalNftMetadataModel, None] = Field()
    __typename: str = Field()


class CreatedCollectionModel(FrozenBaseModel):
    id: str = Field()
    name: str = Field()
    logo: IdUrlModel = Field()
    banner: IdUrlModel = Field()
    verified: Optional[bool] = Field()
    blocked: Optional[bool] = Field()
    metrics: Optional[MetricsModel] = Field()
    categories: Optional[list] = Field()
    creator: Optional[IdModel] = Field()
    __typename: str = Field()


class NextAvailableListingModel(FrozenBaseModel):
    editionId: str = Field()
    assetId: str = Field()
    __typename: str = Field()


class CreditCardModel(FrozenBaseModel):
    firstSixDigits: str = Field()
    lastFourDigits: str = Field()
    isExpired: bool = Field()
    cardType: str = Field()
    uuid: str = Field()
    createdAt: str = Field()
    __typename: str = Field()


class PaidCheckoutModel(FrozenBaseModel):
    id: str = Field()
    amountDecimal: str = Field()
    currency: str = Field()
    asset: AssetModel = Field()
    edition: EditionModel = Field()
    listing: ListingModel = Field()
    cartQuantity: int = Field()
    paidAt: str = Field()
    seller: SellerModel = Field()
    gateway: str = Field()
    __typename: str = Field()


class CategoryModel(FrozenBaseModel):
    id: str = Field()
    name: str = Field()
    unselectable: str = Field()
    __typename: str = Field()


class IdUrlModel(FrozenBaseModel):
    id: str = Field()
    url: str = Field()
    __typename: str = Field()


class BidModel(FrozenBaseModel):
    id: str = Field()
    createdAt: str = Field()
    edition: IdModel = Field()
    priceDecimal: str = Field()
    listing: dict = Field()
    buyer: dict = Field()
    __typename: str = Field()


class OpenPackModel(FrozenBaseModel):
    id: str = Field()
    index: int = Field()
    asset: AssetModel = Field()
    __typename: str = Field()

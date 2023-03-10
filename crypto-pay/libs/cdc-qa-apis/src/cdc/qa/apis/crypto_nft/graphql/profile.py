GetProfileAssetsTotal = """
query GetProfileAssetsTotal($cacheId: ID, $userId: ID!) {
  public(cacheId: $cacheId) {
    collectedEditionsTotal(ownerId: $userId)
    profileCreatedAssetsTotal(creatorId: $userId)
    profileLikedAssetsTotal(likedById: $userId)
    __typename
  }
}
"""

GetUserPrivateAssetsTotal = """
    query GetUserPrivateAssetsTotal {
      collectedEditionsTotal
      createdAssetsTotal
    }
"""

GetProfileCollections = """
    query GetProfileCollections($cacheId: ID, $search: String, $first: Int, $skip: Int, $sort: SingleFieldSort, \
    $withStats: Boolean!, $collectionIds: [ID!], $isSortFieldZeroLast: Boolean!, $verifiedOnly: Boolean, \
    $verifiedFirst: Boolean, $creatorId: ID, $assetOwnerId: ID, $assetCreatorId: ID, $assetLikedById: ID) {
      public(cacheId: $cacheId) {
        profileCollections(
          search: $search
          first: $first
          skip: $skip
          sort: $sort
          collectionIds: $collectionIds
          isSortFieldZeroLast: $isSortFieldZeroLast
          verifiedOnly: $verifiedOnly
          verifiedFirst: $verifiedFirst
          creatorId: $creatorId
          assetOwnerId: $assetOwnerId
          assetCreatorId: $assetCreatorId
          assetLikedById: $assetLikedById
        ) {
          id
          name
          logo {
            url
            __typename
          }
          banner {
            url
            __typename
          }
          verified
          metrics {
            items
            __typename
          }
          stats @include(if: $withStats) {
            floorPriceDecimal
            oneDayFloorPriceDecimalChange
            oneDayVolumeDecimal
            oneDayVolumeDecimalChange
            sevenDayFloorPriceDecimalChange
            sevenDayVolumeDecimal
            sevenDayVolumeDecimalChange
            thirtyDayFloorPriceDecimalChange
            thirtyDayVolumeDecimal
            thirtyDayVolumeDecimalChange
            __typename
          }
          __typename
        }
        __typename
      }
    }
"""

LiveAndIncomingDrops = """
    query LiveAndIncomingDrops($dropStatuses: [DropStatus!], $endAt: DateTimeFilter!) {
      public(cacheId: "landingPage-LiveAndIncomingDrops") {
        drops(dropStatuses: $dropStatuses, endAt: $endAt) {
          id
          name
          description
          cover {
            url
            __typename
          }
          creator {
            displayName
            username
            avatar {
              url
              __typename
            }
            __typename
          }
          startAt
          endAt
          dropStatus
          isPublicReadOnly
          premiumDropConfig {
            endAt
            id
            startAt
            type
            __typename
          }
          __typename
        }
        __typename
      }
    }
"""

UserMetrics = """
query UserMetrics($id: ID!) {
  userMetrics(id: $id) {
    likes
    views
    created
    minted
    __typename
  }
}
"""

User = """
  query User($id: ID!, $cacheId: ID) {
    public(cacheId: $cacheId) {
      user(id: $id) {
        uuid
        verified
        id
        username
        bio
        displayName
        instagramUsername
        facebookUsername
        twitterUsername
        isCreator
        canCreateAsset
        croWalletAddress
        avatar {
          url
          __typename
        }
        cover {
          url
          __typename
        }
        __typename
      }
      __typename
    }
  }
"""

getUserCreatedAssets = """
  query getUserCreatedAssets($dropId: ID, $kinds: [AssetKind!], $first: Int, $skip: Int, \
    $hasSecondaryListing: Boolean, $where: AssetsSearch, $sort: [SingleFieldSort!], $listingTypes: [ListingType!], \
      $collections: [ID!], $curation: [Curation!], $categories: [ID!]) {
    creations(
      first: $first
      skip: $skip
      dropId: $dropId
      kinds: $kinds
      hasSecondaryListing: $hasSecondaryListing
      where: $where
      sort: $sort
      listingTypes: $listingTypes
      collections: $collections
      curation: $curation
      categories: $categories
    ) {
      id
      name
      description
      copies
      copiesInCirculation
      collectiblePerPack
      createdAt
      collection {
        logo {
          url
          __typename
        }
        id
        name
        verified
        __typename
      }
      main {
        url
        __typename
      }
      cover {
        url
        __typename
      }
      collection {
        logo {
          url
          __typename
        }
        id
        name
        verified
        __typename
      }
      drop {
        id
        endAt
        __typename
      }
      kind
      defaultEditionId
      defaultOwnerEdition {
        id
        __typename
      }
      defaultPrimaryListing {
        editionId
        priceDecimal
        mode
        auctionHasBids
        auctionCloseAt
        primary
        salePriceDecimalUSD
        currency
        seller {
          id
          __typename
        }
        __typename
      }
      primaryListingsCount
      secondaryListingsCount
      isCurated
      isExternalNft
      externalNftMetadata {
        network
        __typename
      }
      __typename
    }
  }
"""

GetUserCreatedCollections = """
query GetUserCreatedCollections($search: String, $first: Int, $skip: Int, $sort: SingleFieldSort, \
  $withStats: Boolean!, $collectionIds: [ID!], $isSortFieldZeroLast: Boolean!, $verifiedOnly: Boolean, \
    $verifiedFirst: Boolean, $creatorId: ID, $assetOwnerId: ID, $assetCreatorId: ID, $assetLikedById: ID) {
  createdCollections(
    search: $search
    first: $first
    skip: $skip
    sort: $sort
    collectionIds: $collectionIds
    isSortFieldZeroLast: $isSortFieldZeroLast
    verifiedOnly: $verifiedOnly
    verifiedFirst: $verifiedFirst
    creatorId: $creatorId
    assetOwnerId: $assetOwnerId
    assetCreatorId: $assetCreatorId
    assetLikedById: $assetLikedById
  ) {
    id
    name
    logo {
      url
      __typename
    }
    banner {
      url
      __typename
    }
    verified
    metrics {
      items
      __typename
    }
    stats @include(if: $withStats) {
      floorPriceDecimal
      oneDayFloorPriceDecimalChange
      oneDayVolumeDecimal
      oneDayVolumeDecimalChange
      sevenDayFloorPriceDecimalChange
      sevenDayVolumeDecimal
      sevenDayVolumeDecimalChange
      thirtyDayFloorPriceDecimalChange
      thirtyDayVolumeDecimal
      thirtyDayVolumeDecimalChange
      __typename
    }
    __typename
  }
}
"""

getMyMetrics = """
  query getMyMetrics {
    myMetrics {
      likes
      views
      created
      minted
      __typename
    }
  }
"""

completeProfile = """
  mutation completeProfile($name: String!, $username: String!) {
    completeProfile(name: $name, username: $username) {
      email
      name
      username
      uuid
      __typename
    }
  }
"""

UpdateProfile = """
    mutation UpdateProfile($bio: String,
    $name: String,
    $username: String,
    $displayName: String,
    $instagramUsername: String,
    $facebookUsername: String,
    $twitterUsername: String,
    $coverId: ID,
    $avatarId: ID) {
      updateProfile(
        bio: $bio
        name: $name
        username: $username
        displayName: $displayName
        instagramUsername: $instagramUsername
        facebookUsername: $facebookUsername
        twitterUsername: $twitterUsername
        coverId: $coverId
        avatarId: $avatarId
      ) {
        id
        bio
        name
        username
        displayName
        instagramUsername
        facebookUsername
        twitterUsername
        avatar {
          url
          __typename
        }
        cover {
          url
          __typename
        }
        __typename
      }
    }
"""

GetUnopenedPacks = """
query GetUnopenedPacks($first: Int, $skip: Int) {
  packs(first: $first, skip: $skip) {
    id
    asset {
      collectiblePerPack
      name
      cover {
        url
        __typename
      }
      drop {
        endAt
        __typename
      }
      likes
      views
      __typename
    }
    __typename
  }
}
"""

GetPack = """
query GetPack($editionId: ID!, $ownerId: ID, $cacheId: ID) {
  public(cacheId: $cacheId) {
    edition(id: $editionId, ownerId: $ownerId) {
      id
      asset {
        collectiblePerPack
        name
        cover {
          url
          __typename
        }
        likes
        views
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

OpenPack = """
mutation OpenPack($editionId: ID!) {
  openPack(editionId: $editionId) {
    id
    index
    asset {
      id
      name
      copies
      creator {
        displayName
        username
        uuid
        avatar {
          url
          __typename
        }
        __typename
      }
      cover {
        url
        __typename
      }
      main {
        url
        __typename
      }
      likes
      views
      __typename
    }
    __typename
  }
}
"""

GetProfileAssets = """
  fragment AssetBaseDetail on Asset {
    id
    name
    copies
    copiesInCirculation
    main {
      url
      __typename
    }
    cover {
      url
      __typename
    }
    primaryListingsCount
    secondaryListingsCount
    isCurated
    isSoulbound
    isExternalNft
    __typename
  }

  fragment AssetListing on Listing {
    id
    editionId
    priceDecimal
    auctionMinPriceDecimal
    auctionCloseAt
    mode
    salePriceDecimalUSD
    auctionHasBids
    currency
    source
    seller {
      id
      uuid
      __typename
    }
    __typename
  }

  fragment DefaultListingWithFilter on Asset {
    defaultListing(where: $where) {
      ...AssetListing
      __typename
    }
    __typename
  }

  fragment DefaultAuctionListingWithFilter on Asset {
    defaultAuctionListing(where: $where) {
      ...AssetListing
      __typename
    }
    __typename
  }

  fragment DefaultSaleListingWithFilter on Asset {
    defaultSaleListing(where: $where) {
      ...AssetListing
      __typename
    }
    __typename
  }

  fragment DefaultSecondaryAuctionListingWithFilter on Asset {
    secondaryListingsCount
    defaultSecondaryAuctionListing(where: $where) {
      ...AssetListing
      __typename
    }
    __typename
  }

  fragment DefaultSecondarySaleListingWithFilter on Asset {
    defaultSecondarySaleListing(where: $where) {
      ...AssetListing
      __typename
    }
    __typename
  }

  fragment DefaultPrimaryListingWithFilter on Asset {
    primaryListingsCount
    primarySalesCount
    defaultPrimaryListing(where: $where) {
      ...AssetListing
      primary
      source
      externalUser {
        address
        username
        avatar {
          url
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }

  fragment DefaultSecondaryListingWithFilter on Asset {
    secondaryListingsCount
    defaultSecondaryListing(where: $where) {
      ...AssetListing
      __typename
    }
    __typename
  }

  query GetProfileAssets($audience: Audience, $brandId: ID, $categories: [ID!], $collectionId: ID, $creatorId: ID, \
  $ownerId: ID, $first: Int!, $skip: Int!, $cacheId: ID, $hasSecondaryListing: Boolean, $where: AssetsSearch, \
  $sort: [SingleFieldSort!], $isCurated: Boolean, $createdPublicView: Boolean, $listingTypes: [ListingType!], \
  $collections: [ID!], $curation: [Curation!], $likedById: ID) {
    public(cacheId: $cacheId) {
      profileAssets(
        audience: $audience
        brandId: $brandId
        categories: $categories
        collectionId: $collectionId
        creatorId: $creatorId
        ownerId: $ownerId
        first: $first
        skip: $skip
        hasSecondaryListing: $hasSecondaryListing
        where: $where
        sort: $sort
        isCurated: $isCurated
        createdPublicView: $createdPublicView
        listingTypes: $listingTypes
        collections: $collections
        curation: $curation
        likedById: $likedById
      ) {
        ...AssetBaseDetail
        drop {
          id
          __typename
        }
        primarySalesCount
        totalSalesDecimal
        collection {
          rarityMetadata {
            totalSupply
            __typename
          }
          metrics {
            items
            __typename
          }
          logo {
            url
            __typename
          }
          id
          name
          verified
          enableInternalRarity
          enableExternalRarity
          __typename
        }
        ...DefaultListingWithFilter
        ...DefaultAuctionListingWithFilter
        ...DefaultSaleListingWithFilter
        ...DefaultSecondaryListingWithFilter
        ...DefaultSecondaryAuctionListingWithFilter
        ...DefaultSecondarySaleListingWithFilter
        ...DefaultPrimaryListingWithFilter
        rarityScore
        rarityRank
        externalRarityScore
        externalRarityRank
        defaultEditionId
        externalNftMetadata {
          network
          isSuspicious
          __typename
        }
        ownerEditionsTotal
        latestPurchasedEdition {
          id
          priceUSD
          __typename
        }
        __typename
      }
      __typename
    }
  }
"""

updateCollection = """
mutation updateCollection($bannerId: ID, $categories: [ID!], $description: String, $id: ID!, $logoId: ID, \
$name: String) {
  updateCollection(
    bannerId: $bannerId
    categories: $categories
    description: $description
    id: $id
    logoId: $logoId
    name: $name
  ) {
    id
    creator {
      id
      __typename
    }
    name
    description
    logo {
      id
      url
      __typename
    }
    banner {
      id
      url
      __typename
    }
    blocked
    categories
    __typename
  }
}
"""

createCollection = """
mutation createCollection($bannerId: ID!, $categories: [ID!], $description: String, $logoId: ID!, $name: String!) {
  createCollection(
    bannerId: $bannerId
    categories: $categories
    description: $description
    logoId: $logoId
    name: $name
  ) {
    id
    creator {
      id
      __typename
    }
    name
    description
    logo {
      id
      url
      __typename
    }
    banner {
      id
      url
      __typename
    }
    blocked
    categories
    __typename
  }
}
"""

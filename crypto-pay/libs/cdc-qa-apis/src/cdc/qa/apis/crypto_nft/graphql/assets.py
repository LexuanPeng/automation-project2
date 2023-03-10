getNextAvailableOpenListingEdition = """
  query getNextAvailableOpenListingEdition($assetId: ID!) {
    getNextAvailableOpenListingEdition(assetId: $assetId) {
      editionId
      assetId
      __typename
    }
  }
"""

increaseAssetViews = """
    mutation increaseAssetViews($assetId: ID!) {
      increaseAssetViews(assetId: $assetId) {
        id
        views
        __typename
      }
    }
"""

GetAssetMinPrice = """
    query GetAssetMinPrice($assetId: ID!, $editionId: ID!) {
      assetMinPrice(assetId: $assetId, editionId: $editionId)
    }
"""

GetAssetById = """
    fragment UserData on User {
      uuid
      id
      username
      displayName
      isCreator
      avatar {
        url
        __typename
      }
      isCreationWithdrawalBlocked
      creationWithdrawalBlockExpiredAt
      verified
      __typename
    }
    query GetAssetById($id: ID!, $cacheId: ID) {
      public(cacheId: $cacheId) {
        asset(id: $id) {
          id
          name
          collectiblePerPack
          maxItemsPerCheckout
          copies
          copiesInCirculation
          description
          categories {
            name
            __typename
          }
          creator {
            ...UserData
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
          royaltiesRateDecimal
          primaryListingsCount
          secondaryListingsCount
          primarySalesCount
          isAssetWithdrawableOnChain
          drop {
            id
            startAt
            endAt
            premiumDropConfig {
              id
              type
              startAt
              endAt
              __typename
            }
            creator {
              ...UserData
              __typename
            }
            __typename
          }
          defaultPrimaryListing {
            id
            editionId
            priceDecimal
            mode
            auctionHasBids
            primary
            source
            salePriceDecimalUSD
            currency
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
          kind
          pack {
            id
            primaryListingsCount
            __typename
          }
          likes
          views
          auctionMaxEndDate
          remark
          isOwnerExternal
          isCurated
          collection {
            totalSupply
            enableExternalRarity
            enableInternalRarity
            defaultRarityType
            logo {
              url
              __typename
            }
            id
            name
            verified
            rarityMetadata {
              attributeJson {
                percentage
                trait_type
                value
                __typename
              }
              __typename
            }
            metrics {
              items
              minSaleListingPriceDecimal
              __typename
            }
            __typename
          }
          denomId
          defaultEditionId
          defaultAuctionListing {
            editionId
            priceDecimal
            auctionMinPriceDecimal
            auctionCloseAt
            mode
            auctionHasBids
            currency
            __typename
          }
          defaultSaleListing {
            editionId
            priceDecimal
            mode
            salePriceDecimalUSD
            currency
            __typename
          }
          defaultListing {
            editionId
            priceDecimal
            mode
            auctionHasBids
            salePriceDecimalUSD
            currency
            __typename
          }
          defaultSecondaryAuctionListing {
            editionId
            priceDecimal
            auctionMinPriceDecimal
            auctionCloseAt
            mode
            auctionHasBids
            currency
            __typename
          }
          defaultSecondarySaleListing {
            editionId
            priceDecimal
            mode
            currency
            salePriceDecimalUSD
            __typename
          }
          isExternalNft
          isLiked
          externalNftMetadata {
            chainCollection {
              name
              avatar {
                url
                __typename
              }
              __typename
            }
            creator {
              name
              avatar {
                url
                __typename
              }
              __typename
            }
            network
            creatorAddress
            chainCollectionId
            tokenId
            __typename
          }
          crossChainCreator {
            id
            username
            displayName
            avatar {
              url
              __typename
            }
            verified
            __typename
          }
          isOwnerOnly
          isOwnerExternal
          rarityScore
          defaultRarityRank
          externalRarityScore
          externalRarityRank
          priceAlert {
            enabled
            frequency
            id
            price
            target
            type
            __typename
          }
          __typename
        }
        __typename
      }
    }
"""

getEditionsByAssetId = """
    fragment UserData on User {
      uuid
      id
      username
      displayName
      isCreator
      avatar {
        url
        __typename
      }
      isCreationWithdrawalBlocked
      creationWithdrawalBlockExpiredAt
      verified
      __typename
    }

    query getEditionsByAssetId(
      $assetId: ID!,
      $first: Int,
      $skip: Int,
      $ownerId: ID,
      $primary: Boolean,
      $hasListing: Boolean,
      $cacheId: ID,
      $sort: [SingleFieldSort!],
      $mode: String,
      $editionIndex: String,
      $isDropLast: Boolean,
      $excludeOwnerId: ID) {
      public(cacheId: $cacheId) {
        editions(
          assetId: $assetId
          primary: $primary
          hasListing: $hasListing
          ownerId: $ownerId
          first: $first
          skip: $skip
          sort: $sort
          mode: $mode
          editionIndex: $editionIndex
          isDropLast: $isDropLast
          excludeOwnerId: $excludeOwnerId
        ) {
          totalCount
          editions {
            id
            index
            listing {
              id
              price
              currency
              primary
              auctionCloseAt
              auctionMinPriceDecimal
              auctionHasBids
              priceDecimal
              mode
              salePriceDecimalUSD
              __typename
            }
            owner {
              ...UserData
              __typename
            }
            ownership {
              primary
              __typename
            }
            acceptedOffer {
              id
              __typename
            }
            chainMintStatus
            chainTransferStatus
            chainWithdrawStatus
            __typename
          }
          __typename
        }
        __typename
      }
    }
"""

GetUserAssetsQuery = """
  query GetUserAssetsQuery($skipCount: Boolean!, $creatorId: ID, $hasSecondaryListing: Boolean, $first: Int!, \
    $skip: Int!, $assetIds: [ID!], $where: AssetsSearch, $sort: [SingleFieldSort!], $listingTypes: [ListingType!], \
      $collections: [ID!], $curation: [Curation!], $categories: [ID!]) {
    assets(
      creatorId: $creatorId
      hasSecondaryListing: $hasSecondaryListing
      first: $first
      skip: $skip
      assetIds: $assetIds
      where: $where
      sort: $sort
      listingTypes: $listingTypes
      collections: $collections
      curation: $curation
      categories: $categories
    ) {
      id
      name
      copies
      copiesInCirculation
      main {
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
      cover {
        url
        __typename
      }
      defaultEditionId
      defaultOwnerEdition(where: $where) {
        id
        listing {
          id
          auctionCloseAt
          auctionHasBids
          auctionMinPriceDecimal
          mode
          priceDecimal
          currency
          salePriceDecimalUSD
          __typename
        }
        __typename
      }
      defaultOwnerSaleEdition(where: $where) {
        id
        listing {
          id
          auctionCloseAt
          auctionHasBids
          auctionMinPriceDecimal
          mode
          priceDecimal
          salePriceDecimalUSD
          currency
          __typename
        }
        __typename
      }
      defaultOwnerAuctionEdition(where: $where) {
        id
        listing {
          id
          auctionCloseAt
          auctionHasBids
          auctionMinPriceDecimal
          mode
          priceDecimal
          salePriceDecimalUSD
          currency
          __typename
        }
        __typename
      }
      primaryListingsCount @skip(if: $skipCount)
      secondaryListingsCount @skip(if: $skipCount)
      defaultListing(where: $where) {
        id
        editionId
        priceDecimal
        mode
        auctionHasBids
        salePriceDecimalUSD
        currency
        __typename
      }
      defaultAuctionListing(where: $where) {
        id
        editionId
        priceDecimal
        auctionMinPriceDecimal
        auctionCloseAt
        mode
        auctionHasBids
        currency
        __typename
      }
      defaultSaleListing(where: $where) {
        id
        editionId
        priceDecimal
        mode
        salePriceDecimalUSD
        currency
        __typename
      }
      defaultPrimaryListing(where: $where) {
        id
        editionId
        priceDecimal
        mode
        auctionHasBids
        primary
        salePriceDecimalUSD
        currency
        __typename
      }
      defaultSecondaryListing(where: $where) {
        id
        editionId
        priceDecimal
        mode
        auctionHasBids
        currency
        salePriceDecimalUSD
        __typename
      }
      defaultSecondaryAuctionListing(where: $where) {
        id
        editionId
        priceDecimal
        auctionMinPriceDecimal
        auctionCloseAt
        mode
        auctionHasBids
        currency
        __typename
      }
      defaultSecondarySaleListing(where: $where) {
        id
        editionId
        priceDecimal
        mode
        currency
        salePriceDecimalUSD
        __typename
      }
      isExternalNft
      isCurated
      externalNftMetadata {
        network
        __typename
      }
      ownerEditionsTotal
      ownerEditionsForSale
      __typename
    }
  }
"""

getEditionByAssetId = """
    query getEditionByAssetId($editionId: ID, $assetId: ID, $editionIndex: Int, $cacheId: ID) {
      public(cacheId: $cacheId) {
        edition(id: $editionId, assetId: $assetId, editionIndex: $editionIndex) {
          id
          assetId
          index
          listing {
            id
            price
            currency
            primary
            auctionCloseAt
            auctionHasBids
            auctionMinPriceDecimal
            expiredAt
            priceDecimal
            mode
            isCancellable
            status
            source
            salePriceDecimalUSD
            externalUser {
              address
              username
              avatar {
                url
                __typename
              }
              __typename
            }
            seller {
              uuid
              __typename
            }
            __typename
          }
          primaryListing {
            id
            price
            currency
            primary
            auctionCloseAt
            auctionHasBids
            auctionMinPriceDecimal
            expiredAt
            priceDecimal
            mode
            isCancellable
            status
            source
            salePriceDecimalUSD
            externalUser {
              address
              username
              avatar {
                url
                __typename
              }
              __typename
            }
            seller {
              uuid
              __typename
            }
            __typename
          }
          owner {
            uuid
            id
            username
            displayName
            avatar {
              url
              __typename
            }
            croWalletAddress
            isCreator
            verified
            __typename
          }
          ownership {
            primary
            __typename
          }
          chainMintStatus
          chainTransferStatus
          chainWithdrawStatus
          acceptedOffer {
            id
            user {
              id
              __typename
            }
            __typename
          }
          minOfferAmountDecimal
          mintTime
          __typename
        }
        __typename
      }
    }
"""

editionPriceQuote = """
  fragment EditionPriceQuoteFragment on EditionPriceQuote {
    createdAt
    priceUSD
    validMs
    __typename
  }

  mutation editionPriceQuote($editionId: ID!) {
    editionPriceQuote(editionId: $editionId) {
      ...EditionPriceQuoteFragment
      __typename
    }
  }
"""

GetAssets = """
    query GetAssets($audience: Audience,
    $brandId: ID, $categories: [ID!],
    $collectionId: ID,
    $creatorId: ID,
    $ownerId: ID,
    $first: Int!,
    $skip: Int!,
    $cacheId: ID,
    $hasSecondaryListing: Boolean,
    $where: AssetsSearch,
    $sort: [SingleFieldSort!],
    $isCurated: Boolean,
    $createdPublicView: Boolean,
    $listingTypes: [ListingType!],
    $collections: [ID!],
    $curation: [Curation!]) {
      public(cacheId: $cacheId) {
        assets(
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
        ) {
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
          royaltiesRateDecimal
          primaryListingsCount
          secondaryListingsCount
          primarySalesCount
          totalSalesDecimal
          collection {
            logo {
              url
              __typename
            }
            id
            name
            verified
            totalSupply
            metrics {
              items
              __typename
            }
            enableInternalRarity
            enableExternalRarity
            defaultRarityType
            __typename
          }
          defaultListing(where: $where) {
            id
            editionId
            priceDecimal
            mode
            auctionHasBids
            salePriceDecimalUSD
            currency
            seller {
              id
              uuid
              __typename
            }
            __typename
          }
          defaultAuctionListing(where: $where) {
            id
            editionId
            priceDecimal
            auctionMinPriceDecimal
            auctionCloseAt
            mode
            auctionHasBids
            currency
            seller {
              id
              uuid
              __typename
            }
            __typename
          }
          defaultSaleListing(where: $where) {
            id
            editionId
            priceDecimal
            mode
            salePriceDecimalUSD
            currency
            seller {
              id
              uuid
              __typename
            }
            __typename
          }
          defaultPrimaryListing(where: $where) {
            id
            editionId
            priceDecimal
            mode
            auctionHasBids
            primary
            salePriceDecimalUSD
            currency
            seller {
              id
              uuid
              __typename
            }
            __typename
          }
          defaultSecondaryListing(where: $where) {
            id
            editionId
            priceDecimal
            mode
            auctionHasBids
            currency
            salePriceDecimalUSD
            seller {
              id
              uuid
              __typename
            }
            __typename
          }
          defaultSecondaryAuctionListing(where: $where) {
            id
            editionId
            priceDecimal
            auctionMinPriceDecimal
            auctionCloseAt
            mode
            auctionHasBids
            currency
            seller {
              id
              uuid
              __typename
            }
            __typename
          }
          defaultSecondarySaleListing(where: $where) {
            id
            editionId
            priceDecimal
            mode
            currency
            salePriceDecimalUSD
            seller {
              id
              uuid
              __typename
            }
            __typename
          }
          rarityScore
          defaultRarityRank
          externalRarityScore
          externalRarityRank
          isCurated
          defaultEditionId
          isExternalNft
          externalNftMetadata {
            network
            isSuspicious
            __typename
          }
          __typename
        }
        __typename
      }
    }
"""

GetAssetsInPack = """
  query GetAssetsInPack($dropId: ID!, $packId: ID!, $cacheId: ID) {
    public(cacheId: $cacheId) {
      assets(
        dropId: $dropId
        packId: $packId
        first: 100
        skip: 0
        kinds: [COLLECTIBLE, PACK]
      ) {
        id
        name
        description
        copies
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
        cover {
          url
          __typename
        }
        main {
          url
          __typename
        }
        drop {
          id
          endAt
          __typename
        }
        kind
        defaultPrimaryListing {
          editionId
          priceDecimal
          mode
          auctionHasBids
          primary
          salePriceDecimalUSD
          currency
          __typename
        }
        externalNftMetadata {
          network
          __typename
        }
        isExternalNft
        isCurated
        __typename
      }
      __typename
    }
  }
"""

GetAssetListingsById = """
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
  seller {
    id
    uuid
    __typename
  }
  __typename
}

fragment DefaultListing on Asset {
  defaultListing {
    ...AssetListing
    __typename
  }
  __typename
}

fragment DefaultAuctionListing on Asset {
  defaultAuctionListing {
    ...AssetListing
    __typename
  }
  __typename
}

fragment DefaultSaleListing on Asset {
  defaultSaleListing {
    ...AssetListing
    __typename
  }
  __typename
}

fragment DefaultSecondaryAuctionListing on Asset {
  secondaryListingsCount
  defaultSecondaryAuctionListing {
    ...AssetListing
    __typename
  }
  __typename
}

fragment DefaultSecondarySaleListing on Asset {
  defaultSecondarySaleListing {
    ...AssetListing
    __typename
  }
  __typename
}

fragment DefaultPrimaryListing on Asset {
  primaryListingsCount
  primarySalesCount
  defaultPrimaryListing {
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

query GetAssetListingsById($id: ID!, $cacheId: ID) {
  public(cacheId: $cacheId) {
    asset(id: $id) {
      ...DefaultListing
      ...DefaultAuctionListing
      ...DefaultSaleListing
      ...DefaultSecondaryAuctionListing
      ...DefaultSecondarySaleListing
      ...DefaultPrimaryListing
      __typename
    }
    __typename
  }
}
"""

GetAssetDetailById = """
    fragment UserData on User {
      uuid
      id
      username
      displayName
      isCreator
      avatar {
        url
        __typename
      }
      isCreationWithdrawalBlocked
      creationWithdrawalBlockExpiredAt
      verified
      __typename
    }

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

    fragment AssetDetail on Asset {
      ...AssetBaseDetail
      collectiblePerPack
      maxItemsPerCheckout
      description
      categories {
        name
        __typename
      }
      creator {
        ...UserData
        __typename
      }
      royaltiesRateDecimal
      primarySalesCount
      isAssetWithdrawableOnChain
      drop {
        id
        startAt
        endAt
        premiumDropConfig {
          id
          type
          startAt
          endAt
          __typename
        }
        creator {
          ...UserData
          __typename
        }
        __typename
      }
      kind
      pack {
        id
        primaryListingsCount
        __typename
      }
      likes
      views
      auctionMaxEndDate
      remark
      isOwnerExternal
      collection {
        totalSupply
        enableExternalRarity
        enableInternalRarity
        defaultRarityType
        logo {
          url
          __typename
        }
        id
        name
        verified
        rarityMetadata {
          attributeJson {
            percentage
            trait_type
            value
            __typename
          }
          __typename
        }
        metrics {
          items
          minSaleListingPriceDecimal
          __typename
        }
        __typename
      }
      denomId
      defaultEditionId
      isLiked
      externalNftMetadata {
        chainCollection {
          name
          avatar {
            url
            __typename
          }
          __typename
        }
        creator {
          name
          avatar {
            url
            __typename
          }
          __typename
        }
        network
        creatorAddress
        chainCollectionId
        tokenId
        isSuspicious
        __typename
      }
      crossChainCreator {
        id
        username
        displayName
        avatar {
          url
          __typename
        }
        verified
        __typename
      }
      isOwnerOnly
      isOwnerExternal
      rarityScore
      defaultRarityRank
      externalRarityScore
      externalRarityRank
      priceAlert {
        enabled
        frequency
        id
        price
        target
        type
        __typename
      }
      isCrossChainSelfMint
      __typename
    }

    query GetAssetDetailById($id: ID!, $cacheId: ID) {
      public(cacheId: $cacheId) {
        asset(id: $id) {
          ...AssetDetail
          __typename
        }
        __typename
      }
    }
"""

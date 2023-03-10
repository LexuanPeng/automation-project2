GetMarketplaceAssets = """
    query GetMarketplaceAssets($audience: Audience, $brandId: ID, $categories: [ID!], $collectionId: ID, \
        $creatorId: ID, $ownerId: ID, $first: Int!, $skip: Int!, $cacheId: ID, $hasSecondaryListing: Boolean, \
            $where: AssetsSearch, $sort: [SingleFieldSort!], $isCurated: Boolean, $createdPublicView: Boolean, \
                $listingTypes: [ListingType!], $collections: [ID!], $curation: [Curation!]) {
    public(cacheId: $cacheId) {
        assets: marketplaceAssets(
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
        isCurated
        externalNftMetadata {
            network
            __typename
        }
        secondaryListingsCount
        primaryListingsCount
        isExternalNft
        __typename
        }
        __typename
    }
    }
"""

canUserCreateListing = """
    query canUserCreateListing($canUserCreateListingId: ID!) {
      canUserCreateListing(id: $canUserCreateListingId)
    }
"""

CreateListing = """
    mutation CreateListing($editionId: ID!, $mode: String, $priceDecimal: String, $clientOtpCode: String) {
      createListing(
        editionId: $editionId
        mode: $mode
        priceDecimal: $priceDecimal
        clientOtpCode: $clientOtpCode
      ) {
        id
        __typename
      }
    }
"""

CreateAuctionListing = """
    mutation CreateAuctionListing($editionId: ID!,
    $auctionCloseAt: DateTime!,
    $auctionMinPriceDecimal: String!,
    $clientOtpCode: String,
    $mode: String!) {
      createListing(
        editionId: $editionId
        auctionCloseAt: $auctionCloseAt
        auctionMinPriceDecimal: $auctionMinPriceDecimal
        clientOtpCode: $clientOtpCode
        mode: $mode
      ) {
        id
        __typename
      }
    }
"""

getSearchPreviewResults = """
    query getSearchPreviewResults($keyWord: String!) {
      public {
        dropDown(keyWord: $keyWord) {
          collectibles {
            id
            cover {
              url
              __typename
            }
            name
            externalNftMetadata {
              network
              __typename
            }
            copies
            copiesInCirculation
            defaultEditionId
            primaryListingsCount
            secondaryListingsCount
            kind
            isCurated
            defaultSecondaryListing {
              editionId
              __typename
            }
            defaultListing {
              editionId
              __typename
            }
            defaultSecondarySaleListing {
              editionId
              __typename
            }
            defaultSaleListing {
              editionId
              __typename
            }
            __typename
          }
          collections {
            id
            logo {
              url
              __typename
            }
            name
            verified
            metrics {
              items
              __typename
            }
            __typename
          }
          users {
            avatar {
              url
              __typename
            }
            displayName
            username
            verified
            __typename
          }
          __typename
        }
        __typename
      }
    }
"""

cancelListing = """
    mutation cancelListing($id: ID!) {
      cancelListing(id: $id) {
        id
        __typename
      }
    }
"""

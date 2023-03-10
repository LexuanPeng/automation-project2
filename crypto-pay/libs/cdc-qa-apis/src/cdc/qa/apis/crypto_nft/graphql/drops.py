GetDrops = """
  query GetDrops($cacheId: ID, $dropStatuses: [DropStatus!], $endAt: DateTimeFilter, $sort: [SingleFieldSort!], \
    $first: Int, $skip: Int, $withDropStatusField: Boolean = false) {
    public(cacheId: $cacheId) {
      drops(
        dropStatuses: $dropStatuses
        endAt: $endAt
        sort: $sort
        first: $first
        skip: $skip
      ) {
        id
        name
        cover {
          url
          __typename
        }
        creator {
          uuid
          username
          displayName
          avatar {
            url
            __typename
          }
          verified
          __typename
        }
        creatorInfo
        description
        startAt
        endAt
        video {
          url
          __typename
        }
        isPublicReadOnly
        premiumDropConfig {
          description
          endAt
          id
          startAt
          type
          title
          __typename
        }
        dropStatus @include(if: $withDropStatusField)
        __typename
      }
      __typename
    }
  }
"""

GetDrop = """
  fragment DropDetail on Drop {
    id
    name
    cover {
      url
      __typename
    }
    creator {
      uuid
      id
      displayName
      username
      bio
      avatar {
        url
        __typename
      }
      instagramUsername
      facebookUsername
      twitterUsername
      verified
      __typename
    }
    creatorInfo
    description
    startAt
    endAt
    showCollectible
    video {
      url
      __typename
    }
    whatInsideDescription
    termsAndConditions
    dropStatus
    isPublicReadOnly
    premiumDropConfig {
      description
      endAt
      id
      startAt
      type
      title
      __typename
    }
    __typename
  }

  query Drop($id: ID!, $cacheId: ID) {
    public(cacheId: $cacheId) {
      drop(id: $id) {
        ...DropDetail
        __typename
      }
      __typename
    }
  }
"""

GetDropAssetsQuery = """
    query GetDropAssetsQuery($id: ID!, $cacheId: ID) {
      public(cacheId: $cacheId) {
        assets(
          dropId: $id
          first: 100
          skip: 0
          kinds: [COLLECTIBLE, OPEN_COLLECTIBLE, PACK]
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
          primaryListingsCount
          secondaryListingsCount
          primarySalesCount
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
          isExternalNft
          externalNftMetadata {
            network
            __typename
          }
          isCurated
          __typename
        }
        __typename
      }
    }
"""

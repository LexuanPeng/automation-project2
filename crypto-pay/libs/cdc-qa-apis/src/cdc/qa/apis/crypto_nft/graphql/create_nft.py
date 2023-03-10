getCollectionsByCreator = """
    query getCollectionsByCreator(
    $creatorId: ID!,
    $first: Int,
    $sort: SingleFieldSort,
    $verifiedOnly: Boolean) {
      public {
        collections(
          creatorId: $creatorId
          first: $first
          sort: $sort
          verifiedOnly: $verifiedOnly
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
          verified
          __typename
        }
        __typename
      }
    }
"""

GetCreatorWeeklyCreateStatus = """
    query GetCreatorWeeklyCreateStatus {
      creatorWeeklyCreateStatus {
          hasReachedWeeklyLimit
              __typename
      }
    }
"""

GetAttachment = """
    query GetAttachment($id: ID!) {
      attachment(id: $id) {
        id
        url
        coverUrl
        contentModeration {
          status
          expiredAt
          __typename
        }
        __typename
      }
    }
"""

CreateAsset = """
    mutation CreateAsset(
    $categories: [ID!],
    $attributes: [AttributeArgs!],
    $copies: Int!,
    $description: String!,
    $mainId: String!,
    $name: String!,
    $collectionId: ID,
    $network: SupportedNetwork!) {
      createAsset(
        categories: $categories
        copies: $copies
        description: $description
        mainId: $mainId
        name: $name
        collectionId: $collectionId
        network: $network
        attributes: $attributes
      ) {
        uuid
        __typename
      }
    }
"""

checkoutAssetRecord = """
    mutation checkoutAssetRecord($assetCreateRecordId: String!, $kind: CheckoutKind!) {
      createCheckout(assetCreateRecordId: $assetCreateRecordId, kind: $kind) {
        id
        asset {
          id
          __typename
        }
        amountDecimal
        __typename
      }
    }
"""

GetCreatorApplicationStatus = """
    query GetCreatorApplicationStatus {
      creatorApplicationStatus {
        status
        statusUpdatedAt
        __typename
      }
    }
"""

mintHistory = """
    query mintHistory($first: Int, $skip: Int) {
      mintHistory(first: $first, skip: $skip) {
        id
        name
        copies
        cover {
          url
          __typename
        }
        createdAt
        network
        walletAddress
        checkoutId
        gateway
        mintFee
        __typename
      }
      countMintHistory
    }
"""

getCrossChainMintFeeQuote = """
    mutation getCrossChainMintFeeQuote($assetCreateRecordId: String!) {
      crossChainMintFeeQuote(assetCreateRecordId: $assetCreateRecordId) {
        mintFeeUSD
        assetCreateRecordId
        createdAt
        expiredAt
        validMs
        __typename
      }
    }
"""

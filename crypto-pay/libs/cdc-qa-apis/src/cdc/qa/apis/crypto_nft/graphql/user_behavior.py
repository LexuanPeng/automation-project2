createPriceAlert = """
    mutation createPriceAlert($input: CreatePriceAlertInput!) {
      createPriceAlert(input: $input) {
        enabled
        frequency
        id
        price
        target
        type
        __typename
      }
    }
"""

getPriceAlerts = """
    query getPriceAlerts($first: Int, $skip: Int, $target: PriceAlertTarget!) {
      priceAlerts(first: $first, skip: $skip, target: $target) {
        ...PriceAlertData
        __typename
      }
      priceAlertCount(target: $target)
    }
    fragment PriceAlertData on PriceAlert {
      asset {
        collection {
          ...CollectionData
          __typename
        }
        cover {
          url
          __typename
        }
        defaultAuctionListing {
          id
          editionId
          __typename
        }
        defaultSaleListing {
          id
          editionId
          __typename
        }
        defaultSecondaryAuctionListing {
          id
          editionId
          __typename
        }
        defaultSecondarySaleListing {
          id
          editionId
          __typename
        }
        defaultEditionId
        id
        isCurated
        name
        __typename
      }
      collection {
        ...CollectionData
        __typename
      }
      enabled
      frequency
      id
      price
      target
      type
      __typename
    }
    fragment CollectionData on Collection {
      id
      logo {
        url
        __typename
      }
      name
      verified
      watched
      __typename
    }
"""

getPriceAlertCounts = """
    query getPriceAlertCounts {
      collectionAlerts: priceAlertCount(target: COLLECTION)
      collectibleAlerts: priceAlertCount(target: COLLECTIBLE)
    }
"""

deletePriceAlert = """
    mutation deletePriceAlert($input: DeletePriceAlertInput!) {
      deletePriceAlert(input: $input) {
        enabled
        frequency
        id
        price
        target
        type
        __typename
      }
    }
"""

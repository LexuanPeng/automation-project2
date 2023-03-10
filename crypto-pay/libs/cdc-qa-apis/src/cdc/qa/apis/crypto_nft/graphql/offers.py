createOffer = """
    mutation createOffer($amountDecimal: String!, $editionId: ID!) {
      createOffer(amountDecimal: $amountDecimal, editionId: $editionId) {
        id
        __typename
      }
    }
"""

getOffer = """
    query getOffer($offerId: ID!) {
      offer(id: $offerId) {
        id
        amountDecimal
        createdAt
        asset {
          id
          blocked
          name
          copies
          cover {
            url
            __typename
          }
          main {
            url
            __typename
          }
          kind
          royaltiesRateDecimal
          isCurated
          copiesInCirculation
          isExternalNft
          __typename
        }
        user {
          ...UserData
          __typename
        }
        toUser {
          ...UserData
          __typename
        }
        edition {
          id
          index
          __typename
        }
        status
        minServiceFeeDecimal
        __typename
      }
    }

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
"""

getOffersMade = """
    query getOffersMade($first: Int, $skip: Int) {
      offersMade(first: $first, skip: $skip) {
        id
        amountDecimal
        createdAt
        asset {
          id
          name
          copies
          cover {
            url
            __typename
          }
          kind
          copiesInCirculation
          isExternalNft
          __typename
        }
        edition {
          id
          index
          acceptedOffer {
            id
            __typename
          }
          __typename
        }
        user {
          ...UserData
          __typename
        }
        toUser {
          ...UserData
          __typename
        }
        status
        __typename
      }
      countOffersMade
    }

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
"""

getOffersRecieved = """
    query getOffersRecieved($first: Int, $skip: Int) {
      offersRecieved(first: $first, skip: $skip) {
        id
        amountDecimal
        createdAt
        asset {
          id
          name
          copies
          cover {
            url
            __typename
          }
          kind
          copiesInCirculation
          isExternalNft
          __typename
        }
        edition {
          id
          index
          acceptedOffer {
            id
            __typename
          }
          __typename
        }
        user {
          ...UserData
          __typename
        }
        toUser {
          ...UserData
          __typename
        }
        status
        __typename
      }
      countOffersReceived
    }

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
"""

acceptOffer = """
    mutation acceptOffer($id: ID!, $clientOtpCode: String) {
      acceptOffer(id: $id, clientOtpCode: $clientOtpCode) {
        id
        __typename
      }
    }
"""

getMyWallets = """"
    query getMyWallets {
      wallets {
        network
        address
        status
        __typename
      }
    }
"""

accountBalanceQuery = """
    query accountBalanceQuery {
      accountBalance {
        amountDecimal
        currency
        __typename
      }
    }
"""

rejectOffer = """
    mutation rejectOffer($id: ID!) {
      rejectOffer(id: $id) {
        id
        __typename
      }
    }
"""

GetBrands = """
    query GetBrands {
        public {
            brands {
                id
                username
                name
                __typename
            }
            __typename
        }
    }
"""

getPlatformFee = """
    query GetPlatformFee {
      platformFee {
        isEnabled
        minFee
        __typename
      }
    }
"""

CreateCheckout = """
    mutation CreateCheckout(
      $listingId: ID
      $offerId: ID
      $kind: CheckoutKind
      $quantity: Int
    ) {
      createCheckout(
        listingId: $listingId
        offerId: $offerId
        kind: $kind
        quantity: $quantity
      ) {
        id
        __typename
      }
    }
"""

CreateAndCaptureAccountPayment = """
    mutation CreateAndCaptureAccountPayment($checkoutId: ID!) {
      createAndCaptureAccountPayment(checkoutId: $checkoutId) {
        id
        status
        __typename
      }
    }
"""

Checkout = """
    query Checkout($id: ID!) {
      checkout(id: $id) {
        id
        amountDecimal
        currency
        asset {
          id
          name
          copies
          cover {
            url
            __typename
          }
          collectiblePerPack
          kind
          isExternalNft
          collection {
            name
            __typename
          }
          __typename
        }
        edition {
          id
          index
          __typename
        }
        listing {
          id
          mode
          primary
          source
          __typename
        }
        cartQuantity
        listingMode
        paidAt
        seller {
          username
          isCreator
          uuid
          displayName
          __typename
        }
        kind
        assetCreateRecord {
          id
          name
          copies
          main {
            coverUrl
            __typename
          }
          collection {
            name
            id
            __typename
          }
          network
          __typename
        }
        __typename
      }
    }
"""

GetCroMintFee = """
    query GetCroMintFee {
      me {
        creatorConfig {
          canMintFree
          hasMinted
          __typename
        }
        croMintFeeConfig {
          isEnabled
          fee
          defaultFee
          __typename
        }
        __typename
      }
    }
"""

getUserCardTier = """
    query getUserCardTier($id: ID!) {
      getUserCardTier(id: $id) {
        status
        cardName
        __typename
      }
    }
"""

getMe = """
    fragment MeResponse on Me {
      uuid
      verified
      id
      bio
      displayName
      instagramUsername
      facebookUsername
      twitterUsername
      countryCode
      phoneNumber
      isPhoneNumberVerified
      isPriceAlertLimitReached
      username
      name
      avatar {
        url
        __typename
      }
      cover {
        url
        __typename
      }
      segmentUserId
      subscribed
      primaryFee
      email
      id
      confirmedAt
      displayName
      connectedCRO
      disablePayout
      mainAppStatus
      creationPayoutBlockExpiredAt
      creationWithdrawalBlockExpiredAt
      isCreationPayoutBlocked
      isCreationWithdrawalBlocked
      isEmailMismatch
      croUserUUID
      weeklyUsedCreditCardBalanceDecimal {
        drops
        marketplace
        __typename
      }
      croWalletAddress
      offerBlockUntil
      creatorConfig {
        canCreateAsset
        defaultRoyaltiesRate
        maxCategoriesPerAsset
        maxEditionsPerAsset
        maxAssetsPerWeek
        marketplacePrimaryFeeRate
        __typename
      }
      antiPhishingCode
      clientOtpEnabled
      addressWhitelistingEnabled
      newWhitelistAddressLockEnabled
      securityChangeWithdrawalLocked
      clientOtpEnabledAt
      userMFAConfig {
        requireAcceptingBidOrOffer2FA
        requireCreatingListing2FA
        __typename
      }
      featureFlags
      tmxProfileSessionId
      registrationCompleted
      utmId
      __typename
    }

    query getMe {
      me {
        ...MeResponse
        __typename
      }
    }
"""

getUserCardStake = """
    query getUserCardStake($id: ID!) {
      getUserCardStake(id: $id) {
        stakingType
        planId
        __typename
      }
    }
"""

getCreditCards = """
    query getCreditCards {
    creditCards {
        firstSixDigits
        lastFourDigits
        isExpired
        cardType
        uuid
        createdAt
        __typename
    }
    }
"""

createIXOPayment = """
    mutation createIXOPayment($cardFirstSixDigits: String, $cardLastFourDigits: String, $checkoutId: ID!, $cardId: ID) {
    createIXOPayment(
        cardFirstSixDigits: $cardFirstSixDigits
        cardLastFourDigits: $cardLastFourDigits
        checkoutId: $checkoutId
        cardId: $cardId
    ) {
        id
        __typename
    }
    }
"""

preauthIXOPayment = """
    mutation preauthIXOPayment($checkoutId: ID!, $paymentId: ID!, $transactionToken: String, \
        $withRegister: Boolean = false) {
    preauthIXOPayment(
        checkoutId: $checkoutId
        paymentId: $paymentId
        transactionToken: $transactionToken
        withRegister: $withRegister
    ) {
        preauthRedirectUrl
        preauthReturnType
        status
        __typename
    }
    }
"""

captureIXOPayment = """
    mutation captureIXOPayment($checkoutId: ID!, $paymentId: ID!) {
    captureIXOPayment(checkoutId: $checkoutId, paymentId: $paymentId) {
        preauthRedirectUrl
        status
        checkout {
        listingMode
        listing {
            source
            __typename
        }
        __typename
        }
        __typename
    }
    }
"""

paidCheckouts = """
    query paidCheckouts($first: Int, $skip: Int) {
    paidCheckouts(first: $first, skip: $skip) {
        id
        amountDecimal
        currency
        asset {
        id
        name
        copies
        cover {
            url
            __typename
        }
        collectiblePerPack
        kind
        isExternalNft
        __typename
        }
        edition {
        id
        index
        owner {
            id
            uuid
            isCreator
            __typename
        }
        __typename
        }
        listing {
        id
        mode
        primary
        source
        externalUser {
            address
            __typename
        }
        __typename
        }
        cartQuantity
        paidAt
        seller {
        username
        isCreator
        uuid
        displayName
        __typename
        }
        gateway
        __typename
    }
    countPaidCheckouts
    }
"""

getCategories = """
  query getCategories($first: Int, $skip: Int) {
    public {
      categories(first: $first, skip: $skip) {
        id
        name
        unselectable
        __typename
      }
      __typename
    }
  }
"""

CreateAttachment = """
  mutation CreateAttachment(
    $isGenerateCover: Boolean
    $upload: Upload!
    $nature: String!
  ) {
    createAttachment(
      isGenerateCover: $isGenerateCover
      upload: $upload
      nature: $nature
    ) {
      id
      url
      coverUrl
      __typename
    }
  }
"""

PlaceBidMutation = """
  mutation PlaceBidMutation($bidPriceDecimal: String!, $listingId: ID!) {
    createCheckout(bidPriceDecimal: $bidPriceDecimal, listingId: $listingId) {
      id
      bidPriceDecimal
      __typename
    }
  }
"""

GetCollection = """
    query GetCollection($collectionId: ID!) {
      public {
        collection(id: $collectionId) {
          id
          name
          description
          categories
          banner {
            url
            __typename
          }
          logo {
            url
            __typename
          }
          creator {
            displayName
            id
            __typename
          }
          aggregatedAttributes {
            label: traitType
            options: attributes {
              value: id
              label: value
              total
              __typename
            }
            __typename
          }
          metrics {
            items
            minAuctionListingPriceDecimal
            minSaleListingPriceDecimal
            owners
            totalSalesDecimal
            statisticSource
            totalSalesCount
            __typename
          }
          network
          verified
          instagramUsername
          twitterUsername
          websiteUrl
          discordUsername
          enableInternalRarity
          enableExternalRarity
          enableOfficialRarity
          defaultRarityType
          priceAlert {
            enabled
            frequency
            id
            price
            target
            type
            __typename
          }
          watched
          __typename
        }
        __typename
      }
    }
"""

getBiddingHistory = """
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

query getBiddingHistory($listingId: ID!) {
  public {
    bids(listingId: $listingId, first: 300) {
      id
      createdAt
      edition {
        id
        __typename
      }
      priceDecimal
      listing {
        priceDecimal
        currency
        __typename
      }
      buyer {
        ...UserData
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

deleteCreditCard = """
mutation deleteCreditCard($cardId: ID!) {
  deleteCreditCard(cardId: $cardId) {
    uuid
    __typename
  }
}
"""

GetTopCollectibles = """
query GetTopCollectibles($topCollectiblesFilter: TopCollectiblesFilter!, \
  $topCollectiblesFilterBy: TopCollectiblesFilterBy!, $cacheId: ID, $brandId: ID, $page: Int, $pageSize: Int) {
  public(cacheId: $cacheId) {
    topCollectibles(
      filter: $topCollectiblesFilter
      filterBy: $topCollectiblesFilterBy
      brandId: $brandId
      page: $page
      pageSize: $pageSize
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
        __typename
      }
      primaryListingsCount
      secondaryListingsCount
      primarySalesCount
      latestPurchasedEdition {
        id
        priceUSD
        __typename
      }
      totalSalesDecimal
      defaultListing {
        id
        editionId
        priceDecimal
        mode
        auctionHasBids
        salePriceDecimalUSD
        currency
        source
        seller {
          id
          uuid
          __typename
        }
        __typename
      }
      defaultAuctionListing {
        id
        editionId
        priceDecimal
        auctionMinPriceDecimal
        auctionCloseAt
        mode
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
      defaultSaleListing {
        id
        editionId
        priceDecimal
        mode
        salePriceDecimalUSD
        currency
        source
        seller {
          id
          uuid
          __typename
        }
        __typename
      }
      defaultSecondaryListing {
        id
        editionId
        priceDecimal
        mode
        auctionHasBids
        currency
        salePriceDecimalUSD
        source
        seller {
          id
          uuid
          __typename
        }
        __typename
      }
      defaultSecondaryAuctionListing {
        id
        editionId
        priceDecimal
        auctionMinPriceDecimal
        auctionCloseAt
        mode
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
      defaultSecondarySaleListing {
        id
        editionId
        priceDecimal
        mode
        currency
        salePriceDecimalUSD
        source
        seller {
          id
          uuid
          __typename
        }
        __typename
      }
      likes
      recentLikes
      views
      recentViews
      isCurated
      isSoulbound
      defaultEditionId
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

CheckoutAmount = """
query CheckoutAmount($id: ID!) {
  checkout(id: $id) {
    amountDecimal
    __typename
  }
}
"""

GET_CRYPTO_PURCHASE = """
query getCryptoPurchases(
  $page: Int
  $perPage: Int
  $filterBy: PurchaseFilters
) {
  cryptoPurchases(page: $page, perPage: $perPage, filterBy: $filterBy) {
    nodes {
      id
      createdAt
      totalAmount
      cryptoAmount
      cryptoCurrency
      cryptoPurchaseStatus
      customerAccountId
      customerCardId
      customerCard {
        id
        lastFourDigits
        brand
        expiryDate
        fingerprint
        __typename
      }
      deviceId
      exchangeRate
      liveMode
      merchantId
      merchantName
      merchantReferenceId
      networkFee
      networkName
      paymentAmount
      paymentCurrency
      paymentId
      paymentMethod
      payoutTransactionId
      refUserId
      transactionFee
      walletAddress
      ixopay {
        adapterCode
        adapterMessage
        code
        merchantTransactionId
        message
        result
        __typename
      }
      __typename
    }
    pageInfo {
      pagesCount
      nodesCount
      currentPage
      hasNextPage
      hasPreviousPage
      __typename
    }
    __typename
  }
}
"""

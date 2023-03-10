GET_OPS_PAYOUTS = """
query ($page: Int, $perPage: Int, $filterBy: PayoutFilters) {
  payouts(page: $page, perPage: $perPage, filterBy: $filterBy) {
    nodes {
      id
      txnId
      approveMethod
      status
      currency
      amount
      amountInUsd
      fee
      feeInUsd
      description
      result
      merchantId
      merchantName
      createdAt
      updatedAt
      payoutAccountData {
        id
        accountType
        currency
        countryCode
        accountHolder
        accountHolderType
        firstAccountName
        lastAccountName
        businessAddress
        iban
        address
        via
        accountNumber
        addressType
        accountName
        beneficiaryAddress {
          city
          countryCode
          postalCode
          region
          streetAddress
          streetAddressTwo
        }
      }
    }
    pageInfo {
      pagesCount
      nodesCount
      currentPage
      hasNextPage
      hasPreviousPage
    }
  }
}
"""

GET_BALANCE_AND_ACCOUNT = """
query ($accountId: ID!, $teamId: ID!) {
  account(accountId: $accountId) {
    id
    balance {
      currency
      fiatSymbol
      totalBalance
      totalAvailable
      totalLocked
      wallets {
        id
        currency
        fiatSymbol
        available
        locked
        balance
        payoutMode
        nextPayoutDate
        payoutMinimumBalance
        autoPayoutPercentage
        convertMinimumBalance
      }
    }
  }
  team(teamId: $teamId) {
    defaultPayoutAccounts {
      walletCurrency
      currency
      accountType
      addressTypes {
        code
        name
        payoutMinimumBalance
      }
    }
  }
}
"""

UPDATE_OPS_PAYOUT_STATUS = """
    mutation UpdatePayout($payoutId: ID!, $status: String, $result: String) {
        updatePayout(input: { payoutId: $payoutId, status: $status, result: $result }) {
          payout {
            id
            status
            currency
            amount
            description
            result
            createdAt
            updatedAt
            payoutAccount {
              id
              status
              accountType
              currency
              countryCode
              accountHolder
              iban
              address
            }
        }
          errors {
            message
            path
          }
        }
    }
    """
GET_MERCHANT_PAYOUT_FEE = """
query getPayoutFee($teamId: ID!, $currency: String!) {
  team(teamId: $teamId) {
    payoutFee(currency: $currency) {
      feeRate
      minFee
    }
  }
}
"""

GET_OPS_AUTO_PAYOUT = """
mutation InvokeAutoPayout($scheduleType: String!, $accountId: String, $payoutAccountId: String) {
  invokeAutoPayout(
    input: { scheduleType: $scheduleType, accountId: $accountId, payoutAccountId: $payoutAccountId }
  ) {
    result
  }
}
"""

GET_CURRENCY_MINIMUM_AMOUNT = """
query ($teamId: ID!) {
  team(teamId: $teamId) {
    payoutFeeRate
    limitAmount {
      dailyAmount
      annualAmount
    }
    currencyMinimumAmounts {
      currency
      amount
    }
  }
  payoutAmountFee(teamId: $teamId) {
    currencyMinimumFees {
      currency
      fee
    }
    blockchainNetworkFees {
      currency
      fee
    }
    pricingMinimumAmounts {
      currency
      amount
    }
  }
}
"""

GET_PAYOUT_REPORT = """
query (
  $first: Int
  $last: Int
  $after: String
  $before: String
  $filterBy: PayoutFilters!
) {
  payouts(
    filterBy: $filterBy
    first: $first
    last: $last
    after: $after
    before: $before
  ) {
    nodes {
      legalEntity
      id
      status
      currency
      amount
      amountInUsd
      fee
      feeInUsd
      description
      result
      merchantId
      merchantName
      createdAt
      updatedAt
      processedAt
      payoutAccount {
        id
        status
        accountType
        currency
        countryCode
        accountHolder
        businessAddress
        iban
        address
      }
    }
    pageInfo {
      startCursor
      endCursor
      hasNextPage
      hasPreviousPage
    }
  }
}
"""

GET_CRYPTO_PURCHASE_AMOUNT = """
query getCryptoPurchases(
  $first: Int!
  $after: String
  $filterBy: CryptoPurchasesFilters
) {
  cryptoPurchases(first: $first, after: $after, filterBy: $filterBy) {
    nodes {
      cryptoPurchaseId
      merchantName
      merchantId
      paymentId
      cryptoPurchaseStatus
      paymentMethod
      cryptoCurrency
      cryptoAmount
      paymentCurrency
      paymentAmount
      paymentAmountInUsd
      exchangeRate
      networkName
      netAmount
      netAmountInUsd
      networkFee
      transactionFee
      paymentCreatedTime
      paymentCompletedTime
      customerAccountId
      refUserId
      deviceId
      networkFeeInUsd
      transactionFeeInUsd
      walletAddress
      customer {
        name
        address
        email
        birthday
      }
      customerCard {
        lastFourDigits
        brand
        fingerprint
      }
      ixopay {
        result
        merchantTransactionId
        code
        message
        adapterCode
        adapterMessage
      }
    }
    pageInfo {
      startCursor
      endCursor
      hasNextPage
      hasPreviousPage
    }
  }
}
"""


GET_CRYPTO_PURCHASE_CARD_INBOUND_DETAILS = """
query getCardInboundFunds($page: Int, $perPage: Int, $filterBy: CardInboundFundFilters) {
  cardInboundFunds(page: $page, perPage: $perPage, filterBy: $filterBy) {
    nodes {
      id
      paymentId
      purchaseId
      amount
      currency
      status
      reason
      reasonDetail
      createdAt
      updatedAt
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

GET_CRYPTO_PURCHASE_DETAILS = """
query getCryptoPurchases($page: Int, $perPage: Int, $filterBy: PurchaseFilters) {
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

GET_CRYPTO_PURCHASE_TROUBLESHOOTING_DETAILS = """
    query ($filterBy: TroubleshootingFilters!) {
      troubleshootingPayCoreGeneralQuery(filterBy: $filterBy)
    }
"""

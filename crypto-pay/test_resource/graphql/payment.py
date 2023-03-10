UPDATE_PAYMENT_SETTINGS = """
     mutation updatePaymentSettings(
        $teamId: ID!
        $preferredCurrency: String
        $creditToBaseCurrency: Boolean
        $paymentTimeOut: Int
    ) {
        updatePaymentSettings(
            input: {
                teamId: $teamId
                preferredCurrency: $preferredCurrency
                creditToBaseCurrency: $creditToBaseCurrency
                paymentTimeOut: $paymentTimeOut
            }
        ) {
            team {
                id
                preferredCurrency
                creditToBaseCurrency
                paymentTimeOut
            }
            errors {
                path
                message
            }
        }
    }
    """
CREATE_PAYMENT_REFUND = """
    mutation CreatePaymentRefund(
        $accountId: ID!
        $paymentId: ID!
        $amount: Float!
        $reason: String!
        $notes: String!,
        $email: String,
        $debitCurrency: String!) {
        createPaymentRefund(input: {
            accountId: $accountId
            paymentId: $paymentId
            amount: $amount
            reason: $reason
            notes: $notes
            email: $email
            debitCurrency: $debitCurrency
          }) {
          refund {
            id
            currency
            amount
            reason
            notes
            debitCurrency
            debitAmount
            fulfilledOnchain
            status
            cryptoCurrency
          }
          errors {
            path
            message
          }
        }
      }
    """

GET_OPS_ONCHAIN_INBOUND = """
query getInboundFunds($page: Int, $perPage: Int, $filterBy: InboundFundsFilters!) {
  inboundFunds(page: $page, perPage: $perPage, filterBy: $filterBy) {
    nodes {
      id
      amount
      currency
      paymentId
      txnId
      status
      sender
      recipient
      reason
      createdAt
      defiSwapTransaction {
        id
        createdAt
        status
        txnId
        txnValue
        txnEstimatedGas
        txnFrom
        amountIn
        amountInMax
        amountOut
        slippage
        allowance
        walletConnect
        approvalRequired
        gasPrice
        receivedAt
        confirmedAt
        approvalFrom
        approvalGas
        approvalTxnId
        approvalValue
        token {
          name
          address
          symbol
          decimals
          chainId
          balance
        }
      }
      payment {
        id
        txnId
        orderId
        merchantId
        merchantName
        cryptoCurrency
        cryptoAmount
        liveMode
        createdAt
        currency
        amount
        originalAmount
        status
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

GET_OPS_REFUND_HISTORY = """
query ($page: Int, $perPage: Int, $filterBy: RefundFilters!) {
  refunds(filterBy: $filterBy, page: $page, perPage: $perPage) {
    nodes {
      id
      paymentId
      customerEmail
      customerProvidedEmail
      status
      amount
      currency
      cryptoCurrency
      cryptoAmount
      createdAt
      liveMode
      isOnchain
      team {
        id
        name
      }
      subMerchantId
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

GET_OPS_ONCHAIN_OUTBOUND = """
query getOutboundFunds(
  $page: Int
  $perPage: Int
  $filterBy: OutboundFundsFilters!
) {
  outboundFunds(page: $page, perPage: $perPage, filterBy: $filterBy) {
    nodes {
      id
      email
      amount
      requestedAmount
      inboundFundId
      cryptoCurrency
      requestAt
      reason
      paymentId
      walletAddress
      txnId
      status
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

PROCESS_REBOUND = """
mutation ProcessRebound($outboundFundRequestId: ID!, $actionType: String!) {
  processRebound(input: {outboundFundRequestId: $outboundFundRequestId, actionType: $actionType}) {
    outboundFund {
      id
      email
      amount
      txnId
      status
      __typename
    }
    errors {
      message
      path
      __typename
    }
    __typename
  }
}
"""

GET_PAYMENT_SETTINGS = """
query ($teamId: ID!) {
  team(teamId: $teamId) {
    id
    preferredCurrency
    creditToBaseCurrency
    paymentTimeOut
    paymentMethods {
      nodes {
        enable
        name
      }
    }
    paymentThreshold {
      absolute {
        currency
        amount
      }
      relative {
        amount
      }
    }
  }
  walletCurrencies(teamId: $teamId)
}
"""

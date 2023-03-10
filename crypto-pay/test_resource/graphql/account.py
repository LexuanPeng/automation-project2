GET_PAY_ID_BY_ACCOUNT_ID = """
    query getAccount($accountId: ID!, $invoiceId: ID!) {
    account(accountId: $accountId) {
        invoice(invoiceId: $invoiceId) {
            paymentId
            }
        }
    }
    """

GET_INVOICES_BY_ACCOUNT_ID = """
    query getAccount($accountId: ID!) {
        account(accountId: $accountId) {
            invoices {
                nodes {
                    id
                    amount
                    status
                }
            }
        }
    }
    """

GET_PK_KEY_BY_ACCOUNT_ID = """
    query getAccount($accountId: ID!) {
        account(accountId: $accountId) {
            publishableKey
        }
    }
    """

GET_SECRET_KEY_BY_ACCOUNT_ID = """
    query ($accountId: ID!) {
      accountSecretKey(accountId: $accountId) {
        secretKey
      }
    }
"""

CREATE_CUSTOMER = """
    mutation createCustomer(
        $accountId: ID!
        $name: String!
        $email: String!
        $description: String!
      ) {
        createCustomer(
          input: {
            accountId: $accountId
            name: $name
            email: $email
            description: $description
          }
        ) {
          customer {
            id
            name
            email
            description
            referenceId
          }
          errors {
            path
            message
          }
        }
      }
    """

CREATE_PRODUCT = """
    mutation CreateProduct($accountId: ID!, $name: String!, $pricingPlans: [PricingPlanInput!]!)  {
      createProduct(input: {
        name: $name
        active: true,
        accountId: $accountId,
        pricingPlans: $pricingPlans
      }) {
        product {
          id
          active
          description
          metadata
          name
          pricingPlans {
            id
            active
            amount
            currency
            interval
            intervalCount
            metadata
            description
          }
        }
        errors {
          message
          path
        }
      }
    }
    """

UPDATE_OPS_PRODUCT_PERMISSION = """
mutation UpdateRole(
    $roleId: ID!
    $name: String
    $scopeLevel: String
    $description: String
    $permissions: [PermissionInput!]
  ) {
    updateRole(
      input: {
        roleId: $roleId
        name: $name
        scopeLevel: $scopeLevel
        description: $description
        permissions: $permissions
      }
    ) {
      role {
        name
        scopeLevel
        description
        permissions {
          controlScope
          controlActions {
            key
            value
          }
        }
      }
      errors {
        path
        message
      }
    }
  }
"""

GET_PRODUCT_ROLE_ID = """
{
  roles {
    nodes {
      id
      name
      description
      scopeLevel
      businessRole
    }
  }
}
"""

GET_OPS_TEAM_ID = """
query getMerchants(
  $page: Int
  $perPage: Int
  $sorter: SorterFilter
  $filterBy: TeamsFilters!
) {
  teams(page: $page, perPage: $perPage, sorter: $sorter, filterBy: $filterBy) {
    nodes {
      id
      businessRole
      name
      active
      legalEntityName
      kycStatus
      kycSubStatus
      kycRepresentativeEmail
      kycLevel
      liveAccountEnabled
      liveAccountId
      sandboxAccountId
      createdAt
      updatedAt
      oneDayTransactionsVolume
      referralCode
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

GET_OPS_TERM_INFO = """
query ($teamId: ID!) {
  team(teamId: $teamId) {
    id
    name
    kycLevel
    supportEmail
    kycStatus
    riskScore
    cashbackRate
    missInfoReasons
    rejectReasons
    termVersion
    termLegalEntity
    termTrack {
      id
      termVersion
      legalEntity
      termsAcceptedAt
      __typename
    }
    noLiveTxReminded
    notUsedTxReminded
    dailyLimitAmount
    annualLimitAmount
    limitAmount {
      kycOneDailyAmount
      kycOneAnnualAmount
      kycTwoDailyAmount
      kycTwoAnnualAmount
      kycThreeDailyAmount
      kycThreeAnnualAmount
      __typename
    }
    thirtyDaysTransactionsVolume
    oneDayTransactionsVolume
    annualTransactionVolume
    active
    liveAccountEnabled
    payoutFeeRate
    website
    legalEntityName
    taxId
    preferredCurrency
    businessCategory
    businessIndustry
    businessDescription
    registrationNumber
    businessAddress
    incorporationCountry
    operationalAddress
    operationalProvince
    operationalRegion
    operationalZipCode
    operationalCountry
    featureFlags
    featureFlagsSelected
    internalNote
    enableOnchainPayment
    referralCode
    documentsFeedback
    firstSubmittedKycTime
    requiredEdd
    purposeOfUsage {
      invoicing
      onlineCheckout
      merchantPlatform
      ownerSharesHolder
      __typename
    }
    additionalDocumentRecords {
      id
      documentType
      documentTooltip
      attachmentId
      internal
      documentName
      isRequired
      additionalAttachment {
        id
        name
        filename
        kycStatus
        url
        __typename
      }
      __typename
    }
    defaultCurrencies
    defaultCurrencyOptions
    representative {
      id
      userId
      firstName
      lastName
      dateOfBirth
      idCard
      taxId
      homeAddress
      region
      zipCode
      province
      country
      __typename
    }
    anticipatedDaily {
      dailyVolume {
        id
        range
        __typename
      }
      dailyCustomer {
        id
        range
        __typename
      }
      monthlyPayout {
        id
        range
        __typename
      }
      __typename
    }
    businessOwners {
      nodes {
        id
        userId
        firstName
        lastName
        dateOfBirth
        idCard
        taxId
        homeAddress
        region
        zipCode
        province
        country
        __typename
      }
      __typename
    }
    __typename
  }
  countries {
    code
    name
    __typename
  }
  businessCategories {
    key
    name
    __typename
  }
  businessIndustries {
    key
    name
    __typename
  }
  merchantPlatforms
  onchainAllowCountries
}
"""

GET_SUB_MERCHANT_MCC_CODE = """
query getMccCodes {
  mccCodes {
    code
    desc
    __typename
  }
}
"""

UPDATE_PAYOUT_ACCOUNT_INFO = """
mutation UpdatePayoutAccount(
  $payoutAccountId: ID!
  $accountHolder: String
  $iban: String
  $countryCode: String
  $address: String
  $businessAddress: String
  $mode: String
  $addressType: String
  $autoPayoutSettings: AutoPayoutSettingsInput
  $via: String
  $accountName: String
  $accountNumber: String
  $routingNumber: String
  $achCheckType: String
  $achAccountType: String
  $label: String
  $bankName: String
  $bsbNumber: String
  $swiftCode: String
  $intermediaryBankName: String
  $intermediaryBankReference: String
  $haveFurtherCreditAccount: Boolean
  $furtherCreditAccountName: String
  $furtherCreditAccountNumber: String
  $intermediaryBankAddress: PayoutAccountAddressInput
  $beneficiaryAddress: PayoutAccountAddressInput
  $clientMutationId: String
  $accountHolderType: String
  $firstAccountName: String
  $lastAccountName: String
  $beneficiaryEmailAddress: String
  $beneficiaryEinTin: String
) {
  updatePayoutAccount(
    input: {
      payoutAccountId: $payoutAccountId
      accountHolder: $accountHolder
      iban: $iban
      countryCode: $countryCode
      address: $address
      businessAddress: $businessAddress
      mode: $mode
      addressType: $addressType
      autoPayoutSettings: $autoPayoutSettings
      via: $via
      accountName: $accountName
      accountNumber: $accountNumber
      routingNumber: $routingNumber
      achCheckType: $achCheckType
      achAccountType: $achAccountType
      label: $label
      bankName: $bankName
      swiftCode: $swiftCode
      intermediaryBankName: $intermediaryBankName
      intermediaryBankReference: $intermediaryBankReference
      haveFurtherCreditAccount: $haveFurtherCreditAccount
      furtherCreditAccountName: $furtherCreditAccountName
      furtherCreditAccountNumber: $furtherCreditAccountNumber
      intermediaryBankAddress: $intermediaryBankAddress
      beneficiaryAddress: $beneficiaryAddress
      clientMutationId: $clientMutationId
      accountHolderType: $accountHolderType
      firstAccountName: $firstAccountName
      lastAccountName: $lastAccountName
      beneficiaryEmailAddress: $beneficiaryEmailAddress
      beneficiaryEinTin: $beneficiaryEinTin
      bsbNumber: $bsbNumber
    }
  ) {
    payoutAccount {
      id
      status
      accountType
      currency
      countryCode
      accountHolder
      accountHolderType
      firstAccountName
      lastAccountName
      beneficiaryEmailAddress
      beneficiaryEinTin
      iban
      address
      addressType
      businessAddress
      mode
      autoPayoutSettings {
        scheduleType
        percentage
      }
    }
    errors {
      message
      path
    }
  }
}
"""

GET_PAYOUT_ID_BY_TEAM_ID = """
query ($teamId: ID!) {
  team(teamId: $teamId) {
    id
    ibanMaxLength
    defaultPayoutAccounts {
      walletCurrency
      currency
      accountType
      addressTypes {
        code
        name
        payoutMinimumBalance
        __typename
      }
      ibanConfig {
        countryCode
        countryName
        ibanLength
        __typename
      }
      __typename
    }
    payoutAccounts {
      accountHolder
      accountName
      accountNumber
      accountType
      achAccountType
      achCheckType
      address
      addressName
      addressType
      autoPayoutSettings {
        nextPayoutDate
        percentage
        scheduleType
        __typename
      }
      bankName
      beneficiaryAddress {
        city
        countryCode
        postalCode
        region
        streetAddress
        streetAddressTwo
        __typename
      }
      businessAddress
      countryCode
      createdAt
      currency
      furtherCreditAccountName
      furtherCreditAccountNumber
      haveFurtherCreditAccount
      iban
      id
      intermediaryBankAddress {
        city
        countryCode
        postalCode
        region
        streetAddress
        streetAddressTwo
        __typename
      }
      intermediaryBankName
      intermediaryBankReference
      label
      mode
      payoutMinimumBalance
      routingNumber
      status
      swiftCode
      via
      walletCurrency
      __typename
    }
    __typename
  }
}

"""

GET_PAYMENT_CURRENCY = """
{
  paymentCurrencies {
    currency
    exponent
    precision
  }
}
"""

UPDATE_SHOP_DETAIL = """
mutation updateShopDetail(
  $teamId: ID!
  $incorporationCountry: String
  $businessCategory: String!
  $legalEntityName: String
  $taxId: String
  $registrationNumber: String
  $businessAddress: String!
  $businessAddress2: String
  $region: String!
  $zipCode: String!
  $province: String!
  $operationalAddress: String
  $operationalAddress2: String
  $operationalProvince: String
  $operationalRegion: String
  $operationalZipCode: String
  $operationalCountry: String
) {
  updateShopDetail(
    input: {
      teamId: $teamId
      incorporationCountry: $incorporationCountry
      businessCategory: $businessCategory
      registrationNumber: $registrationNumber
      legalEntityName: $legalEntityName
      taxId: $taxId
      businessAddress: $businessAddress
      businessAddress2: $businessAddress2
      region: $region
      zipCode: $zipCode
      province: $province
      operationalAddress: $operationalAddress
      operationalAddress2: $operationalAddress2
      operationalProvince: $operationalProvince
      operationalRegion: $operationalRegion
      operationalZipCode: $operationalZipCode
      operationalCountry: $operationalCountry
    }
  ) {
    team {
      id
      name
      preferredCurrency
      kycStatus
      termVersion
      creditToBaseCurrency
      businessSettings {
        businessCategory
        country
        registrationNumber
        legalEntityName
        taxId
        businessAddress
        region
        zipCode
        province
        __typename
      }
      __typename
    }
    errors {
      path
      message
      __typename
    }
    __typename
  }
}
"""

GET_TEAM_NOTIFICATIONS = """
query getTeamNotifications(
  $page: Int
  $perPage: Int
  $teamId: ID!
  $status: String
) {
  teamNotifications(
    page: $page
    perPage: $perPage
    teamId: $teamId
    status: $status
  ) {
    nodes {
      id
      notifyType
      createdAt
      status
      payload {
        title
        message
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
GET_CUSTOMER = """
query getCustomers(
  $accountId: ID!
  $page: Int
  $perPage: Int
  $filterBy: CustomerFilters
) {
  account(accountId: $accountId) {
    id
    customers(filterBy: $filterBy, page: $page, perPage: $perPage) {
      nodes {
        id
        email
        name
        description
        createdAt
        referenceId
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
}
"""

DELETE_CUSTOMER = """
mutation deleteCustomer($accountId: ID!, $customerId: ID!) {
  deleteCustomer(input: { accountId: $accountId, customerId: $customerId }) {
    account {
      id
      customers {
        nodes {
          id
          email
        }
        pageInfo {
          hasNextPage
        }
      }
    }
    errors {
      path
      message
    }
  }
}

"""

UPDATE_CUSTOMER = """
mutation updateCustomer(
  $customerId: ID!
  $email: String
  $name: String
  $description: String
  $customerDetails: CustomerDetailsInput
) {
  updateCustomer(
    input: {
      customerId: $customerId
      email: $email
      name: $name
      description: $description
      customerDetails: $customerDetails
    }
  ) {
    customer {
      id
      email
      name
      description
      referenceId
      customerDetails {
        billingDetails {
          address
          address2
          city
          state
          country
          postalCode
          phone
        }
        shippingDetails {
          address
          address2
          city
          state
          country
          postalCode
          phone
        }
        shippingDiffBilling
      }
    }
    errors {
      path
      message
    }
  }
}
"""

OPS_UPDATE_PAYOUT_ACCOUNT = """
mutation UpdatePayoutAccount($payoutAccountId: ID!, $status: String) {
  updatePayoutAccount(input: {payoutAccountId: $payoutAccountId, status: $status}) {
    payoutAccount {
      id
      status
      accountType
      currency
      countryCode
      accountHolder
      accountHolderType
      businessAddress
      iban
      address
      via
      accountName
      accountNumber
      routingNumber
      achCheckType
      achAccountType
      label
      bankName
      swiftCode
      firstAccountName
      lastAccountName
      beneficiaryEmailAddress
      beneficiaryEinTin
      intermediaryBankName
      intermediaryBankReference
      haveFurtherCreditAccount
      furtherCreditAccountName
      furtherCreditAccountNumber
      createdAt
      updatedAt
      team {
        id
        active
        name
        kycLevel
        kycStatus
        updatedAt
        legalEntityName
        liveAccountEnabled
        liveAccountId
      }
    }
    errors {
      message
      path
    }
  }
}
"""
UPDATE_CARD_PAYMENT = """
mutation updatePayChannel($teamId: ID!, $channel: String!, $enabled: Boolean!) {
  updatePayChannel(input: {teamId: $teamId, channel: $channel, enabled: $enabled}) {
    paymentMethods {
      enable
      name
      __typename
    }
    errors {
      path
      message
      __typename
    }
    __typename
  }
}
"""

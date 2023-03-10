GET_TEAMS = """
    query {
        viewer {
            id
            teams {
                id
                name
                liveAccount {
                    id
                    enabled
                }
                sandboxAccount {
                    id
                    enabled
                }
            }
        }
    }
    """
GET_PAYOUT_ACCOUNTS = """
  query getPayoutAccounts($teamId: ID!) {
    team(teamId: $teamId) {
      id
      defaultPayoutAccounts {
        walletCurrency
        currency
        accountType
        addressTypes {
          code
          name
          payoutMinimumBalance
        }
        ibanConfig {
          countryCode
          countryName
          ibanLength
        }
      }
    }
  }
"""

CREATE_TEAM = """
    mutation CreateTeam(
    $name: String!
    $website: String!
    $preferredCurrency: String!
    $referralCode: String
    $businessCategory: String!
    $businessRole: String!
    $dailyVolume: String!
    ) {
      createTeam(
        input: {
          name: $name
          website: $website
          preferredCurrency: $preferredCurrency
          referralCode: $referralCode
          businessCategory: $businessCategory
          businessRole: $businessRole
          dailyVolume: $dailyVolume
        }
      ) {
        team {
          id
          name
          termVersion
          cashbackRate
          kycLevel
          limitAmount {
            kycOneDailyAmount
            kycOneAnnualAmount
            kycTwoDailyAmount
            kycTwoAnnualAmount
            kycThreeDailyAmount
            kycThreeAnnualAmount
          }
          businessSettings {
            website
            businessCategory
          }
          preferredCurrency
          liveAccount {
            id
            enabled
          }
          sandboxAccount {
            id
            enabled
          }
          invitedByReferral
          businessRole
          role {
            id
            name
            description
            permissions {
              controlScope
              controlActions {
                key
                value
              }
            }
          }
          roles {
            id
            name
            description
            permissions {
              controlScope
              controlActions {
                key
                value
              }
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

OPS_UPDATE_TEAM = """
mutation UpdateTeam(
  $teamId: ID!
  $name: String
  $businessRole: String
  $preferredCurrency: String
  $kycLevel: Int
  $riskScore: String
  $kycStatus: String
  $kycSubStatus: String
  $kycRepresentativeEmail: String
  $missInfoReasons: [KycMissingReason!]
  $rejectReasons: [String!]
  $active: Int
  $liveAccountEnabled: Int
  $enableOnchainPayment: Int
  $internalNote: String
  $payoutFeeRate: String
  $payoutNetworkFeeDiscountRate: String
  $paylaterFeeRate: String
  $configurations: JSON
  $dailyPayoutCount: Int
  $subMerchantLimitCount: Int
  $website: String
  $websiteServicePolicy: Boolean
  $supportEmail: String
  $featureFlags: String
  $businessCategory: String
  $businessIndustry: String
  $businessDescription: String
  $registrationNumber: String
  $businessAddress: String
  $businessAddress2: String
  $incorporationCountry: String
  $legalEntityName: String
  $region: String
  $zipCode: String
  $province: String
  $dailyLimitAmount: String
  $annualLimitAmount: String
  $requiredEdd: Boolean
  $taxId: String
  $defaultCurrencies: [String!]
  $creditToBaseCurrency: Boolean
  $representativeId: ID
  $representativeFirstName: String
  $representativeLastName: String
  $representativeDateOfBirth: String
  $representativeTaxId: String
  $representativeIdCard: String
  $representativeHomeAddress: String
  $representativeHomeAddress2: String
  $representativeRegion: String
  $representativeZipCode: String
  $representativeProvince: String
  $representativeCountry: String
  $representativeNationality: String
) {
  updateTeam(
    input: {
      teamId: $teamId
      name: $name
      businessRole: $businessRole
      preferredCurrency: $preferredCurrency
      kycLevel: $kycLevel
      riskScore: $riskScore
      kycStatus: $kycStatus
      kycSubStatus: $kycSubStatus
      kycRepresentativeEmail: $kycRepresentativeEmail
      missInfoReasons: $missInfoReasons
      rejectReasons: $rejectReasons
      active: $active
      liveAccountEnabled: $liveAccountEnabled
      enableOnchainPayment: $enableOnchainPayment
      internalNote: $internalNote
      payoutFeeRate: $payoutFeeRate
      payoutNetworkFeeDiscountRate: $payoutNetworkFeeDiscountRate
      paylaterFeeRate: $paylaterFeeRate
      configurations: $configurations
      dailyPayoutCount: $dailyPayoutCount
      subMerchantLimitCount: $subMerchantLimitCount
      website: $website
      websiteServicePolicy: $websiteServicePolicy
      supportEmail: $supportEmail
      legalEntityName: $legalEntityName
      featureFlags: $featureFlags
      businessCategory: $businessCategory
      businessIndustry: $businessIndustry
      businessDescription: $businessDescription
      registrationNumber: $registrationNumber
      businessAddress: $businessAddress
      businessAddress2: $businessAddress2
      incorporationCountry: $incorporationCountry
      region: $region
      zipCode: $zipCode
      province: $province
      dailyLimitAmount: $dailyLimitAmount
      annualLimitAmount: $annualLimitAmount
      requiredEdd: $requiredEdd
      taxId: $taxId
      defaultCurrencies: $defaultCurrencies
      creditToBaseCurrency: $creditToBaseCurrency
      representativeId: $representativeId
      representativeFirstName: $representativeFirstName
      representativeLastName: $representativeLastName
      representativeDateOfBirth: $representativeDateOfBirth
      representativeTaxId: $representativeTaxId
      representativeIdCard: $representativeIdCard
      representativeHomeAddress: $representativeHomeAddress
      representativeHomeAddress2: $representativeHomeAddress2
      representativeRegion: $representativeRegion
      representativeZipCode: $representativeZipCode
      representativeProvince: $representativeProvince
      representativeCountry: $representativeCountry
      representativeNationality: $representativeNationality
    }
  ) {
    team {
      id
      name
      kycLevel
      supportEmail
      kycStatus
      kycSubStatus
      kycRepresentativeEmail
      riskScore
      cashbackRate
      missInfoReasons {
        id
        description
        __typename
      }
      rejectReasons
      termVersion
      dailyPayoutCount
      subMerchantLimitCount
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
      websiteServicePolicy
      thirtyDaysTransactionsVolume
      oneDayTransactionsVolume
      annualTransactionVolume
      active
      liveAccountEnabled
      payoutFeeRate
      payoutNetworkFeeDiscountRate
      paylaterFeeRate
      configurations
      website
      legalEntityName
      taxId
      preferredCurrency
      incorporationCountry
      businessRole
      businessCategory
      businessIndustry
      province
      region
      zipCode
      businessDescription
      registrationNumber
      businessAddress
      businessAddress2
      featureFlags
      featureFlagsSelected
      internalNote
      enableOnchainPayment
      referralCode
      requiredEdd
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
      creditToBaseCurrency
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
        nationality
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
    errors {
      path
      message
      __typename
    }
    __typename
  }
}
 """

OPS_GET_TEAM = """
query ($teamId: ID!) {
  team(teamId: $teamId) {
    id
    name
    businessRole
    kycLevel
    supportEmail
    kycStatus
    kycSubStatus
    kycRepresentativeEmail
    riskScore
    cashbackRate
    firstLivePaymentCapturedTime
    missInfoReasons {
      id
      description
    }
    rejectReasons
    termVersion
    termLegalEntity
    dailyPayoutCount
    termTrack {
      id
      termVersion
      legalEntity
      termsAcceptedAt
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
    }
    subMerchantLimitCount
    websiteServicePolicy
    thirtyDaysTransactionsVolume
    oneDayTransactionsVolume
    annualTransactionVolume
    active
    liveAccountEnabled
    payoutFeeRate
    payoutNetworkFeeDiscountRate
    paylaterFeeRate
    configurations
    website
    legalEntityName
    taxId
    preferredCurrency
    businessCategory
    businessIndustry
    riskLevel
    businessIndustry
    businessDescription
    registrationNumber
    businessAddress
    businessAddress2
    province
    region
    zipCode
    incorporationCountry
    operationalAddress
    operationalAddress2
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
    }
    additionalDocumentRecords {
      id
      documentType
      documentTooltip
      attachmentId
      internal
      documentName
      isRequired
      status
      additionalAttachment {
        id
        name
        filename
        kycStatus
        url
      }
    }
    defaultCurrencies
    defaultCurrencyOptions
    creditToBaseCurrency
    representative {
      id
      userId
      firstName
      lastName
      dateOfBirth
      idCard
      taxId
      homeAddress
      homeAddress2
      region
      zipCode
      province
      country
      nationality
    }
    anticipatedDaily {
      dailyVolume {
        id
        range
      }
      dailyCustomer {
        id
        range
      }
      monthlyPayout {
        id
        range
      }
    }
    avatarUrl
    productImgUrl
    serviceRegion
    serviceCountry
  }
  countries {
    code
    name
  }
  businessCategories {
    key
    name
  }
  businessIndustries {
    key
    name
  }
  merchantPlatforms
}
"""

OPS_SENT_KYC_EMAIL = """
mutation KycStatusEmail($teamId: ID!) {
    kycStatusEmail(input: {teamId: $teamId}) {
        errors {
            message
            path
            __typename
        }
    __typename
    }
}
"""

GET_OVERVIEW_INFO = """
query ($accountId: ID!, $fromTime: String!, $toTime: String!, $period: String!) {
  account(accountId: $accountId) {
    id
    metrics(fromTime: $fromTime, toTime: $toTime, period: $period) {
      currency
      fiatSymbol
      grossVolume
      refundVolume
      customers
      successfulPayments
      grossVolumeBreakdown {
        x
        y
        __typename
      }
      refundVolumeBreakdown {
        x
        y
        __typename
      }
      customersBreakdown {
        x
        y
        __typename
      }
      successfulPaymentsBreakdown {
        x
        y
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

OPS_GET_MISSING_INFO_REASONS = """
query getMissingInfoReasons(
  $filterBy: KycMissingInfoReasonsFilters
  $page: Int
  $perPage: Int
) {
  missInfoReasons(filterBy: $filterBy, page: $page, perPage: $perPage) {
    nodes {
      id
      description
      isTemplate
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

GET_ACCOUNT_ID_BY_TEAM_ID = """
query Team($teamId: ID!) {
  team(teamId: $teamId) {
    id
    name
    avatarUrl
    preferredCurrency
    supportEmail
    liveAccount {
      id
      enabled
    }
  }
}
"""

GET_MERCHANTS = """
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

GET_TEAM_ANTICIPATED_INFO = """
query getTeamAnticipatedInfo {
  teamAnticipatedInfo {
    defaultAnticipated {
      anticipatedType
      range {
        id
        min
        max
      }
    }
  }
}
"""

OPS_UPDATE_SUBMERCHANT = """
mutation UpdateSubMerchant(
  $subMerchantId: ID!
  $name: String
  $supportEmail: String
  $riskScore: String
  $internalNote: String
  $liveAccountEnabled: Int
  $businessSettings: BusinessSettings
  $representative: Representative
) {
  updateSubMerchant(
    input: {
      subMerchantId: $subMerchantId
      name: $name
      supportEmail: $supportEmail
      riskScore: $riskScore
      internalNote: $internalNote
      liveAccountEnabled: $liveAccountEnabled
      businessSettings: $businessSettings
      representative: $representative
    }
  ) {
    subMerchant {
      id
      name
      accountId
      externalId
      liveAccountEnabled
      supportEmail
      createdAt
      updatedAt
      cashbackRate
      riskScore
      internalNote
      oneDayTransactionsVolume
      thirtyDaysTransactionsVolume
      annualTransactionVolume
      representative {
        id
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
      }
      businessOwners {
        nodes {
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
        }
      }
      additionalDocumentRecords {
        id
        subMerchantId
        documentType
        documentName
        attachmentId
        internal
        documentTooltip
        additionalAttachment {
          id
          name
          filename
          kycStatus
          url
        }
      }
      businessSettings {
        website
        legalEntityName
        businessCategory
        businessIndustry
        registrationNumber
        businessAddress
        incorporationCountry
      }
    }
    errors {
      path
      message
    }
  }
}
"""

OPS_GET_SUBMERCHANT = """
query getSubMerchants(
  $filterBy: SubMerchantsFilters
  $sorter: SubMerchantSorterFilter
  $page: Int
  $perPage: Int
) {
  subMerchants(
    filterBy: $filterBy
    sorter: $sorter
    page: $page
    perPage: $perPage
  ) {
    nodes {
      id
      name
      createdAt
      updatedAt
      acquirerId
      acquirerName
      supportEmail
      cashbackRate
      externalId
      liveAccountEnabled
      oneDayTransactionsVolume
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

OPS_GET_PAYOUT_ACCOUNTS = """
query getPayoutAccounts($page: Int, $perPage: Int, $filterBy: PayoutAccountFilters) {
  payoutAccounts(page: $page, perPage: $perPage, filterBy: $filterBy) {
    nodes {
      id
      status
      accountType
      currency
      countryCode
      accountHolder
      accountHolderType
      accountHolderName
      firstAccountName
      lastAccountName
      businessAddress
      iban
      address
      via
      accountNumber
      addressType
      accountName
      bankName
      bsbNumber
      routingNumber
      achCheckType
      achAccountType
      label
      swiftCode
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
        kycSubStatus
        updatedAt
        legalEntityName
        fullLegalName
        liveAccountEnabled
        liveAccountId
        businessCategory
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

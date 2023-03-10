authenicateByEmail = """
    fragment PreAuthV2Response on PreAuthV2 {
      lastLoginAt
      requiredSteps
      token
      unauthorizedMe {
        email
        name
        username
        uuid
        __typename
      }
      __typename
    }
    mutation authenticateByEmail(
      $email: String!
      $password: String!
      $recaptcha: RecaptchaArgs!
    ) {
      authenticateByEmail(
        email: $email
        password: $password
        recaptcha: $recaptcha
      ) {
        ...PreAuthV2Response
        __typename
      }
    }
"""

prepareEmailOtp = """
  mutation prepareEmailOtp {
    prepareOtp {
      success
      __typename
    }
  }
"""

continueAuthentication = """
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

    mutation continueAuthentication(
      $clientOtpCode: String
      $emailOtpCode: String
      $smsOtpCode: String
    ) {
      continueAuthentication(
        clientOtpCode: $clientOtpCode
        emailOtpCode: $emailOtpCode
        smsOtpCode: $smsOtpCode
      ) {
        __typename
        ... on AuthV2 {
          me {
            ...MeResponse
            __typename
          }
          token
          __typename
        }
        __typename
        ... on ContinueAuth {
          requiredSteps
          token
          unauthorizedMe {
            email
            name
            username
            uuid
            registrationCompleted
            __typename
          }
          __typename
        }
      }
    }
"""

authenticate = """
  mutation authenticate(
    $email: String!
    $password: String!
    $recaptcha: RecaptchaArgs!
  ) {
    authenticate(email: $email, password: $password, recaptcha: $recaptcha) {
      token
      me {
        uuid
        email
        clientOtpEnabled
        __typename
      }
      __typename
    }
  }
"""

authenticateWithOtp = """
  mutation authenticateWithOtp($otpCode: String, $clientOtpCode: String) {
    authenticateWithOtp(otpCode: $otpCode, clientOtpCode: $clientOtpCode) {
      token
      me {
        ...MeResponse
        __typename
      }
      lastLoginAt
      __typename
    }
  }

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
    __typename
  }
"""

requestQrCodeLogin = """
  mutation requestQrCodeLogin($ott: String!) {
    requestQrCodeLogin(ott: $ott) {
      encodedQr
      sessionId
      status
      __typename
    }
  }
"""

getQrCodeLoginStatus = """
  mutation getQrCodeLoginStatus {
    qrCodeLoginStatus {
      status
      __typename
    }
  }
"""

authenticateByQrCode = """
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

    fragment PreAuthV2Response on PreAuthV2 {
      lastLoginAt
      requiredSteps
      token
      unauthorizedMe {
        email
        name
        username
        uuid
        registrationCompleted
        __typename
      }
      __typename
    }

    mutation authenticateByQrCode($recaptcha: RecaptchaArgs!) {
      authenticateByQrCode(recaptcha: $recaptcha) {
        __typename
        ... on AuthV2 {
          me {
            ...MeResponse
            __typename
          }
          token
          __typename
        }
        __typename
        ... on PreAuthV2 {
          ...PreAuthV2Response
          __typename
        }
      }
    }
"""

logout = """
  mutation logout {
    logout
  }
"""

sendSmsCode = """
mutation sendSmsCode($phoneNumber: String, $recaptcha: RecaptchaArgs!) {
  sendSmsCode(phoneNumber: $phoneNumber, recaptcha: $recaptcha) {
    maskedRecipientPhoneNumber
    __typename
  }
}
"""

requestResetPassword = """
mutation requestResetPasswordV2($email: String!, $recaptcha: RecaptchaArgs!) {
  requestResetPasswordV2(email: $email, recaptcha: $recaptcha) {
    status
    token
    __typename
  }
}
"""

refreshToken = """
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
  mainAppCountryCode
  phoneNumber
  isPhoneNumberVerified
  mainAppPhoneCountryCode
  isPriceAlertLimitReached
  isWatchlistLimitReached
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
  purchasedCount
  canManageDrop
  __typename
}

mutation refreshToken {
  refreshToken {
    token
    me {
      ...MeResponse
      __typename
    }
    __typename
  }
}
"""

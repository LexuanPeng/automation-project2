CREATE_PAYOUT_ACCOUNT = """
    mutation CreatePayoutAccount(
      $teamId: ID!
      $walletCurrency: String!
      $currency: String!
      $countryCode: String
      $accountHolder: String
      $accountHolderType: String
      $iban: String
      $address: String
      $addressType: String!
      $businessAddress: String
      $firstAccountName: String
      $lastAccountName: String
      $mode: String
      $autoPayoutSettings: AutoPayoutSettingsInput
      $via: String
      $beneficiaryEmailAddress: String
      $beneficiaryEinTin: String
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
    ) {
      createPayoutAccount(
        input: {
          teamId: $teamId
          walletCurrency: $walletCurrency
          currency: $currency
          countryCode: $countryCode
          accountHolder: $accountHolder
          accountHolderType: $accountHolderType
          iban: $iban
          address: $address
          addressType: $addressType
          businessAddress: $businessAddress
          firstAccountName: $firstAccountName
          lastAccountName: $lastAccountName
          mode: $mode
          autoPayoutSettings: $autoPayoutSettings
          via: $via
          beneficiaryEmailAddress: $beneficiaryEmailAddress
          beneficiaryEinTin: $beneficiaryEinTin
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
          bsbNumber: $bsbNumber
        }
      ) {
        payoutAccount {
          id
          status
          accountType
          currency
          walletCurrency
          countryCode
          accountHolder
          accountHolderType
          iban
          address
          addressType
          businessAddress
          createdAt
          mode
          firstAccountName
          lastAccountName
          beneficiaryEmailAddress
          beneficiaryEinTin
          autoPayoutSettings {
            scheduleType
            percentage
            nextPayoutDate
            __typename
          }
          via
          accountName
          accountNumber
          routingNumber
          achCheckType
          achAccountType
          label
          bankName
          swiftCode
          intermediaryBankName
          intermediaryBankReference
          haveFurtherCreditAccount
          furtherCreditAccountName
          furtherCreditAccountNumber
          intermediaryBankAddress {
            countryCode
            streetAddress
            streetAddressTwo
            city
            region
            postalCode
            __typename
          }
          beneficiaryAddress {
            countryCode
            streetAddress
            streetAddressTwo
            city
            region
            postalCode
            __typename
          }
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

CREATE_SHOP_OWNER = """
    mutation CreateShopOwner(
      $teamId: ID!
      $userId: String
      $firstName: String!
      $lastName: String!
      $dateOfBirth: String
      $taxId: String
      $idCard: String
      $homeAddress: String
      $homeAddress2: String
      $region: String
      $zipCode: String
      $province: String
      $country: String
      $isRepresentative: Boolean!
      $nationality: String!
    ) {
      createShopOwner(
        input: {
          teamId: $teamId
          userId: $userId
          firstName: $firstName
          lastName: $lastName
          dateOfBirth: $dateOfBirth
          taxId: $taxId
          idCard: $idCard
          homeAddress: $homeAddress
          homeAddress2: $homeAddress2
          region: $region
          zipCode: $zipCode
          province: $province
          country: $country
          isRepresentative: $isRepresentative
          nationality: $nationality
        }
      ) {
        team {
          id
          representative {
            id
            userId
            firstName
            lastName
            dateOfBirth
            homeAddress
            homeAddress2
            region
            zipCode
            province
            country
            nationality
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

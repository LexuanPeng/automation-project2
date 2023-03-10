ACCEPT_TERMS = """
    mutation acceptTerms($teamId: ID!, $kycChanged: Boolean) {
      acceptTerms(input: { teamId: $teamId, kycChanged: $kycChanged }) {
        team {
          id
          kycStatus
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

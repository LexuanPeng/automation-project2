OPS_GET_USERS_BY_KEYWORDS = """
query User(
    $first: Int
    $last: Int
    $after: String
    $before: String
    $filterBy: UsersFilters!
  ) {
    users(
      first: $first
      last: $last
      after: $after
      before: $before
      filterBy: $filterBy
    ) {
      nodes {
        id
        firstName
        lastName
        email
        createdAt
        totpEnabled
      }
      pageInfo {
        startCursor
        hasNextPage
        endCursor
        hasPreviousPage
      }
    }
  }
"""
OPS_GET_USER_BY_ID = """
 query ($userId: ID!) {
    user(userId: $userId) {
      id
      firstName
      lastName
      email
      emailConfirmed
      phone
      phoneConfirmed
      totpEnabled
      teams {
        id
        name
        disable(userId: $userId)
      }
    }
  }
"""

OPS_DISABLE_TOTP = """
mutation DisableTotp($userId: ID!) {
    disableTotp(input: { userId: $userId }) {
      user {
        id
        totpEnabled
      }
    }
  }
"""

OPS_ADD_RISK_ADDRESS = """
mutation AddHighRiskAddress($address: String!) {
    addHighRiskAddress(input: { address: $address }) {
      address
      errors {
        path
        message
      }
    }
  }
"""

OPS_REMOVE_RISK_ADDRESS = """
mutation RemoveHighRiskAddress($address: String!) {
    removeHighRiskAddress(input: { address: $address }) {
      address
    }
  }
"""

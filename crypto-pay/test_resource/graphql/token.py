CREATE_TOKEN = """
    mutation CreateToken($email: String!, $password: String!, $captcha: CaptchaInput!) {
    createToken(input: {
        email: $email, password: $password, captcha: $captcha
        }) {
             token
            totp
            __typename
        }
    }
    """
CREATE_CAPTCHA = """
    mutation CreateCaptcha {
        createCaptcha(input: {}) {
            fallback
            challenge
            geetestId
            newCaptcha
            signature
        }
    }
    """

CREATE_REGISTRATION = """
mutation CreateRegistration(
  $firstName: String!
  $lastName: String!
  $email: String!
  $password: String!
  $invitationId: ID
  $referralCode: String
  $captcha: CaptchaInput!
) {
  createRegistration(
    input: {
      firstName: $firstName
      lastName: $lastName
      email: $email
      password: $password
      invitationId: $invitationId
      referralCode: $referralCode
      captcha: $captcha
    }
  ) {
    errors {
      path
      message
    }
  }
}
"""

GET_SAFE_HEADERS = """
 query {
    safeHeaders {
      publicKey
    }
  }
"""

ACTIVATE_REGISTRATION = """
mutation activateRegistration($signupIntentToken: String!, $userId: ID!) {
  activateRegistration(
    input: { signupIntentToken: $signupIntentToken, userId: $userId }
  ) {
    token
    errors {
      path
      message
    }
  }
}
"""

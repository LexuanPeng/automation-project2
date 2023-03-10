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
        token
        viewer {
            id
        }
        errors {
            message
            path
        }
        }
    }
    """
GET_SAFE_HEADERS = """
    safeHeaders {
            publicKey
    }
    """

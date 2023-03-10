import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import test_resource.graphql as gql
import requests
import logging

from common.api import StagingPayment
from common.utils.gmail_helper import GmailHelper

logger = logging.getLogger(__name__)


class StagingRegistration:
    registration_host = f"{os.environ['api_host']}"
    registration_gql = f"{registration_host}/graphql"

    @classmethod
    def create_registration(cls, email, password):
        # create registration without getting signupIntentToken and userId
        captcha = StagingPayment.create_captcha()
        fm = datetime.now().strftime("%Y%m%d%H%M%S%f")
        account_info = {
            "email": email,
            "password": password,
            "first_name": f"firstName{fm}",
            "last_name": f"lastName{fm}",
            "business_role": "merchant",
        }
        variables = {
            "firstName": account_info["first_name"],
            "lastName": account_info["last_name"],
            "email": account_info["email"],
            "password": account_info["password"],
            "referralCode": "",
            "captcha": captcha,
        }
        r = requests.post(
            url=cls.registration_gql,
            json={"query": gql.token.CREATE_REGISTRATION, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Create registration failed】： {str(t)}")
            logger.info(f"【Create registration】：{str(t)}")
        else:
            raise Exception(f"【Create registration failed】： {r.text}")

    @classmethod
    def get_gmail_address_signup_intent_token_and_user_id(cls, gmail_address):
        # open email to get registration link
        url = GmailHelper().get_register_link(gmail_address)
        # get signupIntentToken and user_id from redirect url
        r = requests.get(url)
        parsed_url = urlparse(r.url)
        signup_intent_token = parse_qs(parsed_url.query)["signupIntentToken"][0]
        user_id = parse_qs(parsed_url.query)["userId"][0]
        return signup_intent_token, user_id

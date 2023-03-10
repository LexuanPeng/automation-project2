import json
import os
import time
from datetime import datetime
import test_resource.graphql as gql

import requests
import logging
import uuid
from decimal import Decimal
from typing import Union, List

from common.utils.tools import Tools

logger = logging.getLogger(__name__)


class StagingPayment:
    payment_host = f"{os.environ['api_host']}"
    payment_gql = f"{payment_host}/graphql"
    payment_sdk = f"{payment_host}/sdk/payments"
    payment_node_host = "https://pay-node.3ona.co"

    @classmethod
    def create_payment(
        cls,
        amount: Union[str, int, float],
        pk_key: str,
        currency: str = "USD",
        whitelist_address: str = None,
        sub_merchant_id: str = None,
        delayed_capture: str = "false",
        expired_at: str = None,
        cancel_url: str = "https://google.com",
    ):
        """
        Create payment for shop
        @param cancel_url:  cancel_url
        @param expired_at:  expired_at
        @param delayed_capture: delayed_capture
        @param sub_merchant_id: sub_merchant_id
        @param whitelist_address:  whitelist_address
        @param amount: amount
        @param pk_key: pk_key for shop
        @param currency: currency
        @return: check out payment details
        """
        url = f"{cls.payment_host}/api/payments"
        headers = {"Authorization": f"Bearer {pk_key}", "Content-Type": "application/json"}
        # amount = Decimal(amount)
        data = {
            "currency": currency,
            "amount": amount,
            "description": f"Automation Test {str(uuid.uuid4())}",
            "order_id": f"Automation {str(uuid.uuid4())}",
            "metadata": {"customer_name": "Automation", "customer_email": "automation@auto.com"},
        }
        if delayed_capture == "true":
            data["delayed_capture"] = delayed_capture
        if whitelist_address is not None:
            data["whitelist_addresses"] = whitelist_address
        if sub_merchant_id is not None:
            data["sub_merchant_id"] = sub_merchant_id
        if expired_at is not None:
            data["expired_at"] = int(time.time()) + int(expired_at) * 60
        if cancel_url is not None:
            data["cancel_url"] = cancel_url

        r = requests.post(url=url, json=data, headers=headers)
        logger.debug(f"【Create payment request】: {url} - {data} - {headers}")
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Create payment failed】： {str(t)}")
            logger.info(f"【Create payment passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Create payment failed】： {r.text}")

    @classmethod
    def capture_payment(cls, payment_id: str, pk_key: str):
        url = f"{cls.payment_host}/api/payments/{payment_id}/capture"
        headers = {"Authorization": f"Bearer {pk_key}"}
        r = requests.post(url=url, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Capture payment failed】： {str(t)}")
            logger.info(f"【Capture payment passed】:{str(t)}")
            return t
        else:
            raise Exception(f"【Capture payment failed】： {r.text}")

    @classmethod
    def void_payment(cls, payment_id: str, pk_key: str):
        url = f"{cls.payment_host}/api/payments/{payment_id}/void"
        headers = {"Authorization": f"Bearer {pk_key}"}
        r = requests.post(url=url, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Void payment failed】： {str(t)}")
            logger.info(f"【Void payment passed】:{str(t)}")
            return t
        else:
            raise Exception(f"【Void payment failed】： {r.text}")

    @classmethod
    def validate_payment(cls, pk_key: str, payment_details: dict, token: str, target_currency: str = "USDC"):
        """
        To valid the payment by admin, it's not a real check out and this payment can't be refunded
        @param pk_key: shop pk key
        @param payment_details: payment created before
        @param token: admin token
        @param target_currency: currency to pay
        @return: payment details
        """
        url = f"{cls.payment_host}/admin/api/payments/inbound_fund"
        payment_id = payment_details["id"]
        sdk_payment_details = cls.get_sdk_payment_details(payment_id, pk_key)
        target_amount = sdk_payment_details["meta"]["crypto_amounts"][target_currency.upper()]

        txn_id = str(uuid.uuid4())
        txn_created_at = int(time.time())

        headers = {"AUTHORIZATION": f"Token {token}"}

        data = {
            "payment_id": payment_details["id"],
            "amount": f"{target_amount}",
            "txn_id": txn_id,
            "txn_created_at": txn_created_at,
            "currency": target_currency,
            "payer_id": payment_details["id"],
        }
        r = requests.post(url=url, data=data, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Validate payment failed】： {str(t)}")
            t.update(data)
            logger.info(f"【Validate payment passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Validate payment failed】： {r.text}")

    @classmethod
    def create_validate_payment(
        cls,
        amount: Union[str, int, float],
        pk_key: str,
        admin_token: str,
        currency: str = None,
        whitelist_address: str = None,
        sub_merchant_id: str = None,
    ):
        """
        A flow from create checkout to mock validate payment
        """
        if currency is None:
            payment_details = cls.create_payment(
                amount=amount, pk_key=pk_key, whitelist_address=whitelist_address, sub_merchant_id=sub_merchant_id
            )
        else:
            payment_details = cls.create_payment(
                amount=amount,
                pk_key=pk_key,
                currency=currency,
                whitelist_address=whitelist_address,
                sub_merchant_id=sub_merchant_id,
            )

        r = cls.validate_payment(
            payment_details=payment_details,
            token=admin_token,
            pk_key=pk_key,
        )
        payment_details["amount"] = r["amount"]
        return payment_details

    @classmethod
    def get_login_token(cls, user_name: str, password: str):
        """
        Get the merchant dashboard login token
        @param user_name: user name
        @param password: password
        @return: login token
        """
        captcha = cls.create_captcha()
        variables = {"email": user_name, "password": password, "captcha": captcha}
        r = requests.post(url=cls.payment_gql, json={"query": gql.token.CREATE_TOKEN, "variables": variables})
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get login token failed】： {str(t)}")
            logger.info(f"【Get login token passed】：{str(t)}")
            return t["data"]["createToken"]["token"]
        else:
            raise Exception(f"【Get login token failed】： {r.text}")

    @classmethod
    def get_pay_id_after_send_invoices(cls, user_name: str, password: str, account_id: str, invoice_id: str):
        """
        Get the paymentId from field: account, invoice and then we could get the payment url by it
        @param user_name: user name
        @param password: password
        @param account_id: account id for shop
        @param invoice_id: invoice id can be get after create invoices
        @return:
        """
        token = cls.get_login_token(user_name, password)

        variables = {"accountId": account_id, "invoiceId": invoice_id}
        headers = {"AUTHORIZATION": f"Bearer {token}"}

        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.account.GET_PAY_ID_BY_ACCOUNT_ID, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get payment id after send invoices failed】： {str(t)}")
            logger.info(f"【Get payment id after send invoices passed】：{str(t)}")
            return t["data"]["account"]["invoice"]["paymentId"]
        else:
            raise Exception(f"【Get payment id after send invoices failed】： {r.text}")

    @classmethod
    def clear_all_draft_invoices(cls, user_name: str, password: str, account_id: str):
        """
        Clear all existing draft invoices for current shop
        @param user_name: user name
        @param password: password
        @param account_id: account id for shop
        @return:
        """
        token = cls.get_login_token(user_name, password)

        variables = {"accountId": account_id}
        headers = {"AUTHORIZATION": f"Bearer {token}"}

        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.account.GET_INVOICES_BY_ACCOUNT_ID, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Clear all draft invoices failed】： {str(t)}")
            invoices_list: list = t["data"]["account"]["invoices"]["nodes"]
            draft_invoices_list = list(filter(lambda x: x["status"] == "draft", invoices_list))
            if len(draft_invoices_list) > 0:
                for invoice in draft_invoices_list:
                    invoice_id = invoice["id"]
                    variables = {"invoiceId": invoice_id}
                    requests.post(
                        url=cls.payment_gql,
                        json={"query": gql.invoices.DELETE_INVOICES, "variables": variables},
                        headers=headers,
                    )
                logger.info(f"【Clear all draft invoices passed】: {str(draft_invoices_list)}")
        else:
            raise Exception(f"【Clear all draft invoices failed】： {r.text}")

    @classmethod
    def get_payment_details(cls, payment_id: str, pk_key: str):
        """
        Get the payment details by payment id for the shop - pk_key
        @param payment_id: payment id
        @param pk_key: shop pk key
        @return: payment_details
        """
        url = f"{cls.payment_host}/api/payments/{payment_id}"
        headers = {"Authorization": f"Bearer {pk_key}"}

        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get payment failed】： {str(t)}")
            logger.info(f"【Get payment passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get payment failed】： {r.text}")

    @classmethod
    def get_sdk_payment_details(cls, payment_id: str, pk_key: str):
        """
        Get the sdk payment details by payment id for the shop - pk_key
        @param payment_id: payment id
        @param pk_key: shop pk key
        @return: skd payment_details
        """
        url = f"{cls.payment_sdk}/{payment_id}"
        headers = {"Authorization": f"Bearer {pk_key}"}

        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get sdk payment failed】： {str(t)}")
            logger.info(f"【Get sdk payment passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get sdk payment failed】： {r.text}")

    @classmethod
    def update_payment_settings(
        cls,
        user_name: str,
        password: str,
        team_id: str,
        preferred_currency: str = "USD",
        credit_to_base: bool = False,
        payment_time_out: int = None,
        token: str = None,
    ):
        """
        Update the payment setting - preferredCurrency and creditToBaseCurrency
        @param user_name: user name
        @param password: password
        @param team_id: team id
        @param preferred_currency: currency
        @param credit_to_base: if set to base
        @param payment_time_out: payment_time_out
        """
        if token is None:
            token = cls.get_login_token(user_name=user_name, password=password)
        headers = {"AUTHORIZATION": f"Bearer {token}"}

        variables = {
            "teamId": team_id,
            "preferredCurrency": preferred_currency,
            "creditToBaseCurrency": credit_to_base,
            "paymentTimeOut": payment_time_out,
        }

        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.payment.UPDATE_PAYMENT_SETTINGS, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Update payment setting failed】： {str(t)}")
            logger.info(f"【Update payment settings passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Update payment setting failed】： {r.text}")

    @classmethod
    def get_teams(cls, user_name: str, password: str):
        """
        Get all teams details for currency user
        @param user_name: user name
        @param password: password
        @return: teams details
        """
        token = cls.get_login_token(user_name, password)
        headers = {"AUTHORIZATION": f"Bearer {token}"}

        r = requests.post(url=cls.payment_gql, json={"query": gql.team.GET_TEAMS}, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get teams details failed】： {str(t)}")
            logger.info(f"【Get teams details passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get teams details failed】： {r.text}")

    @classmethod
    def get_team_id_by_name(cls, user_name: str, password: str, name: str):
        """
        Get the team id from teams details by the shop name
        @param user_name: user name
        @param password: password
        @param name: shop name
        @return: matched team details
        """
        teams_details = cls.get_teams(user_name, password)
        teams: list = teams_details["data"]["viewer"]["teams"]
        matched_team = list(filter(lambda team: team["name"] == name, teams))
        if len(matched_team) == 0:
            raise Exception(f"【Get team id by shop name failed】: {str(teams)}")
        logger.info(f"【Get team id by shop name failed】：{str(matched_team)}")
        return matched_team[0]["id"]

    @classmethod
    def generate_2fa_token(cls, user_name: str, password: str):
        """
        Generate 2fa token for create payout api
        @param user_name: user name
        @param password: password
        @return: two_fa_token
        """
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5
        import base64

        token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}

        r = requests.post(url=cls.payment_gql, json={"query": gql.token.GET_SAFE_HEADERS}, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if t["data"] is None:
                raise Exception(f"【Generate 2fa token failed】: {str(t['errors'])}")
            logger.info(f"【Generate 2fa token passed】：{str(t)}")
            public_key = t["data"]["safeHeaders"]["publicKey"]
            import_key = RSA.importKey(public_key)
            pkcs1_v1_5 = PKCS1_v1_5.new(import_key)
            two_fa_token = base64.b64encode(pkcs1_v1_5.encrypt(password.encode()))
            return token, two_fa_token.decode("utf-8")
        else:
            raise Exception(f"【Generate 2fa token failed】： {r.text}")

    @classmethod
    def create_registration_and_team(cls, account_info: dict, support_token: str):
        """
        Create a registration and add a shop, must create account_info, please make sure the info is union
        fm = datetime.now().strftime("%Y%m%d%H%M%S")
        account_info = {
            "email": f"auto{fm}@email.com",
            "password": "Tester@#$1",
            "first_name": f"firstName{fm}",
            "last_name": f"lastName{fm}",
            "invitationId": "{Not required}",
            "referralCode": "{Not required}",
            "shop_name": "auto_" + datetime.now().strftime("%Y%m%d%H%M%S"),
            "website": "{website}",
            "preferred_currency": "{preferred_currency}"
            "business_category": "{business_category}"
        }
        @param support_token: support_token
        @param account_info: a map store account info and team info
        @return: r_registration
        """
        shop_name = account_info.get("shop_name", "auto_" + datetime.now().strftime("%Y%m%d%H%M%S%f"))
        website = account_info.get("website", "www.automation.com")
        preferred_currency = account_info.get("preferred_currency", "USD")
        business_category = account_info.get("business_category", "corporation")
        business_role = account_info.get("business_role", "merchant")
        daily_volume_range = account_info.get("daily_volume_range", None)

        r_registration = cls.create_registration(account_info, support_token)
        login_token = r_registration["data"]["createRegistration"]["token"]
        team_details = cls.create_team(
            shop_name=shop_name,
            website=website,
            business_category=business_category,
            preferred_currency=preferred_currency,
            token=login_token,
            business_role=business_role,
            daily_volume_range=daily_volume_range,
        )
        r_registration["account_info"] = account_info
        r_registration["team_details"] = team_details
        return r_registration

    @classmethod
    def create_registration(cls, account_info: dict, support_token: str):
        first_name = account_info["first_name"]
        last_name = account_info["last_name"]
        email = account_info["email"]
        password = account_info["password"]

        invitation_id = account_info.get("invitationId", None)
        referral_code = account_info.get("referralCode", None)

        captcha = cls.create_captcha()

        variables = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password,
            "captcha": captcha,
        }
        if invitation_id is not None:
            variables["invitationId"] = invitation_id

        if referral_code is not None:
            variables["referralCode"] = referral_code

        r_registration = requests.post(
            url=cls.payment_gql, json={"query": gql.token.CREATE_REGISTRATION, "variables": variables}
        )

        if r_registration.status_code == 200:
            r_registration = r_registration.json()
            if r_registration["data"]["createRegistration"]["errors"] is not None:
                raise Exception(f"【Create registration failed】： {str(r_registration)}")
        else:
            raise Exception(f"【Create registration failed】： {r_registration.text}")

        signup_intent_token, user_id = cls.get_signup_intent_token(email, support_token)
        token = cls.activate_registration(signup_intent_token, user_id)
        r_registration["data"]["createRegistration"]["token"] = token
        r_registration["data"]["createRegistration"]["user_id"] = user_id
        logger.info(f"【Create registration passed】：{str(r_registration)}")
        return r_registration

    @classmethod
    def activate_registration(cls, signup_intent_token: str, user_id: str):
        """
        Activate registration after create registration
        @param signup_intent_token:signup_intent_token
        @param user_id: user_id
        @return: token
        """
        variables = {
            "signupIntentToken": signup_intent_token,
            "userId": user_id,
        }

        r = requests.post(url=cls.payment_gql, json={"query": gql.token.ACTIVATE_REGISTRATION, "variables": variables})
        if r.status_code == 200:
            t = r.json()
            if t["data"]["activateRegistration"]["errors"] is not None:
                raise Exception(f"【Activate registration failed】： {str(t)}")
        else:
            raise Exception(f"【Activate registration failed】： {r.text}")

        logger.info(f"【Activate registration passed】：{str(t)}")
        return t["data"]["activateRegistration"]["token"]

    @classmethod
    def get_signup_intent_token(cls, email: str, support_token: str):
        """
        You must create registration before getting signup intent token
        @param support_token: support token
        @param email: email registration before
        @return: signupIntentToken and userId
        """
        headers = {"Authorization": f"Bearer {support_token}"}
        url = f"{cls.payment_host}/testing_supports/signup_intent_token?email={email}"

        r = requests.get(url=url, headers=headers)
        Tools.sleep(2)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get signupIntentToken by {email} after registration failed】： {str(t)}")
            logger.info(f"【Get signupIntentToken by {email} after registration passed】：{str(t)}")
            return t["data"]["signup_intent_token"], t["data"]["user_id"]
        else:
            raise Exception(f"【Get signupIntentToken by {email} after registration failed】： {r.text}")

    @classmethod
    def create_captcha(cls):
        """
        Create captcha from BE and add it to getToken api
        """
        r = requests.post(url=cls.payment_gql, json={"query": gql.token.CREATE_CAPTCHA})
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Create captcha failed】： {str(t)}")
            t = t["data"]["createCaptcha"]
            captcha = {
                "challenge": t["challenge"],
                "signature": t["signature"],
                "code": "automation|jordan",
            }
            return captcha
        else:
            raise Exception(f"【Create captcha failed】： {r.text}")

    @classmethod
    def get_team_anticipated_info(
        cls,
        user_name: str = None,
        password: str = None,
        token: str = None,
        daily_volume_range: dict = None,
        daily_customer_range: dict = None,
        monthly_payout_range: dict = None,
    ):
        if token is None:
            token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.team.GET_TEAM_ANTICIPATED_INFO},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "data" not in t.keys():
                raise Exception(f"【Get team anticipated info failed】： {str(t)}")
            t = t["data"]["teamAnticipatedInfo"]["defaultAnticipated"]

            if daily_volume_range is None:
                daily_volume_range = {"min": None, "max": 10000}

            if daily_customer_range is None:
                daily_customer_range = {"min": None, "max": 10}

            if monthly_payout_range is None:
                monthly_payout_range = {"min": 4, "max": None}

            daily_volume = list(filter(lambda x: x["anticipatedType"] == "daily_volume", t))
            daily_volume = daily_volume[0]["range"]
            daily_volume = list(
                filter(
                    lambda x: x["min"] == daily_volume_range["min"] and x["max"] == daily_volume_range["max"],
                    daily_volume,
                )
            )[0]["id"]

            daily_customer = list(filter(lambda x: x["anticipatedType"] == "daily_customer", t))
            daily_customer = daily_customer[0]["range"]
            daily_customer = list(
                filter(
                    lambda x: x["min"] == daily_customer_range["min"] and x["max"] == daily_customer_range["max"],
                    daily_customer,
                )
            )[0]["id"]

            monthly_payout = list(filter(lambda x: x["anticipatedType"] == "monthly_payout", t))
            monthly_payout = monthly_payout[0]["range"]
            monthly_payout = list(
                filter(
                    lambda x: x["min"] == monthly_payout_range["min"] and x["max"] == monthly_payout_range["max"],
                    monthly_payout,
                )
            )[0]["id"]

            logger.info(f"【Get team anticipated info passed】：{daily_volume},{daily_customer},{monthly_payout}")
            return daily_volume, daily_customer, monthly_payout
        else:
            raise Exception(f"【Get team anticipated info failed】： {r.text}")

    @classmethod
    def create_team(
        cls,
        shop_name: str,
        website: str,
        preferred_currency: str,
        business_category: str,
        business_role: str,
        referral_code: str = None,
        user_name: str = None,
        password: str = None,
        token: str = None,
        daily_volume_range: dict = None,
        daily_customer_range: dict = None,
        monthly_payout_range: dict = None,
    ):
        """
        Create a team(shop) for the user, if you input the token, please user_name and password are not required
        @param business_role: Merchant or Acquirer
        @param shop_name: shop name
        @param website: website e.g www.automation.com
        @param preferred_currency: e.g USD
        @param business_category: e.g corporation
        @param referral_code: not required
        @param user_name: user name - not required
        @param password: password - not required
        @param token: token you get by user_name and password
        @return:
        """
        if token is None:
            token = cls.get_login_token(user_name, password)

        headers = {"Authorization": f"Bearer {token}"}

        if (daily_volume_range is None) and (daily_customer_range is None) and (monthly_payout_range is None):
            daily_volume, daily_customer, monthly_payout = cls.get_team_anticipated_info(token=token)
        else:
            daily_volume, daily_customer, monthly_payout = cls.get_team_anticipated_info(
                token=token,
                daily_volume_range=daily_volume_range,
                daily_customer_range=daily_customer_range,
                monthly_payout_range=monthly_payout_range,
            )
        variables = {
            "name": shop_name,
            "website": website,
            "preferredCurrency": preferred_currency,
            "businessCategory": business_category,
            "businessRole": business_role,
            "dailyVolume": daily_volume,
        }
        if referral_code is not None:
            variables["$referralCode"] = referral_code

        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.team.CREATE_TEAM, "variables": variables},
            headers=headers,
            timeout=30,
        )

        if r.status_code == 200:
            t = r.json()
            if t["data"]["createTeam"]["errors"] is not None or "data" not in t.keys():
                raise Exception(f"【Create team failed】： {str(t)}")
            logger.info("【Create team passed】")
            return t["data"]["createTeam"]["team"]
        else:
            raise Exception(f"【Create team failed】： {r.text}")

    @staticmethod
    def get_dollar_unit_type(currency: str):
        if currency == "USD":
            unit_type = "$"
        elif currency == "BTC":
            unit_type = "BTC"
        elif currency == "GBP":
            unit_type = "£"
        elif currency == "CAD":
            unit_type = "C$"
        elif currency == "AUD":
            unit_type = "A$"
        elif currency == "EUR":
            unit_type = "€"
        elif currency == "ETH":
            unit_type = "ETH"
        elif currency == "CRO":
            unit_type = "CRO"
        elif currency == "BRL":
            unit_type = "R$"
        else:
            logger.warning(f"【Unsupported wallet currency】: {currency}")
            return currency
        return unit_type

    @staticmethod
    def get_dollar_currency_type(unit_type: str):
        if unit_type == "$":
            currency = "USD"
        elif unit_type == "BTC":
            currency = "BTC"
        elif unit_type == "£":
            currency = "GBP"
        elif unit_type == "C$":
            currency = "CAD"
        elif unit_type == "A$":
            currency = "AUD"
        elif unit_type == "€":
            currency = "EUR"
        elif unit_type == "ETH":
            currency = "ETH"
        elif unit_type == "CRO":
            currency = "CRO"
        elif unit_type == "R$":
            currency = "BRL"
        else:
            logger.warning(f"【Unsupported wallet unit_type】: {unit_type}")
            return unit_type
        return currency

    @staticmethod
    def get_currency_unit(currency: str):
        if currency in ["USD", "EUR", "AUD", "GBP", "CNY", "CAD"]:
            return 2
        return 6

    @staticmethod
    def get_payout_wallet_code(payout_currency: str):
        code_map = {
            "BTC": "wallet",
            "ETH": "wallet",
            "CRO": "wallet",
            # "TUSD": "trust_token",
            "USDC": "wallet",
            "EUR": "fiat_eur",
            "USD": "fiat_usd",
            # "TCAD": "wallet",
            # "TAUD": "wallet",
            # "TGBP": "wallet",
            "AUD": "fiat_aud",
            "GBP": "fiat_gbp",
        }
        if payout_currency not in code_map.keys():
            raise NotImplementedError("not supported payout currency")
        wallet_code = code_map[payout_currency]
        return wallet_code

    @staticmethod
    def get_payout_currency_by_wallet_currency(currency: str):
        payout_wallet_map = {
            # "USD": "TUSD",
            "USDC": "USDC",
            "EUR": "EUR",
            # "CAD": "TCAD",
            # "AUD": "TAUD",
            # "GBP": "TGBP",
            "BTC": "BTC",
            "ETH": "ETH",
            "CRO": "CRO",
        }
        if currency not in payout_wallet_map.keys():
            raise NotImplementedError("Not supported currency")
        payout_currency = payout_wallet_map[currency]
        return payout_currency

    @staticmethod
    def get_wallet_currency_by_payout_currency(payout_currency: str):
        wallet_map = {
            # "TUSD": "USD",
            "USDC": "USD",
            "EUR": "EUR",
            # "TCAD": "CAD",
            # "TAUD": "AUD",
            # "TGBP": "GBP",
            "BTC": "BTC",
            "ETH": "ETH",
            "CRO": "CRO",
            "USD": "USD",
            "AUD": "AUD",
            "GBP": "GBP",
        }

        if payout_currency not in wallet_map.keys():
            raise NotImplementedError("Not supported payout currency")
        wallet_currency = wallet_map[payout_currency]
        return wallet_currency

    @classmethod
    def get_converted_amount(cls, currency: str, target_currency: str, amount: str):
        """
        Get the converted amount from currencyA to currencyB
        @param currency: currency
        @param target_currency: target currency
        @param amount: covert amount
        @return: result
        """
        url = f"{cls.payment_node_host}/quotations/quote"

        params = {"currency": currency, "target_currency": target_currency, "amount": amount}
        r = requests.post(url=url, params=params)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get converted amount failed】： {str(t)}")
            logger.info(f"【Get converted amount passed】：{str(t)}")
            target_amount = t["target_amount"]
            return target_amount
        else:
            raise Exception(f"【Get converted amount failed】： {r.text}")

    @classmethod
    def get_pk_key(
        cls,
        user_name: str,
        password: str,
        account_id: str,
    ):
        """Get developer pk, sk key, two_fa_token"""
        variables = {"accountId": account_id}
        token, two_fa_token = cls.generate_2fa_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}", "X-2Fa-Secret": two_fa_token}

        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.account.GET_PK_KEY_BY_ACCOUNT_ID, "variables": variables},
            headers=headers,
        )

        r2 = requests.post(
            url=cls.payment_gql,
            json={"query": gql.account.GET_SECRET_KEY_BY_ACCOUNT_ID, "variables": variables},
            headers=headers,
        )

        if r.status_code == 200:
            t = r.json()
            t2 = r2.json()
            if "errors" in t.keys():
                raise Exception(f"【Get pk key failed】： {str(t)}")
            if "errors" in t2.keys():
                raise Exception(f"【Get secret key failed】： {str(t2)}")
            logger.info(f"【Get pk key and secret key passed】：{str(t)} {str(t2)}")
            account = t["data"]["account"]
            account2 = t2["data"]["accountSecretKey"]
            return account["publishableKey"], account2["secretKey"], token, two_fa_token
        else:
            raise Exception(f"【Get pk key failed】： {r.text}")

    @classmethod
    def get_onchain_refund_min_chain_network_cost(cls, withdraw_token: str = None):
        url = f"{cls.payment_host}/api/withdraw_currencies?token={withdraw_token}"
        r = requests.get(url=url)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get withdraw fee failed】： {str(t)}")
            currency_list = list()
            for currency in t.values():
                fee = currency["currency_fee"]
                currency_list.append(Decimal(str(fee)))
            min_chain_network_cost = min(currency_list)
            logger.info(f"【Get refund min chain passed】: {min_chain_network_cost}  - {str(t)}")
            return str(min_chain_network_cost)
        else:
            raise Exception(f"【Get refund min chain failed】： {r.text}")

    @classmethod
    def get_on_chain_refund_network_cost(cls, token_coin: str, withdraw_token: str = None):
        if withdraw_token is None:
            currency_cost = {
                "BTC": "0.0005",
                "CRO": "1.0",
                "CRO_NATIVE": "0.001",
                "ETH": "0.01",
                # "TUSD": "1.0",
                "USDC": "1.0",
                "CRO_CRONOS": "0.2",
            }
            if token_coin not in currency_cost.keys():
                raise Exception(f"【Not supported token coin {token_coin}】")
            return currency_cost[token_coin]
        else:
            url = f"{cls.payment_host}/api/withdraw_currencies?token={withdraw_token}"
            r = requests.get(url=url)
            if r.status_code == 200:
                t = r.json()
                if "errors" in t.keys():
                    raise Exception(f"【Get withdraw fee failed】： {str(t)}")
                logger.info(f"【Get withdraw fee passed】: {t}")
                decimal_n = cls.get_currency_unit(token_coin)
                currency_fee = t[token_coin]["currency_fee"]
                currency_fee = Tools.keep_float(currency_fee, decimal_n, True)
                return currency_fee
            else:
                raise Exception(f"【Get withdraw fee failed】： {r.text}")

    @classmethod
    def get_on_chain_refund_prepare_url(cls, r_d: str, token: str, refund_type: str = "refund"):
        """
        The url prepare for on chain payment refund or rebound
        @param r_d: id get from method 'get_onchain_inbound'
        @param token: support token
        @param refund_type: refund or rebound
        @return: result
        """
        headers = {"Authorization": f"Bearer {token}"}
        if refund_type == "refund":
            url = f"{cls.payment_host}/testing_supports/refund_url?id={r_d}"
        else:
            url = f"{cls.payment_host}/testing_supports/rebound_url?id={r_d}"

        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get {refund_type} prepare url failed】： {str(t)}")
            logger.info(f"【Get {refund_type} prepare url passed】：{str(t)}")
            return t["data"]
        else:
            raise Exception(f"【Get {refund_type} prepare url failed】： {r.text}")

    @classmethod
    def refund_off_chain_payment(
        cls,
        user_name: str,
        password: str,
        payment_id: str,
        account_id: str,
        debit_currency: str,
        amount: Union[float, str],
        note: str = "Automation Refund",
        reason: str = "Requested by customer",
        email: str = "automation@email.com",
    ):
        token, two_fa_token = cls.generate_2fa_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}", "X-2Fa-Secret": two_fa_token}
        variables = {
            "accountId": account_id,
            "paymentId": payment_id,
            "amount": float(amount),
            "reason": reason,
            "notes": note,
            "email": email,
            "debitCurrency": debit_currency,
        }
        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.payment.CREATE_PAYMENT_REFUND, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Refund off chain payment {payment_id} failed】： {str(t)}")
            logger.info(f"【Refund off chain payment {payment_id} passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Refund off chain payment {payment_id} failed】： {r.text}")

    @classmethod
    def get_payout_fee(cls, token: str, team_id: str, currency: str, address_type: str = "wallet"):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        variables = {"teamId": team_id, "currency": currency, "addressType": address_type}
        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.balances.GET_MERCHANT_PAYOUT_FEE, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get get_payout_fee failed】： {str(t)}")
            logger.info(f"【Get Payout fee passed】：{str(t)}")
            return t["data"]["team"]["payoutFee"]["minFee"], t["data"]["team"]["payoutFee"]["feeRate"]
        else:
            raise Exception(f"【Get get_payout_fee failed】： {r.text}")

    @classmethod
    def get_target_payout_mini_amount(
        cls,
        token: str,
        team_id: str,
        currency: str = "USDC",
        payout_percent: str = "0.2",
    ):
        min_fee, fee_rate = cls.get_payout_fee(token=token, team_id=team_id, currency=currency)
        if min_fee == "0.0":
            min_fee = "1"
        return float(min_fee) / (float(payout_percent) * float(fee_rate))

    @classmethod
    def get_payout_account_by_currency(
        cls, user_name: str, password: str, team_id: str, currency: str, code: str = "wallet", token=None
    ):
        # Currency: USD, USDC, BTC, GBP and so on
        # code: wallet or trust_token
        if token is None:
            token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"teamId": team_id}

        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.team.GET_PAYOUT_ACCOUNTS, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get payout account by {currency} failed】： {str(t)}")
            t = t["data"]["team"]["defaultPayoutAccounts"]
            t = list(filter(lambda x: x["currency"] == currency, t))
            if len(t) > 1:
                t = list(filter(lambda x: x["code"] == code, t))
            logger.info(f"【Get payout account by {currency} passed】：{str(t)}")
            return t, token
        else:
            raise Exception(f"【Get payout account by {currency} failed】： {r.text}")

    @classmethod
    def get_onchain_outbound_qr_code(cls, token: str):
        url = f"{cls.payment_host}/api/onchain_outbound?token={token}"
        r = requests.get(url=url)

        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get onchain_outbound qr_code failed】： {str(t)}")
            logger.info(f"【Get onchain_outbound qr_code passed】：{str(t)}")
            return t["qr_code"]
        else:
            raise Exception(f"【Get onchain_outbound qr_code failed】： {r.text}")

    @classmethod
    def get_overview_info(
        cls, user_name: str, password: str, account_id: str, from_time: str, period: str, to_time: str
    ):
        token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"accountId": account_id, "fromTime": from_time, "period": period, "toTime": to_time}
        r = requests.post(
            url=cls.payment_gql,
            headers=headers,
            json={"query": gql.team.GET_OVERVIEW_INFO, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get overview info from {from_time} to {to_time} failed】： {str(t)}")
            logger.info(f"【Get overview info from {from_time} to {to_time} passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get overview info from {from_time} to {to_time} failed】： {r.text}")

    @classmethod
    def update_payout_account_info(
        cls,
        user_name: str,
        password: str,
        payout_account_id: str,
        address: str,
        mode: str = "manual",
        address_type: str = "wallet",
        usd_account: bool = False,
        gbp_account: bool = False,
        auto_payout_settings: dict = None,
    ):
        token, two_fa_token = cls.generate_2fa_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}", "X-2Fa-Secret": two_fa_token}

        if mode == "auto":
            auto_payout_settings = (
                {"percentage": 20, "scheduleType": "weekly"} if auto_payout_settings is None else auto_payout_settings
            )
        variables = {
            "payoutAccountId": payout_account_id,
            "accountHolder": "Automation Tester",
            "address": address,
            "mode": mode,
            "addressType": address_type,
            "autoPayoutSettings": auto_payout_settings,
        }
        if usd_account:
            update_usd = {
                "via": "send_wyre",
                "countryCode": "AF",
                "achAccountType": "checking",
                "swiftCode": "ABFDGB22",
                "accountNumber": "GB01TCCL45005989275659",
                "accountHolderType": "individual",
                "accountHolder": "Automation Tester",
                "businessAddress": "Automation",
            }
            variables.update(update_usd)
        if gbp_account:
            update_gbp = {
                "via": "bcb",
                "countryCode": "GB",
                "accountNumber": "10132268",
                "accountHolder": "Automation Tester",
                "sortCode": "040541",
                "accountHolderType": "individual",
            }
            variables.update(update_gbp)
        r = requests.post(
            url=cls.payment_gql,
            headers=headers,
            json={"query": gql.account.UPDATE_PAYOUT_ACCOUNT_INFO, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Update payout account {payout_account_id} failed】： {str(t)}")
            logger.info(f"【Update payout account {payout_account_id} pass】：{str(t)}")
        else:
            raise Exception(f"【Update payout account {payout_account_id} failed】： {r.text}")

    @classmethod
    def get_payout_account_id_by_team_id(
        cls,
        user_name: str,
        password: str,
        team_id: str,
    ):
        token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}
        variables = {
            "teamId": team_id,
        }
        r = requests.post(
            url=cls.payment_gql,
            headers=headers,
            json={"query": gql.account.GET_PAYOUT_ID_BY_TEAM_ID, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get Payout Account by team id and currency failed】： {str(t)}")
            payout_accounts = t["data"]["team"]["payoutAccounts"]
            payout_accounts = list(filter(lambda x: x["status"] == "active", payout_accounts))
            logger.info(f"【Get Payout Account by team id and currency passed】：{str(payout_accounts)}")
            return payout_accounts
        else:
            raise Exception(f"【Get Payout Account by team id and currency failed】： {r.text}")

    @classmethod
    def get_payout_account_details_by_currency(
        cls,
        user_name: str,
        password: str,
        team_id: str,
        currency: str,
    ):
        token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}
        variables = {
            "teamId": team_id,
        }
        r = requests.post(
            url=cls.payment_gql,
            headers=headers,
            json={"query": gql.account.GET_PAYOUT_ID_BY_TEAM_ID, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get Payout Account by team id and currency failed】： {str(t)}")
            payout_accounts = t["data"]["team"]["payoutAccounts"]
            payout_accounts = list(filter(lambda x: x["currency"] == currency, payout_accounts))
            logger.info(f"【Get Payout Account by team id and currency passed】：{str(payout_accounts)}")
            return payout_accounts[0]
        else:
            raise Exception(f"【Get Payout Account by team id and currency failed】： {r.text}")

    @classmethod
    def get_account_id_by_team_id(cls, user_name: str, password: str, team_id: str):
        token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}
        variables = {
            "teamId": team_id,
        }
        r = requests.post(
            url=cls.payment_gql,
            headers=headers,
            json={"query": gql.team.GET_ACCOUNT_ID_BY_TEAM_ID, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get Account id by team id failed】： {str(t)}")
            account_id = t["data"]["team"]["liveAccount"]["id"]
            logger.info(f"【Get Account id by team id passed】：{str(account_id)}")
            return account_id
        else:
            raise Exception(f"【Get Account id by team id failed】： {r.text}")

    @classmethod
    def get_chain_name(cls, pay_currency: str):
        if ":cronos" in pay_currency or ":cro_native" in pay_currency:
            temp = pay_currency.split(":")
            return temp[-1]
        elif "_CRONOS" in pay_currency:
            return "cronos"
        elif "_NATIVE" in pay_currency:
            return "cro_native"
        else:
            return "erc20"

    @classmethod
    def create_payment_check_error(
        cls,
        amount: Union[str, int, float],
        pk_key: str,
        currency: str = "USD",
        sub_merchant_id: str = None,
    ):
        """
        Create payment to check error
        @param amount: amount
        @param pk_key: pk_key for shop
        @param currency: currency
        """
        url = f"{cls.payment_host}/api/payments"
        headers = {"Authorization": f"Bearer {pk_key}"}
        amount = Decimal(amount)
        data = {
            "currency": currency,
            "amount": amount,
            "description": f"Automation Test {str(uuid.uuid4())}",
            "order_id": f"Automation {str(uuid.uuid4())}",
        }
        if sub_merchant_id is not None:
            data["sub_merchant_id"] = sub_merchant_id
        r = requests.post(url=url, data=data, headers=headers)
        logger.debug(f"【Create payment request】: {url} - {data} - {headers}")
        if r.status_code == 200:
            t = r.json()
            logger.info(f"【Create payment passed】：{str(t)}")
            return t
        else:
            return r.json()["error"]

    @classmethod
    def update_setting_business_details(
        cls,
        user_name: str,
        password: str,
        ops_token: str,
        team_id: str,
        variables_update: dict = None,
    ):
        token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}

        from .payment_ops import StagingPaymentOps

        ops_api = StagingPaymentOps()
        team_details = ops_api.get_team(token=ops_token, team_id=team_id)["data"]["team"]

        business_role = team_details["businessRole"]
        business_category = team_details["businessCategory"]
        business_address = team_details["businessAddress"]
        business_address2 = team_details["businessAddress2"]
        province = team_details["province"]
        region = team_details["region"]
        incorporation_country = team_details["incorporationCountry"]
        zip_code = team_details["zipCode"]

        variables = {
            "businessRole": business_role,
            "businessCategory": business_category,
            "businessAddress": business_address,
            "businessAddress2": business_address2,
            "province": province,
            "region": region,
            "incorporationCountry": incorporation_country,
            "zipCode": zip_code,
            "teamId": team_id,
        }

        if "businessCategory" in variables_update:
            if variables_update["businessCategory"] != "individual_or_sole_proprietorship":
                variables["legalEntityName"] = "auto_legal_entity_name"
                variables["registrationNumber"] = "123456"
                variables["taxId"] = "autoTaxid"
        else:
            if business_category != "individual_or_sole_proprietorship":
                legal_entity_name = team_details["legalEntityName"]
                registration_number = team_details["registrationNumber"]
                tax_id = team_details["registrationNumber"]
                variables["legalEntityName"] = legal_entity_name
                variables["registrationNumber"] = registration_number
                variables["taxId"] = tax_id

        for k, v in variables_update.items():
            variables[k] = v

        r = requests.post(
            url=cls.payment_gql,
            headers=headers,
            json={"query": gql.account.UPDATE_SHOP_DETAIL, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Update team {team_id} shop details failed】： {str(t)}")
            logger.info(f"【Update team {team_id} shop details pass】：{str(t)}")
        else:
            raise Exception(f"【Update team {team_id} shop details failed】： {r.text}")

    @classmethod
    def set_pay_core_for_team(cls, team_id: str, support_token: str):
        headers = {"Authorization": f"Bearer {support_token}"}
        url = f"{cls.payment_host}/testing_supports/create_pay_core_account?team_id={team_id}"

        r = requests.post(url=url, headers=headers)
        if r.status_code == 200:
            t = r.json()
            logger.info(f"【Set pay core for team {team_id} passed】：{str(t)}")
        else:
            raise Exception(f"【Set pay core for team {team_id} failed】： {str(r.text)}")

    @classmethod
    def pay_core_enable(cls, team_id: str, support_token: str):
        headers = {"Authorization": f"Bearer {support_token}"}
        url = f"{cls.payment_host}/testing_supports/pay_core_setting?team_id={team_id}"

        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            t = r.json()
            logger.info(f"【Check {team_id} if is pay core passed】：{str(t)}")
            return t["in_sysconfig"]
        else:
            raise Exception(f"【Check {team_id} if is pay core failed】： {str(r.text)}")

    @classmethod
    def get_team_notifications(
        cls,
        user_name: str,
        password: str,
        team_id: str,
        page: int = 1,
        per_page: int = 10,
    ):
        token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}

        variables = {"teamId": team_id, "perPage": per_page, "page": page}

        r = requests.post(
            url=cls.payment_gql,
            headers=headers,
            json={"query": gql.account.GET_TEAM_NOTIFICATIONS, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get team {team_id} notifications failed】： {str(t)}")
            logger.info(f"【Get team {team_id} notifications pass】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get team {team_id} notifications failed】： {r.text}")

    @classmethod
    def get_balance_and_account(cls, user_name: str, password: str, account_id: str, team_id: str):
        token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}

        variables = {"teamId": team_id, "accountId": account_id}

        r = requests.post(
            url=cls.payment_gql,
            headers=headers,
            json={"query": gql.balances.GET_BALANCE_AND_ACCOUNT, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get team balance and account failed】： {str(t)}")
            logger.info(f"【Get team balance and account passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get team balance and account failed】： {r.text}")

    @classmethod
    def cancel_auto_payout(cls, wallet_addresses: List[tuple], support_token: str):
        """
        wallet_address =
        [
            ("wallet_addresses[]", "?"),
            ("wallet_addresses[]", "?")
        ]
        """
        headers = {"Authorization": f"Bearer {support_token}"}
        url = f"{cls.payment_host}/testing_supports/cancel_auto_payout"
        r = requests.put(url=url, params=wallet_addresses, headers=headers)
        if r.status_code == 200:
            t = r.json()
            logger.info(f"【Cancel auto payout by wallets passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Cancel auto payout by wallets failed】： {str(r.text)}")

    @classmethod
    def create_payment_with_customer(
        cls,
        amount: Union[str, int, float],
        pk_key: str,
        customer_object: bool = False,
        customer_id: str = None,
        ref_id: str = None,
        email: str = None,
        name: str = None,
        currency: str = "USD",
    ):
        """
        Create payment with customer object
        @param customer_id:  customer id
        @param ref_id:  ref id
        @param email: customer email
        @param name: customer name
        @param amount: amount
        @param pk_key: pk_key for shop
        @param currency: currency
        @return: check out payment details
        """
        url = f"{cls.payment_host}/api/payments"
        headers = {"Authorization": f"Bearer {pk_key}", "Content-Type": "application/json"}
        # amount = Decimal(amount)
        data = {
            "currency": currency,
            "amount": amount,
            "description": f"Automation Test {str(uuid.uuid4())}",
            "order_id": f"Automation {str(uuid.uuid4())}",
            "metadata": {"customer_name": "Automation", "customer_email": "automation@auto.com"},
            "customer_id": customer_id,
        }
        if customer_object:
            data["customer"] = {
                "ref_id": ref_id,
                "name": name,
                "email": email,
                "customer_details": {
                    "billing_details": {
                        "address": "string",
                        "address2": "string",
                        "city": "string",
                        "state": "string",
                        "country": "string",
                        "postal_code": "string",
                        "phone": "string",
                    },
                    "shipping_details": {
                        "address": "string",
                        "address2": "string",
                        "city": "string",
                        "state": "string",
                        "country": "string",
                        "postal_code": "string",
                        "phone": "string",
                    },
                },
            }
        r = requests.post(url=url, json=data, headers=headers)
        # logger.debug(f"【Create payment request】: {url} - {data} - {headers}")
        if r.status_code == 200:
            t = r.json()
            logger.info(f"【Create payment passed】：{str(t)}")
            return t
        else:
            logger.info(r.json()["error"])
            return r.json()["error"]

    @classmethod
    def get_customer(cls, token, user_name, password, account_id):
        if token is None:
            token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}

        variables = {"accountId": account_id, "perPage": 10, "page": 1, "filterBy": {}}

        r = requests.post(
            url=cls.payment_gql,
            headers=headers,
            json={"query": gql.account.GET_CUSTOMER, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get customer by account id {account_id} failed】： {str(t)}")
            customer_nodes: list = t["data"]["account"]["customers"]["nodes"]
            logger.info(f"【Get customer by account id {account_id} pass】")
            return customer_nodes
        else:
            raise Exception(f"【Get customer by account id {account_id} failed】： {r.text}")

    @classmethod
    def delete_customer_by_id(cls, token, user_name, password, account_id, customer_id):
        if token is None:
            token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}

        variables = {"accountId": account_id, "customerId": customer_id}

        r = requests.post(
            url=cls.payment_gql,
            headers=headers,
            json={"query": gql.account.DELETE_CUSTOMER, "variables": variables},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Delete customer by customer id {customer_id} failed】： {str(t)}")
            logger.info(f"【Delete customer by account id {customer_id} passed】")
        else:
            raise Exception(f"【Delete customer by account id {customer_id} failed】： {r.text}")

    @classmethod
    def update_minimum_payout_amount(cls, support_token: str, team_id: str, currency: str, minimum_payout_amount: str):
        headers = {"Authorization": f"Bearer {support_token}"}
        configuration_data = {"minPayoutAmount": {f"{currency}": float(minimum_payout_amount)}}
        json_data = {"id": team_id, "configurations": json.dumps(configuration_data)}
        url = f"{cls.payment_host}/testing_supports/update_team"
        r = requests.put(url=url, params=json_data, headers=headers)
        if r.status_code == 200:
            t = r.json()
            logger.info("【Update minimum payout amount passed】")
            return t
        else:
            raise Exception(f"【Update minimum payout amount failed】： {str(r.text)}")

    @classmethod
    def update_minimum_payout_fee(cls, support_token: str, team_id: str, currency: str, minimum_payout_fee: str):
        headers = {"Authorization": f"Bearer {support_token}"}
        configuration_data = {"minPayoutFee": {f"{currency}": float(minimum_payout_fee)}}
        json_data = {"id": team_id, "configurations": json.dumps(configuration_data)}
        url = f"{cls.payment_host}/testing_supports/update_team"
        r = requests.put(url=url, params=json_data, headers=headers)
        if r.status_code == 200:
            t = r.json()
            logger.info("【Update minimum payout fee passed】")
            return t
        else:
            raise Exception(f"【Update minimum fee amount failed】： {str(r.text)}")

    @classmethod
    def get_currency_minimum_payout_amount(cls, token: str, team_id: str, payout_currency: str):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        variables = {"teamId": team_id}
        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.balances.GET_CURRENCY_MINIMUM_AMOUNT, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get Currency minimum amount failed】： {str(t)}")
            minimum_currency_amount_list: list = t["data"]["team"]["currencyMinimumAmounts"]
            filtered_currency_amount_list = list(
                filter(lambda x: x["currency"] == payout_currency, minimum_currency_amount_list)
            )
            minimum_amount = filtered_currency_amount_list[0]["amount"]
            logger.info(f"【Get Currency minimum amount passed】：{minimum_amount}")
            return minimum_amount
        else:
            raise Exception(f"【Get Currency minimum amount failed】： {r.text}")

    @classmethod
    def get_currency_minimum_payout_fee(cls, token: str, team_id: str, payout_currency: str):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        variables = {"teamId": team_id}
        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.balances.GET_CURRENCY_MINIMUM_AMOUNT, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get Currency minimum payout fee failed】： {str(t)}")
            minimum_currency_fee_list: list = t["data"]["payoutAmountFee"]["currencyMinimumFees"]
            filtered_currency_fee_list = list(
                filter(lambda x: x["currency"] == payout_currency, minimum_currency_fee_list)
            )
            minimum_payout_fee = filtered_currency_fee_list[0]["fee"]
            logger.info(f"【Get Currency minimum payout fee passed】：{minimum_payout_fee}")
            return minimum_payout_fee
        else:
            raise Exception(f"【Get Currency minimum payout fee failed】： {r.text}")

    @classmethod
    def get_currency_network_fee(cls, token: str, team_id: str, currency: str):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        variables = {"teamId": team_id}
        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.balances.GET_CURRENCY_MINIMUM_AMOUNT, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get Currency network fee failed】： {str(t)}")
            currency_network_fee_list: list = t["data"]["payoutAmountFee"]["blockchainNetworkFees"]
            filtered_currency_network_fee_list = list(
                filter(lambda x: x["currency"] == currency, currency_network_fee_list)
            )
            network_fee = filtered_currency_network_fee_list[0]["fee"]
            logger.info(f"【Get Currency network fee passed】：{network_fee}")
            return network_fee
        else:
            raise Exception(f"【Get Currency network fee failed】： {r.text}")

    @classmethod
    def get_payment_settings_onchain_enabled(
        cls, user_name: str, password: str, team_id: str, payment_option: str = "onchain"
    ):
        login_token = cls.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {login_token}"}
        variables = {"teamId": team_id}

        r = requests.post(
            url=cls.payment_gql,
            json={"query": gql.payment.GET_PAYMENT_SETTINGS, "variables": variables},
            headers=headers,
        )

        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get Payment Settings Onchain Enabled failed】： {str(t)}")
            nodes = t["data"]["team"]["paymentMethods"]["nodes"]
            filtered_nodes = list(filter(lambda x: x["name"] == payment_option, nodes))
            payment_is_enabled = filtered_nodes[0]["enable"]
            logger.info(f"【Get Payment Settings Onchain Enabled passed】：{str(payment_is_enabled)}")
            return payment_is_enabled
        else:
            raise Exception(f"【Get Payment Settings Onchain Enabled failed】： {r.text}")

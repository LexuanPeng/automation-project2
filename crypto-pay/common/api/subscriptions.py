import datetime
import logging
import os
import time
import uuid

import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import test_resource.graphql as gql
from .payment import StagingPayment

logger = logging.getLogger(__name__)


class StagingSubscriptions:
    subscription_host = f"{os.environ['api_host']}"
    subscription_gql = f"{subscription_host}/graphql"

    @classmethod
    def create_customer(
        cls, user_name: str, password: str, account_id: str, customer_name: str, customer_email: str = "auto"
    ):
        token = StagingPayment.get_login_token(user_name, password)
        if customer_email == "auto":
            customer_email = f"auto_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}@auto.com"
        description = f"Automation {uuid.uuid4()}"
        headers = {"Authorization": f"Bearer {token}"}
        variables = {
            "accountId": account_id,
            "name": customer_name,
            "email": customer_email,
            "description": description,
        }

        r = requests.post(
            url=cls.subscription_gql,
            json={"query": gql.account.CREATE_CUSTOMER, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Create customer failed】： {str(t)}")
            logger.info(f"【Create customer passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Create customer failed】： {r.text}")

    @classmethod
    def create_product(
        cls, user_name: str, password: str, account_id: str, name: str = None, pricing_plan: list = None
    ):
        if pricing_plan is None:
            pricing_plan = [
                {
                    "active": True,
                    "amount": 3,
                    "currency": "USD",
                    "interval": "minute",
                    "intervalCount": 1,
                    "purchaseType": "recurring",
                }
            ]
        if name is None:
            name = f"Product_{uuid.uuid4()}"
        token = StagingPayment.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"accountId": account_id, "name": name, "pricingPlans": pricing_plan}

        r = requests.post(
            url=cls.subscription_gql,
            json={"query": gql.account.CREATE_PRODUCT, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Create product failed】： {str(t)}")
            logger.info(f"【Create product passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Create product failed】： {r.text}")

    @classmethod
    def get_subscriptions(cls, subscriptions_id: str, sk_key: str):
        url = f"{cls.subscription_host}/api/subscriptions/{subscriptions_id}"
        headers = {"Authorization": f"Bearer {sk_key}"}

        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Create subscriptions failed】： {str(t)}")
            logger.info(f"【Create subscriptions passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Create subscriptions failed】： {r.text}")

    @classmethod
    def get_products_list_by_id(cls, sk_key: str, product_id: str):
        url = f"{cls.subscription_host}/api/products/{product_id}"
        headers = {"Authorization": f"Bearer {sk_key}"}

        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get product by id {product_id} failed】： {str(t)}")
            logger.info(f"【Get product by id {product_id} passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get product by id {product_id} failed】： {r.text}")

    @classmethod
    def get_payment_currency(cls, user_name, password):
        token = StagingPayment.get_login_token(user_name, password)
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.post(
            url=cls.subscription_gql,
            json={"query": gql.account.GET_PAYMENT_CURRENCY},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()["data"]["paymentCurrencies"]
            logger.info(f"【Get payment currency passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get payment currency failed】： {r.text}")

    @classmethod
    def create_subscription_with_customer(
        cls,
        secret_key: str,
        pricing_plan_id: str,
        customer_object: bool = False,
        customer_id: str = None,
        ref_id: str = None,
        email: str = None,
        name: str = None,
    ):
        url = f"{cls.subscription_host}/api/subscriptions"
        headers = {"Authorization": f"Bearer {secret_key}", "Content-Type": "application/json"}
        data = {
            "cycle_count": 1,
            "cancel_at_period_end": True,
            "note": "string",
            "reference": "string",
            "return_url": "https://crypto.org",
            "items": [{"plan_id": f"{pricing_plan_id}", "quantity": 1}],
        }
        if customer_id:
            data["customer_id"] = customer_id
        if customer_object:
            data["customer"] = {
                "customer_details": {
                    "shipping_details": {
                        "address": "string",
                        "address2": "string",
                        "city": "string",
                        "state": "string",
                        "country": "string",
                        "postal_code": "string",
                        "phone": "string",
                    },
                    "billing_details": {
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
            if name:
                data["customer"]["name"] = name
            if email:
                data["customer"]["email"] = email
            if ref_id:
                data["customer"]["ref_id"] = ref_id

        r = requests.post(url=url, json=data, headers=headers)
        if r.status_code == 200:
            t = r.json()
            logger.info(f"【Create Subscription passed】：{str(t)}")
            return t
        else:
            logger.info(r.json()["error"])
            return r.json()["error"]

    @classmethod
    def update_customer(
        cls,
        token: str,
        customer_id: str,
        email: str,
        name: str,
        billing_details: dict,
        shipping_details: dict,
        shipping_diff_billing: bool,
    ):

        headers = {"Authorization": f"Bearer {token}"}
        variables = {
            "customerDetails": {
                "billingDetails": billing_details,
                "shippingDiffBilling": shipping_diff_billing,
            },
            "customerId": customer_id,
            "description": None,
            "email": email,
            "name": name,
        }
        if shipping_diff_billing:
            variables["customerDetails"]["shippingDetails"] = shipping_details
        r = requests.post(
            url=cls.subscription_gql,
            json={"query": gql.account.UPDATE_CUSTOMER, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Update customer failed】： {str(t)}")
            logger.info(f"【Update customer passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Update customer failed】： {r.text}")

    @classmethod
    def get_payout_report(cls, report_token: str, merchant_name: str, from_date: str, to_date: str):
        headers = {"Authorization": f"Bearer {report_token}"}
        variables = {
            "first": 100,
            "filterBy": {"fromDate": from_date, "toDate": to_date},
        }
        r = requests.post(
            url=f"{cls.subscription_host}/report/graphql",
            json={"query": gql.balances.GET_PAYOUT_REPORT, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get payout report failed】： {str(t)}")
            logger.info(f"【Get payout report passed】：{str(t)}")
            node_list: list = t["data"]["payouts"]["nodes"]
            filtered_node_list = list(filter(lambda x: x["merchantName"] == merchant_name, node_list))
            return filtered_node_list[0]
        else:
            raise Exception(f"【Get payout report failed】： {r.text}")

    @classmethod
    def get_slack_message(cls, slack_bot_token: str, channel_id: str):
        client = WebClient(token=slack_bot_token)
        channel_id = channel_id
        try:
            history = client.api_call(api_method="conversations.history", data={"channel": channel_id})
            time.sleep(10)
            conversation_history = history["messages"]
            logger.info("Get conversion history from slack channel passed")
            return conversation_history
        except SlackApiError as e:
            logger.error("Error retrieving conversation: {}".format(e))

    @classmethod
    def enable_card_payment(cls, token: str, team_id: str):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"channel": "card_payment", "enabled": True, "teamId": team_id}
        r = requests.post(
            url=cls.subscription_gql,
            json={"query": gql.account.UPDATE_CARD_PAYMENT, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Enable Card Payment failed】： {str(t)}")
            logger.info(f"【Enable Card Payment passed】：{str(t)}")
        else:
            raise Exception(f"【Update Card Payment failed】： {r.text}")

    @classmethod
    def create_crypto_purchase(
        cls,
        secret_key: str,
        wallet_address: str,
        fiat_currency: str,
        network: str,
        amount: str,
        order_currency: str,
        return_url: str = "https://www.sina.com",
        cancel_url: str = "https://www.google.com",
        ref_user_id: str = "aa123456789",
        session_id: str = "aa123456789",
        device_id: str = "aa123456789",
    ):
        headers = {"Authorization": f"Bearer {secret_key}"}
        data = {
            "cancel_url": cancel_url,
            "currency": fiat_currency,
            "network": network,
            "order_amount": amount,
            "order_currency": order_currency,
            "return_url": return_url,
            "wallet_address": wallet_address,
            "device_id": device_id,
            "ref_user_id": ref_user_id,
            "session_id": session_id,
        }
        r = requests.post(
            url=f"{cls.subscription_host}/api/crypto_purchases",
            json=data,
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Create crypto purchase failed】： {str(t)}")
            logger.info(f"【Create crypto purchase passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Create crypto purchase failed】： {r.text}")

    @classmethod
    def create_crypto_purchase_catch_error(
        cls,
        secret_key: str,
        wallet_address: str,
        fiat_currency: str,
        network: str,
        amount: str,
        order_currency: str,
        return_url: str = "https://www.sina.com",
        cancel_url: str = "https://www.google.com",
        ref_user_id: str = "123456789",
        session_id: str = "123456789",
        device_id: str = "123456789",
    ):
        headers = {"Authorization": f"Bearer {secret_key}"}
        data = {
            "cancel_url": cancel_url,
            "currency": fiat_currency,
            "network": network,
            "order_amount": amount,
            "order_currency": order_currency,
            "return_url": return_url,
            "wallet_address": wallet_address,
            "device_id": device_id,
            "ref_user_id": ref_user_id,
            "session_id": session_id,
        }
        r = requests.post(
            url=f"{cls.subscription_host}/api/crypto_purchases",
            json=data,
            headers=headers,
        )
        if r.status_code != 200:
            t = r.json()
            logger.info(f"【Create crypto purchase failed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Create crypto purchase passed】： {r.text}")

    @classmethod
    def get_crypto_purchase_amount_by_wallet_address(
        cls, report_token: str, from_date: str, to_date: str, wallet_address: str
    ):
        headers = {"Authorization": f"Bearer {report_token}"}
        variables = {
            "first": 100,
            "filterBy": {"fromDate": from_date, "toDate": to_date, "walletAddress": wallet_address},
        }
        r = requests.post(
            url=f"{cls.subscription_host}/report/graphql",
            json={"query": gql.balances.GET_CRYPTO_PURCHASE_AMOUNT, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get crypto purchase report failed】： {str(t)}")
            logger.info("【Get crypto purchase report passed】")
            nodes = t["data"]["cryptoPurchases"]["nodes"]
            return nodes
        else:
            raise Exception(f"【Get crypto purchase report failed】： {r.text}")

    @classmethod
    def set_crypto_purchase_send_otp_count(cls, support_token: str, email_address: str, send_count: str):
        headers = {"Authorization": f"Bearer {support_token}"}
        r = requests.post(
            url=f"{cls.subscription_host}/testing_supports/set_send_otp_count",
            headers=headers,
            data={"email": email_address, "send_count": send_count},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys() or t["succ"] is False:
                raise Exception(f"【set send otp count with {send_count} failed】： {str(t)}")
            else:
                logger.info(f"【set send otp count with {send_count} passed】")

    @classmethod
    def get_crypto_purchase_otp_code(cls, pk_key: str, email_address: str):
        headers = {"Authorization": f"Bearer {pk_key}"}
        r = requests.post(
            url=f"{cls.subscription_host}/api/crypto_purchases/send_otp",
            headers=headers,
            data={"email": email_address},
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys() or t["ok"] is False:
                raise Exception(f"【get otp code by {email_address} failed】： {str(t)}")
            return t["code"]
        else:
            raise Exception(f"【get otp code by {email_address} failed】： {str(r)}")

    @classmethod
    def get_crypto_purchase_details(cls, ops_token: str, crypto_purchase_id: str):
        headers = {"Authorization": f"Bearer {ops_token}"}
        variables = {"page": 1, "perPage": 10, "filterBy": {"keyword": crypto_purchase_id}}
        r = requests.post(
            url=f"{cls.subscription_host}/ops/graphql",
            json={"query": gql.balances.GET_CRYPTO_PURCHASE_DETAILS, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get crypto purchase details failed】： {str(t)}")
            logger.info("【Get crypto purchase details passed】")
            nodes = t["data"]["cryptoPurchases"]["nodes"]
            return nodes[0]
        else:
            raise Exception(f"【Get crypto purchase details failed】： {r.text}")

    @classmethod
    def get_crypto_purchase_card_inbound_details(cls, ops_token: str, crypto_purchase_id: str):
        headers = {"Authorization": f"Bearer {ops_token}"}
        variables = {"page": 1, "perPage": 10, "filterBy": {"keyword": crypto_purchase_id}}
        r = requests.post(
            url=f"{cls.subscription_host}/ops/graphql",
            json={"query": gql.balances.GET_CRYPTO_PURCHASE_CARD_INBOUND_DETAILS, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get crypto purchase card inbound fund details failed】： {str(t)}")
            logger.info("【Get crypto purchase card inbound fund details passed】")
            nodes = t["data"]["cardInboundFunds"]["nodes"]
            return nodes[0]
        else:
            raise Exception(f"【Get crypto purchase card inbound fund details failed】： {r.text}")

    @classmethod
    def get_pay_core_troubleshooting_by_purchase_id(cls, ops_token: str, verify_type: str, crypto_purchase_id: str):
        headers = {"Authorization": f"Bearer {ops_token}"}
        variables = {
            "filterBy": {
                "businessType": "purchase",
                "businessId": crypto_purchase_id,
                "relatedBusinessType": verify_type,
            }
        }
        r = requests.post(
            url=f"{cls.subscription_host}/ops/graphql",
            json={"query": gql.balances.GET_CRYPTO_PURCHASE_TROUBLESHOOTING_DETAILS, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get crypto purchase troubleshooting details failed】： {str(t)}")
            logger.info("【Get crypto purchase troubleshooting details passed】")
            troubleshooting_status = t["data"]["troubleshootingPayCoreGeneralQuery"][0]["status"]
            return troubleshooting_status
        else:
            raise Exception(f"【Get crypto purchase troubleshooting details failed】： {r.text}")

import logging
import os

import requests
import test_resource.graphql as gql

logger = logging.getLogger(__name__)


class StagingSubscriptionsOps:
    subscription_host = f"{os.environ['api_host']}"
    subscription_ops_gql = f"{subscription_host}/ops/graphql"

    @classmethod
    def update_product_permission(cls, ops_token: str, roleId: str, update_status: str, permissions: list = None):
        headers = {"authorization": f"Bearer {ops_token}"}
        if update_status.lower() == "false":
            status = ["unavailable"]
        else:
            status = ["create", "view"]
        if permissions is None:
            permissions = [
                {"controlScope": "enableAccount", "controlActions": ["view", "enable"]},
                {"controlScope": "liveAccount", "controlActions": ["view"]},
                {"controlScope": "balance", "controlActions": ["view"]},
                {"controlScope": "metrics", "controlActions": ["view"]},
                {"controlScope": "payment", "controlActions": ["view"]},
                {"controlScope": "paymentRefund", "controlActions": ["view", "create"]},
                {"controlScope": "unresolvedInboundFunds", "controlActions": ["view"]},
                {"controlScope": "transaction", "controlActions": ["view"]},
                {"controlScope": "payout", "controlActions": ["view", "create"]},
                {"controlScope": "invoice", "controlActions": ["view", "create", "delete", "update", "send"]},
                {"controlScope": "customer", "controlActions": ["view", "create", "update", "delete"]},
                {"controlScope": "publishableKey", "controlActions": ["view"]},
                {"controlScope": "apiKeys", "controlActions": ["view", "create"]},
                {"controlScope": "secretKey", "controlActions": ["view"]},
                {"controlScope": "keysCreatedAt", "controlActions": ["view"]},
                {"controlScope": "webhook", "controlActions": ["view", "create", "update"]},
                {"controlScope": "woocommerce", "controlActions": ["view", "create", "update"]},
                {"controlScope": "webhookEvents", "controlActions": ["view"]},
                {"controlScope": "member", "controlActions": ["view", "update"]},
                {"controlScope": "payoutAccount", "controlActions": ["view", "create", "update"]},
                {"controlScope": "paymentSettings", "controlActions": ["view", "update"]},
                {"controlScope": "businessSettings", "controlActions": ["view", "update"]},
                {"controlScope": "businessOwners", "controlActions": ["view", "create", "update", "delete"]},
                {"controlScope": "conversion", "controlActions": ["view", "create", "cancel", "confirm", "refresh"]},
                {"controlScope": "payChannel", "controlActions": ["view", "update"]},
                {"controlScope": "invitation", "controlActions": ["view", "create", "resend", "cancel"]},
                {"controlScope": "product", "controlActions": status},
                {"controlScope": "subscription", "controlActions": ["view", "create"]},
                {"controlScope": "subMerchant", "controlActions": ["view", "create", "update"]},
                {"controlScope": "reboundLink", "controlActions": ["view", "update"]},
            ]
        variables = {
            "roleId": roleId,
            "permissions": permissions,
            "name": "Owner",
            "description": "test",
            "scopeLevel": "1",
        }
        r = requests.post(
            url=cls.subscription_ops_gql,
            json={"query": gql.account.UPDATE_OPS_PRODUCT_PERMISSION, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【update product permission failed】： {str(t)}")
            logger.info(f"【update product permission passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【update product permission failed】： {r.text}")

    @classmethod
    def get_role(cls, ops_token: str):
        headers = {"authorization": f"Bearer {ops_token}"}
        r = requests.post(
            url=cls.subscription_ops_gql,
            json={"query": gql.account.GET_PRODUCT_ROLE_ID},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【get owner role id failed】： {r.text}")
            return t
        else:
            raise Exception(f"【get owner role id failed】： {r.text}")

    @classmethod
    def get_sub_merchant_mcc_code(cls, ops_token: str):
        headers = {"authorization": f"Bearer {ops_token}"}
        variables = {}
        r = requests.post(
            url=cls.subscription_ops_gql,
            json={"query": gql.account.GET_SUB_MERCHANT_MCC_CODE, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get Sub_Merchant MCC code failed】： {str(t)}")
            return t["data"]["mccCodes"]
        else:
            raise Exception(f"【Get Sub_Merchant MCC code failed】： {r.text}")

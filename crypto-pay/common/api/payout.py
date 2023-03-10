import logging
import os

import requests

import test_resource.graphql as gql

logger = logging.getLogger(__name__)


class StagingPayout:
    payout_host = f"{os.environ['api_host']}"
    payout_gql = f"{payout_host}/graphql"

    @classmethod
    def create_payout_account(
        cls,
        address_type: str,
        currency: str,
        team_id: str,
        token: str,
        two_fa_token: str,
        payout_account_details: dict,
        auto_payout_settings: dict = None,
    ):
        """
        Create payout account
        @param address_type: wallet or fiat
        @param currency: currency
        @param team_id: team_id
        @param token: user token
        @param two_fa_token: two_fa_token
        @param payout_account_details:
            payout_account_details for fiat
                account_number: "1234567898"
                account_holder: "Automation Tester"
                account_holder_type: "individual" or "corporate"
                ach_account_type: "checking" or "savings"
                country_code: "AT"
                mode: "auto" or ""manual
            payout_account_details for wallet
                mode: "auto" or ""manual
                account_holder: "Automation Tester"
                address: "0x30509945d2B329Cc253A8Bb2E2c54bDBb08B1070"
                wallet_currency: "USD" | "CAD" | "AUD" | "GBP"
        @param auto_payout_settings: provide if mode is auto
            schedule_type: "weekly"
            percentage: 50 or any number from 10 to 100 which is divisible by 10
        """
        headers = {"Authorization": f"Bearer {token}", "X-2fa-secret": two_fa_token}
        variables = {
            "currency": currency,
            "accountHolder": payout_account_details["account_holder"],
            "mode": payout_account_details["mode"],
            "teamId": team_id,
        }
        if address_type == "wallet":
            additional_variables = {
                "address": payout_account_details["address"],
                "addressType": "wallet",
                "walletCurrency": payout_account_details["wallet_currency"],
            }
        else:
            additional_variables = {
                "accountHolderType": payout_account_details["account_holder_type"],
                "accountNumber": payout_account_details["account_number"],
                "achAccountType": payout_account_details["ach_account_type"],
                "addressType": f"fiat_{currency.lower()}",
                "businessAddress": "12 Automation Test Address",
                "countryCode": payout_account_details["country_code"],
                "swiftCode": "ABFDGB22",
                "via": "send_wyre",
                "walletCurrency": currency,
            }
        variables.update(additional_variables)
        if auto_payout_settings is not None:
            variables["autoPayoutSettings"] = {}
            auto_settings = {
                "scheduleType": auto_payout_settings["schedule_type"],
                "percentage": auto_payout_settings["percentage"],
            }
            variables["autoPayoutSettings"].update(auto_settings)

        r = requests.post(
            url=cls.payout_gql,
            json={"query": gql.payout.CREATE_PAYOUT_ACCOUNT, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Create payout account failed】： {str(t)}")
            logger.info(f"【Create payout account】：{str(t)}")
            return t["data"]["createPayoutAccount"]["payoutAccount"]["id"]
        else:
            raise Exception(f"【Create payout account failed】： {r.text}")

    @classmethod
    def create_shop_owner(cls, token, team_id, user_id, first_name, last_name):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {
            "userId": user_id,
            "firstName": first_name,
            "lastName": last_name,
            "nationality": "AF",
            "idCard": "23546789",
            "dateOfBirth": "2022-10-21T03:14:41.778Z",
            "homeAddress": "Home Address Test Automation",
            "homeAddress2": "",
            "province": "Province Test Automation",
            "region": "Region Test Automation",
            "country": "AF",
            "zipCode": "234",
            "teamId": team_id,
            "isRepresentative": True,
        }
        r = requests.post(
            url=cls.payout_gql,
            json={"query": gql.payout.CREATE_SHOP_OWNER, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Create shop owner failed】： {str(t)}")
            logger.info(f"【Create shop owner】：{str(t)}")
        else:
            raise Exception(f"【Create shop owner failed】： {r.text}")

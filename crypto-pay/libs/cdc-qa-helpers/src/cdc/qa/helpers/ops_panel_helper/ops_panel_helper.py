import logging
import os
import time
from typing import Union, Set, TypeVar, Type, List

import requests

import json
from cdc.qa.core import secretsmanager as se
from cdc.qa.apis.qa_tools import QAToolsApiServices

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from cdc.qa.helpers.ops_panel_helper import UserFeatureFlag
from cdc.qa.helpers.ops_panel_helper.data import UserTag

logger = logging.getLogger(__name__)


UserTagOrFeatureFlag = Union[UserTag, UserFeatureFlag]
T = TypeVar("T", bound=UserTagOrFeatureFlag)


class OpsPanelKeyRefresher:
    REFRESHER_URL = "http://10.10.170.21"
    EXPIRE_TIME = 10 * 60
    _data: dict = {"last_updated": 0}

    @classmethod
    def refresher_update(cls):
        url = f"{cls.REFRESHER_URL}/key/api/get"
        cls._data = requests.get(url).json()

    @classmethod
    def refresher_expired(cls) -> bool:
        return time.time() > cls._data["last_updated"] + cls.EXPIRE_TIME

    @classmethod
    def get_keys(cls):
        if cls.refresher_expired():
            cls.refresher_update()
        return cls._data["opspanel_key"], cls._data["x_csrf_token"]


class OpsPanelHelper:
    # Default stg
    OPS_HOST = "https://ops.3ona.co"
    GQL_URL = f"{OPS_HOST}/graphql"

    def __init__(self):
        self.OPS_HOST = f"https://{os.environ.get('OPS_ENV_HOST', 'ops.3ona.co')}"
        self.GQL_URL = f"{self.OPS_HOST}/graphql"

    @staticmethod
    def __get_ops_token__():
        key_pair = json.loads(se.get_secret("main-app-ops-panel-key"))
        data = (
            QAToolsApiServices(
                secret_key=key_pair["API_MAINAPP_SECRET_KEY"],
                api_key=key_pair["API_MAINAPP_API_KEY"],
            )
            .ops.get_ops_panel_token(env=os.environ.get("ENV", "stg"))
            .data
        )
        return data.opspanel_key, data.x_csrf_token

    @staticmethod
    def get_client() -> Client:
        opspanel_key, x_csrf_token = OpsPanelHelper.__get_ops_token__()
        transport = RequestsHTTPTransport(
            url=OpsPanelHelper().GQL_URL,
            headers={
                "cookie": f"_opspanel_key={opspanel_key}",
                "x-csrf-token": x_csrf_token,
            },
        )
        return Client(transport=transport)

    @staticmethod
    def ops_panel_approve(user_id, dob="1999-12-31", legal_name="Auto QA", status="approved"):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation UpdateIdentity($userId: Int!, $identityInput: UpdateIdentityParams!) {
                updateIdentity(userId: $userId, identityInput: $identityInput) {
                    id
                }
            }
            """
        )
        params = {
            "userId": user_id,
            "identityInput": {
                "livenessReviewStatus": "approved",
                "verification": status,
                "riskLevel": "low",
                "reviewNote": "account auto create",
                "dob": dob,
                "name": legal_name,
            },
        }
        return client.execute(query, variable_values=params)

    @staticmethod
    def get_user_uuid(user_id: int):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            query userBasicInfo($id: Int) {
              user(id: $id) {
                uuid
              }
            }
            """
        )

        params = {"id": user_id}

        return client.execute(query, variable_values=params)["user"]["uuid"]

    @staticmethod
    def get_compliance_list(email):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            query searchComplianceList($filter: UserFilter!) {
                users(filter: $filter) {
                    userRows {
                        id
                        email
                        identity {
                            verification
                        }
                    }
                }
            }
            """
        )
        params = {"filter": {"email": email}}
        return client.execute(query, variable_values=params)

    @staticmethod
    def get_verification_status(user_id):
        """
        Args:
            user_id: Crypto App user id

        Returns:
            user's verification status
        """

        client = OpsPanelHelper.get_client()
        query = gql(
            """
            query GetComplianceUserData($id: Int!) {
                user(id: $id){
                    identity{
                        verification
                    }
                }
            }
            """
        )
        params = {"id": user_id}
        resp = client.execute(query, variable_values=params)
        logger.info(f"user verification status: {resp['user']['identity']['verification']}")
        return resp["user"]["identity"]["verification"]

    @staticmethod
    def get_manual_liveless_image(user_id):
        """
        Args:
            user_id: Crypto App user id

        Returns:
            requests response if status code = 200, else return None
        """
        url = f"{OpsPanelHelper().OPS_HOST}/api/jumio/{user_id}/manual_liveness"
        opspanel_key, x_csrf_token = OpsPanelHelper.__get_ops_token__()
        headers = {
            "content-type": "application/json",
            "cookie": f"_opspanel_key={opspanel_key}",
            "x-csrf-token": x_csrf_token,
        }
        response = requests.request("GET", url, headers=headers, verify=False)
        logger.info(f"Get manual liveless image response status code: {response.status_code}")
        logger.debug(response.json())
        if response.status_code == 200:
            return response.json().get("image_url", {}).get("image_url")

    @staticmethod
    def _get_property_type_str(property_type: Type[UserTagOrFeatureFlag]) -> str:
        if property_type is UserTag:
            return "tags"
        elif property_type is UserFeatureFlag:
            return "features"
        else:
            raise ValueError

    def _parse_flags_into_set(self, flags: List[str], property_type: Type[T]) -> Set[Union[str, T]]:
        new_flags = set()
        for flag in flags:
            try:
                new_flags.add(property_type[flag])
            except KeyError:
                logger.warning(f"Flag {flag} is not added to {property_type}.")
                new_flags.add(flag)
        return new_flags

    def _get_user_properties(self, user_id: int, property_type: Type[T]) -> Set[Union[str, T]]:
        type_in_str = self._get_property_type_str(property_type)

        client = OpsPanelHelper.get_client()
        query = gql(
            f"""
            query GetComplianceUserData($id: Int!) {{
                user(id: $id){{
                    {type_in_str}
                }}
            }}
            """
        )
        params = {"id": user_id}
        resp = client.execute(query, variable_values=params)
        return self._parse_flags_into_set(resp["user"][type_in_str], property_type)

    def _update_user_properties(self, user_id: int, property_type: Type[T], property_set: Set[Union[str, T]]):
        type_in_str = self._get_property_type_str(property_type)

        client = OpsPanelHelper.get_client()
        query = gql(
            f"""
            mutation updateUser($id: Int!, $userInput: UpdateUserParams!) {{
                updateUser(id: $id, userInput: $userInput){{
                    {type_in_str}
                }}
            }}
            """
        )

        properties_in_str_list = []
        for property in property_set:
            if type(property) is str:
                properties_in_str_list.append(property)
            else:
                properties_in_str_list.append(property.value)
        params = {"id": user_id, "userInput": {type_in_str: properties_in_str_list}}
        client.execute(query, variable_values=params)

    def _add_user_properties(
        self,
        user_id: int,
        property_type: Type[T],
        properties_to_be_added: Union[str, T, Set[Union[str, T]]],
    ):
        properties = self._get_user_properties(user_id, property_type)

        if isinstance(properties_to_be_added, (UserTag, UserFeatureFlag, str)):
            properties_to_be_added = {properties_to_be_added}

        properties |= properties_to_be_added
        self._update_user_properties(user_id, property_type, properties)

    def _remove_user_properties(
        self,
        user_id: int,
        property_type: Type[T],
        properties_to_be_removed: Union[str, T, Set[Union[str, T]]],
    ):
        properties = self._get_user_properties(user_id, property_type)

        if isinstance(properties_to_be_removed, (str, UserTag, UserFeatureFlag)):
            properties_to_be_removed = {properties_to_be_removed}

        properties -= properties_to_be_removed
        self._update_user_properties(user_id, property_type, properties)

    def get_user_feature_flags(self, user_id: int) -> Set[Union[str, UserFeatureFlag]]:
        """
        Args:
            user_id: Crypto App user id

        Returns:
            List of feature flags in enum UserFeatureFlag
        """
        return self._get_user_properties(user_id, UserFeatureFlag)

    def _update_user_feature_flags(self, user_id: int, feature_flags: Set[Union[str, UserFeatureFlag]]):
        """
        Args:
            user_id: Crypto App user id
            feature_flags(list): ALL user feature flags in list
        """
        self._update_user_properties(user_id, UserFeatureFlag, feature_flags)

    def add_user_feature_flags(
        self,
        user_id: int,
        feature_flags_to_be_added: Union[str, UserFeatureFlag, Set[Union[str, UserFeatureFlag]]],
    ):
        """
        Add user feature flags to specific user account

        Args:
            user_id: Crypto App user id
            feature_flags_to_be_added: feature flag(s) to be added, take enum UserFeatureFlag or list of UserFeatureFla
            -gs
        """
        self._add_user_properties(user_id, UserFeatureFlag, feature_flags_to_be_added)

    def remove_user_feature_flags(
        self,
        user_id: int,
        feature_flags_to_be_removed: Union[str, UserFeatureFlag, Set[Union[str, UserFeatureFlag]]],
    ):
        """Remove user feature flags to specific user account

        Args:
            user_id: Crypto App user id
            feature_flags_to_be_removed: feature flag(s) to be removed, take enum UserFeatureFlag or list of UserFeature
            -Flags
        """
        return self._remove_user_properties(user_id, UserFeatureFlag, feature_flags_to_be_removed)

    def get_user_tags(self, user_id: int) -> Set[Union[str, UserTag]]:
        return self._get_user_properties(user_id, UserTag)

    def add_user_tags(self, user_id: int, tags_to_be_added: Union[str, UserTag, Set[Union[str, UserTag]]]):
        """Add user tags to specific user account

        Args:
            user_id: Crypto App user id
            tags_to_be_added: User tag(s) to be added, take enum UserTag or list of UserTags
        """
        self._add_user_properties(user_id, UserTag, tags_to_be_added)

    def remove_user_tags(self, user_id: int, tags_to_be_removed: Union[str, UserTag, Set[Union[str, UserTag]]]):
        """Remove user tags to specific user account

        Args:
            user_id: Crypto App user id
            tags_to_be_removed: User tag(s) to be removed, take enum UserTag or list of UserTags
        """
        self._remove_user_properties(user_id, UserTag, tags_to_be_removed)

    def approve_bank_account(self, user_id: int):
        user_uuid = self.get_user_uuid(user_id)
        ids = self._get_bank_account_ids(user_uuid)
        for account_id in ids:
            self._approve_bank_account_by_id(account_id["id"])

    @staticmethod
    def _get_bank_account_ids(user_uuid: str):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            query bankAccounts($filter: BankAccountFilter) {
              bankAccounts(filter: $filter) {
                bankAccountRows {
                  id
                }
              }
            }
            """
        )

        params = {
            "filter": {"user_uuid": user_uuid},
        }
        return client.execute(query, variable_values=params)["bankAccounts"]["bankAccountRows"]

    @staticmethod
    def _approve_bank_account_by_id(account_id: str):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation approveBankAccount($bankAccountId: String!) {
                approveBankAccount(bankAccountId: $bankAccountId)
            }
            """
        )

        params = {"bankAccountId": account_id}
        return client.execute(query, variable_values=params)

    @staticmethod
    def get_sms_verification_status(user_id: int) -> bool:
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            query GetComplianceUserData($id: Int!) {
                user(id: $id){
                    mainAppSmsVerificationStatus
                }
            }
            """
        )
        params = {"id": user_id}
        resp = client.execute(query, variable_values=params)
        status = resp["user"]["mainAppSmsVerificationStatus"]
        logger.debug(f"SMS verification status: {status}")
        return status

    def set_sms_verification_status(self, user_id: int, state: bool):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation UpdateUserMainAppSmsVerification($userUuid: String!, $state: Boolean!) {
                updateUserMainAppSmsVerification(userUuid: $userUuid, state: $state)
            }
            """
        )
        params = {
            "userUuid": self.get_user_uuid(user_id),
            "state": state,
        }
        return client.execute(query, variable_values=params)

    @staticmethod
    def revoke_totp(user_id):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation revokeTotp($userId: Int!) {
                revokeTotp(userId: $userId)
            }
            """
        )

        params = {"userId": user_id}
        return client.execute(query, variable_values=params)

    def ca_dc_bank_application_attempts_reset(self, user_id):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation resetCaDcbankApplicationAttempt($userUuid: String!, $reset: Boolean!) {
                resetCaDcbankApplicationAttempt(userUuid: $userUuid, reset: $reset)
            }
            """
        )

        params = {"userUuid": self.get_user_uuid(user_id), "reset": True}
        resp = client.execute(query, variable_values=params)
        logger.debug(f"Reset Ca Dcbank Application Attempt status: {resp}")

    def ca_dc_bank_application_approve(self, user_id):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation updateCaDcbankApplicationState($userUuid: String!, $state: String!) {
                updateCaDcbankApplicationState(userUuid: $userUuid, state: $state)
            }
            """
        )

        params = {"userUuid": self.get_user_uuid(user_id), "state": "approved"}
        resp = client.execute(query, variable_values=params)
        logger.debug(f"Approved Ca Dcbank Application status: {resp}")

    def ca_dc_bank_application_reject(self, user_id):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation updateCaDcbankApplicationState($userUuid: String!, $state: String!) {
                updateCaDcbankApplicationState(userUuid: $userUuid, state: $state)
            }
            """
        )

        params = {"userUuid": self.get_user_uuid(user_id), "state": "rejected"}
        resp = client.execute(query, variable_values=params)
        logger.debug(f"Approved Ca Dcbank Application status: {resp}")

    def approve_uk_bcb_application(self, user_id):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation approveUkBcbApplication($userUuid: String!) {
                  approveUkBcbApplication(userUuid: $userUuid)
                  }
            """
        )

        params = {"userUuid": self.get_user_uuid(user_id)}
        return client.execute(query, variable_values=params)

    def approve_uk_mco_card_application(self, user_id):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation updateWirecardUkCardApplicationState($userUuid: String!, $state: String!) {
                updateWirecardUkCardApplicationState(userUuid: $userUuid, state: $state)
                }
            """
        )
        params = {"userUuid": self.get_user_uuid(user_id), "state": "approved"}
        return client.execute(query, variable_values=params)

    def approve_foris_au_card_application(self, user_id):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation updateAusForisVerificationStatus($userUuid: UUID!, $status: String!) {
                updateAusForisVerificationStatus(userUuid: $userUuid, status: $status)
                }
            """
        )
        params = {"userUuid": self.get_user_uuid(user_id), "status": "approved"}
        return client.execute(query, variable_values=params)

    def update_wire_card_application(self, user_id):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation updateWirecardUkApplication($state: String!, $addressInput: UpdateWirecardUkAddressParams!, $userUuid: String!) {
                updateWirecardUkCardApplicationAddress(addressInput: $addressInput, userUuid: $userUuid)
                updateWirecardUkCardApplicationState(state: $state, userUuid: $userUuid)
            }
            """  # noqa: E501
        )

        params = {
            "state": "approved",
            "addressInput": {
                "address1": "address1",
                "address2": "address2",
                "city": "London",
                "countryCode": "GBR",
                "postcode": "11111",
                "state": "",
            },
            "userUuid": self.get_user_uuid(user_id),
        }
        return client.execute(query, variable_values=params)

    # fmt: off
    def get_card_provider(self, user_id):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            query UserCardApplication($userId: Int!, $maskUserPiiFields: Boolean) {
              user(id: $userId, maskUserPiiFields: $maskUserPiiFields) {
                id
                cardProvider
                uuid
                tags
                cardApplication {
                  cardApplicationState
                  addressVerification
                  termsAccepted
                  residentialAddress {
                    address1
                    address2
                    city
                    country
                    postcode
                    stateCode
                    zipCode
                    __typename
                  }
                  shippingAddress {
                    address1
                    address2
                    postcode
                    country
                    city
                    __typename
                  }
                  shipping {
                    state
                    courier
                    trackingNumber
                    __typename
                  }
                  differentAddressForShipping
                  applicationCompleted
                  shippingAddressLogData
                  residentialAddressLogData
                  residentialAddressProofScanProvider
                  residentialAddressProofScanReference
                  __typename
                }
                __typename
              }
              cardReservation(filter: {userId: $userId}, maskUserPiiFields: $maskUserPiiFields) {
                nameOnCard
                firstName
                lastName
                __typename
              }
              identity(filter: {userId: $userId}, maskUserPiiFields: $maskUserPiiFields) {
                name
                __typename
              }
            }
            """
        )
        param = {
            "userId": user_id
        }
        return client.execute(query, variable_values=param)["user"]["cardProvider"]

    def approve_card_application(self, user_id):
        card_provider = self.get_card_provider(user_id)
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation UpdateCardApplicationVerificationStatus($userUuid: UUID!, $cardProvider: String!, $status: String!) {
                updateCardApplicationVerificationStatus(userUuid: $userUuid, cardProvider: $cardProvider, status: $status)
            }
            """  # noqa: E501
        )
        params = {
            "cardProvider": card_provider,
            "status": "approved",
            "userUuid": self.get_user_uuid(user_id)
        }
        return client.execute(query, variable_values=params)
    # fmt: on

    def brl_wallet_approve(self, user_id):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation updateBrlBancoPluralApplicationState($userUuid: String!, $state: BrlBancoPluralState!) {
                updateBrlBancoPluralApplicationState(userUuid: $userUuid, state: $state)
            }
            """
        )

        params = {"userUuid": self.get_user_uuid(user_id), "state": "ESCALATED"}
        resp = client.execute(query, variable_values=params)
        logger.debug(f"Approved BRL wallet Application status: {resp}")

        time.sleep(30)

        params = {"userUuid": self.get_user_uuid(user_id), "state": "APPROVED"}
        resp = client.execute(query, variable_values=params)
        logger.debug(f"Approved BRL wallet Application status: {resp}")

    def resolve_cra_report_address_manual_review(self, user_id: str, decision: str, reason: str = "tseting"):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
                mutation resolveCraReportAddressManualReview($userUuid: UUID!, $decision: String!, $reason: String!) {
                    resolveCraReportAddressManualReview(userUuid: $userUuid, decision: $decision, reason: $reason)
                    {
                        id
                        status
                        __typename
                    }
                }
            """
        )

        params = {"userUuid": self.get_user_uuid(user_id), "decision": decision, "reason": reason}
        return client.execute(query, variable_values=params)

    def circle_application_verification_step(
        self,
        action: str,
        application_id: str,
        reason: str = "testing",
        verificationSteps: List[str] = None,
    ):
        """action: failed, approve, reject"""
        client = OpsPanelHelper.get_client()

        def failed_query():
            q = gql(
                """
                mutation failUsdcSwiftApplication($id: String!, $reason: String, $verificationSteps: [String]) {
                  failUsdcSwiftApplication(
                    id: $id
                    reason: $reason
                    verificationSteps: $verificationSteps
                  )
                }
                """
            )
            p = {"id": application_id, "reason": reason, "verificationSteps": verificationSteps}
            return q, p

        def approve_query():
            g = gql(
                """
                mutation approveUsdcSwiftApplication($id: String!) {
                    approveUsdcSwiftApplication(id: $id)
                }
                """
            )
            p = {"id": application_id}
            return g, p

        def reject_query():
            q = gql(
                """
                mutation rejectUsdcSwiftApplication($id: String!, $reason: String!) {
                    rejectUsdcSwiftApplication(id: $id, reason: $reason)
                }
                """
            )
            p = {"id": application_id, "reason": reason}
            return q, p

        if action == "failed":
            query, params = failed_query()
        elif action == "approve":
            query, params = approve_query()
        elif action == "reject":
            query, params = reject_query()
        else:
            raise NotImplementedError

        return client.execute(query, variable_values=params)

    def update_dcbank_ca_card_application(self, user_id, state: str = "approved"):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation updateCaDcbankApplicationState($userUuid: String!, $state: String!) {
                updateCaDcbankApplicationState(userUuid: $userUuid, state: $state)
                }
            """
        )
        params = {"userUuid": self.get_user_uuid(user_id), "state": state}
        return client.execute(query, variable_values=params)

    def update_foris_br_card_application(self, user_id, state: str = "approved"):
        client = OpsPanelHelper.get_client()
        query = gql(
            """
            mutation updateBrlBancoPluralApplicationState($userUuid: String!, $state: BrlBancoPluralState!) {
                updateBrlBancoPluralApplicationState(userUuid: $userUuid, state: $state)
                }
            """
        )
        params = {"userUuid": self.get_user_uuid(user_id), "state": state.upper()}
        return client.execute(query, variable_values=params)

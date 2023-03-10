import os
import requests
import logging
import test_resource.graphql as gql

logger = logging.getLogger(__name__)


class StagingPaymentOps:
    _payment_ops_gql = f"{os.environ['api_host']}/ops/graphql"

    @classmethod
    def get_payouts(
        cls, ops_token: str, page: int = 1, per_page: int = 1000, filter_by: dict = None, pay_core_enable="false"
    ):
        """
        Get all payouts details then we could get the payout id to do any approve actions
        @param per_page: per_page
        @param page: page
        @param ops_token: ops token
        @param filter_by: filter by status or settlementAgent, e.g {"status":"pending"}
        @return: payouts details
        """
        headers = {"Authorization": f"Bearer {ops_token}"}

        if filter_by is None:
            filter_by = {}

        filter_by["payCore"] = pay_core_enable
        variables = {"page": page, "perPage": per_page, "filterBy": filter_by}
        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.balances.GET_OPS_PAYOUTS, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get ops payouts failed】： {str(t)}")
            return t
        else:
            raise Exception(f"【Get ops payouts failed】： {r.text}")

    @staticmethod
    def get_payout_id_by_desc(
        desc: str, ops_token: str, page: int = 1, per_page: int = 1000, filter_by: dict = None, pay_core_enable="false"
    ):
        """
        Get the payout id by the description, please input union description(note) when you create payout
        @param page: page
        @param per_page: per_page
        @param desc: description (note)
        @param ops_token: ops token
        @param filter_by: filter by status or settlementAgent, e.g {"status":"pending"}
        @return: payout id and payout status
        """
        r = StagingPaymentOps.get_payouts(ops_token, page, per_page, filter_by, pay_core_enable=pay_core_enable)
        nodes = r["data"]["payouts"]["nodes"]
        matched_node = list(filter(lambda node: node["description"] == desc, nodes))

        if len(matched_node) == 0:
            raise Exception(f"【Get payout id by desc failed】: {str(nodes)}")
        payout_id = matched_node[0]["id"]
        status = matched_node[0]["status"]
        logger.info(f"【Get payout id by desc {desc} passed】: {payout_id} with status {status}")
        return payout_id, status

    @staticmethod
    def get_payout_id_by_shop_name(
        shop_name: str,
        ops_token: str,
        page: int = 1,
        per_page: int = 1000,
        filter_by: dict = None,
        pay_core_enable="false",
    ):
        """
        Get the payout id by the shop name, please input union description(note) when you create payout
        @param page: page
        @param per_page: per_page
        @param shop name: shop_name
        @param ops_token: ops token
        @param filter_by: filter by status or settlementAgent, e.g {"status":"pending"}
        @return: payout id and payout status
        """
        r = StagingPaymentOps.get_payouts(ops_token, page, per_page, filter_by, pay_core_enable=pay_core_enable)
        nodes = r["data"]["payouts"]["nodes"]
        matched_node = list(
            filter(lambda node: node["merchantName"] == shop_name and node["status"] == "pending", nodes)
        )

        if len(matched_node) == 0:
            raise Exception(f"【Get payout id by shop_name failed】: {str(nodes)}")
        payout_id_list = [x["id"] for x in matched_node]
        logger.info(f"【Get payout id list by shop name {shop_name} passed】: {payout_id_list} ")
        return payout_id_list

    @staticmethod
    def get_payout_by_id(payout_id, ops_token: str, page: int = 1, per_page: int = 1000, filter_by: dict = None):
        """
        Get the payout id by id
        @param per_page:  per_page
        @param page:  page
        @param payout_id: payout_id
        @param ops_token: ops token
        @param filter_by: filter by status or settlementAgent, e.g {"status":"pending"}
        @return: payout id and payout status
        """
        r = StagingPaymentOps.get_payouts(ops_token, page, per_page, filter_by)
        nodes = r["data"]["payouts"]["nodes"]
        matched_node = list(filter(lambda node: node["id"] == payout_id, nodes))

        if len(matched_node) == 0:
            raise Exception(f"【Get payout by id failed】: {str(nodes)}")
        payout_id = matched_node[0]["id"]
        status = matched_node[0]["status"]
        logger.info(f"【Get payout by id {payout_id} passed】")
        return payout_id, status

    @staticmethod
    def clear_active_payouts_by_shop_name(
        shop_name: str,
        ops_token: str,
        page: int = 1,
        per_page: int = 1000,
        filter_by: dict = None,
        pay_core_enable="false",
    ):
        """
        Reject or failed all active (pending, approved, processed) payouts for shop
        @param per_page: per_page
        @param page: page
        @param shop_name: shop name
        @param ops_token: ops token
        @param filter_by: filter by status or settlementAgent, e.g {"status":"pending"}
        """
        r = StagingPaymentOps.get_payouts(ops_token, page, per_page, filter_by, pay_core_enable=pay_core_enable)
        nodes = r["data"]["payouts"]["nodes"]
        matched_node = list(filter(lambda node: node["merchantName"] == shop_name, nodes))
        if len(matched_node) != 0:
            for m in matched_node:
                payout_id = m["id"]
                status = m["status"]

                if status in ["rejected", "failed", "high_risk"]:
                    continue
                # Approved, Reject -> Processed, Reject -> Failed
                if status == "pending":
                    StagingPaymentOps.update_payout_status_by_id("rejected", payout_id, ops_token)
                if status == "approved":
                    StagingPaymentOps.update_payout_status_by_id("rejected", payout_id, ops_token)
                if status == "processed":
                    StagingPaymentOps.update_payout_status_by_id("failed", payout_id, ops_token)
        logger.info(f"【Clear all active payouts by shop name {shop_name}】")

    @classmethod
    def update_payout_status_by_id(
        cls,
        status: str,
        payout_id: str,
        ops_token: str,
        result: str = "account_closed",
    ):
        """
        Update payout status by payout id: Pending -> Approved, Reject -> Processed, Reject -> Failed
        @param status: status to update
        @param payout_id: payout id
        @param ops_token: ops token
        @param result: reject or failed result reason
        """
        headers = {"Authorization": f"Bearer {ops_token}"}
        update_payout = gql.balances.UPDATE_OPS_PAYOUT_STATUS
        ops_url = cls._payment_ops_gql

        variables = {
            "payoutId": payout_id,
            "status": status,
            "result": result,
        }
        # Pending -> Approved, Reject -> Processed, Reject -> Failed
        if status == "approved" or status == "processed" or status == "failed":
            variables["status"] = "approved"
            r = requests.post(url=ops_url, json={"query": update_payout, "variables": variables}, headers=headers)

            if status == "processed" or status == "failed":
                variables["status"] = "processed"
                r = requests.post(url=ops_url, json={"query": update_payout, "variables": variables}, headers=headers)

                if status == "failed":
                    variables["status"] = "failed"
                    r = requests.post(
                        url=ops_url, json={"query": update_payout, "variables": variables}, headers=headers
                    )
        else:
            variables["status"] = "rejected"
            r = requests.post(url=ops_url, json={"query": update_payout, "variables": variables}, headers=headers)

        if r.status_code == 200:
            t = r.json()["data"]["updatePayout"]
            if t["payout"] is None:
                raise Exception(
                    f"【Update ops payouts {status} failed, "
                    f"You have to follow Pending -> Approved, Reject -> Processed, Reject -> Failed】: "
                    f"{str(t['errors'])}"
                )
            logger.info(f"【Update ops payouts {status} passed】：{str(t)}")
            return t["payout"]
        else:
            raise Exception(f"【Update ops payouts {status} failed】： {r.text}")

    @classmethod
    def ops_update_team(
        cls,
        team_id: str,
        token: str,
        featureFlags: str = None,
        kyc_status: str = "approved",
        kyc_level: int = 3,
        live_account_enabled: int = 1,
        payout_fee_rate: str = "0.005",
        incorporationCountry: str = "AU",
        daily_payout_count: int = None,
        daily_limit_amount: str = "5000000000.0",
        annual_limit_amount: str = "5000000000.0",
        legal_entity_name: str = "Automation Tester",
        payout_settings: dict = None,
        variables_dict: dict = None,
    ):
        """Update the team to be active"""
        if featureFlags is None:
            featureFlags = (
                "invoice,exptl_subscription,monaco_rails_admin_notify_payment_captured_enabled,follow_up_seven_days,"
                "follow_up_no_payment,ncw_metamask_plugin,ncw_wallet_connect,defi_swap,"
                "cro_chain,onchain_enabled,debug,refund_qr_code,payment_qr_code,"
                "exptl_qr_code_payment,exptl_qr_code_refund,btc_payment,mass_payout,exptl_cronos,usd_bank_payout,"
                "exptl_onchain_rebound,exptl_qr_code_rebound,exptl_auto_snapshotting,"
                "monaco_rails_admin_notify_refund_perform_enabled,exptl_vvs_enabled,"
                "exptl_bnpl,specify_refund_email,shopify"
            )
        headers = {"Authorization": f"Bearer {token}"}

        if variables_dict is None:
            if incorporationCountry != "US":
                enable_onchain_payment = 1
            else:
                enable_onchain_payment = 0
            variables = {
                "teamId": f"{team_id}",
                "featureFlags": featureFlags,
                "invoicing": True,
                "kycLevel": kyc_level,
                "active": 1,
                "kycStatus": f"{kyc_status}",
                "liveAccountEnabled": live_account_enabled,
                "enableOnchainPayment": enable_onchain_payment,
                "businessDescription": "Test",
                "registrationNumber": "tete",
                "businessAddress": "tesdwqqsd",
                "incorporationCountry": f"{incorporationCountry}",
                "dailyLimitAmount": daily_limit_amount,
                "annualLimitAmount": annual_limit_amount,
                "taxId": "1123141",
                "defaultCurrencies": ["USD", "EUR", "GBP", "CAD", "AUD", "BTC", "ETH", "CRO"],
                "supportEmail": "auto@auto.com",
                "payoutFeeRate": f"{payout_fee_rate}",
                "legalEntityName": f"{legal_entity_name}",
            }
        else:
            variables = {
                "teamId": f"{team_id}",
                "featureFlags": featureFlags,
                "liveAccountEnabled": live_account_enabled,
                "defaultCurrencies": ["USD", "EUR", "GBP", "CAD", "AUD", "BTC", "ETH", "CRO"],
            }
            variables.update(variables_dict)

        if daily_payout_count is not None:
            variables["dailyPayoutCount"] = daily_payout_count
        if kyc_status == "missing_info":
            missing_info_reason = cls.get_missing_info_reasons(token)
            missing_info_reason = missing_info_reason[0]
            if "isTemplate" in missing_info_reason.keys():
                del missing_info_reason["isTemplate"]
            variables["missInfoReasons"] = [missing_info_reason]
        if payout_settings is not None:
            variables["configurations"] = payout_settings

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.team.OPS_UPDATE_TEAM, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Update ops team failed】：{str(t)}")

            onchain_enable = t["data"]["updateTeam"]["team"]["enableOnchainPayment"]
            if not onchain_enable:
                t = requests.post(
                    url=cls._payment_ops_gql,
                    json={"query": gql.team.OPS_UPDATE_TEAM, "variables": variables},
                    headers=headers,
                    timeout=30,
                ).json()
                if "errors" in t.keys():
                    raise Exception(f"【Update ops team failed】：{str(t)}")

            logger.info(f"【Update ops team passed】：{str(r)}")
            return t
        else:
            raise Exception(f"【Update ops team failed】： {r.text}")

    @classmethod
    def ops_sent_kyc_email(cls, team_id: str, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"teamId": f"{team_id}"}
        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.team.OPS_SENT_KYC_EMAIL, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Sent ops kyc email failed】：{str(t)}")
            logger.info(f"【Sent ops kyc email passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Sent ops kyc email failed】： {r.text}")

    @classmethod
    def get_team(cls, team_id: str, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"teamId": team_id}

        r = requests.post(
            url=cls._payment_ops_gql, json={"query": gql.team.OPS_GET_TEAM, "variables": variables}, headers=headers
        )

        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get ops team failed】：{str(t)}")
            logger.info("【Get ops team passed】")
            return t
        else:
            raise Exception(f"【Get ops team failed】： {r.text}")

    @classmethod
    def get_user_by_user_name(cls, user_name: str, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"filterBy": {"keyword": user_name}}

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.user.OPS_GET_USERS_BY_KEYWORDS, "variables": variables},
            headers=headers,
        )

        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get user by keyword failed】： {str(t)}")
            logger.info(f"【Get user by keyword passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get user by keyword failed】： {r.text}")

    @classmethod
    def disable_totp2fa(cls, user_name: str, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        rr = cls.get_user_by_user_name(user_name, token)
        current_node = rr["data"]["users"]["nodes"][0]
        is_enable_2fa = current_node["totpEnabled"]

        if is_enable_2fa:
            user_id = current_node["id"]
            variables = {"userId": user_id}
            r = requests.post(
                url=cls._payment_ops_gql,
                json={"query": gql.user.OPS_DISABLE_TOTP, "variables": variables},
                headers=headers,
            )

            if r.status_code == 200:
                t = r.json()
                if "errors" in t.keys():
                    raise Exception(f"【Totp 2fa disable failed】： {str(t)}")
                logger.info(f"【Totp 2fa disable passed】：{str(t)}")
                return t
            else:
                raise Exception(f"【Totp 2fa disable failed】： {r.text}")
        else:
            logger.info("【Totp 2fa already disabled】")

    @classmethod
    def risk_on_chain_address_mag(cls, address: str, token: str, action: str = "add"):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"address": address}
        if action == "add":
            query = gql.user.OPS_ADD_RISK_ADDRESS
        else:
            query = gql.user.OPS_REMOVE_RISK_ADDRESS

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": query, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【{action.title()} risk address failed】： {str(t)}")
            logger.info(f"【{action.title()} risk address passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【{action.title()} risk address failed】： {r.text}")

    @classmethod
    def get_onchain_inbound(
        cls,
        token,
        payment_id: str = None,
        first: int = 3,
        last: int = None,
        type_ops: str = "onchain_inbound",
        pay_core_enable: str = "false",
    ):
        """get onchain_inbound or refund history by payment_id"""
        headers = {"Authorization": f"Bearer {token}"}
        if payment_id is not None:
            filter_by = {"keyword": payment_id}
        else:
            filter_by = {}

        filter_by["payCore"] = pay_core_enable
        if last is not None:
            variables = {"first": last, "filterBy": filter_by}
        else:
            variables = {"first": first, "filterBy": filter_by}

        if type_ops == "onchain_inbound":
            query = gql.payment.GET_OPS_ONCHAIN_INBOUND
        else:
            query = gql.payment.GET_OPS_REFUND_HISTORY

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": query, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get {type_ops} failed】： {str(t)}")
            logger.info(f"【Get {type_ops} passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get {type_ops} failed】： {r.text}")

    @classmethod
    def ops_get_auto_payout(cls, token, payout_schedule, account_id: str = None):
        """
        get auto payout in ops
        """
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"scheduleType": f"{payout_schedule}"}
        if account_id is not None:
            variables["accountId"] = account_id

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.balances.GET_OPS_AUTO_PAYOUT, "variables": variables},
            headers=headers,
        )
        try:
            if r.status_code == 200:
                t = r.json()
                if "errors" in t.keys():
                    variables = {"scheduleType": f"{payout_schedule}"}
                    r = requests.post(
                        url=cls._payment_ops_gql,
                        json={"query": gql.balances.GET_OPS_AUTO_PAYOUT, "variables": variables},
                        headers=headers,
                    )
                    t = r.json()
                logger.info(f"【Trigger auto payout for {payout_schedule} passed】：{str(t)}")
                return t
            else:
                raise Exception(f"【Trigger auto payout for {payout_schedule} failed】： {r.text}")
        except Exception as e:
            logger.warning(f"【Trigger auto payout for {payout_schedule} failed】: Ready to wait 60s manually: {str(e)}")

    @classmethod
    def ops_get_team_id(cls, token, merchant_name):
        """
        get team id by merchant name
        """
        headers = {"Authorization": f"Bearer {token}"}
        filterBy = {"keyword": merchant_name}
        variables = {"first": 10, "filterBy": filterBy}
        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.account.GET_OPS_TEAM_ID, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get team id by {merchant_name} failed】： {str(t)}")
            logger.info(f"【Get team id by {merchant_name} passed】：{str(t)}")
            return t["data"]["teams"]["nodes"][0]["id"]
        else:
            raise Exception(f"【Get team id by {merchant_name} failed】： {r.text}")

    @classmethod
    def ops_get_term_info(cls, token, team_id):
        """
        get term information by team id
        """
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"teamId": team_id}
        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.team.OPS_GET_TEAM, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get term info by {team_id} failed】： {str(t)}")
            term_name = t["data"]["team"]["termTrack"][0]["legalEntity"]
            term_version = t["data"]["team"]["termTrack"][0]["termVersion"]
            kyc_status = t["data"]["team"]["kycStatus"]
            logger.info(f"【Get term info by {team_id} passed】：{str(term_name), str(term_version), str(kyc_status)}")
            return str(term_name), str(term_version), str(kyc_status)
        else:
            raise Exception(f"【Get term info by {team_id} failed】： {r.text}")

    @classmethod
    def get_onchain_outbound(
        cls,
        token: str,
        payment_id: str = None,
        wallet_address: str = None,
        inbound_fund_id: str = None,
        pay_core_enable: str = "false",
    ):
        headers = {"Authorization": f"Bearer {token}"}
        if payment_id is not None:
            filter_by = {"keyword": payment_id}
        elif wallet_address is not None:
            filter_by = {"keyword": wallet_address}
        elif inbound_fund_id is not None:
            filter_by = {"keyword": inbound_fund_id}
        else:
            filter_by = {}

        filter_by["payCore"] = str(pay_core_enable).lower()
        variables = {"filterBy": filter_by}
        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.payment.GET_OPS_ONCHAIN_OUTBOUND, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"[Get onchain inbound by {filter_by} failed】： {str(t)}")
            outbound_nodes_details = t["data"]["outboundFunds"]["nodes"]
            logger.info(f"【Get onchain inbound by {filter_by} passed】：{outbound_nodes_details}")
            return outbound_nodes_details
        else:
            raise Exception(f"[Get onchain inbound by {filter_by} failed】： {r.text}")

    @classmethod
    def process_rebound(
        cls,
        token: str,
        payment_id: str,
        action_type: str = "approve",
        pay_core_enable: str = "false",
    ):
        outbound_list = cls.get_onchain_outbound(token, payment_id=payment_id, pay_core_enable=pay_core_enable)
        if len(outbound_list) > 0:

            outbound_nodes_details = outbound_list[0]
            out_bound_Id = outbound_nodes_details["id"]

            headers = {"Authorization": f"Bearer {token}"}
            variables = {"outboundFundRequestId": out_bound_Id, "actionType": action_type}

            r = requests.post(
                url=cls._payment_ops_gql,
                json={"query": gql.payment.PROCESS_REBOUND, "variables": variables},
                headers=headers,
            )

            if r.status_code == 200:
                t = r.json()
                if "errors" in t.keys():
                    raise Exception(f"【Process rebound by {payment_id} failed】： {str(t)}")
                outboundFund = t["data"]["processRebound"]["outboundFund"]
                logger.info(f"【Process rebound by {payment_id} passed】：{outboundFund}")
                return outboundFund
            else:
                raise Exception(f"【Process rebound by {payment_id} failed】： {r.text}")
        else:
            raise Exception(f"【Process rebound {payment_id} failed】: get no result from rebound list")

    @classmethod
    def get_missing_info_reasons(cls, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.team.OPS_GET_MISSING_INFO_REASONS},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get missing info reasons failed】： {r.text}")
            nodes = t["data"]["missInfoReasons"]["nodes"]
            logger.info(f"【Get missing info reasons passed】：{nodes}")
            return nodes
        else:
            raise Exception(f"【Get missing info reasons failed】： {r.text}")

    @classmethod
    def get_merchant_transaction_fee_rate(cls, team_id: str, token: str):
        """
        get merchant transaction fee rate by team id
        """
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"teamId": team_id}
        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.team.OPS_GET_TEAM, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get term info by {team_id} failed】： {str(t)}")
            paylater_fee_rate = t["data"]["team"]["paylaterFeeRate"]
            logger.info(f"【Get merchant transaction fee rate by {team_id} passed】：{str(paylater_fee_rate)}")
            return str(paylater_fee_rate)
        else:
            raise Exception(f"【Get merchant transaction fee rate by {team_id} failed】： {r.text}")

    @classmethod
    def get_merchants_by_name(cls, token: str, merchant_name: str):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"filterBy": {"keyword": f"{merchant_name}"}}

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.team.GET_MERCHANTS, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get merchant info by {merchant_name} failed】： {str(t)}")
            logger.info(f"【Get merchant info by {merchant_name} passed】： {str(t)}")
            return t
        else:
            raise Exception(f"【Get merchant info by {merchant_name} failed】： {str(r.text)}")

    @classmethod
    def get_sub_merchant(cls, token: str, sub_merchant_id: str = None):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"page": 1, "perPage": 10}
        if sub_merchant_id is not None:
            variables["filterBy"] = {"keyword": sub_merchant_id}

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.team.OPS_GET_SUBMERCHANT, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get sub-merchant info by {sub_merchant_id} failed】： {str(t)}")
            logger.info(f"【Get sub-merchant info by {sub_merchant_id} passed】：{t}")
            return t
        else:
            raise Exception(f"【Get sub-merchant info by {sub_merchant_id} failed】： {str(r.text)}")

    @classmethod
    def enable_sub_merchant_payment(cls, token: str, sub_merchant_id: str, live_account_enabled: int = 1):
        headers = {"Authorization": f"Bearer {token}"}
        sub_merchant_info = cls.get_sub_merchant(token, sub_merchant_id)
        sub_merchant_ops_id = sub_merchant_info["data"]["subMerchants"]["nodes"][0]["id"]
        variables = {"subMerchantId": sub_merchant_ops_id, "liveAccountEnabled": live_account_enabled}

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.team.OPS_UPDATE_SUBMERCHANT, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Enable sub-merchant payment by {sub_merchant_id} failed】： {str(t)}")
            logger.info(f"【Enable sub-merchant payment {sub_merchant_id} passed】：{t}")
            return t
        else:
            raise Exception(f"【Enable sub-merchant payment {sub_merchant_id} failed】： {str(r.text)}")

    @classmethod
    def get_refund_id_before_today(
        cls,
        token,
        shop_name: str,
        type_ops: str = "refund_history",
        pay_core_enable: str = "false",
    ):
        """get onchain_inbound or refund history by merchant name"""
        headers = {"Authorization": f"Bearer {token}"}
        filter_by = {"keyword": shop_name, "status": "pending"}
        filter_by["payCore"] = pay_core_enable
        variables = {"page": 1, "perPage": 10, "filterBy": filter_by}

        query = gql.payment.GET_OPS_REFUND_HISTORY

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": query, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get {type_ops} failed】： {str(t)}")
            nodes = t["data"]["refunds"]["nodes"]

            from datetime import date
            from datetime import datetime

            today = date.today()
            midnight = datetime.combine(today, datetime.min.time())
            timestamp = datetime.timestamp(midnight)

            matched_node = list(filter(lambda node: node["createdAt"] < timestamp, nodes))
            matched_refund_id = matched_node[0]["id"]
            logger.info(f"【Get {type_ops} passed】：{str(matched_node)}")
            return matched_refund_id
        else:
            raise Exception(f"【Get {type_ops} failed】： {r.text}")

    @classmethod
    def get_country_name_by_country_code(cls, team_id: str, token: str, country_code: str):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"teamId": team_id}

        r = requests.post(
            url=cls._payment_ops_gql, json={"query": gql.team.OPS_GET_TEAM, "variables": variables}, headers=headers
        )

        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get ops team failed】：{str(t)}")
            logger.info("【Get ops team passed】")
            nodes = t["data"]["countries"]
            filtered_nodes = list(filter(lambda x: x["code"] == country_code, nodes))
            country_name = filtered_nodes[0]["name"]
            return country_name
        else:
            raise Exception(f"【Get ops team failed】： {r.text}")

    @classmethod
    def get_country_code_by_country_name(cls, team_id: str, token: str, country_name: str):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"teamId": team_id}

        r = requests.post(
            url=cls._payment_ops_gql, json={"query": gql.team.OPS_GET_TEAM, "variables": variables}, headers=headers
        )

        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get ops team country code failed】：{str(t)}")
            logger.info("【Get ops team country code passed】")
            nodes = t["data"]["countries"]
            filtered_nodes = list(filter(lambda x: x["name"] == country_name, nodes))
            country_code = filtered_nodes[0]["code"]
            return country_code
        else:
            raise Exception(f"【Get ops team country code failed】： {r.text}")

    @classmethod
    def ops_get_payout_account(cls, token: str, team_id: str, payout_account_currency: str):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"filterBy": {"keyword": team_id}, "page": 1, "perPage": 10}

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.team.OPS_GET_PAYOUT_ACCOUNTS, "variables": variables},
            headers=headers,
        )

        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get ops payout account failed】：{str(t)}")
            logger.info("【Get ops payout account passed】")
            node = t["data"]["payoutAccounts"]["nodes"]
            filtered_node = list(filter(lambda x: x["currency"] == payout_account_currency, node))
            return filtered_node[0]
        else:
            raise Exception(f"【Get ops payout account failed】： {r.text}")

    @classmethod
    def ops_update_payout_account(cls, token: str, payout_account_id: str, status: str):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"payoutAccountId": payout_account_id, "status": status}

        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.account.OPS_UPDATE_PAYOUT_ACCOUNT, "variables": variables},
            headers=headers,
        )

        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Update ops payout account failed】：{str(t)}")
            logger.info("【Update ops payout account passed】")
        else:
            raise Exception(f"【Update ops payout account failed】： {r.text}")

    @classmethod
    def ops_get_crypto_purchase_by_id(cls, token: str, crypto_purchase_id: str):
        headers = {"Authorization": f"Bearer {token}"}
        filter_by = {"keyword": crypto_purchase_id}
        variables = {"perPage": 10, "page": 1, "filterBy": filter_by}
        r = requests.post(
            url=cls._payment_ops_gql,
            json={"query": gql.crypto_purchase.GET_CRYPTO_PURCHASE, "variables": variables},
            headers=headers,
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Get ops crypto purchase by id {crypto_purchase_id} failed】：{str(t)}")
            logger.info("【Get ops crypto purchase by id {crypto_purchase_id} passed】")
            return t["data"]["cryptoPurchases"]["nodes"][0]
        else:
            raise Exception(f"【Get ops crypto purchase by id {crypto_purchase_id} failed】： {r.text}")

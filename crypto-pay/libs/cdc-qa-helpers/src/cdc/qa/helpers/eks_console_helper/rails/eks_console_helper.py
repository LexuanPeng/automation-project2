import logging
import re
from time import sleep
from typing import Union, Optional, Tuple, List
from cdc.qa.helpers.ssh_console_helper.rails.data import (
    GlobalFlag,
    DobVerificationSettings,
    XfersConnectState,
    InternalTestersList,
)
from cdc.qa.helpers.eks_console_helper.eks_console import EKSConsole
from cdc.qa.helpers.eks_console_helper.exceptions import EKSRailsConsoleException
import datetime

logger = logging.getLogger(__name__)


class RailsConsoleHelper(EKSConsole):
    def get_magic_token(self, email: str, action: str = "default") -> str:
        """Get magic token for user with given email.

        Args:
            email (str): Email of target user.
            action (str): Get Magic token for different type: update phone
        Raises:
            Exception: Magic token not found.

        Returns:
            str: Magic token.
        """

        if action == "update_phone":
            magic_token_type = "MagicTokens::Service.new.set_magic_token(user, column: :unconfirmed_phone)"
        elif action == "update_email":
            magic_token_type = "MagicTokens::Service.new.set_magic_token(user, column: :new_email)"
        else:
            magic_token_type = "MagicTokens::Service.new.set_magic_token(user)"

        cmd = f"""
        user = User.find_by(email: '{email}')
        {magic_token_type}
        """
        pattern = re.compile(r'(?<=").*(?=")')
        match, result = self.exec_command(cmd, pattern)

        if match:
            logger.debug(f"Magic token: {result}")
            return result
        else:
            raise EKSRailsConsoleException(f"Magic token not found. \nResult from command: \n{result}")

    def get_login_magic_link(self, email: str, env_prefix: str = "st") -> str:
        # env_prefix: st or dev
        return f"https://{env_prefix}.mona.co/magic/{self.get_magic_token(email)}?magic_action=login"

    def get_rails_access_token(self, email: str) -> str:
        cmd = f"""
            user = User.find_by(email: '{email}')
            application = Doorkeeper::Application.find_by(name: 'monaco')
            access_token = Doorkeeper::AccessToken.create(application: application, resource_owner_id: user.id)
            access_token.plaintext_token
        """
        pattern = re.compile(r'(?<=")\w*(?=")')
        match, result = self.exec_command(cmd, pattern)

        if match:
            return result
        else:
            raise EKSRailsConsoleException(f"Rails Access Token not found. \nResult from command: \n{result}")

    def get_global_flag_value(self, global_flag: GlobalFlag) -> str:
        """Get global flag value.
        Args:
            global_flag: Global flag value to get. See GlobalFlag.
        """
        cmd = f"Setting.{global_flag.value}"
        pattern = re.compile(r"true|false")
        match, result = self.exec_command(cmd=cmd, pattern=pattern, timeout=15)

        if match:
            return result
        else:
            raise EKSRailsConsoleException(f"Global flag not found. \nResult from command: \n{result}")

    def set_global_flag_value(self, global_flag: GlobalFlag, value: str):
        """Set global flag with given value.
        Args:
            global_flag: Global flag to be set. See GlobalFlag.
            value: value set for the global flag
        Raises:
            Exception: Value not set.
        """

        cmd = f"Setting.{global_flag.value} = {value}"
        pattern = re.compile(r"true|false")
        match, result = self.exec_command(cmd=cmd, pattern=pattern, timeout=15)
        if match:
            logger.debug(f"Global flag {global_flag} has set to {value}")
        else:
            raise EKSRailsConsoleException(
                f"Global flag {global_flag} has failed to set to {value}.\nConsole output:\n{result}"
            )

    def set_app_locks_dob_verification(self, dob_verification_settings: DobVerificationSettings, value: str):
        """Set app_locks's dob_verification's setting."""

        cmd = f"Setting.app_locks[:dob_verification][:{dob_verification_settings.name}] = {value}"
        if dob_verification_settings in [
            DobVerificationSettings.lock_duration_in_minutes,
            DobVerificationSettings.maximum_number_of_verification_attempts,
        ]:
            pattern = re.compile(r"\d+")
        else:
            raise NotImplementedError(f"{dob_verification_settings}'s pattern is not implemented")
        match, result = self.exec_command(cmd=cmd, pattern=pattern, timeout=15)
        if match:
            logger.debug(f"App locks for Dob Verification's {dob_verification_settings} has set to {value}")
        else:
            raise EKSRailsConsoleException(
                f"App locks for Dob Verification's {dob_verification_settings} has failed to set to {value}."
                f"\nConsole output:\n{result}"
            )

    def add_crypto(self, user_email: str, crypto_currency: str, amount: Union[int, str]):
        cmd = f"""
        user = User.find_by(email: '{user_email}')
        user.wallets.find_by(currency: '{crypto_currency}').add_fund!({amount})
        """
        pattern = re.compile(r"#<Wallet id: (.*)")
        match, result = self.exec_command(cmd, pattern, timeout=10)
        if match:
            logger.info(f"{amount} of crypto '{crypto_currency}' has added to user <email: {user_email}>")
        else:
            raise EKSRailsConsoleException(f"Has failed to add crypto '{crypto_currency}'.\nConsole output:\n{result}")

    def create_crypto_wallet(self, user_email: str, crypto_currency: str):
        """Create crypto wallet. In rails backend, for new account, create wallet is an async background job.
        Args:
            user_email: user email
            crypto_currency: crypto currency upper() str code, can be either upper/lower case
        Returns:
            None
        """

        crypto_currency = crypto_currency.upper()
        cmd = f"""
            user = User.find_by(email: '{user_email}')
            user.wallets.find_by(currency: '{crypto_currency}')
        """
        pattern = re.compile(r"#<Wallet id")
        match, result = self.exec_command(cmd, pattern, 15)

        if match:
            logger.debug(f"Crypto wallet '{crypto_currency}' on User '{user_email}' is already created.")
        else:
            cmd = f"""
            begin
                Txns::CreateWalletCommand.new(user: user, currency: '{crypto_currency.upper()}').run!
            rescue ActiveRecord::RecordNotUnique
                nil
            end
            """
            pattern = re.compile(r"(.*)|(\nnil)")
            match, result = self.exec_command(cmd, pattern, timeout=15)

            if match:
                logger.debug(f"Crypto wallet '{crypto_currency}' on User '{user_email}' is already created.")
            else:
                raise EKSRailsConsoleException(
                    f"Crypto wallet '{crypto_currency}' on User '{user_email}' is already created.\n"
                    "Console output:\n"
                    f"{result}"
                )

    def create_wallet_address(self, user_email: str, crypto_currency: str):
        """
        Create crypto wallet address. In rails backend, for new account, create wallet address is an async background
        job. As it depends on crypto-service, it will always be async, so we will always need to wait til address
        created.
        Args:
            user_email: user email
            crypto_currency: crypto currency upper() str code, can be either upper/lower case
        Returns:
            None
        """

        crypto_currency = crypto_currency.upper()
        cmd = f"""
            user = User.find_by(email: '{user_email}')
            user.assign_funding_source('{crypto_currency}')
        """
        pattern = re.compile(r"\[#<CryptoCurrencyNetworkConfig:(.*)]")
        match, result = self.exec_command(cmd, pattern, timeout=30)

        if match:
            logger.debug("Wallet address job queue created.")
        else:
            raise EKSRailsConsoleException(f"Failed to create wallet address.\n" "Console output:\n" f"{result}")

        cmd = f"""
            user = User.find_by(email: '{user_email}')
            WalletSerializer.new(user.wallets.by_currency('{crypto_currency.upper()}')).address
        """
        pattern = re.compile(r'(?<=").*(?=")')
        for _ in range(0, 5):
            is_address_existed, result = self.exec_command(cmd, pattern, timeout=15)
            if is_address_existed:
                return True
            sleep(3)
        return False

    def update_phone_number(self, email, phone_number):
        """
        Args:
            email(str): User email
            phone_number(str): phone number to update.
        """
        pattern = re.compile(r"(Object doesn't support #inspect)\S*")
        cmd = f"""
            user = User.find_by(email: '{email}')
            user.reload
            user.instance_variable_set('@skip_phone_confirmation', true)
            user.phone = '{phone_number}'
            user.unconfirmed_phone = nil
            user.phone_confirmed_at = Time.now
            user.save(validate: false)
            user.reload
            """
        match, result = self.exec_command(cmd, pattern, timeout=20)
        if match:
            logger.info(f"Phone number is set to {phone_number}")
        else:
            raise EKSRailsConsoleException(
                f"Phone number has failed to set to {phone_number}.\nConsole output:\n{result}"
            )

    def update_document_issuing_country(self, email: str, country_code: str):
        """Updates document issuing country for the user by email
        Args:
            email: user email
            country_code: alpha_3 of the country
        Returns:
            None
        """
        pattern = re.compile(r"true")
        match, result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            user.identity.update(document_issuing_country: '{country_code}')
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=10,
        )
        if match:
            logger.debug(f"Document issuing country is set to {country_code}")
        else:
            raise EKSRailsConsoleException(
                f"Document issuing country has failed to set to {country_code}.\nConsole output:\n{result}"
            )

    def add_user_to_internal_tester(self, email: str, internal_tester_list: InternalTestersList):
        """Add user into internal tester list.

        Args:
            email: user email address
            internal_tester_list: internal testers list array in rails console
        Returns:
            None
        """
        cmd = f"""
            Setting.{internal_tester_list.value} |= ['{email}']; nil
            Setting.{internal_tester_list.value}.include? '{email}'
        """
        pattern = re.compile(r"true")
        match, result = self.exec_command(cmd=cmd, pattern=pattern, timeout=15)
        if match:
            logger.info(f"User is added into '{internal_tester_list.value}' internal tester list")
        else:
            raise EKSRailsConsoleException(
                "Cannot find user email in internal tester list, failed to add user into internal tester list"
                f"Internal tester list checking returned: '{result}'"
            )

    def get_user_sms_otp(self, email: str) -> str:
        """Get current SMS OTP for specific user by user email.
        Args:
            email: user email
        Returns:
            User SMS OTP in str
        """
        pattern = re.compile(r'(?<=")\d*(?=")')
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                user.otp_code
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=10,
        )
        if match:
            return result
        else:
            raise EKSRailsConsoleException(f"Get user sms otp failed: {result}")

    def get_user_id(self, email: str) -> int:
        """Get user id with given email.

        Args:
            email (str): Email of target user.

        Raises:
            Exception: Unable to get user id with given email.

        Returns:
            str: user id.
        """
        pattern = re.compile(r"\n\d+")
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                user.id
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=10,
        )
        if match:
            result = re.sub(r"\n(?!<Text>)", "", result)
            return int(result)
        else:
            raise EKSRailsConsoleException(f"Get user id failed: {result}")

    def update_xfers_connect_state(self, email: str, state: XfersConnectState):
        """Update Xfers connect status.

        Args: email: User email address state: States available: 'pending_xfers_verify', 'pending_review',
        'activated', 'disconnected', 'rejected'. See Enum XfersConnectState().

        Returns:
            None
        """

        cmd = f"""
            user = User.find_by(email: '{email}')
            x = XfersAccount.find_by(user: user)
            x.state = '{state.value}'
            x.save
        """
        pattern = re.compile(r"true")
        match, result = self.exec_command(cmd=cmd, pattern=pattern, timeout=30)

        if match:
            logger.debug(f"Xfers connect state is set to {state.value}")
        else:
            raise EKSRailsConsoleException(
                f"Xfers connect state is failed to set to {state.value}.\nConsole output:\n{result}"
            )

    def approve_xfers_withdrawal_transaction(self, email: str):
        cmd = f"""
            user = User.find_by(email: '{email}')
            withdrawal_view = XfersWithdrawalView.where({{user: user, status: 'risk_pending'}})
            Xfers::WithdrawalService.risk_approve(user, withdrawal_view[0].id, 'test', 'risk_team@crypto.com')
            """
        pattern = re.compile(r"^(?![\s\S])")
        match, result = self.exec_command(cmd=cmd, pattern=pattern, timeout=30)
        if match:
            logger.debug(f"Xfers withdrawal of user email approved: {email}")
        else:
            raise EKSRailsConsoleException(f"Xfers withdrawal failed to approve.\nConsole output:\n{result}")

    def get_email_url_from_rails(self, user_id: Union[str, int], message_slug: str) -> str:
        """
        Args:
            user_id(int): user_id
            message_slug(str): message_slug for locating the message type

        Returns:
            str: URL
        Raises:
            Exception: Failed to get url with given user_id and message slug
        """
        cmd = f"""
            user = User.find({user_id})
            MessageJob.where(user_id: user.id).where('message_slug ilike ?', '{message_slug}%').last.message_payload['url']
            """  # noqa: E501
        pattern = re.compile(r"\"(https.+)\"")
        match, result = self.exec_command(cmd=cmd, pattern=pattern, timeout=15)
        logger.info(result)
        if match:
            return result
        else:
            raise EKSRailsConsoleException(f"Unable to get url. \nResult from command: \n{result}")

    def turn_on_button_on_supermenu(self, item: str):
        """
        Args:
            item(str): Supermenu button item name, i.e. 'recurring buy'
        Raises:
            ValueError: Given item name is invalid
        """
        if item.lower() in ["recurring buy"]:
            cmd = """
                button = SuperMenu::MenuItemGroupItem.find_by(menu_item: SuperMenu::MenuItem.find_by(key: 'recurring_buy'))
                button.hidden = false
                button.save!
                """  # noqa: E501
            pattern = re.compile(r"true")
            match, result = self.exec_command(cmd=cmd, pattern=pattern, timeout=15)

            if match:
                logger.debug(result)
            else:
                raise EKSRailsConsoleException(
                    f"Supermenu button '{item}' failed to turn on.\nConsole output:\n{result}"
                )
            logger.debug(result)
        else:
            raise ValueError(f"Item '{item}' is either not yet implemented/item name is incorrect.")

    def set_user_phone_and_phone_country(self, email: str, phone_number: str, country_alpha_3: str):
        """Set user phone number and phone country by user email
        Args:
            email: user email
            phone_number: phone number to be set
            country_alpha_3: country alpha 3 code
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                user.instance_variable_set('@skip_phone_confirmation', true)
                user.phone = '{phone_number}'
                user.unconfirmed_phone = nil
                user.phone_confirmed_at = Time.now
                user.phone_country = "{country_alpha_3.upper()}"
                user.save(validate: false)
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=30,
        )

        if match:
            logger.info(f"Set user.phone = '{phone_number}, user.phone_country = '{country_alpha_3}'")
        else:
            raise EKSRailsConsoleException(
                f"""
                "Failed to set user.phone = '{phone_number}, user.phone_country = '{country_alpha_3}'"
                "Result from command:
                {result}
                """
            )

    def set_user_entity(self, email: str, entity_id: str, country_code: str):
        """Set user entity by user email
        Args:
            email: user email
            entity_id: country name
            country_code: country code in alpha 3
        """

        # self.delete_user_entity(email, entity_id)
        pattern = re.compile(r"(^true$)|(\ntrue)")
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                UserEntityMigration.create!(user_uuid: user.uuid, entity_id: '{entity_id}', status: 'done')
                user.instance_variable_set('@skip_phone_confirmation', true)
                user.update_entity_id!('{entity_id}')
                user.phone_country = "{country_code}"
                user.save(validate: false)
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=15,
        )
        if match:
            logger.info(f"Set user entity for '{email}' to '{entity_id}'")
        else:
            raise EKSRailsConsoleException(
                f"Failed to set user entity to '{entity_id}' \n Result from command: \n{result}"
            )

    def delete_user_entity(self, email: str, entity_id: str):
        """Delete user current entity by user email
        Args:
            email: user email
            entity_id: country name
        """
        pattern = re.compile(r"#<UserEntityMigration id: (.*)")
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                UserEntityMigration.find_by(user_uuid: user.uuid).delete
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=10,
        )

        if match:
            logger.info(f"Deleted user entity for '{email}'")
        else:
            logger.error(f"Failed to delete user entity to '{entity_id}' \n Result from command: \n{result}")

        return match

    def refresh_user_fiat_balance(self, email: str):
        """Refresh user fiat wallet balance on monaco-rails
        Args:
            email: user email
        """
        pattern = re.compile(r"\nnil")
        match, result = self.exec_command(
            f"""
            user = User.find_by!(email: '{email}')
            CryptoFiats::BalanceService.new.refresh(user)
            nil
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=15,
        )

        if match:
            logger.debug("Refreshed fiat balance")
        else:
            raise EKSRailsConsoleException(f"Failed to refresh user {email} fiat balance")

    def approve_malta_entity_address(self, email: str):
        """Approve Malta entity address
        Args:
            email: user email
        """
        pattern = re.compile(r"^true$")
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                MaltaEntityAddresses::Service.new.approve_address(
                        user,
                        MaltaEntityAddress.find_by!(user_uuid: user.uuid),
                        reason: 'reason',
                        done_by: 'xxx@crypto.com'
                      )
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=10,
        )

        if match:
            logger.debug("Malta address had been approved.")
        else:
            logger.error(f"Failed to approve Malta address \n Result from command: \n{result}")

    def get_passcode_reset_magic_token(self, email: str):
        pattern = re.compile(r'(?<=").*?(?=")')
        match, result = self.exec_command(
            f"""
            def reset_passcode_token(user)
              PasscodeResetRequest.transaction do
                request =
                  PasscodeResetRequest.lock.valid_for(user).find_or_initialize_by({'{}'})
                request.set_token! if request.new_record?
                request.token
              end
            end
            user = User.find_by(email: '{email}')
            reset_passcode_token user
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=10,
        )
        if match:
            return result
        else:
            raise EKSRailsConsoleException(f"Get reset passcode magic token failed: \n{result}")

    def enable_quotation_count_down_period(self, timeout: int = 90):
        pattern = re.compile(r"\n\d+")
        match, result = self.exec_command(
            f"""
            Setting.quotation_override_countdown_enabled = true
            Setting.quotation_qa_custom_countdown_period = {timeout}
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=10,
        )

        if match:
            logger.debug(f"Enable quotation count down period time to {timeout}")
        else:
            raise EKSRailsConsoleException(f"Enable quotation count down period time to {timeout} failed: \n{result}")

    def add_mco_card(
        self,
        user_email: str,
        card_reference_num: Optional[Union[str, int]] = None,
        card_program_id: Optional[str] = None,
        base_currency: Optional[str] = None,
        action_type: str = "activate",
    ):
        """Adds MCO card to Crypto App user account by rails console, equal to submitting the form from MCO admin
        panel: https://st.mona.co/admin/cards/new
        Args:
            user_email: user email address
            card_reference_num: number which is unique and assign to the MCO visa card, must be provided if mco_card is
            card_program_id: see https://monacohq.atlassian.net/wiki/spaces/PQA/pages/365395994/Activation, must be
            provided if mco_card is None
            base_currency: fiat currency for the MCO visa card, must be provided if mco_card is None
            action_type: activate, shipped, issued only
        Returns:
            requests response
        """
        card_customer_id = user_email.split("-")[-1].split("@")[0]
        is_physical_card = action_type in ["activate", "shipped"]

        pattern = re.compile(r"{:user_uuid=>.*")
        self.exec_command(
            f"""
            user = User.find_by(email: '{user_email}')
            data = {{
                    user_uuid: user.uuid,
                    card_customer_id:  '{card_customer_id}',
                    card_reference_num: '{card_reference_num}',
                    base_currency: '{base_currency}',
                    masked_number: '434176******1762',
                    card_program_id: '{card_program_id}'
                }}
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=10,
        )
        pattern = re.compile(r"#<Card id: .*")
        if is_physical_card:
            match, result = self.exec_command(
                f"""
                Card.new do |card|
                    card.card_customer_id = data[:card_customer_id]
                    card.card_reference_num = data[:card_reference_num]
                    card.base_currency = data[:base_currency]
                    card.masked_number = data[:masked_number]
                    card.card_program_id = data[:card_program_id]
                    card.user = user
                    card.freezed = false
                    card.shipping_state = "shipped"
                    card.shipping_courier = "DHL"
                    card.shipping_tracking_number = 5354553
                    card.shipped_on = "2019-05-17"
                    {'' if base_currency == 'USD' else 'card.virtual_card_issued_at = Time.zone.now'}
                    {'' if base_currency == 'USD' else 'card.physical_card_issued_at = Time.zone.now'}
                    {'card.activated_at = Time.zone.now' if action_type == 'activate' else  ''}
                    card.i2c_instance_id = CardProgram::Manager.i2c_instance_id(data[:card_program_id])
                    card.international_enabled_at = card.i2c_instance_id == "uk"? Time.zone.now : nil
                    card.save
                end
                """,
                pattern=pattern,
                timeout=10,
            )
        else:
            match, result = self.exec_command(
                """
                Card.new do |card|
                    card.card_customer_id = data[:card_customer_id]
                    card.card_reference_num = data[:card_reference_num]
                    card.base_currency = data[:base_currency]
                    card.masked_number = data[:masked_number]
                    card.card_program_id = data[:card_program_id]
                    card.user = user
                    card.freezed = false
                    card.shipping_state = "pending"
                    card.virtual_card_issued_at = Time.zone.now
                    card.i2c_instance_id = CardProgram::Manager.i2c_instance_id(data[:card_program_id])
                    card.international_enabled_at = card.i2c_instance_id == "uk"? Time.zone.now : nil
                    card.save
                end
                """,
                pattern=pattern,
                timeout=10,
            )

        card_info = {
            "user_email": user_email,
            "card_customer_id": card_customer_id,
            "card_program_id": card_program_id,
            "base_currency": base_currency,
        }

        if match:
            logger.debug(f"MCO Visa card had been added: {card_info}\n{result}")
        else:
            raise EKSRailsConsoleException(f"MCO Visa card is not added . \nResult from command: \n{result}")

    def update_physical_card_application_status(self, status: str, email: str):
        """Update physical card application status
        Args:
            status: pending_submit/submitted
            email: user email
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")
        match, result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            user.primary_card.update(physical_card_issued_at: Time.zone.now)
            user.primary_card.physical_card_application
            user.primary_card.physical_card_application.update(state: '{status}')
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=15,
        )
        if match:
            logger.debug(f"Physical Card issue status changed to {status}")
        else:
            raise EKSRailsConsoleException(f"Physical Card issued changed with error, result: \n{result}")

    def issued_physical_card(self, email: str):
        """Issued physical card
        Args:
            email: user email
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")
        match, result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            card = user.primary_card
            card.update(physical_card_issued_at: Time.zone.now)
            app = card.physical_card_application
            app.issue_started!
            app.issue_succeed!('QA Auto')
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=15,
        )

        if match:
            logger.debug("Physical Card issued")
        else:
            raise EKSRailsConsoleException(f"Physical Card issued with error, result: \n{result}")

    def update_mco_card_holder_name(self, email: str, first_name: str, last_name: str):
        """Updates mco card holder name for user by email
        Args:
            email: user email
            first_name: first name of card holder
            last_name: last name of card holder
        Returns:
            None
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")

        match, result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            user.identity.update!(document_data_cache: {{ document: {{ lastName: '{last_name}', firstName: '{first_name}' }} }})
            """,  # noqa: E501
            wrap_with_begin=True,
            pattern=pattern,
            timeout=15,
        )

        if match:
            logger.debug(f"Mco card holder name is set to: First name = {first_name}, Last name = {last_name}")
        else:
            raise EKSRailsConsoleException(
                f"Mco card holder name has failed to set to: First name = {first_name}, Last name = {last_name}.\n"
                f"Console output:\n{result}"
            )

    def update_unactivated_mco_card_info(self, email: str):
        """Update unactivated MCO card's info such as card_reference_num, masked_number, and shipping info
        Args:
            email: user email
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")
        match, result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            old_card = user.cards[1]
            new_card = user.cards[0]
            new_card.card_reference_num = old_card.card_reference_num
            new_card.masked_number = old_card.masked_number
            new_card.shipping_state = 'shipped'
            new_card.shipping_courier = 'DHL'
            new_card.shipping_tracking_number = 'tracking1234'
            new_card.shipped_on = '2022-10-07'
            new_card.save
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=15,
        )

        if match:
            logger.debug("Updated unactivated MCO Card's info.")
        else:
            raise EKSRailsConsoleException(f"Updated unactivated MCO Card's info with error, result: \n{result}")

    def add_kyc_address(self, email: str):
        """Add user kyc address.
        Args:
            email: user email address
        Returns:
            None
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")

        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                c = WirecardUkCardApplication.find_or_initialize_by(user_uuid: user.uuid)
                c.address = {{address_1: 'xxxx', city: 'xxx', country_code: 'GBR', postcode: 'xxx'}}
                c.save!
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=15,
        )

        if match:
            logger.info("User kyc address successfully added")
        else:
            raise EKSRailsConsoleException("Failed to set user kyc address")

    def set_user_tnc_required(self, email: str, tnc_required: bool):
        """Set user terms and conditions required.
        Args:
            email: user email address
            tnc_required: required tnc or not
        Returns:
            None
        """
        current_year = datetime.date.today().year
        year = str(current_year + 1) if tnc_required else str(current_year)
        pattern = re.compile(r"(^true$)|(\ntrue)")

        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                @card_application = user.wirecard_uk_card_application || user.build_wirecard_uk_card_application
                @card_application.terms_accepted_at = DateTime.new({year[:1]}_{year[1:]}, 1, 1, 0, 0, 0)
                @card_application.save
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=15,
        )
        if match:
            logger.info(f"User card application terms_accepted_at is set to {year}")
        else:
            raise EKSRailsConsoleException(f"Failed to set user card application terms_accepted_at to {year}")

    def add_user_to_crypto_withdrawal_inactive_validations_whitelist(self, email: str):
        """Add user into crypto withdrawal inactive validations whitelist.
        Args:
            email: user email address
        Returns:
            None
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")

        is_added = self.exec_command(
            f"""
                tmp = Setting.crypto_withdrawal_address__inactive_validations_whitelist
                tmp['{email}'] = 'Automation'
                Setting.crypto_withdrawal_address__inactive_validations_whitelist = tmp
                Setting.crypto_withdrawal_address__inactive_validations_whitelist.key?('{email}')
            """,
            wrap_with_begin=True,
            pattern=pattern,
            timeout=15,
        )
        if "true" in is_added:
            logger.info("User is added into crypto withdrawal inactive validation whitelist'")
        else:
            raise EKSRailsConsoleException(f"Internal tester list checking returned: '{is_added}'")

    def _get_ach_i2c_account_id(self, email: str) -> str:
        for i in range(40):
            logger.debug(f"Attempt to get ACH i2c account id #{str(i + 1)}")
            pattern = re.compile(r"\".*\"")
            match, result = self.exec_command(
                f"""
                    user = User.find_by(email: '{email}')
                    user.van_wallet.i2c_van_account_id
                """,
                wrap_with_begin=True,
                pattern=pattern,
                timeout=15,
            )

            if match:
                logger.debug(f"ACH i2c account id = {result}")
                return result
            else:
                raise EKSRailsConsoleException(f"ACH i2c account id not found. \nResult from command: \n{result}")

    def add_usd_via_ach(self, email: str, amount: Union[str, int]):
        """Add USD to fiat wallet via ACH.

        Args:
            email: user email address
            amount: amount of USD to be added

        Returns:
            None
        """

        i2c_account_id = self._get_ach_i2c_account_id(email)

        pattern = re.compile(r":create_us_ach_deposit")
        self.exec_command(
            """
            def create_us_ach_deposit(i2c_account_id, amount, is_debit: false)
                event_id = I2cCore::EventNotification.maximum(:event_id).next.to_s
                transaction_id = I2cCore::EventNotification.maximum(:transaction_id).next.to_s
                message_type = is_debit ? '0420' : '0200'
                event = {
                    'Header' => {
                        'Id' => 'i2c-foris',
                            'UserId' => 'push-notification',
                            'Password' => 'encrypted_password',
                            'MessageCreationDateTime' => '2017-12-3112:34:56'
                    },
                    'Transaction' => {
                        'NotificationEventId' => event_id,
                        'TransactionId' => transaction_id,
                        'MessageType' => message_type,
                        'Date' => '2017-12-31',
                        'Time' => '10:10:15',
                        'ARN' => '',
                        'CardAcceptor' => {
                            'AcquirerId' => '1',
                            'MerchantCode' => '1',
                            'MerchantNameAndLocation' => '1',
                            'MerchantCity' => '1',
                            'MerchantState' => '1',
                            'MerchantZipCode' => '1',
                            'MCC' => '1',
                            'DeviceId' => '1',
                            'DeviceType' => '1',
                            'LocalDateTime' => '2017-12-3112:34:56'
                        },
                        'TransactionType' => 'DD',
                        'Service' => '',
                        'TransactionAmount' => amount,
                        'TransactionCurrency' => 'USD',
                        'TransactionResponseCode' => '00',
                        'AuthorizationCode' => '123',
                        'OriginalTransId' => '123',
                        'TransferID' => '123',
                        'BankAccountNumber' => '123',
                        'TransactionDescription' => '123',
                        'ExternalTransReference' => '123',
                        'ExternalUserReference' => ''
                    },
                    'Card' => {
                        "CardProgramID": 'Foris_US_Fiat',
                        "CardReferenceID": i2c_account_id,
                        "PrimaryCardReferenceID": i2c_account_id,
                        "CustomerId": '364000000000013396',
                        "MemberId": '6bc2449650b0491c9f515f306',
                        "AvailableBalance": '100.00',
                        "LedgerBalance": '100.00',
                        "CardStatus": 'B',
                        "FirstName": 'BENNY A B',
                        "LastName": 'CHAN',
                        "CountryCode": 'USA',
                        "CellNo": '85292213197',
                        "Email": 'benny@gmail.com'
                    }
                }
                event_id = I2cCore::EventNotification.create_with_params!(event).id
                I2cCore::EventNotification.find(event_id).on_new_event_pushed
            end
        """,
            pattern=pattern,
            wrap_with_begin=False,
        )

        pattern = re.compile(r"Enqueued Van::I2c::ProcessEventNotificationJob")
        match, result = self.exec_command(
            f"create_us_ach_deposit('{i2c_account_id}', '{amount}')",
            wrap_with_begin=False,
            pattern=pattern,
            timeout=15,
        )
        if match:
            logger.debug(f"{amount} of USD has added to user <email: {email}>")
        else:
            raise EKSRailsConsoleException(f"Has failed to add USD.\nConsole output:\n{result}")

    def shipped_physical_card(self, email: str):
        """Shipped physical card
        Args:
            email: user email
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                card = user.primary_card
                card.update(shipping_state: 'shipped')
                card.update(shipping_courier: 'DHL')
                card.update(shipping_tracking_number: '5354553')
                card.update(shipped_on: Time.now)
            """,
            pattern=pattern,
            wrap_with_begin=False,
            timeout=15,
        )
        if match:
            logger.debug(f"user: {email} has set physical card status to shipped success!")
        else:
            raise EKSRailsConsoleException(
                "Failed to set physical card status to shipped.\n" f"Console output:\n{result}"
            )

    def activate_physical_card(self, email: str):
        """Activate physical card
        Args:
            email: user email
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                card = user.primary_card
                card.update(activated_at: Time.now)
            """,
            pattern=pattern,
            wrap_with_begin=False,
            timeout=15,
        )
        if match:
            logger.debug(f"user: {email} has activated physical card success!")
        else:
            raise EKSRailsConsoleException(f"Failed to activated physical card.\n Console output:\n{result}")

    def update_payment_network(self, network_type: str, currency: str, user_uuid: str = None):
        if user_uuid is None:
            # ARS only
            user_uuid = "1d2ffd23-fbc0-48e9-9d0d-ff56907ca3d2"
        pattern = re.compile(r"#<CryptoFiats::")
        match, result = self.exec_command(
            "CryptoFiats::CreateOrUpdatePaymentNetworkJob.new.perform('%s',[{ network_type: '%s', currency: '%s'}])"
            % (user_uuid, network_type, currency),
            pattern=pattern,
            wrap_with_begin=False,
            timeout=30,
        )
        if match:
            logger.debug(f"Payment Network update Job was performed for {network_type} - {currency}")
        else:
            raise EKSRailsConsoleException(
                f"Failed to performed update job - payment network.\n Console output:\n{result}"
            )

    def deactivate_payment_network(self, network_type: str, currency: str, user_uuid: str = None):
        if user_uuid is None:
            # ARS only
            user_uuid = "1d2ffd23-fbc0-48e9-9d0d-ff56907ca3d2"
        pattern = re.compile(r"#<CryptoFiat::Account:")
        match, result = self.exec_command(
            "CryptoFiats::DeactivatePaymentNetworksJob.new.perform('%s',[{ network_type: '%s', currency: '%s'}])"
            % (user_uuid, network_type, currency),
            pattern=pattern,
            wrap_with_begin=False,
            timeout=30,
        )
        if match:
            logger.debug(f"Payment Network deactivate Job was performed for {network_type} - {currency}")
        else:
            logger.warning("Payment Network deactivate Job failed, payment network activate before deactivate")

    def send_notification_mco_card_atm_withdrawal_psa_rejected(self, email: str):
        """send notification with:
                Transaction Denied, Local ATM withdrawal is not allowed due to MAS Payment Service Act.
        Args:
            email: user email
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")
        match, result = self.exec_command(
            f"""
                UserPusher.mco_card_atm_withdrawal_psa_rejected(User.find_by(email: '{email}')).notification.push_later
            """,
            pattern=pattern,
            wrap_with_begin=False,
            timeout=1,  # must check app notification alert element instantly, so timeout must be short
        )
        if match:
            logger.debug(f"user: {email} sent notification success!")
        else:
            logger.debug(f"user: {email} sent notification probably success.\n Console output:{result}")
            # now rails return nil, maybe no need to raise exception
            # raise EKSRailsConsoleException(f"Failed to send notification.\n Console output:\n{result}")

    def disable_rails_log(self):
        pattern = re.compile(r"nil")
        match, result = self.exec_command(
            """
                Rails.logger.level = :error
                ActiveRecord::Base.logger.level = :error
                Bugsnag.configure do |config|
                  config.logger.level = Logger::ERROR
                end
            """,
            pattern=pattern,
            wrap_with_begin=True,
            timeout=15,
        )
        if match:
            logger.debug("Set rails logger level passed")
        else:
            logger.warning("Set rails logger level failed")

    def unlock_cro_stake(self, email: str):
        """Unlock MCO card's CRO stakes
        Args:
            email: user email
        """
        pattern = re.compile(r"McoLockups::CommandHandlers::McoLockupCommandHandler")
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                McoLockups::Service.new.update_can_unlock_at(user, can_unlock_at: Time.now)
            """,
            pattern=pattern,
            wrap_with_begin=False,
            timeout=15,
        )
        if match:
            logger.debug(f"Unlocked MCO card's CRO stakes for user email:{email}")
        else:
            raise EKSRailsConsoleException(f"Failed to unlock CRO stake.\n Console output:\n{result}")

    def get_auth_token(self, app_name: str = "Crypto.com iOS") -> str:
        pattern = re.compile(r'(?<=").*?(?=")')
        match, result = self.exec_command(
            f"""
            app = Doorkeeper::Application.find_by_name '{app_name}'
            Doorkeeper::AccessToken.create(application: app, passcode_verification_verified_at: Time.now, sms_verification_verified_at: Time.now).plaintext_token
            """,  # noqa: E501
            pattern=pattern,
            wrap_with_begin=True,
            timeout=60,
        )
        if match:
            return result
        else:
            raise EKSRailsConsoleException(f"Auth token not found. \nResult from command: \n{result}")

    def get_client_credentials(self, app_name: str = "Crypto.com iOS") -> Tuple[str, str]:
        pattern = re.compile(r'(?<=").*?(?=")')
        match, result = self.exec_command(
            f"""
            app = Doorkeeper::Application.find_by_name '{app_name}'
            app.uid
            """,
            pattern=pattern,
            wrap_with_begin=True,
            timeout=60,
        )
        if match:
            client_id = result
        else:
            raise EKSRailsConsoleException(f"client_id not found. \nResult from command: \n{result}")

        match, result = self.exec_command(
            """
            app.secret
            """,
            pattern=pattern,
            wrap_with_begin=True,
            timeout=60,
        )
        if match:
            client_secret = result
        else:
            raise EKSRailsConsoleException(f"client_secret not found. \nResult from command: \n{result}")

        return client_id, client_secret

    def get_passcode_encryption_key(self) -> str:
        pattern = re.compile(r'(?<=").*?(?=")')
        match, result = self.exec_command(
            """
            Rails.application.secrets.passcode_cipher
            """,
            pattern=pattern,
            wrap_with_begin=True,
            timeout=60,
        )
        if match:
            return result
        else:
            raise EKSRailsConsoleException(f"auth token not found. \nResult from command: \n{result}")

    def approve_user(
        self,
        user_id: int,
        dob: str = "1999-12-31",
        name: str = "Auto QA",
        defaults_features: List[str] = None,
    ):
        pattern = re.compile(r"true")
        default_features = defaults_features or [
            "bank_transfer_enabled",
            "credit_card_ixo_pay_enabled",
            "crypto_earn_enabled",
            "gift_card_enabled",
            "mobile_airtime_enabled",
            "referral_v3_enabled",
            "swift_enabled",
            "swift_withdrawal_enabled",
            "us_ach_pull_enabled",
            "viban_withdrawal_enabled",
        ]

        match, result = self.exec_command(
            f"""
               user = User.find({user_id})
               user.identity.update(verification: "approved", liveness_review_status: "approved", risk_level: "low", review_note: "account auto create", dob: "{dob}", name: "{name}")  
               user.update(features: (user.features + {default_features}).uniq)
               user.enable_crypto!
               """,  # noqa
            pattern=pattern,
            wrap_with_begin=True,
            timeout=60,
        )
        if match:
            logger.debug(f"approve user {user_id}")
        else:
            raise EKSRailsConsoleException(f"approving user {user_id} failed. \nResult from command: \n{result}")

    def set_sms_verification_status(self, user_id: int, status: bool = True):
        """
        status: True to disable otherwise enable
        """
        pattern = re.compile(r"true")
        cmd = "disable!" if status else "enable!"

        match, result = self.exec_command(
            f"""
               user = User.find({user_id})
               PhoneOtp::SkipVerificationService.new(user: user).{cmd}
               """,
            pattern=pattern,
            wrap_with_begin=True,
            timeout=60,
        )
        if match:
            logger.debug(f"set_sms_verification_status {status} user {user_id}")
        else:
            raise EKSRailsConsoleException(
                f"set_sms_verification_status {status} user {user_id} failed. \nResult from command: \n{result}"
            )

    def set_passcode(self, email: str, passcode: str):
        pattern = re.compile(r"true")

        match, result = self.exec_command(
            f"""
               user = User.find_by_email('{email}')
               user.passcode.update(Passcode.encrypt('{passcode}'))
               """,
            pattern=pattern,
            wrap_with_begin=True,
            timeout=60,
        )
        if match:
            logger.debug(f"set_passcode user {email}")
        else:
            raise EKSRailsConsoleException(f"set_passcode user {email} failed. \nResult from command: \n{result}")

    def set_user_locale(self, email: str, locale: str):
        """Set user locale under user.user_config:

        Args:
            email: user email
            locale: locale to set
        """
        pattern = re.compile(r"(^true$)|(\ntrue)")
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                user.user_config.update_attributes(preferred_locale: "{locale}", locale: "{locale}")
            """,
            pattern=pattern,
            wrap_with_begin=False,
            timeout=15,
        )
        if match and locale == self.get_user_locale(email):
            logger.debug(f"User {email} locale set to {locale}!")
        else:
            raise EKSRailsConsoleException(f"User {email} locale failed to set to {locale}.\n Console output:{result}")

    def get_user_locale(self, email: str):
        """Set user locales under user.user_config:

        Args:
            email: user email

        Returns:
        str: user's locales.
        """

        pattern = re.compile(r'(?<=").*(?=")')
        match, result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                user.user_config.locale
            """,
            pattern=pattern,
            wrap_with_begin=False,
            timeout=15,
        )
        if match:
            logger.debug(f"User's locale: {result}")
            return result
        else:
            raise EKSRailsConsoleException(f"User's locale not found. \nResult from command: \n{result}")

    def update_feature_flag(self, email: str, feature_flags: List[str], action: str = "add"):
        if action == "add":
            symbol = "+"
        else:
            symbol = "-"

        pattern = re.compile(r"(^true$)|(\ntrue)")
        match, result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            user.update(features: user.features {symbol} {feature_flags})
            """,
            pattern=pattern,
            wrap_with_begin=True,
            timeout=15,
        )
        if match:
            logger.debug(f"User {action} feature flags: {feature_flags} Done")
        else:
            logger.debug(f"Feature flags: {feature_flags} seems not exist in current user or Failed")

    def update_user_identity(self, email: str, identity_key: str, identity_value: str):
        """
        identity_key: name(legal_name), dob, gender
        """
        match, result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            user.identity.update({identity_key}: '{identity_value}')
            """,
            pattern=re.compile(r"(^true$)|(\ntrue)"),
            wrap_with_begin=True,
            timeout=15,
        )
        if match:
            logger.debug(f"User update user identity {identity_key}: '{identity_value}' Passed")
        else:
            raise EKSRailsConsoleException(f"User update user identity {identity_key}: '{identity_value}' Failed")

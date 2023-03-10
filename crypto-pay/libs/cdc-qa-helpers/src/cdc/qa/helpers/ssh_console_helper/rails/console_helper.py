from __future__ import annotations
from typing import TYPE_CHECKING, Iterable, Union, Optional, Tuple, List

import logging
import os
import time
import datetime
import re
from distutils.util import strtobool

from ..constants import SSH_CONFIG_PATH
from ..console_helper import ConsoleHelper
from ..ssh_config import FileSSHConfig, AWSEC2SSHConfig, AWSECSSSHConfig
from .console_interactive import RailsConsoleInteractive
from .data import (
    GlobalFlag,
    InternalTestersList,
    XfersConnectState,
    DobVerificationSettings,
)
from ..exceptions import FailedToStartConsoleException
from retry import retry

if TYPE_CHECKING:
    from ..ssh_config.base import SSHConfig

logger = logging.getLogger(__name__)


class RailsConsoleHelper(ConsoleHelper):
    """A helper class that handles actions through executing commands on rails console."""

    def start_console(self, tries: int = 5):
        """Attempt to start a `RailsConsoleInteractive` instance.

        Args:
            tries (int): Number of retry for each start method upon failing to start the console on all hosts.

        Raises:
            FailedToStartConsoleException: Cannot start a rails console on any of the defined hosts.
        """

        def start_from_config(config: SSHConfig, hostnames: Iterable[str]):
            logger.debug(f"Received hostnames: '{hostnames}'...")
            for hostname in hostnames:
                if "bastion" in hostname:
                    # Skip connect bastion host
                    continue
                logger.debug(f"Resolving hostname '{hostname}'...")
                host = config.resolve_ssh_config(hostname=hostname)
                try:
                    logger.info(f"Starting rails console on '{host['hostname']}'...")
                    self.console = RailsConsoleInteractive(host)
                    logger.info(f"Rails console started on '{host['hostname']}'.")
                    break
                except Exception as e:
                    logger.warning(f"Failed to start rails console on '{host['hostname']}': {e}")
                    try:
                        self.console.shutdown()
                    except Exception:
                        pass
            else:
                logger.error("Failed to start rails console on all predefined hosts.")
                raise FailedToStartConsoleException

        @retry(FailedToStartConsoleException, tries=tries)
        def start_from_file():
            config = FileSSHConfig(SSH_CONFIG_PATH)
            prefix = "staginga-userworker"
            hostnames = (hn for hn in config.hostnames if prefix in hn)
            logger.info("Starting from file config...")
            start_from_config(config, hostnames)

        @retry(FailedToStartConsoleException, tries=tries)
        def start_from_aws_ec2():
            ec2 = {
                "stg": {
                    "node_name": "asta-ecs-node-user-worker",
                    "host_prefix": "staginga-userworker",
                    "bastion_name": "staging-bastion-ecs*",
                },
                "dev": {
                    "node_name": "adev-ecs-node-user-worker",
                    "host_prefix": "dev-userworker",
                    "bastion_name": "dev-bastion-ecs-2*",
                },
            }

            ec2_config = ec2[os.environ.get("ENV", "stg")]
            config = AWSEC2SSHConfig([ec2_config])
            logger.info("[Experimental] Starting from AWS EC2 config...")
            start_from_config(config, config.hostnames)

        @retry(FailedToStartConsoleException, tries=tries)
        def start_from_aws_ecs():
            ecs = {
                "stg": {
                    "host_prefix": "staginga-userworker",
                    "cluster_name": "StagingA",
                    "service_name": "stag-ecs-user-batch-job-worker-service",
                    "bastion_name": "staging-bastion-ecs*",
                },
                "dev": {
                    "host_prefix": "dev-userworker",
                    "cluster_name": "dev",
                    "service_name": "dev-ecs-user-batch-job-worker-service",
                    "bastion_name": "dev-bastion-ecs*",
                },
            }

            ecs_config = ecs[os.environ.get("ENV", "stg")]
            config = AWSECSSSHConfig([ecs_config])
            logger.info("[Experimental] Starting from AWS ECS config...")
            start_from_config(config, config.hostnames)

        start_methods = []
        if strtobool(os.environ.get("RAILS_CONSOLE_CONFIG_AWSECS", "True")):
            start_methods.append(start_from_aws_ecs)
        if strtobool(os.environ.get("RAILS_CONSOLE_CONFIG_AWSEC2", "True")):
            start_methods.append(start_from_aws_ec2)
        start_methods.append(start_from_file)

        for method in start_methods:
            try:
                method()
                break
            except Exception as e:
                logger.error(f"{method=} encountered exception: {e}")
        else:
            raise FailedToStartConsoleException

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

        result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            {magic_token_type}
        """,
            wrap_with_begin=True,
        )

        match = re.search(r'=> "(.*)"', result)
        if match:
            return match.group(1)
        else:
            raise Exception(f"Magic token not found. \nResult from command: \n{result}")

    def get_login_magic_link(self, email):
        return f"https://st.mona.co/magic/{self.get_magic_token(email)}?magic_action=login"

    def get_rails_access_token(self, email):
        result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            application = Doorkeeper::Application.find_by(name: 'monaco')
            access_token = Doorkeeper::AccessToken.create(application: application, resource_owner_id: user.id)
            access_token.plaintext_token
        """,
            wrap_with_begin=True,
        )
        match = re.search(r'=> "(.*)"', result)
        if match:
            return match.group(1)
        else:
            raise Exception(f"Rails Access Token not found. \nResult from command: \n{result}")

    def get_global_flag_value(self, global_flag: GlobalFlag) -> str:
        """Get global flag value.
        Args:
            global_flag: Global flag value to get. See GlobalFlag.
        """
        return re.search(r"=> (.*)", self.exec_command(f"Setting.{global_flag.value}")).group(1).rstrip()

    def set_global_flag_value(self, global_flag: GlobalFlag, value: str):
        """Set global flag with given value.
        Args:
            global_flag: Global flag to be set. See GlobalFlag.
            value: value set for the global flag
        Raises:
            Exception: Value not set.
        """

        result = self.exec_command(f"Setting.{global_flag.value} = {value}")
        if re.search(r"=> (.*)", result):
            logger.debug(f"Global flag {global_flag} has set to {value}")
        else:
            raise Exception(f"Global flag {global_flag} has failed to set to {value}.\nConsole output:\n{result}")

    def set_app_locks_dob_verification(self, dob_verification_settings: DobVerificationSettings, value: str):
        """Set global flag with given value.
        Args:
            dob_verification_settings: dob_verification_settings
            value: value set for the global flag
        Raises:
            Exception: Value not set.
        Returns:
            None
        """

        result = self.exec_command(
            f"Setting.app_locks[:dob_verification][:{dob_verification_settings.value}] = {value}"
        )
        if re.search(r"=> (.*)", result):
            logger.debug(f"App locks for Dob Verification's {dob_verification_settings} has set to {value}")
        else:
            raise Exception(
                f"App locks for Dob Verification's {dob_verification_settings} has failed to set to {value}."
                f"\nConsole output:\n{result}"
            )

    def add_crypto(self, user_email: str, crypto_currency: str, amount: Union[int, str]):
        """Add cryptos with given amount to given user find by email
        Args:
            user_email: user email
            crypto_currency: crypto currency upper() str code, can be either upper/lower case
            amount: amount of crypto to be added, can be either in type str/int
        Returns:
            None
        """
        result = self.exec_command(
            f"""
                user = User.find_by(email: '{user_email}')
                user.wallets.find_by(currency: '{crypto_currency.upper()}').add_fund!('{amount}'.to_d)
            """,
            wrap_with_begin=True,
        )
        if re.search(r"=> #<Wallet id", result):
            logger.debug(f"{amount} of crypto '{crypto_currency}' has added to user <email: {user_email}>")
        else:
            raise Exception(f"Has failed to add crypto '{crypto_currency}'.\nConsole output:\n{result}")

    def create_crypto_wallet(self, user_email: str, crypto_currency: str):
        """Create crypto wallet. In rails backend, for new account, create wallet is a async background job.
        Args:
            user_email: user email
            crypto_currency: crypto currency upper() str code, can be either upper/lower case
        Returns:
            None
        """
        result = self.exec_command(
            f"""
                   user = User.find_by(email: '{user_email}')
                   if !user.wallets.find_by(currency: '{crypto_currency.upper()}')
                       begin
                           Txns::CreateWalletCommand.new(user: user, currency: '{crypto_currency.upper()}').run!
                       rescue ActiveRecord::RecordNotUnique
                           nil
                       end
                   end
               """,
            wrap_with_begin=True,
        )
        if re.search(r"=> (.*)", result):
            logger.debug("Wallet created")
        else:
            logger.error("Failed to create wallet")

    def create_wallet_address(self, user_email: str, crypto_currency: str):
        """Create crypto wallet address. In rails backend, for new account, create wallet address is a async background job.
        As it depends on crypto-service, it will always be async, so we will always need to wait til address created.
        Args:
            user_email: user email
            crypto_currency: crypto currency upper() str code, can be either upper/lower case
        Returns:
            None
        """
        result = self.exec_command(
            f"""
                user = User.find_by(email: '{user_email}')
                user.assign_funding_source('{crypto_currency.upper()}')
            """,
            wrap_with_begin=True,
        )
        if re.search(r"=> (.*)", result):
            logger.debug("create wallet address job queued")
        else:
            logger.error("Failed to create wallet address")

        for _ in range(0, 5):
            check_address_result = self.exec_command(
                f"""
                user = User.find_by(email: '{user_email}')
                WalletSerializer.new(user.wallets.by_currency('{crypto_currency.upper()}')).address
                """,
                wrap_with_begin=True,
            )
            if not re.search("=> nil", check_address_result):
                return True

            time.sleep(3)

        return False

    def _get_ach_i2c_account_id(self, email: str) -> str:
        for i in range(40):
            logger.debug(f"Attempt to get ACH i2c account id #{str(i + 1)}")
            result = self.exec_command(
                f"""
                    user = User.find_by(email: '{email}')
                    user.van_wallet.i2c_van_account_id
                """,
                wrap_with_begin=True,
            )

            match = re.search(r'=> "(.*)"', result)
            if match:
                account_id = match.group(1)
                logger.debug(f"ACH i2c account id = {account_id}")
                return account_id
            else:
                logger.warning(f"ACH i2c account id not found. \nResult from command: \n{result}")
                time.sleep(5)
        raise Exception("ACH i2c account id not found")

    def add_usd_via_ach(self, email: str, amount: Union[str, int]):
        """Add USD to fiat wallet via ACH.

        Args:
            email: user email address
            amount: amount of USD to be added

        Returns:
            None
        """

        i2c_account_id = self._get_ach_i2c_account_id(email)

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
            wrap_with_begin=False,
        )

        result = self.exec_command(f"create_us_ach_deposit('{i2c_account_id}', '{amount}')")

        if re.search(r"Enqueued Van::I2c::ProcessEventNotificationJob", result):
            logger.debug(f"{amount} of USD has added to user <email: {email}>")
        else:
            raise Exception(f"Has failed to add USD.\nConsole output:\n{result}")

    def shipped_physical_card(self, email: str):
        result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            card = user.primary_card
            card.update(shipping_state: 'shipped')
            card.update(shipping_courier: 'DHL')
            card.update(shipping_tracking_number: '5354553')
            card.update(shipped_on: Time.now)
            """,
            wrap_with_begin=False,
        )

        if "true" in result:
            logger.debug(f"user: {email} has set physical card status to shipped success!")
        else:
            raise Exception("Failed to set physical card status to shipped.\n" f"Console output:\n{result}")

    def activate_physical_card(self, email: str):
        result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            card = user.primary_card
            card.update(activated_at: Time.now)
             """,
            wrap_with_begin=False,
        )

        if "true" in result:
            logger.debug(f"user: {email} has activated physical card success!")
        else:
            raise Exception(f"Failed to activated physical card.\n Console output:\n{result}")

    def update_payment_network(self, network_type: str, currency: str, user_uuid: str = None):
        if user_uuid is None:
            # ARS only
            user_uuid = "1d2ffd23-fbc0-48e9-9d0d-ff56907ca3d2"
        result = self.exec_command(
            "CryptoFiats::CreateOrUpdatePaymentNetworkJob.new.perform('%s',[{ network_type: '%s', currency: '%s'}])"
            % (user_uuid, network_type, currency),
            wrap_with_begin=False,
        )
        if "#<CryptoFiats::" in result:
            logger.debug(f"Payment Network update Job was performed for {network_type} - {currency}")
        else:
            raise Exception(f"Failed to performed update job - payment network.\n Console output:\n{result}")

    def deactivate_payment_network(self, network_type: str, currency: str, user_uuid: str = None):
        if user_uuid is None:
            # ARS only
            user_uuid = "1d2ffd23-fbc0-48e9-9d0d-ff56907ca3d2"
        result = self.exec_command(
            "CryptoFiats::DeactivatePaymentNetworksJob.new.perform('%s',[{ network_type: '%s', currency: '%s'}])"
            % (user_uuid, network_type, currency),
            wrap_with_begin=False,
        )
        if "#<CryptoFiat::Account:" in result:
            logger.debug(f"Payment Network deactivate Job was performed for {network_type} - {currency}")
        else:
            logger.warning("Payment Network deactivate Job failed, payment network activate before deactivate")

    def send_notification_mco_card_atm_withdrawal_psa_rejected(self, email: str):
        """send notification with:
                Transaction Denied, Local ATM withdrawal is not allowed due to MAS Payment Service Act.
        Args:
            email: user email
        """
        result = self.exec_command(
            f"""
                UserPusher.mco_card_atm_withdrawal_psa_rejected(User.find_by(email: '{email}')).notification.push_later
            """,
            wrap_with_begin=False,
        )
        if "true" in result:
            logger.debug(f"user: {email} sent notification success!")
        else:
            logger.debug(f"user: {email} sent notification probably success.\n Console output:{result}")

    def disable_rails_log(self):
        result = self.exec_command(
            """
                Rails.logger.level = :error
                ActiveRecord::Base.logger.level = :error
                Bugsnag.configure do |config|
                  config.logger.level = Logger::ERROR
                end
            """,
            wrap_with_begin=True,
        )
        if "nil" in result:
            logger.debug("Set rails logger level passed")
        else:
            logger.warning("Set rails logger level failed")

    def unlock_cro_stake(self, email: str):
        """Unlock MCO card's CRO stakes
        Args:
            email: user email
        """
        result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                McoLockups::Service.new.update_can_unlock_at(user, can_unlock_at: Time.now)
            """,
            wrap_with_begin=False,
        )
        if "McoLockups::CommandHandlers::McoLockupCommandHandler" in result:
            logger.debug(f"Unlocked MCO card's CRO stakes for user email:{email}")
        else:
            raise Exception(f"Failed to unlock CRO stake.\n Console output:\n{result}")

    def get_user_id(self, email: str) -> int:
        """Get user id with given email.

        Args:
            email (str): Email of target user.

        Raises:
            Exception: Unable to get user id with given email.

        Returns:
            str: user id.
        """
        result = self.exec_command(f"User.find_by(email: '{email}').id")
        logger.debug(result)
        match = re.search(r"=> (.*)", result)
        if match:
            return int(match.group(1))
        else:
            raise Exception(f"Unable to get user id with given email. \nResult from command: \n{result}")

    def update_xfers_connect_state(self, email: str, state: XfersConnectState):
        """Update Xfers connect status.

        Args: email: User email address state: States available: 'pending_xfers_verify', 'pending_review',
        'activated', 'disconnected', 'rejected'. See Enum XfersConnectState().

        Returns:
            None
        """

        result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            x = XfersAccount.find_by(user: user)
            x.state = '{state.value}'
            x.save
        """,
            wrap_with_begin=True,
        )

        if re.search("=> true", result):
            logger.debug(f"Xfers connect state is set to {state.value}")
        else:
            raise Exception(f"Xfers connect state is failed to set to {state.value}.\nConsole output:\n{result}")

    def update_phone_number(self, email, phone_number):
        """
        Args:
            email(str): User email
            phone_number(str): phone number to update.
        """
        logger.info(self.exec_command(f"user = User.find_by(email: '{email}')"))
        result = self.exec_command(
            f"""
            user.reload
            user.instance_variable_set('@skip_phone_confirmation', true)
            user.phone = '{phone_number}'
            user.unconfirmed_phone = nil
            user.phone_confirmed_at = Time.now
            user.save(validate: false)
            user.reload
            """,
            wrap_with_begin=True,
        )
        logger.info(result)

    def update_document_issuing_country(self, email, country_code):
        """Updates document issuing country for the user by email
        Args:
            email: user email
            country_code: alpha_3 of the country
        Returns:
            None
        """
        result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            user.identity.update(document_issuing_country: '{country_code}')
            """,
            wrap_with_begin=True,
        )

        if re.search(r"=> true", result):
            logger.debug(f"Document issuing country is set to {country_code}")
        else:
            raise Exception(f"Document issuing country has failed to set to {country_code}.\nConsole output:\n{result}")

    def update_mco_card_holder_name(self, email: str, first_name: str, last_name: str):
        """Updates mco card holder name for user by email
        Args:
            email: user email
            first_name: first name of card holder
            last_name: last name of card holder
        Returns:
            None
        """
        result = self.exec_command(
            f"""
                    user = User.find_by(email: '{email}')
                    user.identity.update!(document_data_cache: {{ document: {{ lastName: '{last_name}', firstName: '{first_name}' }} }})
                """,  # noqa: E501
            wrap_with_begin=True,
        )
        if re.search(r"=> true", result):
            logger.debug(f"Mco card holder name is set to: First name = {first_name}, Last name = {last_name}")
        else:
            raise Exception(
                f"Mco card holder name has failed to set to: First name = {first_name}, Last name = {last_name}.\n"
                f"Console output:\n{result}"
            )

    def update_unactivated_mco_card_info(self, email: str):
        result = self.exec_command(
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
            """,  # noqa: E501
            wrap_with_begin=True,
        )
        if "true" in result:
            logger.debug("Updated unactivated MCO Card's info.")
        else:
            raise Exception(f"Updated unactivated MCO Card's info with error, result: \n{result}")

    def get_email_url_from_rails(self, user_id, message_slug):
        """
        Args:
            user_id(int): user_id
            message_slug(str): message_slug for locating the message type

        Returns:
            str: URL
        Raises:
            Exception: Failed to get url with given user_id and message slug
        """
        result = self.exec_command(
            f"""
            user = User.find({user_id})
            MessageJob.where(user_id: user.id).where('message_slug ilike ?', '{message_slug}%').last.message_payload['url']
            """,  # noqa: E501
            wrap_with_begin=True,
        )
        logger.info(result)
        match = re.search(r"\"(https.+)\"", result)
        if match:
            return match.group(1)
        else:
            raise Exception(f"Unable to get url. \nResult from command: \n{result}")

    def turn_on_button_on_supermenu(self, item):
        """
        Args:
            item(str): Supermenu button item name, i.e. 'recurring buy'
        Raises:
            ValueError: Given item name is invalid
        """
        item = item.lower()
        if item == "recurring buy":
            result = self.exec_command(
                """
                button = SuperMenu::MenuItemGroupItem.find_by(menu_item: SuperMenu::MenuItem.find_by(key: 'recurring_buy'))
                button.hidden = false
                button.save!
                """,  # noqa: E501
                wrap_with_begin=True,
            )
            logger.debug(result)
        else:
            raise ValueError(f"Item '{item}' is either not yet implemented/item name is incorrect.")

    def approve_xfers_withdrawal_transaction(self, email):
        self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            withdrawal_view = XfersWithdrawalView.where({{user: user, status: 'risk_pending'}})
            Xfers::WithdrawalService.risk_approve(user, withdrawal_view[0].id, 'test', 'risk_team@crypto.com')
            """,
            wrap_with_begin=True,
        )

    def add_user_to_internal_tester(self, email: str, internal_tester_list: InternalTestersList):
        """Add user into internal tester list.

        Args:
            email: user email address
            internal_tester_list: internal testers list array in rails console
        Returns:
            None
        """

        is_added = self.exec_command(
            f"""
            Setting.{internal_tester_list.value} |= ['{email}']; nil
            Setting.{internal_tester_list.value}.include? '{email}'
        """,
            wrap_with_begin=True,
        )
        if "true" in is_added:
            logger.info(f"User is added into '{internal_tester_list.value}' internal tester list")
        else:
            logger.error(f"Internal tester list checking returned: '{is_added}'")
            raise ValueError(
                "Cannot find user email in internal tester list, failed to add user into internal tester list"
            )

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
        )

        if is_physical_card:
            result = self.exec_command(
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
                """
            )
        else:
            result = self.exec_command(
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
                """
            )

        card_info = {
            "user_email": user_email,
            "card_customer_id": card_customer_id,
            "card_program_id": card_program_id,
            "base_currency": base_currency,
        }

        if re.search("=> #<Card id", result):
            logger.debug(f"MCO Visa card had been added: {card_info}")
        else:
            raise Exception(f"MCO Visa card is not added . \nResult from command: \n{result}")

    def add_user_to_crypto_withdrawal_inactive_validations_whitelist(self, email: str):
        """Add user into crypto withdrawal inactive validations whitelist.
        Args:
            email: user email address
        Returns:
            None
        """
        is_added = self.exec_command(
            f"""
            tmp = Setting.crypto_withdrawal_address__inactive_validations_whitelist
            tmp['{email}'] = 'Automation'
            Setting.crypto_withdrawal_address__inactive_validations_whitelist = tmp
            Setting.crypto_withdrawal_address__inactive_validations_whitelist.key?('{email}')
            """,
            wrap_with_begin=True,
        )
        if "true" in is_added:
            logger.info("User is added into crypto withdrawal inactive validation whitelist'")
        else:
            logger.error(f"Internal tester list checking returned: '{is_added}'")
            raise ValueError(
                "Cannot find user email, failed to add user into crypto withdrawal invalid validation whitelist"
            )

    def add_kyc_address(self, email: str):
        """Add user kyc address.
        Args:
            email: user email address
        Returns:
            None
        """
        result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                c = WirecardUkCardApplication.find_or_initialize_by(user_uuid: user.uuid)
                c.address = {{address_1: 'xxxx', city: 'xxx', country_code: 'GBR', postcode: 'xxx'}}
                c.save!
            """,
            wrap_with_begin=True,
        )
        if "true" in result:
            logger.info("User kyc address successfully added")
        else:
            raise ValueError("Failed to set user kyc address")

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
        result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                @card_application = user.wirecard_uk_card_application || user.build_wirecard_uk_card_application
                @card_application.terms_accepted_at = DateTime.new({year[:1]}_{year[1:]}, 1, 1, 0, 0, 0)
                @card_application.save
            """,
            wrap_with_begin=True,
        )
        if "true" in result:
            logger.info(f"User card application terms_accepted_at is set to {year}")
        else:
            raise ValueError(f"Failed to set user card application terms_accepted_at to {year}")

    def get_user_sms_otp(self, email: str) -> str:
        """Get current SMS OTP for specific user by user email.
        Args:
            email: user email
        Returns:
            User SMS OTP in str
        """

        result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                user.otp_code
            """,
            wrap_with_begin=True,
        )

        match = re.search(r'=> "(.*)"', result)
        if match:
            return match.group(1)
        else:
            raise Exception(f"SMS OTP not found. \nResult from command: \n{result}")

    def set_user_phone_and_phone_country(self, email: str, phone_number: str, country_alpha_3: str):
        """Set user phone number and phone country by user email
        Args:
            email: user email
            phone_number: phone number to be set
            country_alpha_3: country alpha 3 code
        """

        result = self.exec_command(
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
        )

        match = re.search(r"=> true", result)
        if match:
            logger.info(f"Set user.phone = '{phone_number}, user.phone_country = '{country_alpha_3}'")
        else:
            raise Exception(
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

        result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                UserEntityMigration.create!(user_uuid: user.uuid, entity_id: '{entity_id}', status: 'done')
                user.instance_variable_set('@skip_phone_confirmation', true)
                user.update_entity_id!('{entity_id}')
                user.phone_country = "{country_code}"
                user.save(validate: false)
            """,
            wrap_with_begin=True,
        )

        match = re.search(r"=> true", result)
        if match:
            logger.info(f"Set user entity for '{email}' to '{entity_id}'")
        else:
            logger.error(f"Failed to set user entity to '{entity_id}' \n Result from command: \n{result}")

    def delete_user_entity(self, email: str, entity_id: str):
        """Delete user current entity by user email
        Args:
            email: user email
            entity_id: country name
        """

        result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                UserEntityMigration.find_by(user_uuid: user.uuid).delete
            """,
            wrap_with_begin=True,
        )

        match = re.search(r"=> #<UserEntityMigration id", result)
        if match:
            logger.info(f"Deleted user entity for '{email}'")
        else:
            logger.error(f"Failed to delete user entity to '{entity_id}' \n Result from command: \n{result}")

    def refresh_user_fiat_balance(self, email: str):
        """Refresh user fiat wallet balance on monaco-rails
        Args:
            email: user email
        """

        result = self.exec_command(
            f"""
            user = User.find_by!(email: '{email}')
            CryptoFiats::BalanceService.new.refresh(user)
            nil
            """,
            wrap_with_begin=True,
        )

        if re.search("=> nil", result):
            logger.debug("Refreshed fiat balance")
        else:
            logger.error("Failed to refresh user fiat balance")

    def approve_malta_entity_address(self, email: str):
        """Approve Malta entity address
        Args:
            email: user email
        """

        result = self.exec_command(
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
        )

        if re.search(r"=> true", result):
            logger.debug("Malta address had been approved.")
        else:
            logger.error("Failed to approve Malta address \n Result from command: \n{result}")

    def update_physical_card_application_status(self, status: str, email: str):
        """Update physical card application status
        Args:
            status: pending_submit/submitted
            email: user email
        """
        result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                user.primary_card.update(physical_card_issued_at: Time.zone.now)
                user.primary_card.physical_card_application
                user.primary_card.physical_card_application.update(state: '{status}')
            """,
            wrap_with_begin=True,
        )
        if re.search(r"=> true", result):
            logger.debug(f"Physical Card issue status changed to {status}")
        else:
            logger.error(f"Physical Card issued changed with error, result: \n{result}")

    def issued_physical_card(self, email: str):
        """Issued physical card
        Args:
            email: user email
        """
        result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            card = user.primary_card
            card.update(physical_card_issued_at: Time.zone.now)
            app = card.physical_card_application
            app.issue_started!
            app.issue_succeed!('QA Auto')
            """,
            wrap_with_begin=True,
        )

        if re.search(r"=> true", result):
            logger.debug("Physical Card issued")
        else:
            logger.error(f"Physical Card issued with error, result: \n{result}")

    def get_passcode_reset_magic_token(self, email: str):
        result = self.exec_command(
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
        )
        match = re.search(r'=> "(.*)"', result)
        if match:
            return match.group(1)
        else:
            raise Exception(f"Get reset passcode magic token failed: \n{result}")

    def enable_quotation_count_down_period(self, timeout: int = 90):
        result = self.exec_command(
            f"""
            Setting.quotation_override_countdown_enabled = true
            Setting.quotation_qa_custom_countdown_period = {timeout}
            """
        )
        if re.search(rf"=> {timeout}", result):
            logger.debug("Enable quotation countdown period successes")
        else:
            logger.error(f"Enable quotation countdown period failed, result: \n{result}")

    def get_auth_token(self, app_name: str = "Crypto.com iOS") -> str:
        result = self.exec_command(
            f"""
            app = Doorkeeper::Application.find_by_name '{app_name}'
            Doorkeeper::AccessToken.create(application: app, passcode_verification_verified_at: Time.now, sms_verification_verified_at: Time.now).plaintext_token
            """,  # noqa: E501
            wrap_with_begin=True,
        )
        match = re.search(r'=> "(.*)"', result)
        if match:
            return match.group(1)
        else:
            raise Exception(f"Auth token not found. \nResult from command: \n{result}")

    def get_client_credentials(self, app_name: str = "Crypto.com iOS") -> Tuple[str, str]:
        result = self.exec_command(
            f"""
               app = Doorkeeper::Application.find_by_name "{app_name}"
               app.uid
               """
        )
        match = re.search(r'=> "(.*)"', result)
        if match:
            client_id = match.group(1)
        else:
            raise Exception(f"client_id not found. \nResult from command: \n{result}")

        result = self.exec_command(
            f"""
               app = Doorkeeper::Application.find_by_name "{app_name}"
               app.secret
               """
        )
        match = re.search(r'=> "(.*)"', result)
        if match:
            client_secret = match.group(1)
        else:
            raise Exception(f"client_secret not found. \nResult from command: \n{result}")

        return client_id, client_secret

    def get_passcode_encryption_key(self) -> str:
        result = self.exec_command(
            """
            Rails.application.secrets.passcode_cipher
            """
        )
        match = re.search(r'=> "(.*)"', result)
        if match:
            return match.group(1)
        else:
            raise Exception(f"auth token not found. \nResult from command: \n{result}")

    def approve_user(
        self,
        user_id: int,
        dob: str = "1999-12-31",
        name: str = "Auto QA",
        defaults_features: List[str] = None,
    ):
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

        result = self.exec_command(
            f"""
               user = User.find({user_id})
               user.identity.update(verification: "approved", liveness_review_status: "approved", risk_level: "low", review_note: "account auto create", dob: "{dob}", name: "{name}")  
               user.update(features: (user.features + {default_features}).uniq)
               user.enable_crypto!
               """,  # noqa
            wrap_with_begin=True,
        )
        if re.search("=> true", result):
            logger.debug(f"approve user {user_id}")
        else:
            raise Exception(f"approving user {user_id} failed. \nResult from command: \n{result}")

    def set_sms_verification_status(self, user_id: int, status: bool = True):
        """
        status: True to disable otherwise enable
        """
        cmd = "disable!" if status else "enable!"

        result = self.exec_command(
            f"""
               user = User.find({user_id})
               PhoneOtp::SkipVerificationService.new(user: user).{cmd}
               """,
            wrap_with_begin=True,
        )
        if re.search("=> true", result):
            logger.debug(f"set_sms_verification_status user {user_id}")
        else:
            raise Exception(f"set_sms_verification_status user {user_id} failed. \nResult from command: \n{result}")

    def set_passcode(self, email: str, passcode: str):
        result = self.exec_command(
            f"""
               user = User.find_by_email('{email}')
               user.passcode.update(Passcode.encrypt('{passcode}'))
               """,
            wrap_with_begin=True,
        )
        if re.search("=> true", result):
            logger.debug(f"set_passcode user {email}")
        else:
            raise Exception(f"set_passcode user {email} failed. \nResult from command: \n{result}")

    def set_user_locale(self, email: str, locale: str):
        """Set user locale under user.user_config:

        Args:
            email: user email
            locale: locale to set
        """
        result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                user.user_config.update_attributes(preferred_locale: "{locale}", locale: "{locale}")
            """,
            wrap_with_begin=False,
        )
        match = re.search(re.compile(r"(^true$)|(\ntrue)"), result)
        if match and locale == self.get_user_locale(email):
            logger.debug(f"User {email} locale set to {locale}!")
        else:
            raise Exception(f"User {email} locale failed to set to {locale}.\n Console output:{result}")

    def get_user_locale(self, email: str):
        """Set user locales under user.user_config:

        Args:
            email: user email

        Returns:
        str: user's locales.
        """

        result = self.exec_command(
            f"""
                user = User.find_by(email: '{email}')
                user.user_config.locale
            """,
            wrap_with_begin=False,
        )
        match = re.search(re.compile(r'(?<=").*(?=")'), result)
        if match:
            logger.debug(f"User's locale: {result}")
            return result
        else:
            raise Exception(f"User's locale not found. \nResult from command: \n{result}")

    def update_feature_flag(self, email: str, feature_flags: List[str], action: str = "add"):
        if action == "add":
            symbol = "+"
        else:
            symbol = "-"

        result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            user.update(features: user.features {symbol} {feature_flags})
            """,
            wrap_with_begin=True,
        )
        match = re.search(re.compile(r"(^true$)|(\ntrue)"), result)
        if match:
            logger.debug(f"User {action} feature flags: {feature_flags} Done")
        else:
            logger.debug(f"Feature flags: {feature_flags} seems not exist in current user or Failed")

    def update_user_identity(self, email: str, identity_key: str, identity_value: str):
        """
        identity_key: name(legal_name), dob, gender
        """
        result = self.exec_command(
            f"""
            user = User.find_by(email: '{email}')
            user.identity.update({identity_key}: '{identity_value}')
            """,
            pattern=re.compile(r"(^true$)|(\ntrue)"),
            wrap_with_begin=True,
            timeout=15,
        )
        match = re.search(re.compile(r"(^true$)|(\ntrue)"), result)
        if match:
            logger.debug(f"User update user identity {identity_key}: '{identity_value}' Passed")
        else:
            raise Exception(f"User update user identity {identity_key}: '{identity_value}' Failed")

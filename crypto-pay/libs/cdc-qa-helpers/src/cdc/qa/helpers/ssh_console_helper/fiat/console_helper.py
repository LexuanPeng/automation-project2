from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

import logging
import os
import time
import re
from distutils.util import strtobool

from ..constants import SSH_CONFIG_PATH
from ..console_helper import ConsoleHelper
from ..ssh_config import FileSSHConfig, AWSEC2SSHConfig, AWSECSSSHConfig, TSHSSHConfig
from .console_interactive import FiatConsoleInteractive
from ..exceptions import FailedToStartConsoleException
from retry import retry

if TYPE_CHECKING:
    from ..ssh_config.base import SSHConfig

logger = logging.getLogger(__name__)


class FiatConsoleHelper(ConsoleHelper):
    """A helper class that handles actions through executing commands on fiat console."""

    def start_console(self, tries: int = 5):
        """Attempt to start a `FiatConsoleInteractive` instance.

        Args:
            tries (int): Number of retry for each start method upon failing to start the console on all hosts.

        Raises:
            FailedToStartConsoleException: Cannot start a fiat console on any of the defined hosts.
        """

        def start_from_config(config: SSHConfig, hostnames: Iterable[str]):
            logger.debug(f"Received fiat hostnames: '{hostnames}'...")
            for hostname in hostnames:
                if "bastion" in hostname:
                    # Skip connect bastion host
                    continue
                logger.debug(f"Resolving hostname '{hostname}'...")
                host = config.resolve_ssh_config(hostname=hostname)
                try:
                    logger.info(f"Starting rails console on '{host['hostname']}'...")
                    self.console = FiatConsoleInteractive(host)
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
            prefix = "staginga-fiatworker" if os.environ.get("ENV", "stg") == "stg" else "dev-fiatworker"
            hostnames = (hn for hn in config.hostnames if prefix in hn)
            logger.info("Starting from file config...")
            start_from_config(config, hostnames)

        @retry(FailedToStartConsoleException, tries=tries)
        def start_from_aws_ec2():
            ec2 = {
                "stg": {
                    "node_name": "asta-ecs-node-fiat-worker",
                    "host_prefix": "staginga-fiatworker",
                    "bastion_name": "staging-bastion-ecs*",
                },
                "dev": {
                    "node_name": "adev-ecs-node-fiat-worker",
                    "host_prefix": "dev-fiatworker",
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
                    "host_prefix": "staginga-fiatworker",
                    "cluster_name": "StagingA",
                    "service_name": "staging-ecs-crypto-fiat-worker-service",
                    "bastion_name": "staging-bastion-ecs*",
                },
                "dev": {
                    "host_prefix": "dev-fiatworker",
                    "cluster_name": "dev",
                    "service_name": "dev-ecs-crypto-fiat-worker-service",
                    "bastion_name": "dev-bastion-ecs*",
                },
            }

            ecs_config = ecs[os.environ.get("ENV", "stg")]
            config = AWSECSSSHConfig([ecs_config])
            logger.info("[Experimental] Starting from AWS ECS config...")
            start_from_config(config, config.hostnames)

        @retry(FailedToStartConsoleException, tries=tries)
        def start_from_tsh():
            tsh = {
                "stg": {
                    "hostname": "tech.asta.ap-southeast-1.ecs.node.rails-console",
                    "user": "ec2-user",
                    "tsh_proxy": "internal-tech-teleport-sg.sec-stag.aws.cdcinternal.com",
                    "tsh_cluster": "ap-southeast-1.tech.internal",
                    "tsh_port": 3022,
                },
                "dev": {
                    "hostname": "tech.adev.ap-southeast-1.ecs.node.rails-console",
                    "user": "ec2-user",
                    "tsh_proxy": "internal-tech-teleport-sg.sec-stag.aws.cdcinternal.com",
                    "tsh_cluster": "ap-southeast-1.tech.internal",
                    "tsh_port": 3022,
                },
            }

            tsh_config = tsh[os.environ.get("ENV", "stg")]
            config = TSHSSHConfig([tsh_config])
            logger.info("[Experimental] Starting from TSH config...")
            start_from_config(config, config.hostnames)

        start_methods = []
        if strtobool(os.environ.get("FIAT_CONSOLE_CONFIG_TSH", "True")):
            start_methods.append(start_from_tsh)
        if strtobool(os.environ.get("FIAT_CONSOLE_CONFIG_AWSECS", "False")):
            start_methods.append(start_from_aws_ecs)
        if strtobool(os.environ.get("FIAT_CONSOLE_CONFIG_AWSEC2", "False")):
            start_methods.append(start_from_aws_ec2)
        if strtobool(os.environ.get("FIAT_CONSOLE_CONFIG_FILE", "False")):
            start_methods.append(start_from_file)

        for method in start_methods:
            try:
                method()
                break
            except Exception as e:
                logger.error(f"{method=} encountered exception: {e}")
        else:
            raise FailedToStartConsoleException

    def _deposit_funds(self, email: str, provider: str, currency: str, amount, wrap_with_begin: bool = True):
        """Add fiat to user account.

        Args:
            email(str): user email
            provider(str): fiat wallet service provider
            currency(str): fiat wallet currency
            amount(str): amount to deposit
        """

        if provider not in ["tr", "fps", "au_npp", "au_bpay"]:
            raise ValueError(f"Fiat Wallet provider '{provider}' is not available yet.")

        if currency not in ["EUR", "GBP", "AUD"]:
            raise ValueError(f"Fiat currency '{currency} is not available yet.")

        if provider == "tr":
            simulate_command = (
                f'Transactives::SimulateDepositJob.new.perform(account.id, currency: "{currency}", amount: "{amount}")'
            )
        elif provider in ["au_npp", "au_bpay"]:
            simulate_command = (
                f"""AssemblyPayments::SimulateDepositJob.new.perform(account.id, '{provider}', {amount})"""
            )
        else:
            simulate_command = ""

        skip_risk_approval_command = "DepositAuthorizations::Service.new.skip_risk_approval(DepositAuthorization.find_by(deposit_id: deposits[0].id))"  # noqa: E501
        if provider == "fps":
            skip_risk_approval_command = ""

        result = self.exec_command(
            f"""
            account = AccountView.find_by(email: '{email}')
            admin_user = User.find_by(email: 'qa_automation@crypto.com')
            {simulate_command}
            deposits = DepositView.where(account_id: account.id, status: ['pending_authorization'])
            {skip_risk_approval_command}
            DepositAuthorizations::Service.new.payment_approve(
                admin_user,
                DepositAuthorization.find_by(deposit_id: deposits[0].id)
            )
            """,
            wrap_with_begin=wrap_with_begin,  # noqa: E501
        )

        if re.search(r"=> nil", result):
            logger.debug(f"{amount} of {currency} has added to user <email: {email}>")
        else:
            raise Exception(f"Has failed to add {currency}.\nConsole output:\n{result}")

    def add_eur_via_sepa_transactive(self, email, amount):
        self._deposit_funds(email, "tr", "EUR", amount)

    def add_gbp_via_bcb_payments(self, email: str, unique_code: str, amount: str):
        self.exec_command(
            f"""
            account = AccountView.find_by(email: '{email}')
            ::Bcbs::SimulateDepositJob.new.perform(unique_ref: '{unique_code}', amount: '{amount}')
            """
        )
        time.sleep(240)
        self._deposit_funds(email, "fps", "GBP", amount, wrap_with_begin=False)

    def add_cad_via_dc_bank_simulate(self, email: str, identification_number: str, reference_number: int):

        """
        Add CAD to user account's CAD fiat wallet via Dc Bank SimulateDcBankInteracEmailJob.
        The default amount of deposit by reference number will be $1000

        Args:
            email(str): user email
            identification_number(str): display on CAD fiat wallet deposit info page
            reference_number(int): must unique and within 10 digit number (cannot start with zero)
        """
        result = self.exec_command(
            f"""
            account = AccountView.find_by(email: '{email}')
            DcBanks::SimulateDcBankInteracEmailJob.new.perform(account, '{identification_number}', {reference_number})
            """,
            wrap_with_begin=True,
        )

        if re.search(r"=> nil", result):
            raise Exception(f"Has failed to add CAD deposit.\nConsole output:\n{result}")
        else:
            logger.debug(f"CAD deposit with reference number {reference_number} has added to user <email: {email}>")

    def add_aud_via_npp_simulate(self, email: str, provider: str, amount: str):
        self._deposit_funds(email, provider, "AUD", amount)

    def admin_credit(self, email: str, currency: str, amount: str):
        """
        Admin credit fiat fund to user's fiat wallet

        Args:
            email: user email
            currency: credit currency
            amount: credit amount
        """

        result = self.exec_command(
            f"""
            user = User.find_by!(email: 'qa_automation@crypto.com')
            account = AccountView.find_by!(email: '{email}')
            admin_credit = AdminCredits::Service.new.create(
                user,
                account,
                '{currency}',
                '{amount}'.to_d,
                'auto_qa testing'
            )
            user = User.find_by!(email: 'qa_auto_approve@crypto.com')
            AdminCredits::Service.new.approve(
                user,
                admin_credit
            )
            """,
            wrap_with_begin=True,
        )

        if re.search(r"=> #<AdminCreditView", result):
            logger.debug(f"Admin credited ({currency}{amount}) to user <email: {email}>")
        else:
            logger.error(f"Failed to admin credit.\nConsole output:\n{result}")

    def deposit_fiat_brl(self, email: str, cpf_number: str, amount: str, payment_network: str = "br_pix"):

        """
        Args:
            email: str
            cpf_number: str
            amount: str
            payment_network : br_ted / br_pix / br_cmp / br_doc
        """
        result = self.exec_command(
            f"""
            account = AccountView.find_by(email: '{email}')
            ::BancoPlurals::SimulateDepositJob.new.perform(cpf: '{cpf_number}', amount: '{amount}', payment_network: '{payment_network}', ispb: '18236120', account_number: '1538', account_type_id: 2)
            """,  # noqa: E501
            wrap_with_begin=True,
        )

        if re.search(r"=> nil", result):
            logger.debug(f"BRL deposit with CPF number {cpf_number} has added to user <email: {email}>")
        else:
            raise Exception(
                f"Has failed to deposit BRL via CPF number {cpf_number} to user <email: {email}>."
                f"\nConsole output:\n{result}"
            )

    def get_deposit_id(self, email: str, cpf_number: str):
        result = self.exec_command(
            f"""
            def try_get_deposit_id
                raw = ActiveRecord::Base.connection.execute("SELECT * FROM banco_plural_deposits WHERE raw ->> 'CPFCNPJ' = '{cpf_number}' order by created_at desc limit 1").first["raw"]
                transaction_id = JSON.parse(raw)["Id"]
                account_view = AccountView.find_by(email: '{email}')
                DepositView.where(account_id: account_view.id).select do |deposit|
                    deposit.vendor_transaction_id.include?(transaction_id)
                end.first&.id
            end

            start = Time.now
            while Time.now - start < 10
                deposit_id = try_get_deposit_id
                if deposit_id
                    puts deposit_id
                    break
                end
                sleep(1)
            end
            """,  # noqa: E501
            wrap_with_begin=True,
        )

        if re.search(r"=> nil", result):
            logger.debug(f"Get CPF deposit id {result} for user <email: {email}>")
            return result
        else:
            logger.error(f"Has failed to get CPF deposit id to user <email: {email}>.\nConsole output:\n{result}")
            raise Exception(f"Has failed to get CPF deposit id to user <email: {email}>.\nConsole output:\n{result}")

    def approve_deposit_by_system(self, email: str, cpf_number: str):
        deposit_id = self.get_deposit_id(email=email, cpf_number=cpf_number)
        result = self.exec_command(
            f"""
            DepositAuthorizations::Service.new.risk_approve(‘{deposit_id}’, done_by: ‘system’)
            """,
            wrap_with_begin=True,
        )

        if re.search(r"=> nil", result):
            logger.debug(f"Approve Deposit for user: <{email}>")
            return result
        else:
            raise Exception(f"Has failed to approve Deposit for user: <{email}>.\nConsole output:\n{result}")

    def sgd_standard_chartered_fast_not_matched_name(self, email: str):
        # name != user.legal_name
        command = f"StandardChartereds::SgFast::SimulateDepositJob.new.perform(email: '{email}', name: 'not_legal')"
        result = self.exec_command(command, wrap_with_begin=True)
        match = re.search(r'=> #<DepositView id: "(.*)", account_id:', result)
        if match:
            deposit_id = match.group(1)
            logger.debug(f"SdFast simulate deposit job for not matched with legal name deposit: {deposit_id}")
            return deposit_id
        else:
            raise Exception(f"Failed to perform {command} for {email}")

    def add_sgd_via_standard_chartered_fast(
        self,
        account_id: str,
        email: str = None,
        name: str = None,
        identifier_value: str = None,
        bank_code: str = "DBSSSGSG",
        payment_network: str = "FAST",
        amount: int = 5000,
        env: str = "stg",
    ):
        """
        Add SGD to user account's SGD fiat wallet via Standard Chartered SimulateJob.
        The default amount of deposit will be $5000

        Args:
            email(str): nil, # will get name and virtual account number, optional
            amount(int): 5000, # default 5000, optional
            name(str): nil, # will override email that one, optional if email provided
            identifier_value(str): nil, # virtual account number will override email's value, optional if email provided
            account_id(str): '12345678', # bank account number, default 12345678, optional
            bank_code(str): 'DBSSSGSG' # bank code, default DBSSSGSG, optional
            payment_network(str): 'FAST' # FAST/MEPS/GIRO
            env(optional): default is stg
        """
        if email:
            command = f"StandardChartereds::SgFast::SimulateDepositJob.new.perform(email: '{email}', amount: '{amount}', account_id: '{account_id}', bank_code: '{bank_code}', payment_network: '{payment_network}')"  # noqa: E501
        else:
            command = f"StandardChartereds::SgFast::SimulateDepositJob.new.perform(amount: '{amount}', name: '{name}', identifier_value: '{identifier_value}', account_id: '{account_id}', bank_code: '{bank_code}', payment_network: '{payment_network}')"  # noqa: E501

        result = self.exec_command(command, wrap_with_begin=True)

        """
        TMX & SIFT quick approve
        """
        match = re.search(r'#<DepositView:\w+\W+id: "(.*)"|=> #<DepositView id: "(.*)", account_id:', result)
        if match:
            logger.debug(
                f"SGD Fast deposit <id: {match.group(1)}> has added to user <email: {email}>. "
                f"\nConsole output:\n{result}"
            )
            deposit_id = match.group(1)
            if env == "dev":
                is_completed = self._wait_deposit_completed(deposit_id)
                if is_completed:
                    return
                raise Exception(f"Failed to approve SGD Fast deposit <id: {deposit_id}> \nConsole output:\n{result}")

            result = self.exec_command(
                f"DepositAuthorizations::Service.new.risk_approve('{deposit_id}', done_by: 'system')",
                wrap_with_begin=True,
            )
            if re.search(r"=> #<(.*)|#<DepositAuthorizations::", result):
                logger.debug(f"SGD Fast deposit <id: {deposit_id}> approved. \nConsole output:\n{result}")
            else:
                raise Exception(f"Failed to approve SGD Fast deposit <id: {deposit_id}> \nConsole output:\n{result}")
        else:
            raise Exception(f"Has failed to add SGD Fast deposit.\nConsole output:\n{result}")

    @retry(Exception, tries=10, delay=30)
    def _sgd_fast_withdrawal_process_payment_id(self, withdrawal_id: str):
        command = f"Payments::ProcessTransferJob.new.perform('{withdrawal_id}')"
        result = self.exec_command(command, wrap_with_begin=True)
        if re.search(
            r"=> #<(.*), status:|#<PaymentView:\w+\W+id: \"(.*)\",\s\W+status: \"transfer_processing\"", result
        ):
            logger.debug(f"SGD Fast withdrawal's payment id processed \nConsole output:\n{result}")
        else:
            raise Exception(f"Failed to process SGD Fast withdrawal's payment id \nConsole output:\n{result}")

    def sgd_fast_withdrawal_payment_callback_simulate(self, withdrawal_id: str):
        self._sgd_fast_withdrawal_process_payment_id(withdrawal_id)
        cmd = f"StandardChartereds::SimulatePaymentCallbackJob.new.perform(id:'{withdrawal_id}', status:'Completed')"
        result = self.exec_command(cmd, wrap_with_begin=True)
        if re.search(r"#<StandardChartereds::PaymentRequestService:(.*)", result):
            logger.debug(f"SGD Fast withdrawal processed \nConsole output:\n{result}")
        else:
            raise Exception(f"Failed to process SGD Fast withdrawal \nConsole output:\n{result}")

    def circle_deposit(self, vendor_source_id: str, amount: str = "2000.0"):
        # Find Vendor Account Identifier under
        # "https://stag-crypto-fiat.3ona.co/ops/accounts" by searching account email
        # And put down as source_id
        # TODO need impl how to get the source id by searching account email on fiat ops
        cmd = f"Circles::SimulateDepositJob.new.perform(source_id: '{vendor_source_id}', amount: '{amount}')"
        result = self.exec_command(cmd, wrap_with_begin=True)
        if re.search(r"=> #<DepositView id:(.*)", result):
            logger.debug(f"Circle deposit \nConsole output:\n{result}")
        else:
            logger.error(f"Failed to circle deposit \nConsole output:\n{result}")
            raise Exception(f"Console output:\n{result}")

    def _wait_deposit_completed(self, deposit_id: str):
        result = f"Deposit {deposit_id} is not completed"
        for _ in range(10):
            time.sleep(10)
            result = self.exec_command(f"DepositView.find('{deposit_id}').status")
            if re.search(r'=> "completed"', result):
                logger.debug(f"Deposit <id: {deposit_id} is completed")
                return True

        logger.debug(f"Console output:\n{result}")
        return False

    def deposit_try_via_bulut_simulate(
        self,
        email: str,
        full_name: str,
        amount: str = "1000.0",
        sender_firm_bank_iban: str = "TR140010009999900000008765",
    ):

        """
        Add TRY to user account's TRY fiat wallet via Bulut SimulateDepositJob.

        Args:
            email(str): user email
            full_name(str): user full name
            amount(str): default is 1000
            sender_firm_bank_iban(str): Get valid iban from https://www.iban.com/calculate-iban or use the following
                                        TR470004600807888000123456
                                        TR080014300024200000123456
                                        TR230006701000000000123456
                                        TR220013900099800000123456
                                        TR610004600990888000009876
                                        TR140010009999900000008765
                                        TR380010009999900000007654
                                        TR900004600807888000123458
                                        TR200004600807888000123457
        """
        result = self.exec_command(
            f"""
            account = AccountView.find_by(email: '{email}')
            Buluts::SimulateDepositJob.new.perform(firm_bank_name: 'ADABANK', sender_firm_bank_name: 'ADABANK', amount: '{amount}', full_name: '{full_name}', sender_firm_bank_iban: '{sender_firm_bank_iban}', account_id: account.id)
            """,  # noqa: E501
            wrap_with_begin=True,
        )

        if re.search(r"=> nil", result):
            logger.debug(f"TRY deposit has added to user <email: {email}>")
        else:
            raise Exception(f"Has failed to add TRY deposit.\nConsole output:\n{result}")

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

import logging
import re
from ..rails.console_helper import RailsConsoleHelper

logger = logging.getLogger(__name__)


class ExchangeRailsConsoleHelper(RailsConsoleHelper):
    def add_staking_cro(self, email: str, amount: str) -> bool:
        """Add Staking CRO for user with given email.

        Args:
            email (str): Email of target user.
            amount (str): CRO staking amount

        Raises:
            Exception:

        Returns:

        """
        self.exec_command(f"user = User.find_by(email: '{email}')")
        result = self.exec_command(
            f"Exchange::ApiService.new.add_staking_cro(user_uuid: user.uuid, amount: '{amount}')"
        )

        match = re.search(r'=> #<Hashie::Mash code="(.*?)" data=(.*?) msg="(.*?)">', result)
        if match:
            return match.group(1) == "0" and match.group(3) == "Success"
        else:
            logger.error(f"Add staking CRO failed.\nResult from command: \n{result}")
            raise Exception(f"Add staking CRO failed.\nResult from command: \n{result}")

    def remove_staking_cro(self, email: str, amount: str) -> bool:
        """Remove Staking CRO for user with given email.

        Args:
            email (str): Email of target user.
            amount (str): CRO staking amount

        Raises:
            Exception:

        Returns:

        """
        self.exec_command(f"user = User.find_by(email: '{email}')")
        result = self.exec_command(
            f"Exchange::ApiService.new.remove_staking_cro(user_uuid: user.uuid, amount: '{amount}' )"
        )

        match = re.search(r'=> #<Hashie::Mash code="(.*?)" data=(.*?) msg="(.*?)">', result)
        if match:
            return match.group(1) == "0" and match.group(3) == "Success"
        else:
            logger.error(f"Remove staking CRO failed.\nResult from command: \n{result}")
            raise Exception(f"Remove staking CRO failed.\nResult from command: \n{result}")

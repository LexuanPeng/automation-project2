from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance
from cdc.qa.core import secretsmanager as sm

import logging
from typing import Optional, Union
import re
from retry import retry


logger = logging.getLogger(__name__)


class Twilio:
    def __init__(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None):
        account_sid = account_sid or sm.get_secret_json("twilio")["ACCOUNT_SID"]
        auth_token = auth_token or sm.get_secret_json("twilio")["AUTH_TOKEN"]
        self.client = Client(account_sid, auth_token)

    @retry(ValueError, delay=1, tries=10)
    def get_verification_code(self, phone_number: Union[int, str], pattern: Optional[str] = None) -> str:
        """Get the verification code sent to the phone number.

        Args:
            phone_number (Union[int, str]): The phone number expected to receive the verification code.
            pattern (Optional[str], optional): The pattern used to find verification code in the message.
                Defaults to None.

        Raises:
            ValueError: When the verification code not found in message.
            ValueError: When no message is received by the phone number.

        Returns:
            str: Verification code
        """
        phone_number = str(phone_number)
        pattern = pattern or r".*code is (\d+)"

        messages = self.client.messages.list(to=phone_number, limit=1)
        if messages:
            latest_message: MessageInstance = messages[0]
            logger.debug(f"Latest message for {phone_number=}: {latest_message.body}")

            match = re.match(pattern, latest_message.body)
            if match:
                return match.group(1)
            else:
                raise ValueError(f"Verification code not found in message: {latest_message.body=} {pattern=}")

        else:
            raise ValueError(f"No message found with {phone_number=}")

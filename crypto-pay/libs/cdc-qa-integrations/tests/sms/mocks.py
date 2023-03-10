import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def mock_twilio_secrets_manager(mocker: MockerFixture):
    mocker.patch(
        "cdc.qa.core.secretsmanager.get_secret_json",
        lambda x: {
            "ACCOUNT_SID": "sid",
            "AUTH_TOKEN": "token",
        },
    )


@pytest.fixture
def mock_twilio_message_list(mocker: MockerFixture, mock_twilio_secrets_manager):
    def message_list(self, to: str, *args, **kwargs) -> list:
        class MessageInstance:
            def __init__(self, message: str):
                self.body = message

        if to == "12345678":
            return [MessageInstance("Your Crypto.com verification code is 123456")]
        elif to == "+0012345678":
            return [MessageInstance("Your Crypto.com verification code is 001234")]
        elif to == "+0087654321":
            return [MessageInstance("This message contains no verification code")]
        elif to == "+0088888888":
            return [MessageInstance("[Special code message pattern] Enter 888888 for verification")]
        else:
            return []

    mocker.patch("twilio.rest.api.v2010.account.message.MessageList.list", message_list)

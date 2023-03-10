import pytest

from cdc.qa.integrations import sms

from .mocks import *  # noqa:F401, F403


def test_twilio_instantiate(mock_twilio_secrets_manager):
    assert sms.Twilio()


@pytest.mark.parametrize(
    "phone_number, expected_code",
    [
        (12345678, "123456"),
        ("12345678", "123456"),
        ("+0012345678", "001234"),
    ],
)
def test_twilio_get_code_successful(mock_twilio_message_list, phone_number, expected_code):
    assert sms.Twilio().get_verification_code(phone_number=phone_number) == expected_code


def test_twilio_get_code_no_message(mock_twilio_message_list):
    with pytest.raises(ValueError) as excinfo:
        sms.Twilio().get_verification_code(phone_number="+0011112222")
    assert "No message found" in str(excinfo.value)


def test_twilio_get_code_no_code(mock_twilio_message_list):
    with pytest.raises(ValueError) as excinfo:
        sms.Twilio().get_verification_code(phone_number="+0087654321")
    assert "Verification code not found" in str(excinfo.value)


def test_twilio_get_code_custom_pattern(mock_twilio_message_list):
    assert (
        sms.Twilio().get_verification_code(
            phone_number="+0088888888",
            pattern=r".*Enter (\d+) for verification",
        )
        == "888888"
    )

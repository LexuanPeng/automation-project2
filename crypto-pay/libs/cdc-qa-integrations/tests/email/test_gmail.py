import pytest

from cdc.qa.integrations import email

from .mocks import *  # noqa:F401, F403


def test_gmail_instantiate(mock_gmail_credentials_refresh):
    assert email.Gmail()


@pytest.mark.parametrize(
    "to_addr, from_addr, subject, expected_content",
    [
        ("receiver1", None, None, "Test Content"),
        (None, "sender1", None, "Test Content"),
        (None, None, "Test", "Test Content"),
        (None, None, "Multipart", "HTML Content"),
    ],
)
def test_gmail_read_latest(mock_gmail_resource, to_addr, from_addr, subject, expected_content):
    message = email.Gmail().read_latest(to_addr=to_addr, from_addr=from_addr, subject=subject)
    assert message["content"] == expected_content


# TODO: write more tests (check unread/mark as read)

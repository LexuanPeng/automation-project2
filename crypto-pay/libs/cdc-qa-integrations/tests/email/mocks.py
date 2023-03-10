import pytest
from pytest_mock import MockerFixture

import base64


@pytest.fixture
def mock_gmail_secrets_manager(mocker: MockerFixture):
    mocker.patch(
        "cdc.qa.core.secretsmanager.get_secret_json",
        lambda x: {
            "REFRESH_TOKEN": "token",
            "CLIENT_ID": "id",
            "CLIENT_SECRET": "secret",
        },
    )


@pytest.fixture
def mock_gmail_credentials_refresh(mocker: MockerFixture, mock_gmail_secrets_manager):
    def refresh(self, *args, **kwargs):
        pass

    mocker.patch("google.oauth2.credentials.Credentials.refresh", refresh)


@pytest.fixture
def mock_gmail_resource(mocker: MockerFixture, mock_gmail_secrets_manager, mock_gmail_credentials_refresh):
    MESSAGES_LIST_RESULTS = {
        "to:'receiver1'": {
            "messages": [{"id": "00000001"}],
            "resultSizeEstimate": 1,
        },
        "from:'sender1'": {
            "messages": [{"id": "00000001"}],
            "resultSizeEstimate": 1,
        },
        "subject:'Test'": {
            "messages": [{"id": "00000001"}],
            "resultSizeEstimate": 1,
        },
        "subject:'Multipart'": {
            "messages": [{"id": "00000002"}],
            "resultSizeEstimate": 1,
        },
    }

    MESSAGES_GET_RESULTS = {
        "00000001": {
            "id": "00000001",
            "payload": {
                "headers": [
                    {"name": "To", "value": "receiver1@domain.com"},
                    {"name": "From", "value": "sender1@domain.com"},
                    {"name": "Subject", "value": "Test Email"},
                ],
                "mimeType": "text/html",
                "body": {
                    "data": base64.urlsafe_b64encode("Test Content".encode("utf-8")),
                },
            },
        },
        "00000002": {
            "id": "00000002",
            "payload": {
                "headers": [
                    {"name": "To", "value": "receiver2@domain.com"},
                    {"name": "From", "value": "sender2@domain.com"},
                    {"name": "Subject", "value": "Multipart Email"},
                ],
                "mimeType": "multipart/alternative",
                "body": {},
                "parts": [
                    {
                        "mimeType": "text/plain",
                        "body": {
                            "data": base64.urlsafe_b64encode("Plain Text Content".encode("utf-8")),
                        },
                    },
                    {
                        "mimeType": "text/html",
                        "body": {
                            "data": base64.urlsafe_b64encode("HTML Content".encode("utf-8")),
                        },
                    },
                ],
            },
        },
    }

    class Resource:
        def __init__(self, *args, **kwargs):
            pass

        def users(self):
            class User:
                def messages(self):
                    class Messages:
                        def list(self, q, labelIds, *args, **kwargs):
                            class List:
                                def execute(self) -> dict:
                                    return MESSAGES_LIST_RESULTS.get(q, {"resultSizeEstimate": 0})

                            return List()

                        def get(self, id, *args, **kwargs):
                            class Get:
                                def execute(self) -> dict:
                                    return MESSAGES_GET_RESULTS.get(id, {})

                            return Get()

                        def modify(self, *args, **kwargs):
                            class Modify:
                                def execute(self):
                                    return

                            return Modify()

                    return Messages()

            return User()

    mocker.patch("googleapiclient.discovery.Resource", Resource)

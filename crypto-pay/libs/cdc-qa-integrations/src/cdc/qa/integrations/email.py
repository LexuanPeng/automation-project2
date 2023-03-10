from googleapiclient.discovery import build, Resource
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from cdc.qa.core import secretsmanager as sm

import logging
from typing import Optional
import base64
from retry import retry

logger = logging.getLogger(__name__)


class Gmail:
    def __init__(
        self,
        refresh_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        self.creds = Credentials(
            token=None,
            refresh_token=refresh_token or sm.get_secret_json("gmail")["REFRESH_TOKEN"],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id or sm.get_secret_json("gmail")["CLIENT_ID"],
            client_secret=client_secret or sm.get_secret_json("gmail")["CLIENT_SECRET"],
        )
        self.service: Resource
        self.refresh()

    def refresh(self):
        """Refresh the credentials and gmail service."""
        self.creds.refresh(Request())
        self.service = build("gmail", "v1", credentials=self.creds)

    @retry(ValueError, delay=1, tries=10)
    def read_latest(
        self,
        to_addr: str = "",
        from_addr: str = "",
        subject: str = "",
        is_unread: bool = True,
        mark_read: bool = True,
    ) -> dict:
        """Read the latest email matching the given arguments.

        Args:
            to_addr (str, optional): The address this email is sent to. Defaults to "".
            from_addr (str, optional): The address this email is sent from. Defaults to "".
            subject (str, optional): The subject of this email. Defaults to "".
            is_unread (bool, optional): Whether this email is unread or not. Defaults to True.
            mark_read (bool, optional): Should this email be marked as read after reading it. Defaults to True.

        Raises:
            ValueError: [description]

        Returns:
            dict: [description]
        """
        self.refresh()

        # construct query
        queries = []
        if to_addr:
            to_addr = to_addr.split("@")[0]  # removing the domain part of the email for more lenient match
            queries.append(f"to:'{to_addr}'")
        if from_addr:
            queries.append(f"from:'{from_addr}'")
        if subject:
            queries.append(f"subject:'{subject}'")
        query = " ".join(queries)

        # construct labels
        labels = []
        if is_unread:
            labels.append("UNREAD")

        # search email with query and labels
        messages_list_result = (
            self.service.users()  # type:ignore
            .messages()
            .list(userId="me", q=query, labelIds=labels, maxResults=1)
            .execute()
        )
        logger.debug(f"{messages_list_result['resultSizeEstimate']=}")

        if "messages" in messages_list_result:
            message = messages_list_result["messages"][0]
            logger.debug(f"{message['id']=}")

            # get email
            messages_get_result = (
                self.service.users()  # type:ignore
                .messages()
                .get(userId="me", id=message["id"])
                .execute()
            )
            payload = messages_get_result["payload"]

            headers = payload["headers"]
            mime_type = payload["mimeType"]
            if "multipart" in mime_type:
                parts = payload["parts"]
                body = next(part for part in parts if part["mimeType"] == "text/html")["body"]
            else:
                body = payload["body"]

            _id = messages_get_result["id"]
            _to = next(header for header in headers if header["name"] == "To")["value"]
            _from = next(header for header in headers if header["name"] == "From")["value"]
            _subject = next(header for header in headers if header["name"] == "Subject")["value"]
            _content = str(base64.urlsafe_b64decode(body["data"]), "utf-8")

            # mark email as read (removing "UNREAD" label)
            if mark_read:
                (
                    self.service.users()  # type:ignore
                    .messages()
                    .modify(userId="me", id=message["id"], body={"removeLabelIds": "UNREAD"})
                    .execute()
                )

            return {
                "id": _id,
                "to": _to,
                "from": _from,
                "subject": _subject,
                "content": _content,
            }

        else:
            raise ValueError(f"No message found: {to_addr=}, {from_addr=}, {subject=}, {is_unread=}")

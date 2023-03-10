import logging
import threading
import time
import secrets
from typing import Callable, Optional

import websocket

logger = logging.getLogger(__name__)


class WebSocketClient:
    def __init__(self, host: str):
        self._host: str = host
        self._id: str = secrets.token_hex(8)
        self._alias: Optional[str] = None
        self._ws: Optional[websocket.WebSocketApp] = None

        self._recv_messages: list = []
        self._sent_messages: list = []

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()

    @property
    def tag(self) -> str:
        tag = f"{self._host} <{self._id}>"
        if self._alias:
            tag += f"({self._alias})"
        return tag

    def connect(self, alias: Optional[str] = None):
        if not self._ws:
            self._alias = alias
            self._ws = websocket.WebSocketApp(
                url=self._host,
                on_open=self._on_open,
                on_message=self._on_message,
                on_close=self._on_close,
            )
            thread = threading.Thread(target=self._ws.run_forever)
            thread.daemon = True
            thread.start()
            time.sleep(3)
        else:
            logger.warning("An active WebSocket connection is already established.")

    def is_connected(self) -> bool:
        return self._ws is not None

    def disconnect(self):
        if self._ws:
            self._ws.close()
            self._alias = None
        else:
            logger.warning("No active WebSocket connection established.")

    def _on_open(self, ws):
        logger.debug(f"[WebSocket] {self.tag} connected.")

    def _on_message(self, ws, message):
        logger.debug(f"[WebSocket] {self.tag} message received: {message}")
        self._recv_messages.append(message)

    def _on_close(self, ws, close_status_code, close_msg):
        logger.debug(f"[WebSocket] {self.tag} closed.")
        self._ws = None

    def send(self, message: str):
        if self._ws:
            self._ws.send(data=message)
            self._sent_messages.append(message)
            logger.debug(f"[WebSocket] {self.tag} message sent: {message}")
        else:
            logger.warning(f"No active [WebSocket] {self.tag} connection established.")

    def clear(self):
        self._recv_messages = []
        self._sent_messages = []

    def expect_messages(
        self,
        matcher: Callable[..., bool],
        count: int = 1,
        timeout: int = 10,
        interval: int = 1,
    ) -> list:
        """Expect to receive one or more filtered messages.

        Args:
            matcher (Callable): A matcher function used to filter the received messages.
            count (int, optional): Number of messages to be expected before timeout. Defaults to 1.
            timeout (int, optional): Timeout in seconds. Defaults to 10.
            interval (int, optional): Interval in seconds. Defaults to 1.

        Returns:
            list: A list of messages filtered by the matcher.
        """

        deadline: float = time.time() + timeout
        result: list = []  # messages filtered by the matcher
        seen: list = []  # messages already seen by the matcher to be excluded from further matching

        while time.time() < deadline:
            snapshot: list = [*self._recv_messages]

            for element in seen:
                if element in snapshot:
                    snapshot.remove(element)

            result.extend(filter(matcher, snapshot))
            if len(result) >= count:
                break

            seen.extend(snapshot)
            time.sleep(interval)

        if len(result) < count:
            logger.warning(
                f"({self.tag}) Expected to receive {count} messages, but received only {len(result)} messages."
            )

        return result

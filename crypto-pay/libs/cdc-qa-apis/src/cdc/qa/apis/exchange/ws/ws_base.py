from dataclasses import dataclass, field

from cdc.qa.apis.common.models.ws_client import WebSocketClient
from cdc.qa.apis.common.services.ws_service import WsService

from ..models import ExchangeResponse
from .models import RespondHeartbeatRequest, SubscribeResponse
from typing import Optional


class ExchangeWebSocketClient(WebSocketClient):
    def __init__(
        self,
        host: str,
        heartbeat_auto_respond: bool = True,
        heartbeat_save_message: bool = False,
    ):
        super().__init__(host)
        self._heartbeat_auto_respond: bool = heartbeat_auto_respond
        self._heartbeat_save_message: bool = heartbeat_save_message

    def _on_message(self, ws, message):
        super()._on_message(ws, message)
        response = ExchangeResponse.parse_raw(b=message)

        # Handle heartbeat
        if response.method == "public/heartbeat":
            if self._heartbeat_auto_respond:
                request = RespondHeartbeatRequest(id=response.id)
                self.send(request.json(exclude_none=True))
            if not self._heartbeat_save_message:
                self._recv_messages.remove(message)

    def get_messages(self, method: str, *args, **kwargs) -> list:
        """Get messages filtered by method name."""
        return self.expect_messages(
            lambda message: ExchangeResponse.parse_raw(b=message).method == method,
            *args,
            **kwargs,
        )

    def get_subscription_messages(self, subscription: str, *args, **kwargs) -> list:
        """Get messages filtered by subscription name."""

        def matcher(message):
            resp = ExchangeResponse.parse_raw(b=message)
            if resp.method == "subscribe" and resp.result:
                try:
                    return SubscribeResponse.parse_raw(b=message).result.subscription == subscription
                except AttributeError:
                    return False
            return False

        return self.expect_messages(matcher, *args, **kwargs)


@dataclass(frozen=True)
class ExchangeWsService(WsService):
    client: Optional[ExchangeWebSocketClient] = field(default=None)
    _api_key: str = field(default="")
    _secret_key: str = field(default="")

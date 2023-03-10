from dataclasses import dataclass, field
from typing import Optional
from ..models.ws_client import WebSocketClient


@dataclass(frozen=True)
class WsService:
    client: Optional[WebSocketClient] = field(default=None)

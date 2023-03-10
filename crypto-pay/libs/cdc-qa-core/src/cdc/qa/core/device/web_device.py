import logging

from .device import Device
from ..enums import Platform, Agent

logger = logging.getLogger(__name__)


class WebDevice(Device):
    """A `Device` which is used with `WebApp`."""

    def __init__(
        self,
        *args,
        agent: str,
        platform: str,
        host: str = "",
        capabilities: dict = {},
        options: dict = {},
        **kwargs,
    ):
        self.agent: Agent = Agent(agent)
        self.platform: Platform = Platform(platform)
        self.host: str = host
        self.capabilities: dict = capabilities
        self.options: dict = options

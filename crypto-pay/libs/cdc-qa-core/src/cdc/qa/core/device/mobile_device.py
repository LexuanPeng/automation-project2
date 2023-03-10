import logging
from typing import Optional

from .device import Device
from ..enums import Platform, Agent

from appium.webdriver.webdriver import WebDriver

logger = logging.getLogger(__name__)


class MobileDevice(Device):
    """A `Device` which is used with `MobileApp`.

    Attributes:
        driver (WebDriver): Driver of this device.
        agent (str): `Agent` of this device.
        platform (str): `Platform` of this device.
        platform_version (str): Version of the `Platform`.
        locale (str): Locale of the device.
        host (str): Host for the driver to connect to, e.g. http://localhost:4723/wd/hub
        capabilities (dict): [description]. Defaults to {}.
        proxy (dict): Proxy config used by `ProxyHelper`.
        device_udid (str): UDID of the device.
        device_name (str): Name of the device.
        device_model (str): Model of the device.
    """

    def __init__(
        self,
        *args,
        agent: str,
        platform: str,
        platform_version: str,
        locale: str,
        host: str = "",
        capabilities: dict = {},
        options: dict = {},
        proxy: dict = {},
        device_udid: Optional[str] = None,
        device_name: Optional[str] = None,
        device_model: Optional[str] = None,
        **kwargs,
    ):
        """Inits MobileDevice.

        Args:
            agent (str): `Agent` of this device.
            platform (str): `Platform` of this device.
            platform_version (str): Version of the `Platform`.
            locale (str): Locale of the device.
            host (str, optional): Host for the driver to connect to, e.g. http://localhost:4723/wd/hub
                Has no effect when `agent` is `BROWSERSTACK`. Defaults to None.
            capabilities (dict, optional): [description]. Defaults to {}.
            proxy (dict, optional): Proxy config used by `ProxyHelper`. Defaults to {}.
            device_udid (str, optional): UDID of the device. Defaults to None.
            device_name (str, optional): Name of the device. Defaults to None.
            device_model (str, optional): Model of the device. Defaults to None.
        """
        self.agent: Agent = Agent(agent)
        self.platform: Platform = Platform(platform)
        self.platform_version: str = str(platform_version)
        self.locale: str = locale
        self.host: str = host
        self.capabilities: dict = capabilities
        self.options: dict = options
        self.proxy: dict = proxy

        self.udid: Optional[str] = device_udid
        self.name: Optional[str] = device_name
        self.model: Optional[str] = device_model

    def update_from_driver(self, driver: WebDriver):
        """Update the attributes of this device by getting a new driver and update from it.

        Will quit the driver after performing this operation.
        """
        session = driver.session
        logger.debug(f"Driver session is: {session}")

        # Special mapping for specific attributes
        if "platformName" in session and session["platformName"] == "android":
            session["deviceName"] = session["desired"]["deviceName"]
        if "udid" in session and "deviceUDID" not in session:
            session["deviceUDID"] = session["udid"]
        if "proxyType" in session:
            session["proxy"] = {}
            session["proxy"]["type"] = session["proxyType"]
            if "proxyPort" in session:
                session["proxy"]["port"] = session["proxyPort"]
            if "proxyHubUrl" in session:
                session["proxy"]["hub_url"] = session["proxyHubUrl"]

        # Update attributes
        attr_mapping = {
            "platformVersion": "platform_version",
            "deviceName": "name",
            "deviceUDID": "udid",
            "deviceModel": "model",
            "proxy": "proxy",
        }
        for key, attr in attr_mapping.items():
            if key in session:
                setattr(self, attr, session[key])
                logger.debug(f"Updating attribute [{key}] to value: {session[key]}")

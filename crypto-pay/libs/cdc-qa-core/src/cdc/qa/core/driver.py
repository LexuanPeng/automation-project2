from typing import Optional

import os
import logging

from .app import App, MobileApp, WebApp
from .device import Device, MobileDevice, WebDevice
from .enums import Agent, Platform

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome, DesiredCapabilities, Safari
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


def get_driver(
    app: Optional[App],
    device: Device,
    sonic_cloud_uuid_key: Optional[str] = None,
    ios_sonic_cloud_screen_recording: bool = False,
    **kwargs,
) -> WebDriver:
    if (isinstance(app, MobileApp) or app is None) and isinstance(device, MobileDevice):
        return _mobile_get_driver(app, device, sonic_cloud_uuid_key, ios_sonic_cloud_screen_recording, **kwargs)
    elif (isinstance(app, WebApp) or app is None) and isinstance(device, WebDevice):
        return _web_get_driver(app, device, **kwargs)
    else:
        raise ValueError("App and Device type mismatched.", app, device)


def _mobile_get_driver(
    app: Optional[MobileApp],
    device: MobileDevice,
    sonic_cloud_uuid_key: Optional[str] = None,
    ios_sonic_cloud_screen_recording: bool = False,
    **kwargs,
) -> AppiumWebDriver:
    """Get a driver for this `Device`.

    Each `Device` can only have one driver running. Getting a new driver will quit the last driver.

    Args:
        app (MobileApp, optional): The app this driver runs.
        sonic_cloud_uuid_key(str, optional): Uuid key for calling sonic key api, this key is required when getting a
        driver with sonic server host
        ios_sonic_cloud_screen_recording(bool): If set as True, screen mirroring can be shown on Sonic Cloud. However,
        test execution speed would be slower when screen recording is on.
        **kwargs: Other arguments to override capabilities.

    Raises:
        ValueError: Raised when `agent` is not `LOCAL`, `REMOTE` or `BROWSERSTACK`.

    Returns:
        WebDriver: The driver.
    """
    # App and device platform sanity check
    if app and app.platform is not device.platform:
        raise ValueError(
            "App platform and Device Platform mismatched.",
            app.platform,
            device.platform,
        )

    # Resolve host
    if device.agent in (Agent.LOCAL, Agent.REMOTE):
        host = device.host
    elif device.agent is Agent.BROWSERSTACK:
        raise NotImplementedError
    else:
        raise ValueError

    # Construct capabilities
    capabilities = {
        "platformName": "Android" if device.platform is Platform.ANDROID else "iOS",
        "platformVersion": device.platform_version,
    }
    if app:
        if device.agent is Agent.LOCAL:
            capabilities["app"] = app.app_path
        elif device.agent is Agent.REMOTE:
            if not sonic_cloud_uuid_key:
                raise ValueError("Sonic cloud uuid key must be provided when running remote devices.")

            # Should be switched to app server when it is done
            capabilities["app"] = app.app_path
            capabilities["uuid_key"] = sonic_cloud_uuid_key

            if not ios_sonic_cloud_screen_recording:
                device.capabilities["mjpegServerPort"] = None

        elif device.agent is Agent.BROWSERSTACK:
            # TODO: Implement this
            raise NotImplementedError
    if device.udid:
        capabilities["udid"] = device.udid
    if device.name:
        capabilities["deviceName"] = device.name
    if device.model:
        capabilities["deviceModel"] = device.model
    capabilities = {**capabilities, **device.capabilities, **kwargs}
    logger.debug(f"Capabilities are set to: {capabilities}")

    appium_web_driver = AppiumWebDriver(host, capabilities)

    if device.platform is Platform.IOS and device.agent is Agent.REMOTE and ios_sonic_cloud_screen_recording:
        logging.debug("Start recording screen for sonic cloud.")
        appium_web_driver.start_recording_screen()

    return appium_web_driver


def _web_get_driver(app: Optional[WebApp], device: WebDevice, **kwargs) -> WebDriver:
    """Get a driver for the given `Device`.

    Args:
        app:
        device:
        **kwargs: Other arguments to override capabilities.

    Raises:
        ValueError: Raised when `agent` is not `LOCAL` or `REMOTE`.

    Returns:
        WebDriver: The driver.
    """
    driver: WebDriver

    def _get_driver_web_local(app: Optional[App], device: WebDevice, **kwargs) -> WebDriver:
        """
        chrome options example below:
        device.option: {
            "goog:chromeOptions": {
                "prefs" : {
                    "profile.default_content_setting_values.automatic_downloads": "1"
                }
            },
            "goog:chromeArguments": ["----start-maximized","--disable-popup-blocking"]
        }
        """
        os.environ["WDM_LOG_LEVEL"] = str(logging.WARNING)
        if device.platform is Platform.FIREFOX:
            raise NotImplementedError
        elif device.platform is Platform.SAFARI:
            return Safari()
        elif device.platform is Platform.CHROME:
            chrome_options = Options()
            if "goog:chromeOptions" in device.options.keys():
                for k, v in device.options["goog:chromeOptions"].items():
                    chrome_options.add_experimental_option(k, v)
            if "goog:chromeArguments" in device.options.keys():
                for v in device.options["goog:chromeArguments"]:
                    chrome_options.add_argument(v)
            if "goog:chromeExtensions" in device.options.keys():
                for v in device.options["goog:chromeExtensions"]:
                    chrome_options.add_extension(v)
            return Chrome(
                ChromeDriverManager().install(),
                options=chrome_options,
            )
        else:
            raise ValueError(f"Unhandled device platform '{device.platform}'.")

    def _get_driver_web_remote(
        app: Optional[App],
        device: WebDevice,
        *,
        implicit_wait: int = 3,
        maximize_window: bool = True,
        **kwargs,
    ) -> WebDriver:
        # Construct capabilities
        if device.platform is Platform.FIREFOX:
            capabilities = DesiredCapabilities.FIREFOX.copy()
        elif device.platform is Platform.SAFARI:
            capabilities = DesiredCapabilities.SAFARI.copy()
        elif device.platform is Platform.CHROME:
            capabilities = DesiredCapabilities.CHROME.copy()
            chrome_options = Options()
            if "goog:chromeOptions" in device.options.keys():
                for k, v in device.options["goog:chromeOptions"].items():
                    chrome_options.add_experimental_option(k, v)
            if "goog:chromeArguments" in device.options.keys():
                for v in device.options["goog:chromeArguments"]:
                    chrome_options.add_argument(v)
            if "goog:chromeExtensions" in device.options.keys():
                for v in device.options["goog:chromeExtensions"]:
                    chrome_options.add_extension(v)
            capabilities.update(chrome_options.to_capabilities())
        else:
            raise ValueError(f"Unhandled device platform '{device.platform}'.")
        capabilities = {**capabilities, **device.capabilities, **kwargs}
        logger.debug(f"Capabilities are set to: {capabilities}")

        # Create driver
        remote_driver = WebDriver(command_executor=device.host, desired_capabilities=capabilities)
        logging.info(f"Created remote web driver: {device.host}")

        # Driver setup
        remote_driver.implicitly_wait(implicit_wait)
        if maximize_window:
            remote_driver.maximize_window()

        return remote_driver

    # Resolve agent
    if device.agent is Agent.LOCAL:
        driver = _get_driver_web_local(app, device, **kwargs)
    elif device.agent is Agent.REMOTE:
        driver = _get_driver_web_remote(app, device, **kwargs)
    else:
        raise ValueError("'agent' in the given device is not 'LOCAL' or 'REMOTE'.")

    return driver

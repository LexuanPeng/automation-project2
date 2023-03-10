import os
import yaml
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional
from _pytest.fixtures import fixture, FixtureRequest
from selenium.common.exceptions import ScreenshotException
from selenium.webdriver.remote.webdriver import WebDriver
from cdc.qa.integrations import Qase

logger = logging.getLogger(__name__)
lock = threading.Lock()


@fixture(scope="session", autouse=True)
def global_data(request: FixtureRequest):
    # Create a global cache data
    g = dict()
    g["project_code"] = "PCO"

    return g


@fixture(scope="session", autouse=True)
def take_screenshot(request: FixtureRequest, global_data: dict):
    report_path: str = os.environ.get("report_path")
    screenshot_folder_path = Path.cwd() / report_path / "screenshots"
    screenshot_folder_path.mkdir(parents=True, exist_ok=True)
    env = request.config.getoption("env")

    def screenshot(case_id: str, suffix: str = "") -> Optional[str]:
        screenshot_result = None

        try:
            test_name = os.environ.get("PYTEST_CURRENT_TEST")
            driver: WebDriver = global_data[test_name]["driver"]
            png = driver.get_screenshot_as_png()

            time_prefix = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f'{env}_{case_id}_{time_prefix}{"_" if suffix else ""}{suffix}.png'
            screenshot_path = screenshot_folder_path / filename
            with screenshot_path.open("wb") as f:
                f.write(png)
            screenshot_result = str(screenshot_path)

        except (ScreenshotException, IOError) as e:
            logger.exception(e)
        finally:
            if "png" in locals():
                del png

        return screenshot_result

    return screenshot


@fixture(scope="session")
def qase(request: FixtureRequest, global_data: dict):
    try:
        push_qase = request.config.getoption("qase")
        if push_qase != "false":
            tag = os.environ["tag"]
            qase_config = yaml.safe_load(open("configs/qase_planning.yaml")).get(tag)
            qa_access_token = os.environ.get("QASE_ACCESS_TOKEN", "")

            with lock:
                test_run_id = request.config.getoption("qase_test_run_id")
                test_run_id = None if test_run_id == "NONE" else test_run_id
                qase = Qase(qa_access_token, **qase_config, test_run_id=test_run_id)

                if not test_run_id:
                    env = request.config.getoption("env")
                    build_url = os.environ.get("BUILD_URL", "Local")
                    title = f"Automation {tag.title()} {env.title()}_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    test_run_id = qase.create_test_run(title=title, description=f"JENKINS_DATA|WEB_TEST|{build_url}")
                    request.config.option.__setattr__("qase_test_run_id", test_run_id)
                logger.info(f"Qase test run id: {test_run_id}")
            return qase
        else:
            return None
    except BaseException as e:
        logger.error(f"【Something went wrong while creating Qase fixture】: {str(e)}")
        raise e

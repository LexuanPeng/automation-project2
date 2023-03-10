import time
from logging.config import dictConfig

from common.api import Apis
from common.fixture import *  # noqa
from pathlib import Path
import yaml
import logging
import os
import threading
from _pytest.fixtures import FixtureRequest
from common.single_items import FailedSaver, RailsSaver
from cdc.qa.core import WebDevice, get_driver, MobileDevice, WebApp
from cdc.qa.integrations import Qase
from pytest_bdd.parser import Feature, Step, Scenario
from pytest_bdd.reporting import ScenarioReport, StepReport
from selenium.webdriver.remote.webdriver import WebDriver
from appium.webdriver.webdriver import WebDriver as MobileDriver
from common.utils.tools import Tools
from pages import SuperPages

logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("botocore").setLevel(logging.CRITICAL)

LOGGING_CONFIG_PATH = "configs/logging.yaml"
logging_config_dict = yaml.safe_load(open(LOGGING_CONFIG_PATH))
LOG_LEVEL = os.environ.get("LOG_LEVEL")
logging_config_dict["handlers"]["Console"]["level"] = LOG_LEVEL
dictConfig(logging_config_dict)

logger = logging.getLogger(__name__)

lock = threading.Lock()


# Hooks
def pytest_bdd_before_scenario(request: FixtureRequest, feature: Feature, scenario: Scenario):
    push_qase = request.config.getoption("qase")
    # 获取pytest命令行env的参数值
    env = request.config.getoption("env")
    # common->fixture->__init__.py 下有一个名为global_data的fixture。已导入该包
    global_data = request.getfixturevalue("global_data")
    # pytest自带的环境变量，pytest会在运行测试的时候，给PYTEST_CURRENT_TEST环境变量赋值xx.py::scenario (xx)
    # 例如：'test_cases/staging/test_smoke.py::test_login__login_successful (call)'
    test_name = os.environ.get("PYTEST_CURRENT_TEST")
    global_data[test_name] = dict()
    report_path = Path.cwd() / os.environ.get("report_path")

    try:
        # 设置一个 名为enable_headless 的环境变量
        enable_headless = os.environ.get("enable_headless", "true")
        # 无头模式，后台运行模式
        headless = "false"
        # 无痕浏览模式
        incognito = "false"

        platform = "web"  # default web
        browser = "chrome"  # default chrome
        tags = scenario.tags
        case_id = "PCO-Unknown"

        for tag in tags:
            if "platform" in tag:
                platform = tag.split(":")[1]
            if "browser" in tag:
                browser = tag.split(":")[1]
            if "PCO" in tag:
                case_id = tag
            if "headless" in tag and enable_headless == "true":
                headless = "true"
            if "incognito" in tag:
                incognito = "true"

        # title(): 将每个单词的首字母大写，比如 web -> Web
        threading.current_thread().setName(f"{case_id}_{env.title()}_{platform.title()}_{browser.title()}")
        if push_qase != "false":
            qase: Qase = request.getfixturevalue("qase")
            time.sleep(1)
            qase.start_test_case(qase_id=case_id)
            global_data[test_name]["qase"] = qase

        # 获取测试数据
        feature_data: str = feature.name.lower()
        feature_name: str = feature_data.split("_")[0]
        data_env = os.environ.get("data_env")
        t = yaml.safe_load(open(f"test_resource/data/{data_env}/{feature_name}/{feature_data}_data.yaml"))

        if case_id not in t.keys():
            t[case_id] = dict()

        # 给每一条测试用例增加host地址
        t[case_id]["global_host"] = os.environ["global_host"]
        t[case_id]["api_host"] = os.environ["api_host"]
        t[case_id]["global_ops_host"] = os.environ["global_ops_host"]
        # 给每一条运行的scenario，增加对应的测试信息
        global_data[test_name].update({"case_id": case_id, "test_data": t[case_id], "env": env})

        host = f"http://{request.config.getoption('--host_port')}/wd/hub"
        apis = Apis()

        if platform == "web":
            web_app = WebApp(base_url="", paths={})
            options = {}
            if browser == "chrome":
                options = {
                    "goog:chromeOptions": {
                        "prefs": {
                            "profile.default_content_settings.popups": 0,
                            "profile.default_content_setting_values.automatic_downloads": 1,
                            "download.prompt_for_download": False,
                            "download.directory_upgrade": True,
                            "plugins.always_open_pdf_externally": True,
                        }
                    },
                    "goog:chromeArguments": ["--host-resolver-rules=MAP www.googletagmanager.com 127.0.0.1"],
                }
                if headless == "true":
                    options["goog:chromeArguments"].extend(["--headless", "--window-size=1920,1080"])
                if incognito == "true":
                    options["goog:chromeArguments"].extend(["--incognito"])

            web_device = WebDevice(agent="local", platform=browser, host=host, options=options)
            try:
                driver: WebDriver = get_driver(app=None, device=web_device, implicit_wait=8)
            except Exception as e:
                e = Exception(f"【Failed to init the webdriver】: {str(e)}")
                raise e
            p = SuperPages(driver=driver, device=web_device, env=env, test_data=t[case_id], app=web_app, apis=apis)
            # 每一个 Python 中的 实例对象 中，都有一个内置的 __getattribute__ 函数。当我们访问一个实例属性时，会自动调用 __getattribute__ 函数。
            # p是superPages实例对象。所以这个地方相当于 superPages.staging_web_pages =StgWebPages()。而StgWebPages()就是Pages类。
            # 所以这块相当于pages就是Pages类的实例化对象,且其实例化与p传的参数一致
            pages = p.__getattribute__(f"{env}_{platform}_pages")
        else:
            #  TODO: Will update mobile-driver if we need support mobile test
            mobile_device = MobileDevice(agent="remote", platform=browser, host=host, locale="", platform_version="")
            driver: MobileDriver = get_driver(app=None, device=mobile_device)
            pages = SuperPages(driver=driver, device=mobile_device, env=env, test_data=t[case_id], app=None)

        temp = {"driver": driver, "pages": pages, "apis": apis}
        global_data[test_name].update(temp)

        if "main_app_email" in t[case_id].keys():
            r = RailsSaver()
            t[case_id]["rails_helper"] = r.rails
            logger.info(f"【Get rails helper from RailsSaver to case {case_id}】: {t[case_id]['rails_helper']}")

        if "from_address" in t[case_id].keys():
            from_address_pk_key = os.environ.get(t[case_id]["from_address"], None)
            if from_address_pk_key is None:
                logger.info(
                    f"【Get from_address_pk_key for {t[case_id]['from_address']} from QA TOOL Failed】: "
                    f"Make Sure you put the correct wallet address and pk key in QA TOOL"
                )
            t[case_id]["from_address_pk_key"] = from_address_pk_key

    except BaseException as e:
        error_log = f"【Something went wrong while running before hook】: {str(e)}"
        logger.error(error_log)

        qase = global_data[test_name].get("qase", None)
        if push_qase != "false" and qase is not None:
            qase.end_test_case(status=qase.STATUS.FAILED, time_ms=1000, comment=error_log)
            global_data[test_name]["qase"] = None

        driver = global_data[test_name].get("driver", None)
        if driver is not None:
            driver.quit()

        case_id = global_data[test_name].get("case_id", None)
        if case_id is not None:
            f = FailedSaver()
            if push_qase != "false":
                f.add(case_id, qase.test_run_id)
            else:
                f.add(case_id)
            f.write(report_path / "failed_cases.yml")

        raise e


def pytest_bdd_after_scenario(request: FixtureRequest, feature: Feature, scenario: Scenario):
    push_qase = request.config.getoption("qase")
    global_data = request.getfixturevalue("global_data")

    test_name = os.environ.get("PYTEST_CURRENT_TEST")
    case_id = global_data[test_name].get("case_id", None)
    if case_id is None:
        raise Exception(f"【Current {scenario.name} was not started indeed】")
    report_path = Path.cwd() / os.environ.get("report_path")
    # scenario.failed默认值为false,判断测试场景是否失败
    status = scenario.failed
    test_data = global_data[test_name]["test_data"]

    try:
        driver = global_data[test_name].get("driver", None)
        if driver is not None:
            driver.quit()

        if push_qase != "false":
            qase: Qase = global_data[test_name]["qase"]
            scenario_report: ScenarioReport = getattr(request.node, "__scenario_report__")
            step_reports: list[StepReport] = scenario_report.step_reports
            time_ms = int(sum(step_report.duration for step_report in step_reports) * 1000)
            scenario_status = qase.STATUS.FAILED if status else qase.STATUS.PASSED
            sensitive_key_list = ["pk_key", "secret_key", "password", "token", "two_fa_token", "ops_token"]
            t_s = ""
            for k, v in test_data.items():
                if k in sensitive_key_list:
                    pass
                else:
                    t_s = f"{t_s}{k}: {v}\n"
            comment = f"Test data: \n{t_s}"
            qase.end_test_case(status=scenario_status, time_ms=time_ms, comment=comment)

    except BaseException as e:
        status = True
        error_log = f"【Something went wrong while running after hook】: {str(e)}"
        logger.error(error_log)
        qase = global_data[test_name].get("qase", None)
        if push_qase != "false" and qase is not None:
            qase.end_test_case(status=qase.STATUS.FAILED, time_ms=1000, comment=error_log)

        driver = global_data[test_name].get("driver", None)
        if driver is not None:
            driver.quit()
        raise e
    finally:
        if status:
            f = FailedSaver()
            if push_qase != "false":
                qase = global_data[test_name].get("qase", None)
                f.add(case_id, qase.test_run_id)
            else:
                f.add(case_id)
            f.write(report_path / "failed_cases.yml")
        try:
            user_name = test_data.get("user_name", None)
            password = test_data.get("password", None)
            team_id = test_data.get("team_id", None)
            apis = global_data[test_name].get("apis", None)
            if user_name is not None and password is not None and team_id is not None:
                payout_accounts = apis.payment.get_payout_account_id_by_team_id(user_name, password, team_id)
                filtered_payout_account = list(filter(lambda x: x["mode"] == "auto", payout_accounts))
                if len(filtered_payout_account) > 0:
                    for payout_account in filtered_payout_account:
                        payout_account_id = payout_account["id"]
                        payout_account_address = payout_account["address"]
                        address_type_map = {"USD": "fiat_usd", "AUD": "fiat_aud"}
                        payout_account_currency = payout_account["currency"]
                        if payout_account_currency in ["USD", "AUD"]:
                            apis.payment.update_payout_account_info(
                                user_name=user_name,
                                password=password,
                                payout_account_id=payout_account_id,
                                address=payout_account_address,
                                mode="manual",
                                address_type=address_type_map[payout_account_currency],
                                usd_account=True,
                            )
                        else:
                            apis.payment.update_payout_account_info(
                                user_name, password, payout_account_id, payout_account_address, "manual"
                            )
        except Exception as e:
            logger.warning(f"【Ignore update merchant payout to manual error】: {e}")


def pytest_bdd_after_step(
    request: FixtureRequest, feature: Feature, scenario: Scenario, step: Step, step_func, step_func_args
):
    push_qase = request.config.getoption("qase")
    logger.info(f"【{step.name}】- Passed")
    if push_qase != "false":
        global_data = request.getfixturevalue("global_data")
        test_name = os.environ.get("PYTEST_CURRENT_TEST")
        qase: Qase = global_data[test_name]["qase"]
        test_data = global_data[test_name]["test_data"]
        step_name = Tools.convert_text_from_dict(step.name, test_data)

        # position = 1 + len(qase._test_run_result_steps)
        # step_info = {
        #     "position": position,
        #     "status": qase.STATUS.PASSED.value,
        #     "comment": step_name,
        # }
        # step = ResultUpdateSteps(**step_info)
        # qase._test_run_result_steps.append(step)
        qase.end_test_step(status=qase.STATUS.PASSED, comment=step_name, update_to_qase=False)


def pytest_bdd_step_error(
    request: FixtureRequest, feature: Feature, scenario: Scenario, step: Step, step_func, step_func_args, exception
):
    push_qase = request.config.getoption("qase")
    global_data = request.getfixturevalue("global_data")
    test_name = os.environ.get("PYTEST_CURRENT_TEST")
    case_id = global_data[test_name]["case_id"]

    take_screenshot = request.getfixturevalue("take_screenshot")
    screenshot_path = take_screenshot(case_id, suffix="ERROR")

    scenario.failed = True
    logger.error(f"【{step.name}】- Error: {repr(exception)}")
    if push_qase != "false":
        qase: Qase = global_data[test_name]["qase"]
        test_data = global_data[test_name]["test_data"]
        step_name = Tools.convert_text_from_dict(step.name, test_data)

        # position = 1 + len(qase._test_run_result_steps)
        # step_info = {
        #     "position": position,
        #     "status": qase.STATUS.FAILED.value,
        #     "comment": f"{step_name}, Error:\n{repr(exception)}",
        # }
        # step_with_attachment = ResultUpdateSteps(**step_info, attachments=qase._upload_attachments([screenshot_path]))
        qase.end_test_step(
            status=qase.STATUS.FAILED,
            comment=f"{step_name}, Error:\n{repr(exception)}",
            attachment_paths=[screenshot_path],
            update_to_qase=True,
        )
        # qase._test_run_result_steps.append(step_with_attachment)

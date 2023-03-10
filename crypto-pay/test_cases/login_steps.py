import os
import logging
from datetime import datetime
from decimal import Decimal

from pytest import fixture
from pytest_bdd import when, then, parsers

from common.utils.gmail_helper import GmailHelper
from common.utils.tools import Tools

logger = logging.getLogger(__name__)


@fixture(scope="module")
def login_test_data(global_data):
    current_test = os.environ.get("PYTEST_CURRENT_TEST")
    pages = global_data[current_test]["pages"]
    ops_token = os.environ.get("OPS_TOKEN")
    admin_token = os.environ.get("ADMIN_TOKEN")

    t = {"pages": pages, "ops_token": ops_token, "admin_token": admin_token}

    yield t


@when(parsers.parse("I go to {url} page"))
def go_login_page(url: str, login_test_data: dict):
    pages = login_test_data["pages"]
    pages.login_page.navigate_to_login_home(url)


@when(parsers.parse("I login with correct {user_name} and {password}"))
def input_user_password(user_name: str, password: str, login_test_data: dict):
    pages = login_test_data["pages"]
    pages.login_page.login_by_user_pwd(user_name, password)
    # pages.login_page.confirm_tc_layout()


@then(parsers.parse("I should login successful"))
def login_success(login_test_data: dict):
    pages = login_test_data["pages"]
    pages.login_page.verify_success_after_login()

# # 通常会把这个function作为公共步骤提取出来放到common文件下,方便其他step调用
# def get_min_fee(currency):
#     min_fee = None
#     if currency == "USD":
#         min_fee = 0.5
#     elif currency == "USDC":
#         min_fee = 1
#     elif currency == "EUR":
#         min_fee = 0.5
#     else:
#         print(f"not found the currency:{currency}")
#     return min_fee
#
#
# @when(parsers.parse("I navigate to {url}"))
# def navigate_to_url(driver, url):
#     driver.get(url)
#     driver.maximize_window()
#     driver.implicitly_wait(10)
#
#     current_title = driver.title
#     logger.info(f"current title is {current_title}")
#     current_url = driver.current_url
#     logger.info(f"current url is {current_url}")
#     assert current_url == url


# @then(parsers.parse("The payout fee is calculated correctly at the first payout record"))
# def verify_first_payout_fee(driver):
#     # 找到第一条记录的currency
#     first_record_currency = driver.find_element(By.XPATH,
#                                    "(//table)[2]/tbody/tr/following-sibling::tr/td/following-sibling::*[4]")
#     # 点击进入detail 页面
#     first_record_currency.click()
#     logger.info(f"first record currency:{first_record_currency.text}")
#     # 找到第一条记录的amount
#     first_record_amount = driver.find_element(By.XPATH, '//span[text()="Amount"]/following-sibling::p').text
#     logger.info(f"first record amount:{first_record_amount}")
#     # 找到第一条记录的fee
#     first_record_fee = driver.find_element(By.XPATH, '//span[text()="Payout fee"]/following-sibling::p').text
#     logger.info(f"first record fee:{first_record_fee}")
#     # 根据currency得到min_fee
#     min_fee = get_min_fee(first_record_currency.text)
#     logger.info(f"minimum fee:{min_fee}")
#     # 假设fee_rate = 5%
#     fee_rate = 0.05
#     # 期望的fee
#     ex_fee = min_fee if fee_rate * float(first_record_amount) <= min_fee else fee_rate * float(first_record_amount)
#     logger.info(f"ex_fee:{ex_fee}")
#     # 把所有期望的log放到断言里面输出
#     assert float(first_record_fee) == ex_fee
#
#
# @when("I switch to a lexuan's shop 6")
# def switch_shop(driver):
#     sidebar = driver.find_element(By.XPATH, '//*[@id="sidebar"]/div/div[1]/a')
#     a = ActionChains(driver)
#     hover = a.move_to_element(sidebar).perform()  # 找到元素,并悬停
#     # 找到目标元素
#     target = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/ul/li[1]/ul/li[3]/span/a')
#     # 拖动到可见的元素去
#     driver.execute_script("arguments[0].scrollIntoView();", target)
#     sleep(1)
#     target.click()
#     sleep(1)
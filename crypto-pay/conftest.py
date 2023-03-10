from typing import List

import pytest
from _pytest.mark import Mark
from _pytest.python import Function
from _pytest.runner import CallInfo


# pytest自定义参数，参数值通过 pytest.main 命令输入的参数值传入
def pytest_addoption(parser):
    parser.addoption("--qase_test_run_id", action="store")
    parser.addoption("--host_port", action="store")
    parser.addoption("--env", action="store")
    parser.addoption("--qase", action="store")


# item 是测试用例，call 是测试步骤
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Function, call: CallInfo):
    """Get the result of each execution"""
    if call.when == "setup":
        # 获取每条测试用例的mark标签
        makers: List[Mark] = item.own_markers
        for maker in makers:
            # 当mark标签包含PCO时，修改item.name的值
            if "PCO" in maker.name:  # 'PCO-1058::test_login__login_successful'
                item.name = maker.name + "::" + item.name

    # 获取钩子方法的调用结果，返回一个result对象。相当于return
    outcome = yield
    # 从钩子方法的调用结果中获取测试报告，返回一个report对象
    report = outcome.get_result()
    # setattr() 用于设置指定对象的指定属性的值，该属性不一定是存在的
    # 设置report对象的nodeid属性的值为item.name
    # nodeid是 测试用例的名称，返回格式为 ' xx.py::测试步骤函数名称' 比如：'test_cases/staging/test_smoke.py::test_login__login_successful'
    setattr(report, "nodeid", item.name)

import json
import os

# from os.path import join, dirname

import yaml
import pytest
import argparse

# from dotenv import load_dotenv


from cdc.qa.core import secretsmanager
from cdc.qa.apis.qa_tools import QAToolsApiServices


def build_tags(failed_cases):
    tags = " or "
    test_run_id = None
    with open(failed_cases, "r") as f:
        failed_items = yaml.safe_load(f)
        # Join() - 字符串连接方法，例如通过 " or " 连接词连接，会变成 PCO-1058 or PCO-1059
        tags = tags.join(failed_items.get("Failed"))
        if "Test_Run_ID" in failed_items.keys():
            test_run_id = failed_items["Test_Run_ID"]
        f.close()
    return tags, test_run_id


def run(config, tags: str = None, test_run_id: str = None):
    # Run by pytest
    exist_code = pytest.main(
        [
            f"-m={config.tag if tags is None else tags}",
            "-s",
            f"test_cases/{config.env}",
            "-p",
            "no:logging",
            f"--host_port={config.host_port}",
            f"--tests-per-worker={config.thread}",
            f"--env={config.env}",
            f"--qase={config.qase}",
            f"--qase_test_run_id={'NONE' if test_run_id is None else test_run_id}",
        ]
    )
    return exist_code


def init_env_args(secret_project: str = "crypto-pay", config_host_path: str = "configs/hosts.yaml"):
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", type=str, help="Test tag")
    parser.add_argument("--thread", type=str, help="Thread count", default="1")
    parser.add_argument("--host_port", type=str, help="Remote host port", default="localhost:4444")
    parser.add_argument("--qase_test_run_id", type=str, help="Qase test run id")
    parser.add_argument("--env", type=str, help="Env", default="staging")
    parser.add_argument("--qase", type=str, help="If push test step to qase", default="false")
    parser.add_argument("--rerun", type=str, help="Rerun the failed cases: true, latest, false", default="false")
    parser.add_argument("--data_env", type=str, help="Set the test data resource env folder", default="staging")
    d = parser.parse_args()

    # Sync to test plan name
    os.environ["tag"] = d.tag
    os.environ["data_env"] = d.data_env
    try:
        # Load pays envs from aws
        pays_envs = secretsmanager.get_secret_json(secret_project)
        os.environ.update(pays_envs)
        # load_dotenv(join(dirname(__file__), ".env"))
        wallet_address = get_wallet_address()
        os.environ.update(wallet_address)
    except BaseException as e:
        print(f"Get secret from AWS failed, you might failed during the test: {e.__getattribute__('msg')}")

    hosts: dict = yaml.safe_load(open(config_host_path))
    for k, v in hosts.items():
        if f"merchant_{d.env}" == k:
            os.environ["global_host"] = v
        if f"api_{d.env}" == k:
            os.environ["api_host"] = v
        if f"ops_{d.env}" == k:
            os.environ["global_ops_host"] = v

    print(d)
    return d


def get_wallet_address():
    api_key = os.environ["QA_TOOL_API_KEY"]
    secret_key = os.environ["QA_TOOL_SECRET_KEY"]
    qa_tool_host = os.environ["QA_TOOL_HOST"]
    service_id = int(os.environ["QA_TOOL_SERVICE_ID"])
    qa_tool_services = QAToolsApiServices(api_key=api_key, secret_key=secret_key, host=qa_tool_host)
    resp = qa_tool_services.data_manager.get_service_datas(service_id=service_id, is_lock=0)
    data_list = resp.data.result
    d = json.loads(data_list[0].data)
    return d

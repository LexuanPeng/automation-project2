import os
import sys
import urllib3
import shutil
from pathlib import Path
from datetime import datetime
from common.runner import init_env_args, build_tags, run

# 官方强制验证https的安全证书，如果没有通过是不能通过请求的，虽然添加忽略验证的参数，但是依然会 给出醒目的 Warning
# 所以这个方法是用来禁用警告的
urllib3.disable_warnings()

os.environ.setdefault("LOG_LEVEL", "DEBUG")
os.environ["RAILS_CONSOLE_CONFIG_AWSECS"] = "True"
os.environ["enable_headless"] = "true"

# Debug mode
'''
1.sys.argv 返回脚本本身的名字及给定脚本的参数列表，里边的项为用户输入的参数。
    如在命令行中执行 “python demo.py one two three” 后可以得到以下输出结果：
    print(sys.argv)
    ['demo.py', 'one', 'two', 'three']
因此当开启debug模式时，len(sys.argv) = 1
'''
if len(sys.argv) <= 1:
    debug_args = [
        "--tag=PCO-1058",
        "--host_port=localhost:4444",  # Selenium standalone host port
        "--thread=1",
        "--env=staging",
        "--data_env=staging",  # Set the test data resource env folder
        "--qase=false",  # Push test result to Qase
        "--rerun=false",  # Rerun failed cases after first run
    ]
    sys.argv.extend(debug_args)

if __name__ == "__main__":
    # Get global env args
    run_config = init_env_args()

    # Check report folder
    # os.path.isdir - 判断指定对象是否为目录
    has_report_folder = os.path.isdir("report")
    if not has_report_folder:
        # os.makedirs - 创建多层目录。如果 exist_ok 为 True，则在目标目录已存在的情况下不会触发 FileExistsError 异常。
        os.makedirs(name="report", mode=0o777, exist_ok=True)

    # To clear the report folder when report count >= 5
    report_folder = sorted([name for name in os.listdir("report")])
    if len(report_folder) >= 5:
        for name in report_folder:
            # Path.cwd() - 获取当前工作目录
            full_path = Path.cwd() / f"report/{name}"
            # 如果 full_path是文件则删除该文件(os.unlink)，否则递归删除目录以及目录内的所有内容(shutil.rmtree)
            os.unlink(full_path) if full_path.is_file() else shutil.rmtree(full_path)

    # Create report root path
    report_execution_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    report_path = f"report/{run_config.env.upper()}_{run_config.tag}_{report_execution_name}"
    os.makedirs(name=report_path, mode=0o777, exist_ok=True)
    os.environ["report_path"] = report_path
    exist_code = 0

    if run_config.rerun == "latest":
        failed_cases = Path.cwd() / "failed_cases.yml"
        if failed_cases.is_file():
            tags, test_run_id = build_tags(failed_cases)
            exist_code = run(run_config, tags, test_run_id)
        else:
            print(f"None latest failed cases in {failed_cases}")
    else:
        # Run by pytest
        exist_code = run(run_config)

    # Rerun by pytest
    failed_cases = Path.cwd() / report_path / "failed_cases.yml"
    if run_config.rerun == "true" and failed_cases.is_file():
        tags, test_run_id = build_tags(failed_cases)
        # Create report root path
        rerun_report_path = f"{report_path}/Rerun"
        os.makedirs(name=rerun_report_path, mode=0o777, exist_ok=True)
        os.environ["report_path"] = rerun_report_path
        # run_config.thread = str(1 if int(run_config.thread) // 2 == 0 else int(run_config.thread) // 2)
        # Always set the thread to 1 when rerun
        # run_config.thread = 1
        exist_code = run(run_config, tags, test_run_id)
        failed_cases = Path.cwd() / rerun_report_path / "failed_cases.yml"

    has_log = os.path.isfile("crypto-pay.log")
    if has_log:
        # shutil.copyfile(src, dst,follow_symlinks)将一个文件的内容拷贝到另一个文件中，目标文件无需存在
        shutil.copyfile("crypto-pay.log", f"{report_path}/main.log")

    if failed_cases.is_file():
        shutil.copyfile(failed_cases, Path.cwd() / "failed_cases.yml")

    # 退出程序
    exit(exist_code)

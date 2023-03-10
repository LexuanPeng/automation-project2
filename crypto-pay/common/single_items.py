from pathlib import Path
from threading import Lock
import yaml

from cdc.qa.helpers import RailsConsoleHelper


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class FailedSaver(metaclass=SingletonMeta):
    failed_cases = None

    def __init__(self):
        self.cases_id = list()
        self.failed_cases = {"Failed": self.cases_id}

    def add(self, case_id: str, test_run_id: str = None):
        self.cases_id.append(case_id)
        if test_run_id is not None:
            self.failed_cases["Test_Run_ID"] = test_run_id

    def write(self, path: Path):
        # with FileLock(f"{str(path)}.lock"):
        #     path.write_text(yaml.dump(self.failed_cases))
        with open(path, "w") as ff:
            yaml.safe_dump(self.failed_cases, ff)


class RailsSaver(metaclass=SingletonMeta):
    rails = None

    def __init__(self):
        if self.rails is None:
            self.rails = RailsConsoleHelper()
            self.rails.disable_rails_log()

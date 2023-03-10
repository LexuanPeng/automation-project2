import functools
import logging
import os
import re
import time
from abc import ABC
from typing import Union, Callable

from kubernetes.client import Configuration
from kubernetes import config
from kubernetes.client.api import core_v1_api
from kubernetes.stream import stream
from kubernetes.stream.ws_client import WSClient

from . import monkeypatch  # noqa: F401


logger = logging.getLogger(__name__)


def auto_reconnect(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.is_alive():
            logging.info("EKS Console WS client is not alive, reconnecting...")
            self.shutdown()
            self._client = self.connect_console()
        return method(self, *args, **kwargs)

    return wrapper


class EKSConsole(ABC):
    def __init__(self):
        self.env = os.environ.get("ENV", "stg")
        self.CONTEXT = f"ap-southeast-1.tech.internal-a{'sta' if self.env == 'stg' else self.env}-user-api-122"
        self.NAMESPACE = f"{self.env}-monaco"
        self.STATEFULSET_NAME = f"main-app-monaco-rails-console-{'staging' if self.env == 'stg' else self.env}-0"
        self.CONSOLE_PROMPT = re.compile(r"(Switch to inspect mode)")
        self._read_buffer = ""
        config.load_kube_config(context=self.CONTEXT)
        c = Configuration().get_default_copy()
        Configuration.set_default(c)
        self._core_api = core_v1_api.CoreV1Api()
        self._client: WSClient = self.connect_console()

    def connect_console(self):
        """Connect the k8s wsclient connection with command"""
        logger.info("Start connecting EKS Rails console........")
        exec_command = ["/bin/bash"]
        self._client: WSClient = stream(
            self._core_api.connect_post_namespaced_pod_exec,
            self.STATEFULSET_NAME,
            self.NAMESPACE,
            command=exec_command,
            stderr=True,
            stdin=True,
            stdout=True,
            tty=False,
            _preload_content=False,
        )

        self._client.write_stdin("source .aws-env\n")
        self._client.write_stdin("bin/rails c -- --nomultiline --nocolorize\n")

        match, result = self.expect(self.CONSOLE_PROMPT)
        if match:
            logger.info("Rails console is accessing........")
            return self._client
        else:
            raise ConnectionError(f"Rails console is not access: {result}")

    def expect(self, *args: Union[str, re.Pattern], timeout: int = 60):
        if not self.is_alive():
            raise ConnectionError("Kubernetes wsclient is not open")

        patterns = [arg.pattern if isinstance(arg, re.Pattern) else re.escape(arg) for arg in args]
        pattern = rf"^(?P<before>[\s\S]*)(?P<expected>{'|'.join(patterns)})(?P<after>[\s\S]*)$"
        matcher = re.compile(pattern)
        time_limit = time.time() + timeout
        while time.time() < time_limit:
            self._client.update()
            if self._client.peek_stdout():
                self._read_buffer = self._client.read_all()
                self._client.update()
                match = matcher.match(self._read_buffer)
                if match:
                    logger.debug(f"Current matched buffer: {self._read_buffer}")
                    self._read_buffer = ""
                    return True, match.group("expected")
        else:
            logger.warning(
                f"""
                expect() timeout after {timeout}s.
                Matching pattern: {matcher.pattern}
                Current buffer: {self._read_buffer}
                """
            )
            return False, self._read_buffer

    def write(self, s: str):
        if not self.is_alive():
            raise ConnectionError("Kubernetes wsclient is not open")
        self._client.update()
        logger.debug(f"Rails console writes: \n{s}")
        self._client.write_stdin(f"{s}\n")
        time.sleep(0.5)
        self._client.update()

    def is_alive(self):
        return self._client.is_open()

    @auto_reconnect
    def exec_command(
        self,
        cmd: str,
        pattern: Union[str, re.Pattern],
        wrap_with_begin: bool = True,
        timeout: int = 60,
    ):
        cmd = cmd.strip()
        if wrap_with_begin:
            cmd = f"""
            begin
                {cmd}
            end
            """.strip()
        self.write(f"{cmd}")
        match, result = self.expect(pattern, timeout=timeout)
        self._client.update()
        return match, result

    def shutdown(self):
        return self._client.close()

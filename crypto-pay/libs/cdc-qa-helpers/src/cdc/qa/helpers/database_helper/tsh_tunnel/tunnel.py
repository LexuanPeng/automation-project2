from __future__ import annotations

import logging
import time
import pyotp
import pexpect
import subprocess
import re
import random

from . import exceptions, utils

logger = logging.getLogger(__name__)


class TeleportTunnel:
    """A tunnel-like object implemented using Teleport client."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        otp_secret: str,
        db_identifier: str = "",
        db_name: str = "",
        db_username: str = "",
    ):
        if not self.is_tsh_found():
            raise exceptions.TSHCommandNotFoundException()

        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._otp_secret = otp_secret

        self._db_identifier = db_identifier
        self._db_name = db_name
        self._db_username = db_username

        self._local_bind_host: str = ""
        self._local_bind_port: int = 0

    @property
    def local_bind_host(self) -> str:
        return self._local_bind_host or self._host

    @property
    def local_bind_port(self) -> int:
        return self._local_bind_port or self._port

    @staticmethod
    def is_tsh_found() -> bool:
        """Check if `tsh` command is found.

        Raises:
            Exception: raised when encountering an unexpected error.

        Returns:
            bool: true if `tsh` command is found, false otherwise.
        """
        cmd = "tsh version"
        exit_code, output = subprocess.getstatusoutput(cmd)

        if exit_code == 0:
            return True
        elif exit_code == 127:
            return False
        else:
            raise Exception(f"An unexpected error occurred: {output}")

    def is_logged_in(self) -> bool:
        """Check if logged in with `tsh`.

        Raises:
            Exception: raised when encountering an unexpected error.

        Returns:
            bool: true if logged in, false otherwise.
        """
        cmd = f"tsh --user={self._username} --proxy={self._host} status"
        exit_code, output = subprocess.getstatusoutput(cmd)

        if exit_code == 0:
            return True
        elif exit_code == 1:
            return False
        else:
            if any(keyword in output for keyword in ("not logged in", "Active profile expired", "EXPIRED")):
                return False
            else:
                raise Exception(output)

    def _get_otp_code(self) -> str:
        totp = pyotp.TOTP(self._otp_secret)
        # make sure time left is more than 3 seconds
        left_seconds = 3
        if int(time.time() * 1000 % 30000) >= (30 - left_seconds) * 1000:
            time.sleep(left_seconds)
        return totp.now()

    def login(self):
        if self.is_logged_in():
            return

        cmd = f"tsh --proxy={self._host}:{self._port} --user={self._username} --auth=local login"
        try:
            tsh_command = pexpect.spawn(cmd)
            tsh_command.delaybeforesend = 0.5
            tsh_command.expect("Enter password for Teleport user.*", timeout=10)
            tsh_command.sendline(self._password)
            tsh_command.expect("Enter your OTP token:.*", timeout=10)
            tsh_command.sendline(self._get_otp_code())

            code = tsh_command.expect(".*Logged in.*", timeout=10)
            if code == 0:
                tsh_command.close()
                return
        except pexpect.exceptions.EOF:
            pass

        raise exceptions.TSHLoginFailedException()

    def logout(self):
        exitcode, output = subprocess.getstatusoutput(f"tsh --user={self._username} --proxy={self._host} logout")
        if exitcode == 0:
            return

        raise exceptions.TSHLogoutFailedException(output)

    def db_login(self):
        cmd = (
            f"tsh --proxy={self._host} db login --db-name={self._db_name} --db-user={self._db_username} "
            f"{self._db_identifier}"
        )
        exit_code, output = subprocess.getstatusoutput(cmd)
        if exit_code == 0:
            return
        elif f'Connection information for database "{self._db_identifier}" has been saved' in output:
            return

        raise exceptions.TSHDBLoginFailedException(output)

    def db_connect(self):
        cmd = (
            f"tsh --proxy={self._host} db connect --db-name={self._db_name} --db-user={self._db_username} "
            f"{self._db_identifier}"
        )
        tsh_command = pexpect.spawn(cmd)
        tsh_command.delaybeforesend = 0.1
        index = tsh_command.expect(["SSL connection.*", pexpect.EOF])
        if index == 0:
            tsh_command.sendline("exit")
            tsh_command.close()
            return
        elif index == 1:
            decoded_str = tsh_command.before.decode("utf-8")  # type: ignore
            if '"psql": executable file not found in $PATH' in decoded_str:
                return
            raise exceptions.TSHDBConnectException(decoded_str)
        raise exceptions.TSHDBConnectException()

    def as_proxy(
        self,
        local_bind_host: str = "",
        local_bind_port: int = 0,
    ):
        self._local_bind_host = local_bind_host or "127.0.0.1"
        self._local_bind_port = local_bind_port or random.randint(49152, 65535)

        utils.kill_process_by_port(self._local_bind_port)
        cmd = f"tsh proxy db -p {self._local_bind_port} {self._db_identifier}"
        subprocess.Popen(cmd, shell=True)

    def get_ssl_cert_info(self) -> tuple[str, str, str]:
        cmd = f"tsh --proxy={self._host} db config {self._db_identifier}"
        exit_code, output = subprocess.getstatusoutput(cmd)
        output = output.strip()

        if exit_code == 0:
            pattern = re.compile(
                r"Name:(.*)Host:(.*)Port:(.*)User:(.*)Database:(.*)CA:(.*)Cert:(.*)Key:(.*)",
                re.I | re.DOTALL,
            )
            match = pattern.match(output)
            if match:
                # name = match.group(1).strip()
                # host = match.group(2).strip()
                # port = match.group(3).strip()
                # usernamatche = match.group(4).strip()
                # dbnamatche = match.group(5).strip()
                sslrootcert = match.group(6).strip()
                sslcert = match.group(7).strip()
                sslkey = match.group(8).strip()
                return sslrootcert, sslcert, sslkey
            else:
                raise Exception("Failed to find the certificate info")
        else:
            if "No proxy address specified, missed --proxy flag" in output:
                raise exceptions.TSHNotLoggedInException(output)
            elif "Not logged into database" in output or "Please login using 'tsh db login' first" in output:
                raise exceptions.TSHDBNotLoggedInException(output)
            else:
                raise Exception(output)

    def start(self):
        self.login()
        self.db_login()

    def ssh_port_forwarding(self, remote_host, remote_port, local_bind_port: str, user: str, node: str):
        try:
            utils.get_pid_by_port(local_bind_port)
            utils.kill_process_by_port(local_bind_port)
        except Exception:
            pass
        cmd = f"tsh ssh -NL {local_bind_port}:{remote_host}:{remote_port} {user}@{node}"
        proc = subprocess.Popen(cmd, shell=True)
        return proc

import subprocess


def get_pid_by_port(port: int) -> str:
    """Return the pid of process using the specified port.

    Args:
        port (int): port in usage.

    Raises:
        Exception: raised when encountering an unexpected error.

    Returns:
        str: the pid of the process.
    """
    cmd = f"lsof -ti:{port}"
    exit_code, output = subprocess.getstatusoutput(cmd)

    if exit_code == 0:
        return output
    else:
        raise Exception(f"Failed to get pid by port: {output}")


def kill_process_by_port(port: int):
    """Kill a process occupying the specified port

    Args:
        port (int): port in usage.

    Raises:
        Exception: raised when encountering an unexpected error.
    """
    try:
        pid = get_pid_by_port(port)
    except Exception:
        return
    cmd = f"kill -9 {pid}"
    exit_code, output = subprocess.getstatusoutput(cmd)
    if exit_code:
        raise Exception(f"Failed to kill process by port: {output}")

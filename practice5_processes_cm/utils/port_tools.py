import os
import signal
import subprocess
import time


def _find_pids_on_port(port):
    """ищет pid процессов, слушающих порт, через lsof"""
    try:
        out = subprocess.run(
            ["lsof", "-t", f"-iTCP:{port}", "-sTCP:LISTEN"],
            capture_output=True,
            text=True,
            check=False,
        ).stdout
    except FileNotFoundError:
# lsof нет вернём пустой список
        return []
    pids = set()
    for line in out.splitlines():
        line = line.strip()
        if line and line.isdigit():
            pids.add(int(line))
    return list(pids)


def _kill_procs_on_port(port, wait_sec=1.5):
    """убивает процессы на порту: сначала вежливо, потом жёстко"""
    pids = _find_pids_on_port(port)
    my_pid = os.getpid()
    for pid in pids:
        if pid != my_pid:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
# ждём пока порт освободится
    deadline = time.time() + wait_sec
    while time.time() < deadline:
        if not _find_pids_on_port(port):
            break
        time.sleep(0.1)
# добиваем оставшихся
    for pid in _find_pids_on_port(port):
        if pid != my_pid:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    return


def start_server_on_port(port, cmd_args):
    """освобождает порт и запускает сервер"""
# если порт занят убиваем процессы
    if _find_pids_on_port(port):
        _kill_procs_on_port(port)
# запускаем сервер
    return subprocess.Popen(list(cmd_args))
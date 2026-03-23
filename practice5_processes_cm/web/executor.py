import dataclasses
import resource
import shutil
import subprocess
import sys

@dataclasses.dataclass
class RunResult:
    out: str
    err: str
    exit_code: int | None
    timedout: bool


def _apply_limits(secs):
    """Пытаемся поставить ограничения на ресурсы в дочернем процессе."""
    try:
# лимит CPU
        resource.setrlimit(resource.RLIMIT_CPU, (secs + 1, secs + 1))
    except Exception:
        pass
    try:
# память 256 MB
        resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
    except Exception:
        pass
    try:
        resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))
    except Exception:
        pass


def _make_command(user_code):
    """Собираем команду для запуска python-кода."""
    base = [sys.executable, "-c", user_code]
    if shutil.which("prlimit"):
        return ["prlimit", "--nproc=1:1"] + base
    return base


def _clean_stderr(raw_err):
    """Убираем из трейсбека строки с кодом пользователя."""
    if not raw_err:
        return raw_err
    lines = raw_err.splitlines()
    out = []
    skip = 0
    for line in lines:
        if skip:
            skip -= 1
            continue
        if 'File "<string>"' in line or 'File "<stdin>"' in line:
            out.append(line)
            skip = 2
        else:
            out.append(line)
    if raw_err.endswith("\n"):
        return "\n".join(out) + "\n"
    return "\n".join(out)


def exec_python(code, timeout_sec):
    """Запускает переданный код, возвращает результат выполнения."""
    cmd = _make_command(code)
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        preexec_fn=lambda: _apply_limits(timeout_sec),
    )
    try:
        out, err = proc.communicate(timeout=timeout_sec)
        err = _clean_stderr(err)
        return RunResult(out, err, proc.returncode, False)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        err = _clean_stderr(err)
        return RunResult(out, err, None, True)
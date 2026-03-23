import datetime as dt
from contextlib import contextmanager
from typing import List, Optional

# пытаемся импортировать freezegun
try:
    from freezegun import freeze_time as fz  # type: ignore
    HAS_FREEGUN = True
except ImportError:
    HAS_FREEGUN = False
    fz = None


@contextmanager
def freeze_time(dt_str: str, patch_targets: Optional[List[str]] = None):
    """
    Замораживает время. Если freezegun установлен — используем его.
    Иначе применяем ручной патч через mock.
    """
    if HAS_FREEGUN and fz is not None:
        with fz(dt_str):
            yield
        return

# fallback ручной патч
    if not patch_targets:
        raise RuntimeError(
            "freezegun не установлен, и не заданы patch_targets.\n"
            "Установите freezegun: pip install freezegun"
        )

    from unittest.mock import patch

    fixed_time = dt.datetime.fromisoformat(dt_str)

    class MockDateTime(dt.datetime):
        @classmethod
        def today(cls):
            return fixed_time

        @classmethod
        def now(cls, tz=None):
            if tz is None:
                return fixed_time
            return tz.fromutc(fixed_time.replace(tzinfo=dt.timezone.utc))

# стартуем патчи
    patchers = [patch(target, MockDateTime) for target in patch_targets]
    for p in patchers:
        p.start()

    try:
        yield
    finally:
        for p in reversed(patchers):
            p.stop()
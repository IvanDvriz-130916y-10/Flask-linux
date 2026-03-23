import sys
from typing import IO, Iterable, Optional, Type

class SuppressErrors:
    """Игнорирует исключения из указанного списка (включая наследников)."""
    def __init__(self, exceptions: Iterable[Type[BaseException]]):
        self.exceptions = set(exceptions)  # для быстрой проверки

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
# Проверяем является ли исключение подтипом любого из переданных типов
        for err in self.exceptions:
            if issubclass(exc_type, err):
                return True
        return False


class OutputRedir:
    """Перенаправляет stdout и/или stderr в заданные объекты."""
    def __init__(self, out: Optional[IO[str]] = None, err: Optional[IO[str]] = None):
        self.out = out
        self.err = err
        self._saved_out = None
        self._saved_err = None

    def __enter__(self):
        self._saved_out = sys.stdout
        self._saved_err = sys.stderr
        if self.out is not None:
            sys.stdout = self.out
        if self.err is not None:
            sys.stderr = self.err
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._saved_out is not None:
            sys.stdout = self._saved_out
        if self._saved_err is not None:
            sys.stderr = self._saved_err
        return False  # не подавляем исключения
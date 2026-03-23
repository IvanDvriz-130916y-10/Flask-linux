import unittest
from utils.context_managers import BlockErrors


class TestBlockErrors(unittest.TestCase):
    """Тесты для контекстного менеджера, подавляющего исключения."""

    def test_ignores_matching_exceptions(self):
# ошибки из указанного набора должны игнорироваться
        ignore_set = {ZeroDivisionError, TypeError}
        with BlockErrors(ignore_set):
            _ = 1 / 0  # ZeroDivisionError игнорируем

    def test_raises_non_matching_exceptions(self):
# если ошибка не в списке она должна пробрасываться
        ignore_set = {ZeroDivisionError}
        with self.assertRaises(TypeError):
            with BlockErrors(ignore_set):
                _ = 1 / "0"  # TypeError не входит в ignore_set выбрасывается

    def test_nested_blocks(self):
# вложенные контекстные менеджеры работают независимо
        outer_ignore = {TypeError}
        with BlockErrors(outer_ignore):
            inner_ignore = {ZeroDivisionError}
            with self.assertRaises(TypeError):
                with BlockErrors(inner_ignore):
                    _ = 1 / "0"  # TypeError не игнорируется во внутреннем попадает во внешний

    def test_inheritance_works(self):
# если указан базовый класс дочерние исключения тоже игнорируются
        ignore_set = {Exception}
        with BlockErrors(ignore_set):
            _ = 1 / "0"  # TypeError дочерний от Exception игнорируется


if __name__ == "__main__":
    unittest.main()
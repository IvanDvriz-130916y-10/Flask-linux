import unittest
from person import Person
from tests._freeze import freeze_time


class TestPerson(unittest.TestCase):
    """Тесты для класса Person (задача 4)."""

    def test_initialization(self):
# проверяем что поля устанавливаются корректно
        p = Person("Ivan", 2000, "Ekaterinburg")
        self.assertEqual(p.get_name(), "Ivan")
        self.assertEqual(p.get_address(), "Ekaterinburg")

    def test_age_calculation(self):
        p = Person("Ivan", 2000)
# замораживаем время на определённую дату
        with freeze_time("2026-02-14", patch_targets=["person.datetime.datetime"]):
            self.assertEqual(p.get_age(), 26)

    def test_name_operations(self):
        p = Person("Ivan", 2000)
        self.assertEqual(p.get_name(), "Ivan")
        p.set_name("Petr")
        self.assertEqual(p.get_name(), "Petr")

    def test_address_operations(self):
        p = Person("Ivan", 2000)
        p.set_address("Moscow")
        self.assertEqual(p.get_address(), "Moscow")

    def test_homeless_status(self):
# если адрес пустой или None человек бездомный
        p1 = Person("Ivan", 2000, "")
        self.assertTrue(p1.is_homeless())

        p2 = Person("Ivan", 2000, "Moscow")
        self.assertFalse(p2.is_homeless())

        p3 = Person("Ivan", 2000, None)
        self.assertTrue(p3.is_homeless())

if __name__ == "__main__":
    unittest.main()
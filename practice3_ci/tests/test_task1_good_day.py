import unittest
from tests._freeze import freeze_time
from web.greetings import WEEKDAY_WISHES, get_username_with_weekdate


def extract_wish(msg):
# берём последнюю часть после точки с пробелом убираем восклицательный знак
    return msg.rsplit('. ', 1)[-1].rstrip('!')


class TestGreetings(unittest.TestCase):
# Задача 1 Хорошего дня!

    def test_weekday_wish(self):
# Проверяем все дни недели на конкретной неделе
        test_data = [
            ("2026-02-09", WEEKDAY_WISHES[0]),
            ("2026-02-10", WEEKDAY_WISHES[1]),
            ("2026-02-11", WEEKDAY_WISHES[2]),
            ("2026-02-12", WEEKDAY_WISHES[3]),
            ("2026-02-13", WEEKDAY_WISHES[4]),
            ("2026-02-14", WEEKDAY_WISHES[5]),
            ("2026-02-15", WEEKDAY_WISHES[6]),
        ]
        for date_str, expected in test_data:
            with self.subTest(date=date_str, expected=expected):
                with freeze_time(date_str, patch_targets=["web.greetings.datetime"]):
                    result = get_username_with_weekdate("Петя")
                self.assertEqual(extract_wish(result), expected)

    def test_username_with_wish_ignored(self):
# Даже если в username есть пожелание оно не должно влиять на день недели
        with freeze_time("2026-02-09", patch_targets=["web.greetings.datetime"]):
            msg = get_username_with_weekdate("Хорошей среды")
        self.assertEqual(extract_wish(msg), WEEKDAY_WISHES[0])  # понедельник
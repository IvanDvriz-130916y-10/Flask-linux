import unittest
from cli.task3_decrypt import decrypt


class TestDecrypt(unittest.TestCase):
    """Тесты для дешифратора — проверка всех правил из задания."""

    def test_dot_handling(self):
# Одиночные точки просто удаляются
        self.assertEqual(decrypt("абра-кадабра."), "абра-кадабра")
        self.assertEqual(decrypt("."), "")

# Две точки подряд удаляют предыдущий символ
        self.assertEqual(decrypt("абраа..-кадабра"), "абра-кадабра")
        self.assertEqual(decrypt("абра--..кадабра"), "абра-кадабра")
        self.assertEqual(decrypt("1..2.3"), "23")

# Смешанные случаи
        self.assertEqual(decrypt("абраа..-.кадабра"), "абра-кадабра")
        self.assertEqual(decrypt("абрау...-кадабра"), "абра-кадабра")

# Длинные последовательности точек
        self.assertEqual(decrypt("абра........"), "")
        self.assertEqual(decrypt("абр......a."), "a")
        self.assertEqual(decrypt("1......................."), "")

if __name__ == "__main__":
    unittest.main()
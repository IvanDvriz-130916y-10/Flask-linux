import unittest
from web.app import app, storage


class FinanceTestsBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.seed = [
            ("20260101", 100),
            ("20260214", 150),
            ("20260215", 50),
            ("20251231", 10),
        ]

    def setUp(self):
        storage.clear()
        for d, amt in self.seed:
            storage.add(d, amt)
        self.client = app.test_client()


class AddTests(FinanceTestsBase):
    def test_add_updates_day_total(self):
        rv = self.client.get("/add/20260214/25")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("Итого за день: 175" in rv.get_data(as_text=True))

    def test_add_new_date_works(self):
        rv = self.client.get("/add/20260301/10")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("Итого за день: 10" in rv.get_data(as_text=True))
        self.assertEqual(storage.daily.get("20260301"), 10)

    def test_add_bad_date_raises(self):
        with self.assertRaises(ValueError):
            self.client.get("/add/2026-02-14/10")


class YearTests(FinanceTestsBase):
    def test_year_sum(self):
        rv = self.client.get("/calculate/2026")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("300" in rv.get_data(as_text=True))

    def test_year_missing(self):
        rv = self.client.get("/calculate/1999")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("0" in rv.get_data(as_text=True))

    def test_year_after_add(self):
        self.client.get("/add/20260216/20")
        rv = self.client.get("/calculate/2026")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("320" in rv.get_data(as_text=True))

    def test_year_empty(self):
        storage.clear()
        rv = self.client.get("/calculate/2026")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("0" in rv.get_data(as_text=True))


class MonthTests(FinanceTestsBase):
    def test_month_sum(self):
        rv = self.client.get("/calculate/2026/2")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("200" in rv.get_data(as_text=True))

    def test_month_missing(self):
        rv = self.client.get("/calculate/2026/3")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("0" in rv.get_data(as_text=True))

    def test_month_invalid(self):
        rv = self.client.get("/calculate/2026/13")
        self.assertEqual(rv.status_code, 400)

    def test_month_empty(self):
        storage.clear()
        rv = self.client.get("/calculate/2026/2")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("0" in rv.get_data(as_text=True))
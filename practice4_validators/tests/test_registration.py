import unittest
from web.app import create_app

class TestRegistration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(testing=True)
        cls.client = cls.app.test_client()

    def _get_base_data(self):
        return {
            "email": "user@example.com",
            "phone": 1234567890,
            "name": "Ivan",
            "address": "Lenina 1",
            "index": 620000,
            "comment": "optional",
        }

    def test_good_email(self):
        data = self._get_base_data()
        data["email"] = "a.b-c+tag@sub.example.org"
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 200)

    def test_bad_email(self):
        data = self._get_base_data()
        data["email"] = "not-an-email"
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 400)
        j = resp.get_json()
        self.assertTrue(any("email:" in e for e in j["errors"]))

    def test_missing_email(self):
        data = self._get_base_data()
        del data["email"]
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 400)

    def test_phone_ten_digits(self):
        data = self._get_base_data()
        data["phone"] = 9998887766
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 200)

    def test_phone_too_short(self):
        data = self._get_base_data()
        data["phone"] = 12345
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 400)
        self.assertTrue(any("phone:" in e for e in resp.get_json()["errors"]))

    def test_phone_negative(self):
        data = self._get_base_data()
        data["phone"] = -1234567890
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 400)

    def test_phone_string(self):
        data = self._get_base_data()
        data["phone"] = "abc"
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 400)
        j = resp.get_json()
        self.assertTrue("phone" in j["field_errors"])

    def test_empty_name(self):
        data = self._get_base_data()
        data["name"] = ""
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 400)

    def test_good_name(self):
        data = self._get_base_data()
        data["name"] = "Petr"
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 200)

    def test_missing_address(self):
        data = self._get_base_data()
        del data["address"]
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 400)

    def test_good_address(self):
        data = self._get_base_data()
        data["address"] = "New address"
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 200)

    def test_missing_index(self):
        data = self._get_base_data()
        del data["index"]
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 400)

    def test_index_not_number(self):
        data = self._get_base_data()
        data["index"] = "qwerty"
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 400)
        j = resp.get_json()
        self.assertTrue("index" in j["field_errors"])

    def test_good_index(self):
        data = self._get_base_data()
        data["index"] = 123456
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 200)

    def test_missing_comment_ok(self):
        data = self._get_base_data()
        del data["comment"]
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 200)

    def test_errors_field_exists(self):
        data = self._get_base_data()
        data["email"] = "bad"
        resp = self.client.post("/registration", json=data)
        self.assertEqual(resp.status_code, 400)
        j = resp.get_json()
        self.assertTrue("errors" in j)
        self.assertTrue(isinstance(j["errors"], list))

if __name__ == "__main__":
    unittest.main()
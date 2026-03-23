import unittest
from web.app import create_app


class TestCodeExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({"TESTING": True})
        cls.client = cls.app.test_client()

    def test_timeout_triggers(self):
        payload = {"code": "import time\ntime.sleep(2)\nprint('done')", "timeout": 1}
        response = self.client.post("/execute", data=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["ok"])
        self.assertTrue(data["timed_out"])
        self.assertIn("timeout", data["message"].lower())

    def test_bad_form_data_fails(self):
        response = self.client.post("/execute", data={"code": "print('x')", "timeout": 0})
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result["ok"])
        self.assertIn("timeout", result["errors"])

    def test_injection_attempt_ignored(self):
        malicious = 'print()"; echo "hacked"'
        resp = self.client.post("/execute", data={"code": malicious, "timeout": 5})
        self.assertEqual(resp.status_code, 200)
        out = resp.get_json()
        combined = (out.get("stdout", "") + out.get("stderr", "")).lower()
        self.assertNotIn("hacked", combined)
        self.assertIn("syntax", combined)


if __name__ == "__main__":
    unittest.main()
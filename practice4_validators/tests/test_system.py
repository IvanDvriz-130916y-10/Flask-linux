import unittest
from web.app import create_app


class TestSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = create_app(testing=True)
        cls.client = cls.application.test_client()

    def test_uptime_format(self):
        response = self.client.get("/uptime")
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
# ожидаем "Current uptime is"
        self.assertTrue(data.startswith("Current uptime is "))
# убеждаемся, что load average не показывается
        self.assertNotIn("load average", data)

    def test_ps_with_multiple_args(self):
        resp = self.client.get("/ps?arg=a&arg=u&arg=x")
        self.assertEqual(resp.status_code, 200)
        content = resp.get_data(as_text=True)
        self.assertTrue(content.startswith("<pre>") and content.endswith("</pre>"))

    def test_ps_special_chars_should_not_break(self):
# потенциальная инъекция через аргумент
        r = self.client.get("/ps?arg=aux;rm%20-rf%20/")
        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()
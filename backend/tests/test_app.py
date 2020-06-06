from flask import current_app

from tests.fixtures import BaseTestCase


class ProxyMiddleWareTestCase(BaseTestCase):
    def test_wrong_url_prefix(self):
        current_app.wsgi_app.prefix = "service/123"

        rv = self.client.get("/api/v1/content/my-content")
        self.assert404(rv)
        self.assertEqual(rv.data, b"This url does not belong to the app.")

        rv = self.client.get("service/123/api/v1/content/my-content")
        self.assert404(rv)
        self.assertNotEqual(rv.data, b"This url does not belong to the app.")

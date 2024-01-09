import json
import unittest

from src.main.simple_flask_router import BufferService


class TestFlaskApp(unittest.TestCase):
    buffer_service = BufferService()

    _data = {
        "State": [1.0, 1.1],
        "Reward": [-1, -1],
        "Action": [3, 4],
        "Next state": [1.1, 1.2],
    }

    def setUp(self):
        test_app = self.buffer_service.app
        test_app.config["TESTING"] = True
        self.client = test_app.test_client()

    def test_record_data(self):
        response = self.client.post(
            "record_data", content_type="application/json", data=json.dumps(self._data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "OK")

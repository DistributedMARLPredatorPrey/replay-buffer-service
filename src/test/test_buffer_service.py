import json
import unittest
import pandas as pd

from src.main.buffer_service import BufferService


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

    def test_batch_data(self):
        batch_size = 2
        data = self.client.get(f"batch_data/{batch_size}").text
        self.assertEqual(pd.DataFrame(json.loads(data)).shape[0], batch_size)

import json
import unittest
import pandas as pd

from src.main.service.response import Response
from src.main.service.replay_buffer_service import ReplayBufferService


class TestReplayBufferService(unittest.TestCase):
    replay_buffer_service = ReplayBufferService()

    _data = {
        "State": [1.0, 1.1],
        "Reward": [-1, -1],
        "Action": [3, 4],
        "Next state": [1.1, 1.2],
    }

    def _post_data(self, data):
        return self.client.post(
            "record_data", content_type="application/json", data=json.dumps(data)
        )

    def setUp(self):
        self.client = self.replay_buffer_service.test_client()

    def test_record_data(self):
        response = self._post_data(self._data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, Response.SUCCESSFUL.name)

    def test_batch_data(self):
        batch_size = 2
        self._post_data(self._data)
        data = self.client.get(f"batch_data/{batch_size}").text
        self.assertEqual(pd.DataFrame(json.loads(data)).shape[0], batch_size)

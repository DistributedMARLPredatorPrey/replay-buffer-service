import json
import unittest
from typing import Dict, List

import pandas as pd
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from src.main.service.response import Response
from src.main.service.replay_buffer_service import ReplayBufferService


class TestReplayBufferService(unittest.TestCase):
    _replay_buffer_service: ReplayBufferService = ReplayBufferService()

    _data: Dict[str, List[float]] = {
        "State": [1.0, 1.1],
        "Reward": [-1, -1],
        "Action": [3, 4],
        "Next state": [1.1, 1.2],
    }

    def _post_data(self, data) -> TestResponse:
        """
        Post data using the Replay buffer testing client
        :param data: to be sent
        :return:
        """
        return self.client.post(
            "record_data", content_type="application/json", data=json.dumps(data)
        )

    def setUp(self):
        self.client: FlaskClient = self._replay_buffer_service.test_client()

    def test_record_data(self):
        """
        Test the data to be properly recorded into the Replay buffer
        :return:
        """
        response: TestResponse = self._post_data(self._data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, Response.SUCCESSFUL.name)

    def test_batch_data(self):
        """
        Test the data to be properly batched from the Replay buffer
        :return:
        """
        batch_size: int = 2
        self._post_data(self._data)
        data: str = self.client.get(f"batch_data/{batch_size}").text
        self.assertEqual(pd.DataFrame(json.loads(data)).shape[0], batch_size)

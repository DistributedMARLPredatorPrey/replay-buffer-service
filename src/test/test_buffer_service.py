import json
import os
import unittest
from typing import Dict, List

import pandas as pd
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from src.main.parser.config import ReplayBufferConfig
from src.main.service.post_response import PostResponseStatus
from src.main.service.replay_buffer_service import ReplayBufferService


class TestReplayBufferService(unittest.TestCase):
    __replay_buffer_service: ReplayBufferService = ReplayBufferService(
        ReplayBufferConfig(
            num_predators=1,
            num_preys=1,
            num_states=2,
            num_actions=2,
            dataset_path=os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "resources", "dataset.csv"
            ),
        )
    )

    __data: Dict[str, List[float]] = {
        "State": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
        "Reward": [[1, 2], [1, 2]],
        "Action": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
        "Next State": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
    }

    def __post_data(self, data) -> TestResponse:
        """
        Post data using the Replay buffer testing client
        :param data: to be sent
        :return:
        """
        return self.client.post(
            "record_data/",
            json=data,
        )

    def setUp(self):
        self.client: FlaskClient = self.__replay_buffer_service.test_client()

    def test_record_data_ok(self):
        """
        Test the data to be properly recorded into the Replay buffer
        :return:
        """
        response: TestResponse = self.__post_data(self.__data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.text, json.dumps({"status": PostResponseStatus.OK.value})
        )

    def test_record_data_wrong_schema(self):
        """
        Test the data to be properly recorded into the Replay buffer
        :return:
        """
        invalid_data =  {
            "State": [[1.0, 1.0], [1.1, 1.1, 2.1, 2.1]],
            "Reward": self.__data["Reward"],
            "Action": self.__data["Action"],
            "Next State": self.__data["Next State"]
        }

        response: TestResponse = self.__post_data(invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.text, json.dumps({"status": PostResponseStatus.INVALID_SCHEMA.value})
        )


    # def test_batch_data(self):
    #     """
    #     Test the data to be properly batched from the Replay buffer
    #     :return:
    #     """
    #     batch_size: int = 2
    #     for _ in range(100):
    #         self.__post_data(self.__data)
    #     data: str = self.client.get(f"batch_data/{batch_size}").text
    #     self.assertEqual(pd.DataFrame(json.loads(data)).shape[0], batch_size)

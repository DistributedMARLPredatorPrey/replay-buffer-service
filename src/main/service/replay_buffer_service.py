from typing import List

from flask import request, Flask
import pandas as pd
import os
import numpy as np

from flask.testing import FlaskClient
from pandas import DataFrame

from src.main.service.conf import conf
from src.main.service.response import Response


class ReplayBufferService:
    def __init__(self):
        """
        Init the Replay buffer service by set upping the dataset and by registering the routes.
        """
        self._app: Flask = Flask(__name__)
        self._file_path: str = conf["REPLAY_BUFFER_PATH"]
        self._add_rules()
        self._setup_buffer()

    def _add_rules(self):
        """
        Add routing rules to the Replay buffer service.
        :return:
        """
        self._app.add_url_rule("/batch_data/<size>", "batch data", self._batch_data)
        self._app.add_url_rule(
            "/record_data", "record data", self._record_data, methods=["POST"]
        )

    def _setup_buffer(self):
        """
        Set up the buffer, creating it if it does not exist.
        :return:
        """
        if not os.path.exists(self._file_path):
            header: List[str] = ["State", "Reward", "Action", "Next state"]
            df: DataFrame = pd.DataFrame(columns=header)
            df.to_csv(self._file_path, index=False)

    def _batch_data(self, size) -> str:
        """
        Batches data from the replay buffer.
        :param size: number of rows to batch
        :return: json representing the data batch
        """
        df: DataFrame = pd.read_csv(self._file_path)
        sample: DataFrame = df.sample(size)
        return sample.to_json()

    def _record_data(self) -> str:
        """
        Records data inside the replay buffer.
        :return: Name of the Response:
            - SUCCESSFUL if the data is correctly inserted
            - WRONG_SHAPE if the provided data has a different shape of the replay buffer
            - ERROR if a generic error occurred
        """
        if request.method == "POST":
            data_df: DataFrame = pd.DataFrame(request.get_json())
            df: DataFrame = pd.read_csv(self._file_path)
            if data_df.shape[1] == df.shape[1]:
                df: DataFrame = pd.concat([df, data_df], ignore_index=True)
                df.to_csv(self._file_path, index=False)
                return Response.SUCCESSFUL.name
            return Response.WRONG_SHAPE.name
        return Response.ERROR.name

    def app(self) -> Flask:
        """
        Get the app.
        :return: Flask app of the Replay buffer service
        """
        return self._app

    def test_client(self) -> FlaskClient:
        """
        Get the testing client.
        :return: test client from the Replay buffer service's Flask app
        """
        self._app.config["TESTING"] = True
        return self._app.test_client()

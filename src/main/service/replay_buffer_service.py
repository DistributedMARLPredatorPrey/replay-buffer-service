from io import StringIO
from typing import List

from flask import request, Flask
import pandas as pd
import os

from flask.testing import FlaskClient
from pandas import DataFrame

from src.main.service.response import Response


class ReplayBufferService:
    def __init__(self, predator_dataset_path: str, prey_dataset_path: str):
        """
        Init the Replay buffer service by set upping the dataset and by registering the routes.
        """
        self._app: Flask = Flask(__name__)
        self._predator_dataset_path: str = predator_dataset_path
        self._prey_dataset_path: str = prey_dataset_path
        self._add_rules()
        self._setup_buffers()

    def _add_rules(self):
        """
        Add routing rules to the Replay buffer service.
        :return:
        """
        self._app.add_url_rule(
            "/batch_data/<agent_type>/<size>", "batch data", self._batch_data
        )
        self._app.add_url_rule(
            "/record_data/<agent_type>/",
            "record data",
            self._record_data,
            methods=["POST"],
        )

    def _setup_buffers(self):
        """
        Set up the buffer, creating it if it does not exist.
        :return:
        """
        for dataset_path in [self._predator_dataset_path, self._prey_dataset_path]:
            if not os.path.exists(dataset_path):
                header: List[str] = ["State", "Reward", "Action", "Next state"]
                df: DataFrame = pd.DataFrame(columns=header)
                df.to_csv(dataset_path, index=False)

    def _batch_data(self, agent_type, size) -> str:
        """
        Batches data from the replay buffer.
        :param size: number of rows to batch
        :return: json representing the data batch
        """
        dataset_path = self._dataset_path_by_agent_type(agent_type)
        df = pd.read_csv(dataset_path) if dataset_path is not None else pd.DataFrame()
        return df.sample(int(size)).to_json() if len(df) >= int(size) else "{}"

    def _dataset_path_by_agent_type(self, agent_type):
        """
        Get the dataset path from the agent type
        :param agent_type: either "predator" or "prey"
        :return: predator or prey dataset path, if agent_type exist. None otherwise.
        """
        return (
            self._predator_dataset_path
            if agent_type == "predator"
            else self._prey_dataset_path
            if agent_type == "prey"
            else None
        )

    def _record_data(self, agent_type) -> str:
        """
        Records data inside the replay buffer.
        :return: Name of the Response:
            - SUCCESSFUL if the data is correctly inserted
            - WRONG_SHAPE if the provided data has a different shape of the replay buffer
            - ERROR if a generic error occurred
        """
        if request.method == "POST":
            dataset_path = self._dataset_path_by_agent_type(agent_type)
            data_df: DataFrame = pd.read_json(StringIO(request.get_json()))
            df: DataFrame = pd.read_csv(dataset_path)
            if data_df.shape[1] == df.shape[1]:
                df: DataFrame = pd.concat([df, data_df], ignore_index=True)
                df.to_csv(dataset_path, index=False)
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

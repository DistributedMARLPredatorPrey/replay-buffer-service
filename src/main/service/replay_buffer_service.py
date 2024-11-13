import json
import os
from enum import Enum
from typing import List, Callable

import pandas as pd
from flask import request, Flask
from flask.testing import FlaskClient
from pandas import DataFrame
from jsonschema import validate, ValidationError
import yaml

from src.main.parser.config import ReplayBufferConfig
from src.main.service.post_response import PostResponseStatus


def schema(num_preds, num_preys, num_states, num_actions):
    state_schema = {
        "type": "array",
        "items": {
            "type": "array",
            "minItems": num_states * (num_preds + num_preys),
            "maxItems": num_states * (num_preds + num_preys),
            "items": {"type": "number"},
        },
    }
    return {
        "type": "object",
        "properties": {
            "State": state_schema,
            "Reward": {
                "type": "array",
                "items": {
                    "type": "array",
                    "minItems": num_preds + num_preys,
                    "maxItems": num_preds + num_preys,
                    "items": {"type": "number"},
                },
            },
            "Action": {
                "type": "array",
                "items": {
                    "type": "array",
                    "minItems": num_actions * (num_preds + num_preys),
                    "maxItems": num_actions * (num_preds + num_preys),
                    "items": {"type": "number"},
                },
            },
            "Next State": state_schema,
        },
    }


class ReplayBufferService:
    def __init__(self, config: ReplayBufferConfig):
        """
        Init the Replay buffer service by set upping the dataset and by registering the routes.
        """
        self.__app: Flask = Flask(__name__)
        self.__dataset_path: str = config.dataset_path
        self.__add_rules()
        self.__setup_buffers()
        self.__data_record_schema = schema(
            config.num_predators,
            config.num_preys,
            config.num_states,
            config.num_actions,
        )

    def __schemas(self):
        with open("/schemas.yaml", "r") as schema_file:
            return yaml.safe_load(schema_file)

    def app(self) -> Flask:
        """
        Get the app.
        :return: Flask app of the Replay buffer service
        """
        return self.__app

    def test_client(self) -> FlaskClient:
        """
        Get the testing client.
        :return: test client from the Replay buffer service's Flask app
        """
        self.__app.config["TESTING"] = True
        return self.__app.test_client()

    def __add_rules(self):
        """
        Add routing rules to the Replay buffer service.
        :return:
        """
        self.__app.add_url_rule("/batch_data/<size>", "batch data", self.__batch_data)
        self.__app.add_url_rule(
            "/record_data/",
            "record data",
            self.__record_data,
            methods=["POST"],
        )

    def __setup_buffers(self):
        """
        Set up the buffer, creating it if it does not exist.
        :return:
        """
        if os.path.exists(self.__dataset_path):
            os.remove(self.__dataset_path)

        header: List[str] = ["State", "Reward", "Action", "Next state"]
        df: DataFrame = pd.DataFrame(columns=header)
        df.to_csv(self.__dataset_path, index=False)

    def __batch_data(self, size):
        """
        Batches data from the replay buffer.
        :param size: number of rows to batch
        :return: json representing the data batch
        """
        empty_json_str: str = "{}"
        if self.__dataset_path is not None:
            df: DataFrame = pd.read_csv(self.__dataset_path)
            return (
                df.sample(int(size)).to_json()
                if len(df) >= int(size)
                else empty_json_str
            )
        return empty_json_str

    def __record_data(self):
        """
        Records data inside the replay buffer.
        :return: Name of the Response:
            - SUCCESSFUL if the data is correctly inserted
            - WRONG_SHAPE if the provided data has a different shape of the replay buffer
            - ERROR if a generic error occurred
        """
        response: Callable[[PostResponseStatus], str] = lambda status: json.dumps(
            {"status": status.value}
        )
        row = request.json
        try:
            validate(instance=row, schema=self.__data_record_schema)
            df: DataFrame = pd.read_csv(self.__dataset_path)
            df = pd.concat([df, pd.DataFrame(row)], ignore_index=True)
            df.to_csv(self.__dataset_path, index=False)
            return response(PostResponseStatus.OK)
        except ValidationError:
            return response(PostResponseStatus.INVALID_SCHEMA)
        except:
            return response(PostResponseStatus.INTERNAL_ERROR)

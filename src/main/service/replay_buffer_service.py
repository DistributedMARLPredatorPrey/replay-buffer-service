import os
from typing import List

import pandas as pd
from flask import request, Flask
from jsonschema import ValidationError
from pandas import DataFrame

from src.main.parser.config import ReplayBufferConfig
from src.main.service.data_batch_validator import DataBatchValidator
from src.main.service.record_data_response import (
    RecordDataResponseStatus,
    RecordDataResponse,
)


class ReplayBufferService:
    def __init__(self, config: ReplayBufferConfig):
        """
        Init the Replay buffer service by set upping the dataset and by registering the routes.
        """
        self.app: Flask = Flask(__name__)
        self.__dataset_path: str = os.path.join(
            config.project_root_path,
            "src",
            "main",
            "resources",
            f"dataset_{config.num_predators}_{config.num_preys}.csv",
        )
        self.__setup_buffers()
        self.__data_batch_validator = DataBatchValidator(config)
        self.__add_rules()

    def __add_rules(self):
        """
        Add routing rules to the Replay buffer service.
        :return:
        """
        self.app.add_url_rule("/batch_data/<size>", "batch data", self.__batch_data)
        self.app.add_url_rule(
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
        :return: Json representing the data batch
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
        :return: Json as string containing a RecordDataResponse
            - OK if the data is correctly inserted
            - INVALID_SCHEMA if the provided data has invalid structure
            - INTERNAL_ERROR if a generic error occurred
        """
        data_batch = request.json
        try:
            self.__data_batch_validator.validate(data_batch=data_batch)
            df: DataFrame = pd.read_csv(self.__dataset_path)
            df = pd.concat([df, pd.DataFrame(data_batch)], ignore_index=True)
            df.to_csv(self.__dataset_path, index=False)
            return RecordDataResponse(RecordDataResponseStatus.OK).text
        except ValidationError:
            return RecordDataResponse(RecordDataResponseStatus.INVALID_SCHEMA).text
        except:
            return RecordDataResponse(RecordDataResponseStatus.INTERNAL_ERROR).text

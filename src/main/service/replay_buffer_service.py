from flask import request, Flask
import pandas as pd
import os

# from src.main.service.conf import REPLAY_BUFFER_PATH
from src.main.service.response import Response

REPLAY_BUFFER_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/resources/data.csv"


class ReplayBufferService:
    def __init__(self):
        self._app = Flask(__name__)
        self._add_rules()
        self._file_path = REPLAY_BUFFER_PATH
        self._setup_buffer()

    def _add_rules(self):
        self._app.add_url_rule("/batch_data/<size>", "batch data", self._batch_data)
        self._app.add_url_rule(
            "/record_data", "record data", self._record_data, methods=["POST"]
        )

    def _setup_buffer(self):
        if not os.path.exists(self._file_path):
            header = ["State", "Reward", "Action", "Next state"]
            df = pd.DataFrame(columns=header)
            df.to_csv(self._file_path, index=False)

    def _batch_data(self, size):
        df = pd.read_csv(self._file_path, nrows=int(size))
        return df.to_json()

    def _record_data(self):
        if request.method == "POST":
            data_df = pd.DataFrame(request.get_json())
            df = pd.read_csv(self._file_path)
            if data_df.shape[1] == df.shape[1]:
                df = pd.concat([df, data_df], ignore_index=True)
                df.to_csv(self._file_path, index=False)
                return Response.SUCCESSFUL.name
            return Response.WRONG_SHAPE.name
        return Response.ERROR.name

    def app(self):
        return self._app

    def test_client(self):
        self._app.config["TESTING"] = True
        return self._app.test_client()

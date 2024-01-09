from flask import request, Flask
import pandas as pd
import os


class BufferService:
    def __init__(self):
        self._app = Flask(__name__)
        self._add_rules()
        self._file_path = (
            f"{os.path.dirname(os.path.abspath(__file__))}/resources/data.csv"
        )
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
            data = request.get_json()
            df = pd.read_csv(self._file_path)
            df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
            df.to_csv(self._file_path, index=False)
            return "OK"

    def run(self, **kwargs):
        self._app.run(**kwargs)

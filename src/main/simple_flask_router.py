from flask import request, Flask
import pandas as pd
import os


class BufferService:
    def __init__(self):
        self.app = Flask(__name__)
        self._add_rules()

    def _add_rules(self):
        self.app.add_url_rule("/batch_data/<size>", "batch data", self._batch_data)
        self.app.add_url_rule(
            "/record_data", "record data", self._record_data, methods=["POST"]
        )

    @staticmethod
    def _batch_data():
        return "Batch data"

    @staticmethod
    def _record_data():
        if request.method == "POST":
            data = request.get_json()
            file_path = (
                f"{os.path.dirname(os.path.abspath(__file__))}/resources/data.csv"
            )

            header = ["State", "Reward", "Action", "Next state"]
            df = pd.DataFrame(columns=header, data=data)

            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

            df.to_csv(file_path, index=False)
            return "OK"

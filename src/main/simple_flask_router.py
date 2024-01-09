from flask import request, Flask
import pandas as pd
import os

app = Flask(__name__)


@app.route("/batch_data/<size>")
def batch_data():
    return "Batch data"


@app.route("/record_data", methods=["POST"])
def record_data():
    if request.method == "POST":
        data = request.get_json()
        file_path = f"{os.path.dirname(os.path.abspath(__file__))}/resources/data.csv"

        header = ["State", "Reward", "Action", "Next state"]
        df = pd.DataFrame(columns=header, data=data)

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

        df.to_csv(file_path, index=False)
        return "OK"


def run_flask_app(**kwargs):
    print(f"Running Flask Server {kwargs}")
    app.run(**kwargs)

from flask import request, jsonify, Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    return f"Hello, World!"


@app.route("/batch_data/<size>")
def batch_data():
    return f"Batch data"


@app.route("/record_data", methods=["POST"])
def record_data():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        return jsonify({"message": "JSON received successfully"})

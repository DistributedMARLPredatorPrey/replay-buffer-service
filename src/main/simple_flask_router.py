from flask import request, jsonify, Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/batch_data/<size>")
def batch_data():
    return "Batch data"


@app.route("/record_data", methods=["POST"])
def record_data():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        return jsonify({"message": "JSON received successfully"})


def run_flask_app():
    app.run()

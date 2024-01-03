import unittest
from multiprocessing import Process
from time import sleep

import requests
from flask import request, jsonify, Flask

# from src.main.simple_flask_router import app

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


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:5000/"
        server = Process(target=app.run)
        server.start()
        self.server = server
        sleep(1)

    def test_hello_endpoint(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello, World!")

    def tearDown(self):
        self.server.terminate()
        self.server.join()

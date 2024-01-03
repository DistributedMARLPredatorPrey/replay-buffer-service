import unittest
from multiprocessing import Process

import requests
from flask import Flask


class TestFlaskApp(unittest.TestCase):
    app = Flask(__name__)

    @staticmethod
    def run_flask_app(app):
        app.route("/")(lambda: "Hello, World!")
        app.run()

    def setUp(self):
        self.base_url = "http://127.0.0.1:5000/"
        self.server = Process(target=self.run_flask_app, args=[self.app])
        self.server.start()

    def test_hello_endpoint(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello, World!")

    def tearDown(self):
        self.server.terminate()
        self.server.join()

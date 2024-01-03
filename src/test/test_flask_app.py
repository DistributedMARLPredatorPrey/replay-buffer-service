import unittest
from multiprocessing import Process
from time import sleep

import requests
from flask import Flask


def run_flask_app(app):
    app.route("/")(lambda: "Hello, World!")
    app.run()


class TestFlaskApp(unittest.TestCase):
    # app = Flask(__name__)
    app = Flask(__name__.split('.')[0])

    def setUp(self):
        self.base_url = "http://127.0.0.1:5000/"
        server = Process(target=run_flask_app, args=[self.app])
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

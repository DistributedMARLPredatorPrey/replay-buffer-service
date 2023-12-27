import time
import unittest
from multiprocessing import Process

import requests
from flask import Flask


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.base_url = 'http://127.0.0.1:5000/'

        @self.app.route('/')
        def hello():
            return 'Hello, World!'

        @self.app.route("/shutdown")
        def shutdown():
            print("shutting down")
            raise RuntimeError()

        self.server = Process(target=self.app.run, kwargs={'debug': False})
        self.server.start()
        time.sleep(1)  # Give the server time to start

    def test_hello_endpoint(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hello, World!')

    def tearDown(self):
        self.app.quit = True  # Signal the app to stop
        #requests.get(f"{self.base_url}shutdown")
        self.server.terminate()
        self.server.join()
        # self.server.join()


if __name__ == '__main__':
    unittest.main()

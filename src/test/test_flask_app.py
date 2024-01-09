import time
import unittest
from multiprocessing import Process

import requests

from src.main.simple_flask_router import run_flask_app


class TestFlaskApp(unittest.TestCase):
    _conf = {"host": "127.0.0.1", "port": 5000}

    _data = {
        "State": [1.0, 1.1],
        "Reward": [-1, -1],
        "Action": [3, 4],
        "Next state": [1.1, 1.2],
    }

    def setUp(self):
        self.base_url = f"http://{self._conf['host']}:{self._conf['port']}/"
        self.server = Process(target=run_flask_app, kwargs=self._conf)
        self.server.start()
        time.sleep(1)

    def test_record_data(self):
        response = requests.post(f"{self.base_url}record_data", json=self._data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "OK")

    def tearDown(self):
        self.server.terminate()
        self.server.join()

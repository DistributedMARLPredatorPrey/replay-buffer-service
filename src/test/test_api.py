import unittest

import requests

from src.main.simple_flask_service import SimpleFlaskService


class TestReplayBufferApi(unittest.TestCase):
    simple_flask_service = SimpleFlaskService("127.0.0.1", 8080)

    json_data = {"name": "Luca", "age": 24, "city": "Senigallia"}

    def test_record_data(self):
        self.simple_flask_service.run()
        url = "http://127.0.0.1:8080/record_data"
        response = requests.post(url, json=self.json_data)
        assert response.json() == {"message": "JSON received successfully"}
        self.simple_flask_service.stop()

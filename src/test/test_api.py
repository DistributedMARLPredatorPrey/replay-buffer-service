import unittest

import requests


class TestReplayBufferApi(unittest.TestCase):
    json_data = {
        "name": "Luca",
        "age": 24,
        "city": "Senigallia"
    }

    def test_record_data(self):
        url = "http://127.0.0.1:5000/record_data"
        response = requests.post(url, json=self.json_data)
        assert response.json() == {"message": "JSON received successfully"}

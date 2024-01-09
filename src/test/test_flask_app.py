import json
import unittest


from src.main.simple_flask_router import app


class TestFlaskApp(unittest.TestCase):
    _data = {
        "State": [1.0, 1.1],
        "Reward": [-1, -1],
        "Action": [3, 4],
        "Next state": [1.1, 1.2],
    }

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_record_data(self):
        response = self.app.post(
            "record_data",
            content_type='application/json',
            data=json.dumps(self._data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "OK")

# import unittest
#
# import requests
#
# from src.test.testing_simple_flask_service import TestingSimpleFlaskService
#
#
# class TestReplayBufferApi(unittest.TestCase):
#     service = TestingSimpleFlaskService()
#     ip, port = "localhost", 8080
#
#     json_data = {"name": "Luca", "age": 24, "city": "Senigallia"}
#
#     @classmethod
#     def setUp(cls):
#         print("Setting up")
#         cls.service.run(ip=cls.ip, port=cls.port)
#
#     @classmethod
#     def tearDown(cls):
#         print("Tearing down")
#
#
#     def test_record_data(self):
#         #print("Setting up")
#         #self.service.run(ip=self.ip, port=self.port)
#
#         print("Executing test")
#         response = requests.post(
#            f"http://{self.ip}:{self.port}/record_data", json=self.json_data
#         )
#         assert response.json() == {"message": "JSON received successfully"}
#         print("done")

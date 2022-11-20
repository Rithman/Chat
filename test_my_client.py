import unittest
import json
import datetime
from my_client import create_presence, proccess_response

class TestClient(unittest.TestCase):

    def test_create_presence(self):
        self.assertEqual(create_presence("User-002"), 
        json.dumps(
        {"action": "presence",
        "time": str(datetime.datetime.now()),
        "type": "status",
        "user": {"account_name": "User-002", "status": "Я онлайн!"}
        }).encode("utf-8"))

    def test_proccess_response(self):
        message = json.dumps({"response": 200}).encode("utf-8")
        self.assertEqual(proccess_response(message), "200: OK")

if __name__ == "__main__":
    unittest.main()
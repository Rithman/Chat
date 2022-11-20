import json
import unittest
import datetime
from my_server import proccess_client_message

class TestServer(unittest.TestCase):

    def test_proccess_client_message(self):
        message = {"action": "presence",
                    "time": str(datetime.datetime.now()),
                    "type": "status",
                    "user": {"account_name": "User-001", "status": "Я онлайн!"}}
        self.assertEqual(proccess_client_message(message), json.dumps({"response": 200}).encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
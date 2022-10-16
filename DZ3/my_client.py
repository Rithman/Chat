from socket import *
import datetime
import json
import sys

s_address = sys.argv[1]
s_port = 7777

if sys.argv[2]:
    try:
        s_port = int(sys.argv[2])
    except:
        ValueError("Invalid port")

s = socket(AF_INET, SOCK_STREAM)
s.connect((s_address, s_port))
msg = {
    "action": "presence",
    "time": str(datetime.datetime.now()),
    "type": "status",
    "user":
            {
            "account_name": "User-001",
            "status": "Я онлайн!"
    }
}
s.send(json.dumps(msg).encode("utf-8"))
data = json.loads(s.recv(100000).decode("utf-8"))
print(
    f"Server response:\n{data}\nMessage length: {len(data)} bytes")
s.close

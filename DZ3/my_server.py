from socket import *
import sys
import json
import datetime

s_address = "0.0.0.0"
s_port = 7777

if "-a" in sys.argv:
    try:
        s_address = sys.argv[sys.argv.index("-a") + 1]
    except:
        ValueError("Invalid address")

if "-p" in sys.argv:
    try:
        s_port = int(sys.argv[sys.argv.index("-p") + 1])
    except:
        ValueError("Invalid port")


s = socket(AF_INET, SOCK_STREAM)
s.bind((s_address, s_port))
s.listen(5)

while True:
    client, addr = s.accept()
    data = json.loads(client.recv(100000).decode("utf-8"))
    client_name = data["user"]["account_name"]
    client_status = data["user"]["status"]
    print(f"Messsage recieved: {str(data)}")
    response_data = {
        "server_address": s_address,
        "server_port": s_port,
        "client_name": client_name,
        "client_status": client_status,
        "time": str(datetime.datetime.now())
    }
    msg_to_client = json.dumps(response_data).encode("utf-8")
    client.send(msg_to_client)
    client.close

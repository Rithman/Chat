from socket import *
import sys
import json
import logging
import log.server_log_config
from log.server_log_config import FuncCallLogger

logger = logging.getLogger("my_server")


@FuncCallLogger()
def proccess_client_message(message):
    if "action" in message and message["action"] == "presence" and "time" in message \
            and "user" in message and message["user"]["account_name"] == "User-001":
        return json.dumps({"response": 200}).encode("utf-8")
    return json.dumps({"response": 400, "error": "bad_request"}).encode("utf-8")


def main():
    logger.info("App starts")
    s_address = "0.0.0.0"
    s_port = 7777

    try:
        if "-a" in sys.argv:
            s_address = sys.argv[sys.argv.index("-a") + 1]
        if "-p" in sys.argv:
            s_port = int(sys.argv[sys.argv.index("-p") + 1])
        if s_port < 1024 or s_port > 65535:
            raise ValueError
    except IndexError:
        logger.error(f"IndexError. Invalid port {s_port} was given")
        print('After "-p" a valid port number must follow.')
    except ValueError:
        logger.error(f"IndexError. Invalid port {s_port} was given")
        print('Port number must be an integer in 1024-65535 range')
        sys.exit(1)

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((s_address, s_port))
    s.listen(5)

    while True:
        client, addr = s.accept()
        client_message = json.loads(client.recv(100000).decode("utf-8"))
        print(f"Messsage recieved: {str(client_message)}")
        logger.info(f"Message from {addr} recieved. Text: {client_message}")
        message_to_client = proccess_client_message(client_message)
        client.send(message_to_client)
        logger.info(
            f"Message to {addr} sent. Text: {message_to_client.decode('utf-8')}")
        client.close


if __name__ == "__main__":
    main()

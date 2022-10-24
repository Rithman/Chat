from socket import *
import datetime
import json
import sys
import logging
import log.client_log_config


logger = logging.getLogger("my_client")


def create_presence(account_name="User-001"):
    presence_message = json.dumps(
        {
            "action": "presence",
            "time": str(datetime.datetime.now()),
            "type": "status",
            "user":
                {
                "account_name": account_name,
                "status": "Я онлайн!"
            }
        }).encode("utf-8")
    return presence_message


def proccess_response(message):

    message = json.loads(message.decode("utf-8"))
    if "response" in message:
        if message["response"] == 200:
            return "200: OK"
        return f"400: {message['error']}"


def main():
    logger.info("App starts")
    try:
        s_address = sys.argv[1]
        s_port = int(sys.argv[2])
        if s_port < 1024 or s_port > 65535:
            raise ValueError
    except IndexError:
        s_address = "127.0.0.1"
        s_port = 7777
        logger.error("IndexError. Invalid port was given")
    except ValueError:
        logger.error("ValueError. Invalid port was given")
        print('Port number must be an integer in 1024-65535 range')
        sys.exit(1)

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((s_address, s_port))
    s.send(create_presence())
    logger.info(
        f"Message {create_presence().decode('utf-8')} sent to {s_address} {s_port}")
    server_response = s.recv(100000)
    try:
        answer = proccess_response(server_response)
        print(answer)
        logger.error(
            f"Message from {s_address} {s_port} recieved. Text: {answer}")
    except (ValueError, json.JSONDecodeError):
        print("Can't decode server message")
        logger.error(f"Can't decode message: {server_response}")
    s.close


if __name__ == "__main__":
    main()

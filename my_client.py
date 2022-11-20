from socket import *
import time
import sys
import logging
import argparse
import log.client_log_config

from log.client_log_config import FuncCallLogger
from common.utils import send_message, get_message

logger = logging.getLogger("my_client")


username = ""

@FuncCallLogger()
def get_username():
    global username
    name = input("Enter your name: ")
    username = name



@FuncCallLogger()
def message_from_server(message):
    if "action" in message and message["action"] == "message" and "sender" in message and "message_text" in message:
        print(f"Message from {message['sender']}: {message['message_text']}")
        logger.info(f"Message recieved from {message['sender']}:{message['message_text']}")
    else:
        logger.error(f"Incorrect message recieved from server: {message}")



@FuncCallLogger()
def create_message(sock, account_name=username):
    """
    Формирует и возвращает сообщение в виде словаря
    """
    message = input("Your message: ")
    if message == "!!!":
        sock.close()
        sys.exit(0)
    message_dict = {
        "action": "message",
        "time": time.time(),
        "account_name": account_name,
        "message_text": message
    }
    logger.debug(f"Message created: {message_dict}")
    return message_dict


@FuncCallLogger()
def create_presence(account_name=username):
    presence_message = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user":
                {
                "account_name": account_name,
                "status": "Я онлайн!"
            }
    }
    logger.debug(f"Presence message created: {presence_message}")        
    return presence_message


@FuncCallLogger()
def proccess_response(message):
    logger.debug(f"Proccessing server message: {message}")
    if "response" in message:
        if message["response"] == 200:
            return "200: OK"
        elif message["response"] == 400:
            raise Exception(f"400: {message['error']}")
    raise Exception(f"Required field is missing")


@FuncCallLogger()
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default='127.0.0.1', nargs='?')
    parser.add_argument('port', default=7777, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1024 < server_port < 65536:
        logger.critical(f"Wrong port number was given: {server_port}")
        sys.exit(1)

    if client_mode not in ("listen", "send"):
        logger.critical(f"Wrong running mode was given: {client_mode}")
        sys.exit(1)

    return server_address, server_port, client_mode

    

def main():
    get_username()
    s_address, s_port, client_mode = arg_parser()
    logger.info(f"App starts at {s_address} {s_port} in {client_mode} mode")

    try: 
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((s_address, s_port))
        send_message(transport, create_presence())
        answer = proccess_response(get_message(transport))
        logger.info(f"Established connection with server. Server responce: {answer}")
        print(f"Established connection with server {s_address} {s_port}")
    except Exception as e:
        logger.critical(f"Connection error: {e}")
        print(f"Connection error: {e}")
        sys.exit(1)

    else:
        if client_mode == "send":
            print("Send mode:")
        else:
            print("Listen mode:")
        while True:
            if client_mode == "send":
                try:
                    send_message(transport, create_message(transport))
                except Exception as e:
                    logger.error(f"Connection to the server {s_address} was lost")
                    sys.exit(1)

            if client_mode == "listen":
                try:
                    message_from_server(get_message(transport))
                except Exception as e:
                    logger.error(f"Connection to the server {s_address} was lost")
                    sys.exit(1)


if __name__ == "__main__":
    main()

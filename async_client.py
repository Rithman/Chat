from socket import *
import time
import sys
import logging
import argparse
import log.client_log_config
import dis

from threading import Thread
from log.client_log_config import FuncCallLogger
from common.utils import send_message, get_message


class ClientVerifier(type):
    def __init__(self, name, bases, dct):

        globals = []
        methods = []

        for func in dct:
            try:
                res = dis.get_instructions(dct[func])
            except TypeError:
                pass
            else:
                for i in res:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in globals:
                            globals.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in methods:
                            methods.append(i.argval)

        if 'accept' in methods or 'listen' in methods:
            raise TypeError("Invalid 'accept' or 'listen' method used")
        if not ('SOCK_STREAM' in globals and 'AF_INET' in globals):
            raise TypeError("Invalid socket initialization")
        
        super().__init__(name, bases, dct)

class Client(metaclass=ClientVerifier):
    logger = logging.getLogger("my_client")
    USER = ""

    @FuncCallLogger()
    def get_username():
        global USER
        USER = input("Enter your name: ")
        return USER


    @FuncCallLogger()
    def message_from_server(self, message):

        if "action" in message and message["action"] == "message" and "sender" in message and "message_text" in message:
            print(f"Message from {message['sender']}: {message['message_text']}")
            self.logger.info(
                f"Message recieved from {message['sender']}:{message['message_text']}")
        else:
            self.logger.error(f"Incorrect message recieved from server: {message}")


    @FuncCallLogger()
    def create_message(self, sock, account_name=USER, destination=None):
        """
        Формирует и возвращает сообщение в виде словаря
        """
        message = input(">> ")
        if message == "/q":
            sock.close()
            sys.exit(0)
        elif message.split()[0].lower() == "/pm":
            destination = message.split()[1]
            message = " ".join(message.split()[2:])
        elif message == "/help":
            print("/pm {username} - Private message\n/q - Quit\n/help - Help")
            return
        message_dict = {
            "action": "message",
            "time": time.time(),
            "account_name": account_name,
            "destination": destination,
            "message_text": message
        }
        self.logger.debug(f"Message created: {message_dict}")
        return message_dict


    @FuncCallLogger()
    def create_presence(self, account_name=get_username()):
        presence_message = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user":
                    {
                "account_name": account_name,
                    "status": f"Я онлайн!"
            }
        }
        self.logger.debug(f"Presence message created: {presence_message}")
        return presence_message


    @FuncCallLogger()
    def proccess_response(self, message):
        self.logger.debug(f"Proccessing server message: {message}")
        if "response" in message:
            if message["response"] == 200:
                return "200: OK"
            elif message["response"] == 400:
                raise Exception(f"400: {message['error']}")
        raise Exception(f"Required field is missing")


    @FuncCallLogger()
    def arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default='127.0.0.1', nargs='?')
        parser.add_argument('port', default=7777, type=int, nargs='?')
        namespace = parser.parse_args(sys.argv[1:])
        server_address = namespace.addr
        server_port = namespace.port


        if not 1024 < server_port < 65536:
            self.logger.critical(f"Wrong port number was given: {server_port}")
            sys.exit(1)

        return server_address, server_port


    def start(self):
        username = USER
        print("/pm {username} - Private message\n/q - Quit\n/help - Help")
        s_address, s_port = self.arg_parser()
        self.logger.info(f"App starts at {s_address} {s_port}")

        try:
            transport = socket(AF_INET, SOCK_STREAM)
            transport.connect((s_address, s_port))
            send_message(transport, self.create_presence(USER))
            answer = self.proccess_response(get_message(transport))
            self.logger.info(
                f"Established connection with server. Server responce: {answer}")
            print(f"Established connection with server {s_address} {s_port}")
        except Exception as e:
            self.logger.critical(f"Connection error: {e}")
            print(f"Connection error: {e}")
            sys.exit(1)

        def send():
            while True:
                try:
                    send_message(transport, self.create_message(
                        transport,  username, destination=None))
                except Exception as e:
                    self.logger.error(f"Connection to the server {s_address} was lost")
                    sys.exit(1)

        def listen():
            while True:
                if self.message_from_server(get_message(transport)):
                    try:
                        self.message_from_server(get_message(transport))
                    except Exception as e:
                        self.logger.error(
                            f"Connection to the server {s_address} was lost")
                        sys.exit(1)

        t_send = Thread(target=send, name="t_send")
        t_listen = Thread(target=listen, name="t_listen")
        t_send.start()
        t_listen.start()


if __name__ == "__main__":
    client = Client()
    client.start()
import sys
import json
import logging
import select
import argparse
import time
import log.server_log_config
import ipaddress
import dis

from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from log.server_log_config import FuncCallLogger



class ServerVerifier(type):
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

        if 'connect' in methods:
            raise TypeError("Invalid CONNECT method used")
        if not ('SOCK_STREAM' in globals and 'AF_INET' in globals):
            raise TypeError("Invalid socket initialization")
        super().__init__(name, bases, dct)


class ServSocketDescriptor:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.name == "_s_address":
            try:
                addr = ipaddress.ip_address(value)
            except:
                raise ValueError(f"Invalid ip-address: {value}")
            else: instance.__dict__[self.name] = value
        elif self.name == "_s_port":
            if not 1024 < value < 65536:
                raise ValueError(f"IndexError. Invalid port: {value}")
            else:
                instance.__dict__[self.name] = value


class ServSocket:
    s_address = ServSocketDescriptor() 
    s_port = ServSocketDescriptor()

    @FuncCallLogger()
    def __init__(self, addr, port):
        self.s_address = addr
        self.s_port = port

    def get_addr(self):
        return self.s_address, self.s_port

class Server(metaclass=ServerVerifier):
    logger = logging.getLogger("my_server")
    clients_id_dict = {}


    @FuncCallLogger()
    def arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", default=7777, type=int, nargs="?")
        parser.add_argument("-a", default="0.0.0.0", nargs="?")
        namespace = parser.parse_args(sys.argv[1:])
        listen_port = namespace.p
        listen_address = namespace.a

        return listen_address, listen_port


    @FuncCallLogger()
    def proccess_client_message(self, message, messages_list, client):
        self.logger.debug(f"Message proccesing: {message}")
        if "action" in message and message["action"] == "presence" and "time" in message and "user" in message:
            self.clients_id_dict[client] = message["user"]["account_name"]
            send_message(client, {"response": 200})
            return
        elif "action" in message and message["action"] == "message" and "time" in message and "message_text" in message:
            messages_list.append((message["account_name"], message["message_text"], message["destination"]))
            return
        else:
            send_message(client, {"response": 400, "error": "bad request"})
            return

    
    def start(self):
        sock = ServSocket(self.arg_parser()[0], self.arg_parser()[1])
        s_address, s_port = ServSocket.get_addr(sock)
        self.logger.info(f"App starts at {s_address} {s_port}")
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((s_address, s_port))
        s.settimeout(0.5)
        s.listen(5)
        print(f"Server {s_address} {s_port} starts")

        clients, messages = [], [] 

        while True: 
            try:
                client, client_address = s.accept()
            except OSError:
                pass
            else:
                self.logger.info(f"Connection established with {client_address}")
                clients.append(client)

            recv_data_list = []
            send_data_list = []
            err_list = []

            try:
                if clients:
                    recv_data_list, send_data_list, err_list = select.select(clients, clients, [], 0)
            except OSError:
                pass

            if recv_data_list:
                for client_with_message in recv_data_list:
                    try:
                        self.proccess_client_message(get_message(client_with_message), messages, client_with_message)
                    except:
                        self.logger.info(f"Client {client_with_message.getpeername()} disconected from server")
                        # clients.remove(client_with_message)

            if messages and send_data_list:
                message = {
                    "action": "message",
                    "sender": messages[0][0],
                    "time": time.time(),
                    "message_text": messages[0][1],
                    "destination": messages[0][2]
                }
                del messages[0]
                if message.get("destination") in self.clients_id_dict.values():
                    reciever = list(self.clients_id_dict.keys())[list(self.clients_id_dict.values()).index(message.get("destination"))]
                    try:
                        send_message(reciever, message)
                    except:
                        self.logger.info(f"Client {waiting_client.getpeername()} disconected from server")
                        # clients.remove(reciever)
                elif message.get("destination") == None:
                    for waiting_client in send_data_list:
                        try:
                            send_message(waiting_client, message)
                        except:
                            self.logger.info(f"Client {waiting_client.getpeername()} disconected from server")
                            # clients.remove(waiting_client)
                elif message.get("destination") != None and message.get("destination") not in self.clients_id_dict.values():
                    sender = list(self.clients_id_dict.keys())[list(self.clients_id_dict.values()).index(message.get("sender"))]
                    try:
                        message["message_text"] = "ERROR: No such user"
                        send_message(sender, message)
                    except:
                        self.logger.info(f"Client {waiting_client.getpeername()} disconected from server")
                        # clients.remove(sender)  
                    


if __name__ == "__main__":
    serv = Server()
    serv.start()

import sys
import json
import logging
import select
import argparse
import time
import log.server_log_config

from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from log.server_log_config import FuncCallLogger

class Server:
    logger = logging.getLogger("my_server")
    clients_id_dict = {}

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

    
    @FuncCallLogger()
    def arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", default=7777, type=int, nargs="?")
        parser.add_argument("-a", default="0.0.0.0", nargs="?")
        namespace = parser.parse_args(sys.argv[1:])
        listen_port = namespace.p
        listen_address = namespace.a

        if not 1024 < listen_port < 65536:
            self.logger.critical(f"IndexError. Invalid port {listen_port} was given")
            sys.exit(1)

        return listen_address, listen_port


    def start(self):
        s_address, s_port = self.arg_parser()
        self.logger.info(f"App starts at {s_address} {s_port}")
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((s_address, s_port))
        s.settimeout(0.5)
        s.listen(5)

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

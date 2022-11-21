import subprocess
import argparse
import sys
import os
from pathlib import Path

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default='127.0.0.1', nargs='?')
    parser.add_argument('port', default=7777, type=int, nargs='?')
    parser.add_argument('clients', default=1, type=int, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    number_of_clietns = namespace.clients

    if not 1024 < server_port < 65536:
        print(f"Wrong port number was given: {server_port}")
        sys.exit(1)

    return server_address, server_port, number_of_clietns

    

def start(s_address, s_port, num_of_clietns):
    path = f"{os.path.dirname(os.getcwd())}\\async_client.py"
    for client in range(num_of_clietns):
        subprocess.Popen(["python", path, str(s_address), str(s_port)], creationflags=subprocess.CREATE_NEW_CONSOLE)
            
            
if __name__ == "__main__":
    addr, port, num = arg_parser()
    start(addr, port, num)



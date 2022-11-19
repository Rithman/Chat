from socket import *


ADDRESS = ('127.0.0.1', 10000)


def echo_client():

    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(ADDRESS)
        while True:
            data = sock.recv(1024).decode('unicode_escape')
            if data:
                print('Ответ:', data)


if __name__ == '__main__':
    echo_client()

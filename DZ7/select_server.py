import select
from socket import socket, AF_INET, SOCK_STREAM


def read_requests(r_clients, all_clients):
    responses = []
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses.append(data)
        except:

            print('Клиент {} {} отключился'.format(
                sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)

    return responses


def write_responses(requests, w_clients, all_clients):
    for sock in w_clients:
        try:
            for request in requests:
                resp = request.encode('utf-8')
                sock.send(resp.upper())
        except Exception as e:
            print('Клиент {} {} отключился'.format(
                sock.fileno(), sock.getpeername()))
            sock.close()
            all_clients.remove(sock)


def mainloop():
    address = ('', 10000)
    clients = []
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)

    while True:
        try:
            conn, addr = s.accept()
        except OSError as e:
            pass
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
        finally:
            wait = 100
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass

            requests = read_requests(r, clients)
            if requests:
                write_responses(requests, w, clients)


print('сервер запущен')
mainloop()

import json

from log.client_log_config import FuncCallLogger


@FuncCallLogger()
def send_message(sock, message):
    """
    Принимает, кодирует и отправляет словарь.
    :param sock:
    :param message:
    :return:
    """
    if message == None:
        return
    if not isinstance(message, dict):
        raise ValueError
    js_message = json.dumps(message)
    encoded_message = js_message.encode("utf-8")
    sock.send(encoded_message)


@FuncCallLogger()
def get_message(client):
    """
    Принимает сообщение в виде байтов, декодирует, проверяет его и возвращает словарь.
    :param client:
    :return:
    """
    encoded_response = client.recv(1024)
    if isinstance(encoded_response, bytes):
        response = json.loads(encoded_response.decode('utf-8'))
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError

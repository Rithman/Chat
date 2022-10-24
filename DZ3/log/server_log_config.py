import logging
from logging.handlers import TimedRotatingFileHandler

name = __name__

format = logging.Formatter("%(asctime)s %(levelname)-6s %(name)s %(message)s")

server_hand = TimedRotatingFileHandler(
    '.\log\server.log', when="D", interval=1)
server_hand.setFormatter(format)

server_log = logging.getLogger("my_server")
server_log.setLevel(logging.INFO)
server_log.addHandler(server_hand)

if __name__ == "__main__":
    server_hand.info("Test log message")

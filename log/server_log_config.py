import logging
import datetime
import inspect
import pathlib
from logging.handlers import TimedRotatingFileHandler

name = __name__

format = logging.Formatter("%(asctime)s %(levelname)-6s %(name)s %(message)s")
server_hand = TimedRotatingFileHandler(
    f"{pathlib.Path(__file__).parent.resolve()}\log_data\server.log", when="D", interval=1)
server_hand.setFormatter(format)
server_log = logging.getLogger("my_server")
server_log.setLevel(logging.DEBUG)
server_log.addHandler(server_hand)


class FuncCallLogger:
    def __call__(self, func):
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)
            server_log.info(
                f"Function {func.__name__}() was called from function {inspect.stack()[1][3]}()")
            return res
        return decorated


if __name__ == "__main__":
    server_hand.info("Test log message")

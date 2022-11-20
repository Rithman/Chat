import logging
import datetime
import inspect
import os
import pathlib


name = __name__
format = logging.Formatter("%(asctime)s %(levelname)-6s %(name)s %(message)s")
client_hand = logging.FileHandler(
    f"{pathlib.Path(__file__).parent.resolve()}\log_data\client.log")
client_hand.setFormatter(format)
client_log = logging.getLogger("my_client")
client_log.setLevel(logging.DEBUG)
client_log.addHandler(client_hand)


class FuncCallLogger:
    def __call__(self, func):
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)
            client_log.info(
                f"Function {func.__name__}() was called from function {inspect.stack()[1][3]}()")
            return res
        return decorated


if __name__ == "__main__":
    client_log.info("Test msg")

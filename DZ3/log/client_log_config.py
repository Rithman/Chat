import logging
import datetime
import inspect
from functools import wraps


name = __name__
format = logging.Formatter("%(asctime)s %(levelname)-6s %(name)s %(message)s")
client_hand = logging.FileHandler(
    '.\log\log_data\client.log', encoding="utf-8")
client_hand.setFormatter(format)
client_log = logging.getLogger("my_client")
client_log.setLevel(logging.INFO)
client_log.addHandler(client_hand)


class FuncCallLogger:
    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)
            client_log.info(
                f"Function {func.__name__}() was called from function {inspect.stack()[1][3]}()")
            return res
        return decorated


if __name__ == "__main__":
    client_log.info("Test msg")

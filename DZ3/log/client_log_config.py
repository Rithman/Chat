import logging

name = __name__

format = logging.Formatter("%(asctime)s %(levelname)-6s %(name)s %(message)s")

client_hand = logging.FileHandler('.\log\log_data\client.log')
client_hand.setFormatter(format)

client_log = logging.getLogger("my_client")
client_log.setLevel(logging.INFO)
client_log.addHandler(client_hand)

if __name__ == "__main__":
    client_hand.info("Test log message")

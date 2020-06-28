from modules.internal_bus.subscriber import Subscriber
from config.config import TOPICS_DATA
import time


def recv_data():

    sub = Subscriber(TOPICS_DATA)

    while True:
        t, mes = sub.recv()

        delay_ms = (time.time() - mes["time"]) * 1000

        print(t, delay_ms, mes["data"], "\n")


if __name__ == '__main__':
    recv_data()

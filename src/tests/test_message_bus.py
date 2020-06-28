from modules.internal_bus.message_bus import MessageBus
from modules.internal_bus.publisher import Publisher
from modules.internal_bus.subscriber import Subscriber

from multiprocessing import Process
from random import randint
import time


def run_sub():
    sub = Subscriber(["4"])

    count = 0

    while True:
        _, _ = sub.recv()
        count += 1
        print("Recv", count)


def run_pub():
    pub = Publisher()

    count = 0

    init_time = time.time()

    while True:

        curr_time = time.time()

        t = str(randint(0, 10))
        m = {
            "time": curr_time
        }

        pub.send(t, m)

        count += 1
        elapsed_time = curr_time-init_time

        print("Send", count)
        print("Elapsed Time", elapsed_time)
        print("Messages/Second", count/elapsed_time)


def main():
    p1 = Process(target=MessageBus.run, args=())
    p1.start()

    p2 = Process(target=run_sub, args=())
    p2.start()

    p3 = Process(target=run_pub, args=())
    p3.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()
        p3.terminate()


if __name__ == '__main__':
    main()

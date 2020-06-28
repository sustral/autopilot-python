from modules.internal_bus.message_bus import MessageBus
from modules.internal_bus.subscriber import Subscriber
from modules.internal_bus.publisher import Publisher
from modules.remote_vehicle.vehicle_connection import VehicleConnection

from multiprocessing import Process
from random import randint
import time


def read_data():
    sub = Subscriber(["baro_raw", "mpu_raw", "lsm_raw"])

    while True:
        t, mes = sub.recv()

        print(t, mes)


def send_inst():

    pub = Publisher()

    motor_inst_template = {
        "fl": 0,
        "fr": 0,
        "bl": 0,
        "br": 0
    }

    while True:
        inst = motor_inst_template.copy()
        inst["fl"] = randint(0, 25)
        inst["fr"] = randint(0, 25)
        inst["bl"] = randint(0, 25)
        inst["br"] = randint(0, 25)

        pub.send("motor_inst", inst)

        time.sleep(0.1)


def main():
    p1 = Process(target=MessageBus.run, args=())
    p1.start()

    p2 = Process(target=VehicleConnection.run, args=())
    p2.start()

    p3 = Process(target=read_data, args=())
    p3.start()

    p4 = Process(target=send_inst, args=())
    p4.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()
        p3.terminate()
        p4.terminate()


if __name__ == '__main__':
    main()

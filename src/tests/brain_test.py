from modules.internal_bus.message_bus import MessageBus
from modules.remote_vehicle.vehicle_zmq import VehicleZMQ

from modules.internal_bus.subscriber import Subscriber
from modules.internal_bus.publisher import Publisher

from multiprocessing import Process
from random import randint
import time


def recv_data():

    sub = Subscriber(["baro_raw", "mpu_raw", "lsm_raw"])

    while True:
        t, mes = sub.recv()

        delay_ms = (time.time() - mes["time"]) * 1000

        print(t, delay_ms, mes["data"], "\n")


def send_inst():

    pub = Publisher()

    motor_inst_template = {
        "fl": 0,
        "fr": 0,
        "bl": 0,
        "br": 0
    }

    start_time = time.time()

    cycle_state = 0

    while (time.time() - start_time) < 10.0:
        inst = motor_inst_template.copy()
        inst["fl"] = 20 if cycle_state == 0 else 0
        inst["fr"] = 20 if cycle_state == 3 else 0
        inst["bl"] = 20 if cycle_state == 1 else 0
        inst["br"] = 20 if cycle_state == 2 else 0

        cycle_state += 1
        cycle_state = 0 if cycle_state > 3 else cycle_state

        pub.send("motor_inst", inst)

        time.sleep(1.0)

    while True:
        inst = motor_inst_template.copy()
        inst["fl"] = randint(0, 25)
        inst["fr"] = randint(0, 25)
        inst["bl"] = randint(0, 25)
        inst["br"] = randint(0, 25)

        pub.send("motor_inst", inst)

        time.sleep(0.1)


def main():
    processes = list()

    processes.append(Process(target=MessageBus.run, args=()))

    processes.append(Process(target=VehicleZMQ.run_feed_in, args=()))
    processes.append(Process(target=VehicleZMQ.run_feed_out, args=()))

    processes.append(Process(target=recv_data, args=()))
    processes.append(Process(target=send_inst, args=()))

    for p in processes:
        p.start()

    try:

        start_time = time.time()

        while (time.time() - start_time) < 60.0:
            time.sleep(10)

    except KeyboardInterrupt:
        pass
    finally:
        for p in processes:
            p.terminate()


if __name__ == '__main__':
    main()

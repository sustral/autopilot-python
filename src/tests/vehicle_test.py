from modules.internal_bus.message_bus import MessageBus
from modules.remote_vehicle.vehicle_zmq import VehicleZMQ
from components.navio.barometer import Barometer
from components.navio.imu import IMU
from components.navio.motor import Motor

from multiprocessing import Process
import time


def main():
    processes = list()

    processes.append(Process(target=MessageBus.run, args=()))

    processes.append(Process(target=VehicleZMQ.run_feed_in, args=()))
    processes.append(Process(target=VehicleZMQ.run_feed_out, args=()))

    processes.append(Process(target=Barometer.run, args=()))

    processes.append(Process(target=IMU.run, args=("mpu",)))
    processes.append(Process(target=IMU.run, args=("lsm",)))

    processes.append(Process(target=Motor.run, args=(0, "fr")))
    processes.append(Process(target=Motor.run, args=(1, "bl")))
    processes.append(Process(target=Motor.run, args=(2, "fl")))
    processes.append(Process(target=Motor.run, args=(3, "br")))

    for p in processes:
        p.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()


if __name__ == '__main__':
    main()

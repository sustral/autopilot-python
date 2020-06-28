'''
Wrapper around the two IMU drivers that publishes measurements every 0.03 seconds.
'''

import time
from drivers.navio.mpu9250 import MPU9250
from drivers.navio.lsm9ds1 import LSM9DS1
from modules.internal_bus.publisher import Publisher


class IMU:

    @staticmethod
    def run(name):

        pub = Publisher()

        imu = None
        topic = None

        if name == "mpu":
            imu = MPU9250()
            topic = "mpu_raw"
        elif name == "lsm":
            imu = LSM9DS1()
            topic = "lsm_raw"

        imu.initialize()

        time.sleep(1)

        while True:
            acc, gyr, mag = imu.getMotion9()
            curr_time = time.time()

            message = {
                "time": curr_time,
                "data": {
                    "acc": acc,
                    "gyr": gyr,
                    "mag": mag
                }
            }

            pub.send(topic, message)

            time.sleep(0.025)

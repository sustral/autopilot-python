'''
Wrapper around the MS5611 driver that publishes measurements every 0.05 seconds.
'''

import time
from drivers.navio.ms5611 import MS5611
from modules.internal_bus.publisher import Publisher


class Barometer:

    @staticmethod
    def run():

        pub = Publisher()

        barometer = MS5611()
        barometer.initialize()

        time.sleep(1)

        while True:
            barometer.refreshPressure()
            time.sleep(0.01)
            barometer.readPressure()

            barometer.refreshTemperature()
            time.sleep(0.01)
            barometer.readTemperature()

            barometer.calculatePressureAndTemperature()

            temp = barometer.TEMP
            pres = barometer.PRES
            curr_time = time.time()

            message = {
                "time": curr_time,
                "data": {
                    "temp": temp,
                    "pres": pres
                }
            }

            pub.send("baro_raw", message)

            time.sleep(0.025)

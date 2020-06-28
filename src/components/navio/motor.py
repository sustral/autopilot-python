'''
Wrapper around the PWM (motor) driver that scans the instruction queue every 0.01 seconds.
'''

from drivers.navio.pwm import PWM
from modules.internal_bus.subscriber import Subscriber
import time


class Motor:

    @staticmethod
    def run(pwm_id, name):

        period = 50
        duty_min = 1.000
        duty_max = 2.000
        buffer = 0.100
        throttle_cycle_conversion = (duty_max - (duty_min + buffer)) / 100.0

        sub = Subscriber(["motor_inst"])

        with PWM(pwm_id) as pwm:
            pwm.set_period(period)
            pwm.enable()

            curr_cycle = duty_min + buffer

            last_inst = time.time()

            while True:
                pwm.set_duty_cycle(curr_cycle)

                topic, message = sub.recv_noblock()

                if topic:
                    throttle_value = int(message[name])
                    temp_cycle = duty_min + buffer + (throttle_value * throttle_cycle_conversion)
                    curr_cycle = temp_cycle if temp_cycle <= duty_max else duty_max
                    last_inst = time.time()
                else:
                    curr_time = time.time()

                    # Shut off the motors if there has not been a new instruction in 2 seconds
                    if (curr_time - last_inst) > 2.0:
                        curr_cycle = duty_min + buffer
                        last_inst = curr_time

                time.sleep(0.01)

'''
Electronic Speed Controllers are typically calibrated using a radio, but that method is imprecise
and does not lend itself to setting specific values for the duty cycles. Using this utility, one can set
multiple ESCs to exacting levels.
'''

import drivers.navio.pwm as pwmDev
from threading import Thread
import queue
from queue import Queue
import time


def mass_set_period(pList, period=50):
    for p in pList:
        p.set_period(period)


def mass_enable(pList):
    for p in pList:
        p.enable()


def start_messaging(*args):
    q = args[0]
    f = args[1]
    pList = args[2]
    curr_cycle = args[3]

    while True:
        for p in pList:
            p.set_duty_cycle(curr_cycle)

        try:
            curr_cycle = q.get_nowait()
            q.task_done()
        except queue.Empty:
            pass

        try:
            _ = f.get_nowait()
            f.task_done()
            break
        except queue.Empty:
            pass


def mass_set_duty_cycle(q, duty_cycle):
    q.put(float(duty_cycle))


def kill(f):
    f.put("Exit")


def main():
    duty_min = float(input("duty_min: "))
    duty_max = float(input("duty_max: "))
    duty_mid = float(input("duty_mid: "))


    with pwmDev.PWM(0) as pwm0, pwmDev.PWM(1) as pwm1, pwmDev.PWM(2) as pwm2, pwmDev.PWM(3) as pwm3:

        pwmList = [pwm0, pwm1, pwm2, pwm3]

        mass_set_period(pwmList)
        mass_enable(pwmList)

        q = Queue() # Instruction queue containing the target duty cycle
        f = Queue() # A queue that, if ever not empty, indicates the process has finished

        t1 = Thread(target=start_messaging, args=(q,f,pwmList,duty_min,))
        t1.start()

        time.sleep(3)

        mass_set_duty_cycle(q, duty_max)

        _ = input("Plug In Battery")

        mass_set_duty_cycle(q, duty_min)

        _ = input("Calibration Complete")

        mass_set_duty_cycle(q, duty_mid)

        _ = input("Finish")

        mass_set_duty_cycle(q, duty_min)

        time.sleep(1)

        kill(f)

        time.sleep(1)


if __name__ == '__main__':
    main()

import time
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from PiController import PIDControl
import math

k = 0.22
T_m = 0.16
T = 0.16
TIME_STEP = 0.03

KP = 1 / k * (2 * T_m / T - 1)  
KI = T_m / (T ** 2 * k)   
target_speed = 10

print(KP, KI)

PID_motor = PIDControl(KP, KI, 0, 0, TIME_STEP)

motor = LargeMotor(OUTPUT_B)


def move():
    with open('file.csv', 'w') as stream:
        time_start = time.time()

        while time.time() - time_start < 10:

            tic = time.time()

            current_speed_left = motor.speed * math.pi / 180
            speed_error = target_speed - current_speed_left
            
            PID_motor.updatePI(speed_error)
            
            motor.run_direct(duty_cycle_sp = PID_motor.value)

            stream.write('{}, {}\n'.format(time.time() - time_start, speed_error))
            
            toc = time.time()
            timeDiff = toc - tic
            if timeDiff < TIME_STEP:
                time.sleep(TIME_STEP - timeDiff)
            else:
                print("Warning! Out of time")

    motor.stop()
    

move()



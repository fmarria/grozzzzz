import time
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from PiController import PIDControl
from keyboard_moving import action
import threading
import math

k = 0.22
T_m = 0.2
T = 0.2
TIME_STEP = 0.05

KD = 0
# KP = 1/k * (2 * (T_m + k * KD) / T - 1)
# KI = (T_m + k * KD) / k
KP = 1 / k * (2 * T_m / T - 1)
KI = T_m / (T ** 2 * k)   


r = 56 / 2 / 1000
B = 174 / 1000

right_pid = PIDControl(KP, KI, KD, 0, 0, TIME_STEP)
left_pid = PIDControl(KP, KI, KD, 0, 0, TIME_STEP)
left_target_speed = 20
right_target_speed = 20

left_motor = LargeMotor(OUTPUT_B)
right_motor = LargeMotor(OUTPUT_A)

status = {'v': 0, 'w': 0}


def move(status):
    with open('file.csv', 'w') as stream:
        time_start = time.time()

        while time.time() - time_start < 120:
            tic = time.time()

            # v_ref = 0.1
            v_ref = status['v']
            # w_ref = 0
            w_ref = status['w']
            # print(v_ref, w_ref)

            if not (v_ref or w_ref):
                
                left_motor.stop()
                right_motor.stop()
                # print('stop')

            w_r = 1/r * v_ref + B / (2 * r) * w_ref
            w_l = 1/r * v_ref - B / (2 * r) * w_ref

            current_speed_left = left_motor.speed * math.pi / 180
            current_speed_right = right_motor.speed * math.pi / 180

            left_speed_error = w_l - current_speed_left
            right_speed_error = w_r - current_speed_right
            
            left_pid.updatePI(left_speed_error)
            right_pid.updatePI(right_speed_error)
            
            left_motor.run_direct(duty_cycle_sp = left_pid.value)
            right_motor.run_direct(duty_cycle_sp = right_pid.value)

            stream.write('{}, {}, {}\n'.format(time.time() - time_start, left_speed_error, right_speed_error))
            
            toc = time.time()
            timeDiff = toc - tic
            if timeDiff < TIME_STEP:
                time.sleep(TIME_STEP - timeDiff)
            else:
                print("Warning! Out of time")

    left_motor.stop()
    right_motor.stop()

    print('Motor\'s have been stopped!')


if __name__=="__main__":
    try:
        thr = threading.Thread(target=action, args=(status,),name='keyboard')
        thr.start()

        move(status)
    except Exception as e:
        print(e)
    finally:
        left_motor.stop()
        right_motor.stop()





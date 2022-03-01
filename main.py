import kociemba
import RPi.GPIO as GPIO
import time

# 持ち手の向き 垂直=>0 水平=>1
HOR = [0, 0, 0, 0]  # [L, R, F, B]


def solve(cubestr):
    return kociemba.solve(cubestr)


def rotate(mtr, mode):
    delay = .001
    pins = [
        # [direction, step],
        [3, 4],  # L
        [17, 27],  # R
        [9, 11],  # F
        [14, 15]  # B
    ]
    direction = pins[mtr][0]
    step = pins[mtr][1]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(direction, GPIO.OUT)
    GPIO.setup(step, GPIO.OUT)

    if mode == 0:  # 90°回転
        GPIO.output(direction, 0)
        step_count = 50
        HOR[mtr] = (HOR[mtr] + 1) % 2
    elif mode == 1:  # -90°回転
        GPIO.output(direction, 1)
        step_count = 50
        HOR[mtr] = (HOR[mtr] + 1) % 2
    elif mode == 2:  # 180°回転
        GPIO.output(direction, 0)
        step_count = 100

    for _ in range(step_count):
        GPIO.output(step, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(step, GPIO.LOW)
        time.sleep(delay)

    GPIO.cleanup([direction, step])

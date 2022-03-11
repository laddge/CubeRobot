import kociemba
import RPi.GPIO as GPIO
import time
from threading import Thread

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


def chwid(drc, grab):
    pins = [23, 24]  # [LR, FB]
    pin = pins[drc]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)
    pwm.start(0.0)

    dcs = [[10, 4.5], [4, 11]]
    dc = dcs[drc][grab]
    pwm.ChangeDutyCycle(dc)
    time.sleep(.3)

    GPIO.cleanup(pin)


def run(movestr):
    moves = movestr.strip().split(" ")
    while moves:
        if moves[0][0] == "L" or moves[0][0] == "R":
            if HOR[2] and HOR[3]:
                chwid(1, 0)
                t0 = Thread(target=rotate, args=(2, 0))
                t1 = Thread(target=rotate, args=(3, 0))
                t0.start()
                t1.start()
                t0.join()
                t1.join()
            elif HOR[2]:
                chwid(1, 0)
                rotate(2, 0)
            elif HOR[3]:
                chwid(1, 0)
                rotate(3, 0)
            chwid(1, 1)
            if moves[0][0] == "L":
                mtr0 = 0
            else:
                mtr0 = 1
            if len(moves[0]) == 1:
                mode0 = 0
            elif moves[0][1] == "'":
                mode0 = 1
            else:
                mode0 = 2
            if len(moves) > 1:
                if moves[1][0] == "L" or moves[1][0] == "R":
                    if moves[1][0] == "L":
                        mtr1 = 0
                    else:
                        mtr1 = 1
                    if len(moves[1]) == 1:
                        mode1 = 0
                    elif moves[1][1] == "'":
                        mode1 = 1
                    else:
                        mode1 = 2
                    t0 = Thread(target=rotate, args=(mtr0, mode0))
                    t1 = Thread(target=rotate, args=(mtr1, mode1))
                    t0.start()
                    t1.start()
                    t0.join()
                    t1.join()
                    moves = moves[2:]
                else:
                    rotate(mtr0, mode0)
                    moves = moves[1:]
            else:
                rotate(mtr0, mode0)
                moves = moves[1:]
        elif moves[0][0] == "F" or moves[0][0] == "B":
            if HOR[0] and HOR[1]:
                chwid(0, 0)
                t0 = Thread(target=rotate, args=(0, 0))
                t1 = Thread(target=rotate, args=(1, 0))
                t0.start()
                t1.start()
                t0.join()
                t1.join()
            elif HOR[0]:
                chwid(0, 0)
                rotate(0, 0)
            elif HOR[1]:
                chwid(0, 0)
                rotate(1, 0)
            chwid(0, 1)
            if moves[0][0] == "F":
                mtr0 = 2
            else:
                mtr0 = 3
            if len(moves[0]) == 1:
                mode0 = 0
            elif moves[0][1] == "'":
                mode0 = 1
            else:
                mode0 = 2
            if len(moves) > 1:
                if moves[1][0] == "F" or moves[1][0] == "B":
                    if moves[1][0] == "F":
                        mtr1 = 2
                    else:
                        mtr1 = 3
                    if len(moves[1]) == 1:
                        mode1 = 0
                    elif moves[1][1] == "'":
                        mode1 = 1
                    else:
                        mode1 = 2
                    t0 = Thread(target=rotate, args=(mtr0, mode0))
                    t1 = Thread(target=rotate, args=(mtr1, mode1))
                    t0.start()
                    t1.start()
                    t0.join()
                    t1.join()
                    moves = moves[2:]
                else:
                    rotate(mtr0, mode0)
                    moves = moves[1:]
            else:
                rotate(mtr0, mode0)
                moves = moves[1:]
        else:
            if HOR[0] == HOR[1] == 0:
                if HOR[2] and HOR[3]:
                    chwid(1, 0)
                    t0 = Thread(target=rotate, args=(2, 0))
                    t1 = Thread(target=rotate, args=(3, 0))
                    t0.start()
                    t1.start()
                    t0.join()
                    t1.join()
                elif HOR[2]:
                    chwid(1, 0)
                    rotate(2, 0)
                elif HOR[3]:
                    chwid(2, 0)
                    rotate(3, 0)
                chwid(1, 1)
            if HOR[0] == HOR[1]:
                chwid(0, 0)
                rotate(0, 0)
                chwid(0, 1)
            chwid(1, 0)
            t0 = Thread(target=rotate, args=(0, 0))
            t1 = Thread(target=rotate, args=(1, 1))
            t0.start()
            t1.start()
            t0.join()
            t1.join()
            chwid(1, 1)
            new = []
            for move in moves:
                if move[0] == "U":
                    new.append(move.replace("U", "F"))
                elif move[0] == "F":
                    new.append(move.replace("F", "D"))
                elif move[0] == "D":
                    new.append(move.replace("D", "B"))
                elif move[0] == "B":
                    new.append(move.replace("B", "U"))
                else:
                    new.append(move)
            moves = new

import kociemba
import cv2
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
    time.sleep(.3)


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
    time.sleep(.3)


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
            chwid(0, 1)
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


def getcolor(cap):
    _, img = cap.read()
    pieces = [
        [(500, 100), (580, 100), (500, 20)],
        [(480, 190), (480, 250), (480, 310)],
        [(470, 400), (570, 400), (470, 470)],
        [(260, 100), (320, 100), (380, 100)],
        [(320, 200), (260, 300), (380, 300)],
        [(260, 420), (320, 420), (380, 420)],
        [(160, 100), (60, 100), (160, 20)],
        [(150, 190), (150, 250), (150, 310)],
        [(160, 400), (60, 400), (160, 470)]
    ]
    colors = []
    for piece in pieces:
        hues = []
        sats = []
        for point in piece:
            hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv = hsvimg[point[1], point[0]]
            hues.append(hsv[0])
            sats.append(hsv[1])
        hue = sum(hues) / len(hues)
        sat = sum(sats) / len(sats)
        if sat < 100:
            color = "w"
        elif hue <= 10 or 150 < hsv[0]:
            color = "r"
        elif 10 < hue <= 30:
            color = "o"
        elif 30 < hue <= 40:
            color = "y"
        elif 40 < hue <= 90:
            color = "g"
        else:
            color = "b"
        colors.append(color)
    return colors


def scan():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cubestr = [""] * 54
    c0 = getcolor(cap)
    cubestr[18:27] = c0
    run("L R")
    c1 = getcolor(cap)
    cubestr[0] = c1[0]
    cubestr[3] = c1[3]
    cubestr[6] = c1[6]
    cubestr[29] = c1[2]
    cubestr[32] = c1[5]
    cubestr[35] = c1[8]
    run("L R")
    c2 = getcolor(cap)
    cubestr[45] = c2[8]
    cubestr[47] = c2[6]
    cubestr[48] = c2[5]
    cubestr[50] = c2[3]
    cubestr[51] = c2[2]
    cubestr[53] = c2[0]
    run("L R")
    c3 = getcolor(cap)
    cubestr[2] = c3[2]
    cubestr[5] = c3[5]
    cubestr[8] = c3[8]
    cubestr[27] = c3[0]
    cubestr[30] = c3[3]
    cubestr[33] = c3[6]
    run("L R F B")
    c4 = getcolor(cap)
    cubestr[9:12] = c4[:3]
    cubestr[42:45] = c4[6:]
    run("F B")
    c5 = getcolor(cap)
    cubestr[46] = c5[1]
    cubestr[52] = c5[7]
    run("F B")
    c6 = getcolor(cap)
    cubestr[15:18] = c6[6:]
    cubestr[36:39] = c6[:3]
    run("F B U D")
    c7 = getcolor(cap)
    cubestr[4] = c7[4]
    cubestr[14] = c7[1]
    cubestr[41] = c7[7]
    run("F B")
    c8 = getcolor(cap)
    cubestr[28] = c8[7]
    cubestr[34] = c8[1]
    run("F B")
    c9 = getcolor(cap)
    cubestr[12] = c9[7]
    cubestr[39] = c9[1]
    run("F B")
    cap.release()

    colors = "wrgyob"
    U = cubestr[4]
    F = cubestr[22]
    D = colors[(colors.find(U) + 3) % 6]
    B = colors[(colors.find(F) + 3) % 6]
    cubestr[31] = D
    cubestr[49] = B
    rl = colors.translate(str.maketrans("", "", f"{U}{F}{D}{B}"))
    if colors.find(U) % 3 + colors.find(F) % 3 in [1, 3]:
        if colors.find(U) % 3 < colors.find(F) % 3:
            i = 1
        else:
            i = 0
    else:
        if colors.find(U) % 3 < colors.find(F) % 3:
            i = 0
        else:
            i = 1
    if colors.find(U) > 2:
        i = (i + 1) % 2
    if colors.find(F) > 2:
        i = (i + 1) % 2
    R = rl[i]
    L = rl[(i + 1) % 2]
    cubestr[13] = R
    cubestr[40] = L

    cubestr = "".join(cubestr).translate(str.maketrans(f"{U}{F}{D}{B}{R}{L}", "UFDBRL"))
    return cubestr

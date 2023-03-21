from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from datetime import datetime

cs2 = ColorSensor(INPUT_2)
cs1 = ColorSensor(INPUT_1)

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

squareTurn = 6
rollingTime = 0.2


def getColor():
    return sum(cs1.raw)/3, sum(cs2.raw)/3


print("start")
while True:
    avg_left = sum(cs1.raw) / 3
    avg_right = sum(cs2.raw) / 3

    if abs(avg_right - avg_left) <= 60:
        tank_drive.on(-15, -15)
    elif avg_right > avg_left:
        tank_drive.on(20, -5)
    else:
        tank_drive.on(-5, 20)

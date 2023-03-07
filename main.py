from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

cs2 = ColorSensor(INPUT_2)
cs1 = ColorSensor(INPUT_1)

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

squareTurn = 6
rollingTime = 0.2


def getColor():
    return sum(cs1.raw)/3, sum(cs2.raw)/3


while True:
    avg_left = sum(cs1.raw) / 3
    avg_right = sum(cs2.raw) / 3
    # print(avg_left, avg_right)
    if avg_right > avg_left:
        tank_drive.on_for_seconds(
            SpeedPercent(-5), SpeedPercent(-25), rollingTime)  # turn left
    else:
        tank_drive.on_for_seconds(
            SpeedPercent(-25), SpeedPercent(-5), rollingTime)  # turn right
    if min(getColor()) > 130:
        cnt = 0
        while min(getColor()) > 130 and cnt < squareTurn:
            tank_drive.on_for_seconds(SpeedPercent(
                17), SpeedPercent(-20), rollingTime)  # turn left
            cnt += 1

        cnt = 0
        while min(getColor()) > 130 and cnt < 2*squareTurn:
            tank_drive.on_for_seconds(
                SpeedPercent(-20), SpeedPercent(17), rollingTime)  # turn right
            cnt += 1

    # sleep(0.5)

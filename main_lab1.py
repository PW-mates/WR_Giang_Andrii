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
    # print(avg_left, avg_right)

    if abs(avg_right - avg_left) <= 60:
        tank_drive.on(-15, -15)
        # tank_drive.on_for_seconds(
        #     SpeedPercent(-15), SpeedPercent(-15), rollingTime)  # go straigh
    elif avg_right > avg_left:
        tank_drive.on(20, -5)
        # tank_drive.on_for_seconds(
        #     SpeedPercent(-5), SpeedPercent(-25), rollingTime)  # turn left
    else:
        tank_drive.on(-5, 20)
        # tank_drive.on_for_seconds(
        #     SpeedPercent(-25), SpeedPercent(-5), rollingTime)  # turn right
    # if min(getColor()) > 130:
    #     cnt = 0
    #     start = datetime.now()
    #     while min(getColor()) > 130 and datetime.now() - start <= 3:
    #         tank_drive.on(17, -20)
    #         # tank_drive.on_for_seconds(SpeedPercent(
    #         #     17), SpeedPercent(-20), rollingTime)  # turn left
    #         cnt += 1

    #     cnt = 0
    #     start = datetime.now()
    #     while min(getColor()) > 130 and datetime.now() - start <= 6:
    #         tank_drive.on(17, -20)
    #         # tank_drive.on_for_seconds(
    #         #     SpeedPercent(-20), SpeedPercent(17), rollingTime)  # turn right
    #         cnt += 1

    # sleep(0.5)

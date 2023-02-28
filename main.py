from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

cs1 = ColorSensor(INPUT_1)
cs2 = ColorSensor(INPUT_2)

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)


while True:
    # print(cs1.raw)
    # print(cs2.raw)
    # tank_drive.on_for_seconds(SpeedPercent(60), SpeedPercent(30), 3)
    avg_left = sum(cs1.raw) / 3
    avg_right = sum(cs2.raw) / 3
    # print(avg_left, avg_right)
    if avg_right > avg_left:
        tank_drive.on_for_seconds(SpeedPercent(-10), SpeedPercent(-15), 0.5)
    else:
        tank_drive.on_for_seconds(SpeedPercent(-15), SpeedPercent(-10), 0.5)

    sleep(0.5)
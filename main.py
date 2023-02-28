from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

cs1 = ColorSensor(INPUT_1)
cs2 = ColorSensor(INPUT_2)

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)


tank_drive.on_for_seconds(SpeedPercent(-30), SpeedPercent(-30), 3)

# while True:
#     # print(cs1.raw)
#     # print(cs2.raw)
#     tank_drive.on_for_seconds(SpeedPercent(60), SpeedPercent(30), 3)
#     sleep(3)

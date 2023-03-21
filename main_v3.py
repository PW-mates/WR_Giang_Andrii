from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from time import sleep, time

cs1 = ColorSensor(INPUT_1)
cs2 = ColorSensor(INPUT_2)
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
left_speed = 5
right_speed = 5
print("start")
while True:
    print(cs1.hsv, cs2.hsv)
    if cs1.hsv[2] > cs2.hsv[2]*1.3:
        left_speed = max(left_speed - (cs1.hsv[2]-cs2.hsv[2]) / 50, 0)
        right_speed = min(right_speed + (cs1.hsv[2]-cs2.hsv[2]) - (right_speed - left_speed) / 13 / 70, 8)
    elif cs1.hsv[2]*1.3 < cs2.hsv[2]:
        left_speed = min(left_speed + (cs2.hsv[2]-cs1.hsv[2]) / 70  - (-right_speed + left_speed) / 13, 8)
        right_speed = max(right_speed - (cs2.hsv[2]-cs1.hsv[2]) / 50, 0)
    # left_speed = (100 - cs1.hsv[2]) / 10
    # right_speed = (100 - cs2.hsv[2] ) / 10
    tank_drive.on(left_speed, right_speed)
    

from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from time import sleep, time

BLACK = (0, 0, 0)
WHITE = (258, 258, 258)
YELLOW = ()
RED = ()
GREEN = ()


cs1 = ColorSensor(INPUT_1)
cs2 = ColorSensor(INPUT_2)

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

squareTurn = 5
rollingTime = 0.2


def get_sensor():
    return sum(cs1.raw)/3, sum(cs2.raw)/3


def get_color_sensor_1():
    # LEFT
    return cs1.rgb


def get_color_sensor_2():
    # RIGHT
    return cs2.rgb


def get_color_sensors():
    return (get_color_sensor_1, get_color_sensor_2)


def turn(angle):
    pass


def turn_left():
    tank_drive.on_for_seconds(
        SpeedPercent(-5), SpeedPercent(-20), rollingTime)


def turn_right():
    tank_drive.on_for_seconds(
        SpeedPercent(-20), SpeedPercent(-5), rollingTime)


while True:
    tank_drive.on_for_seconds(
        SpeedPercent(-30), SpeedPercent(-30), rollingTime)

    left, right = get_sensor()
    while left < 100 and right > 100:
        left, right = get_sensor()
        # tank_drive.on(-10, -50)
        tank_drive.on_for_seconds(
            SpeedPercent(0), SpeedPercent(-30), rollingTime)   # turn left

    left, right = get_sensor()
    while right < 100 and left > 100:
        left, right = get_sensor()
        tank_drive.on_for_seconds(
            SpeedPercent(-30), SpeedPercent(0), rollingTime)   # turn left
        # tank_drive.on(-50, -10)

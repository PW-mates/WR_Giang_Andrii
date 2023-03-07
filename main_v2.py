from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from time import sleep, time

BLACK = (0, 0, 0)
WHITE = (258, 258, 258)
YELLOW = ()
RED = ()
GREEN = ()


class Logger:

    def __init__(self) -> None:
        print("Logger start")

    def print_rgb_sensor():
        print(f"sensor1 = {cs1.rgb}")
        print(f"sensor2 = {cs1.rgb}")

    def print_distance_sensor():
        pass


cs1 = ColorSensor(INPUT_1)
cs2 = ColorSensor(INPUT_2)

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

squareTurn = 5
rollingTime = 0.2


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


time_start = time()
log = Logger()

while True:
    if time_start - time() > 3:
        log.print_rgb_sensor()
        time_start = time()

    if sum(get_color_sensor_2) / 3 > sum(get_color_sensor_1) / 3:
        turn_left()
    else:
        turn_right()
    if min(get_color_sensors()) > 130:
        cnt = 0
        while min(get_color_sensors()) > 130 and cnt < squareTurn:
            tank_drive.on_for_seconds(SpeedPercent(
                20), SpeedPercent(-20), rollingTime)  # turn left
            cnt += 1

        cnt = 0
        while min(get_color_sensors()) > 130 and cnt < 2*squareTurn:
            tank_drive.on_for_seconds(
                SpeedPercent(-20), SpeedPercent(20), rollingTime)  # turn right
            cnt += 1

    # sleep(0.5)

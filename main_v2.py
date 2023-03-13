from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from time import sleep, time

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
YELLOW = [5, 5, 5]
RED = [5, 5, 5]
GREEN = [5, 5, 5]

cs1 = ColorSensor(INPUT_1)
cs2 = ColorSensor(INPUT_2)
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

# log = Logger()
INITIAL_RIGHT_SPEED = 15
INITIAL_LEFT_SPEED = 15
MIN_SPEED = -5
MAX_SPEED = 20
STEP = 0.2

right_speed = INITIAL_RIGHT_SPEED
left_speed = INITIAL_LEFT_SPEED

# class Logger:

#     def __init__(self) -> None:
#         print("Logger start")

#     def print_rgb_sensor(self):
#         print(f"sensor1 = {cs1.rgb}")
#         print(f"sensor2 = {cs2.rgb}")

#     def print_distance_sensor(self):
#         pass


def get_color_sensor_1():
    # LEFT
    return cs1.rgb

def get_color_sensor_2():
    # RIGHT
    return cs2.rgb

def get_color_sensors():
    return (get_color_sensor_1(), get_color_sensor_2())
    
def check_zone():
    sensors = get_color_sensors()
    if sensors == (RED, RED):
        print("RED Zone")
    if sensors == (YELLOW, YELLOW):
        print("YELLOW Zone")
    if sensors == (GREEN, GREEN):
        print("GREEN Zone")


def correct_speed():
    global left_speed
    global right_speed
    if sum(get_color_sensor_2()) / 3 > sum(get_color_sensor_1()) / 3:
        if left_speed < right_speed:
            left_speed = INITIAL_LEFT_SPEED
            right_speed = INITIAL_RIGHT_SPEED
        else:
            right_speed = max(MIN_SPEED, right_speed - STEP)
            left_speed = min(MAX_SPEED, left_speed + STEP)
    else:
        if left_speed > right_speed:
            left_speed = INITIAL_LEFT_SPEED
            right_speed = INITIAL_RIGHT_SPEED
        else:
            right_speed = min(MAX_SPEED, right_speed + STEP)
            left_speed = max(MIN_SPEED, left_speed - STEP)



print("start")
while True:
    tank_drive.on(left_speed, right_speed)
    correct_speed()
    check_zone()
    

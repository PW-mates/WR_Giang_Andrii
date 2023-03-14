from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from enum import Enum
from ev3dev2.motor import SpeedRPM

cs2 = ColorSensor(INPUT_2)
cs1 = ColorSensor(INPUT_1)

distance = UltrasonicSensor()

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

my_motor = LargeMotor()

squareTurn = 6
rollingTime = 0.2


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


def check_color(cs):
    r, g, b = cs.raw
    if r < 100 and g < 100 and b > 130:
        return Color.BLUE
    if r > 130 and g < 100 and b < 100:
        return Color.RED
    if r < 100 and g > 130 and b < 100:
        return Color.GREEN
    return None


def getColor():
    return sum(cs1.raw)/3, sum(cs2.raw)/3


def normal_running(priority=None):
    avg_left = sum(cs1.raw) / 3
    avg_right = sum(cs2.raw) / 3

    if avg_right > avg_left or check_color(cs1) == priority:
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


class Mission(Enum):
    PICK_UP = 1
    DELIVERY = 2


def pick_up():
    my_motor.on_for_seconds(SpeedRPM(20), 3)
    pass


def delivery():
    my_motor.on_for_seconds(SpeedRPM(-20), 3)
    pass


def main():
    pick_up_color = Color.RED
    delivery_color = Color.GREEN
    mission = Mission.PICK_UP
    priority = pick_up_color
    while (True):
        normal_running(priority)
        # if mission is Mission.PICK_UP:
        #     priority = Color.RED
        if mission is Mission.PICK_UP:
            if distance.distance_centimeters <= 3 \
                    and check_color(cs1) == pick_up_color \
                    and check_color(cs2) == pick_up_color:
                pick_up()
                priority = delivery_color
        else:
            if check_color(cs1) == delivery_color \
                    and check_color(cs2) == delivery_color:
                delivery()


if __name__ == '__main__':
    main()

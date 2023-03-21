from ev3dev2.sensor import INPUT_2, INPUT_1, INPUT_3
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor
from enum import Enum
from ev3dev2.motor import SpeedRPM

cs2 = ColorSensor(INPUT_2)
cs1 = ColorSensor(INPUT_1)

distance = InfraredSensor(INPUT_3)

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

my_motor = MediumMotor(OUTPUT_D)

squareTurn = 6
rollingTime = 0.2


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    WHITE = 4


def check_color(cs):
    r, g, b = cs.raw
    print(r, g, b)
    if r < 80 and g < 80 and b > 100:
        return Color.BLUE, (r+g+b)/3
    if r > 100 and g < 80 and b < 80:
        return Color.RED, (r+g+b)/3
    if r < 80 and g > 100 and b < 100:
        return Color.GREEN, (r+g+b)/3
    if r > 150 and g > 150 and b > 150:
        return Color.GREEN, (r+g+b)/3
    return None, (r+g+b)/3


def getColor():
    return sum(cs1.raw)/3, sum(cs2.raw)/3


def normal_running(priority=None):
    # avg_left = sum(cs1.raw) / 3
    # avg_right = sum(cs2.raw) / 3

    # if abs(avg_right - avg_left) <= 30:
    #     tank_drive.on_for_seconds(
    #         SpeedPercent(-15), SpeedPercent(-15), rollingTime)  # go straigh
    # elif avg_right > avg_left or check_color(cs1) == priority:
    #     tank_drive.on_for_seconds(
    #         SpeedPercent(-5), SpeedPercent(-25), rollingTime)  # turn left
    # else:
    #     tank_drive.on_for_seconds(
    #         SpeedPercent(-25), SpeedPercent(-5), rollingTime)  # turn right
    # if min(getColor()) > 130:
    #     cnt = 0
    #     while min(getColor()) > 130 and cnt < squareTurn:
    #         tank_drive.on_for_seconds(SpeedPercent(
    #             17), SpeedPercent(-20), rollingTime)  # turn left
    #         cnt += 1

    #     cnt = 0
    #     while min(getColor()) > 130 and cnt < 2*squareTurn:
    #         tank_drive.on_for_seconds(
    #             SpeedPercent(-20), SpeedPercent(17), rollingTime)  # turn right
    #         cnt += 1
    # avg_left = sum(cs1.raw) / 3
    # avg_right = sum(cs2.raw) / 3
    
    ccs1, avg_left = check_color(cs1)
    ccs2, avg_right = check_color(cs2)
    # print(check_color(cs1), check_color(cs2))

    if ccs1 == priority:
        tank_drive.on(20, -5)
    elif ccs2 == priority:
        tank_drive.on(-5, 20)
    elif abs(avg_right - avg_left) <= 60:
        tank_drive.on(-15, -15)
    elif avg_right > avg_left:
        tank_drive.on(20, -5)
    else:
        tank_drive.on(-5, 20)


class Mission(Enum):
    PICK_UP = 1 # pick up the parcel with medium motor only
    DELIVERY = 2 # 
    PATH_TO_PARCEL = 3 # line following until find spesial color(RED GREEN) with ONE of the sensors
    FROM_PATH_TO_PARCEL = 4 # line following until find spesial color(RED GREEN) with TWO of the sensors
    RETURN_TO_PATH = 3 # line following until find spesial color(RED GREEN)depends which one was first




def pick_up():
    print("Picking up!")
    my_motor.on_for_seconds(SpeedRPM(15), 1)
    
    tank_drive.on_for_seconds(
        SpeedPercent(30), SpeedPercent(-30), 1)  # turn back

    tank_drive.on_for_seconds(
        SpeedPercent(-20), SpeedPercent(-20), 1)  # turn back


def delivery():
    print("Delivery!")
    my_motor.on_for_seconds(SpeedRPM(-15), 1)
    
    tank_drive.on_for_seconds(
        SpeedPercent(50), SpeedPercent(50), 1)  # turn back
    tank_drive.on_for_seconds(
        SpeedPercent(50), SpeedPercent(-50), 5)  # cheer

def run_loop(pick_up_color, delivery_color, mission, priority):
    while (True):
        ccs1, rgbcs1 = check_color(cs1)
        ccs2, rgbcs2 = check_color(cs2)
        if mission is Mission.PATH_TO_PARCEL:
            normal_running(priority)
        elif mission is Mission.FROM_PATH_TO_PARCEL:
            m


        normal_running(priority)
        # if mission is Mission.PICK_UP:
        #     priority = Color.RED
        if mission is Mission.PICK_UP:
            # pass
            print(distance.proximity)
            ccs1, _ = check_color(cs1)
            ccs2, _ = check_color(cs2)
            if distance.proximity != None and distance.proximity <= 2 \
                    and ccs1 == pick_up_color \
                    and ccs2 == pick_up_color:
                pick_up()
                priority = delivery_color
                mission = Mission.DELIVERY
        else:
            if ccs1 == delivery_color \
                    and ccs2 == delivery_color:
                delivery()
                print("Deliveried!")
                exit()

def main():
    # while True:
    #     pick_up()
    #     delivery()
    pick_up_color = Color.RED
    delivery_color = Color.GREEN
    mission = Mission.PICK_UP
    priority = pick_up_color
    run_loop(pick_up_color, delivery_color, mission, priority)
    


if __name__ == '__main__':
    print("start")
    main()

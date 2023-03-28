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


class TaskExecution:

    def __init__(self, mission, col_sens_1, col_sens_2, parcel_zone_color, delivery_zone_color, path_to_parcel_color, path_to_delivery_color):
        self.pick_up_status = False
        self.current_mission = mission
        self.col_sens_1 = col_sens_1
        self.col_sens_2 = col_sens_2
        self.parcel_zone_color = parcel_zone_color
        self.delivery_zone_color = delivery_zone_color
        self.path_to_parcel_color = path_to_parcel_color
        self.path_to_delivery_color = path_to_delivery_color
        self._tmp_side_flag = None
        self._is_turned = False

    def normal_following(self, param=60):
        _, avg_left = self.col_sens_1
        _, avg_right = self.col_sens_2
        if abs(avg_right - avg_left) <= param:
            tank_drive.on(-10, -10)
        elif avg_right > avg_left:
            tank_drive.on(15, -5)  # Turn left
        else:
            tank_drive.on(-5, 15)  # Turn right

    def correct_picking_position(self):
        print("Correct me!")

    def pick_up(self):
        print("Picking up!")
        if distance.proximity != None and distance.proximity <= 2:
            my_motor.on_for_seconds(SpeedRPM(15), 1)
            self.current_mission = Mission.RETURN_TO_PATH
        else:
            self.correct_picking_position()

        # tank_drive.on_for_seconds(
        #     SpeedPercent(30), SpeedPercent(-30), 1)  # turn back

        # tank_drive.on_for_seconds(
        #     SpeedPercent(-20), SpeedPercent(-20), 1)  # turn back

    def delivery():
        print("Delivery!")
        my_motor.on_for_seconds(SpeedRPM(-15), 1)

        tank_drive.on_for_seconds(
            SpeedPercent(50), SpeedPercent(50), 1)  # turn back
        tank_drive.on_for_seconds(
            SpeedPercent(50), SpeedPercent(-50), 5)  # cheer

    def from_path_to_parcel(self):
        if self._is_turned:
            pass
        elif self._tmp_side_flag == Side.LEFT:
            tank_drive.on_for_seconds(SpeedPercent(
                7), SpeedPercent(-15), 2)  # should turn left
            self._is_turned = True
        elif self._tmp_side_flag == Side.RIGHT:
            tank_drive.on_for_seconds(
                SpeedPercent(-15), SpeedPercent(7), 2)  # should turn right
            self._is_turned = True

    def event_check(self):
        ccs1, avg_left = self.col_sens_1
        ccs2, avg_right = self.col_sens_2
        if self.current_mission == Mission.PATH_TO_PARCEL and \
                (ccs1 == self.path_to_parcel_color or ccs2 == self.path_to_parcel_color):
            self.current_mission = Mission.FROM_PATH_TO_PARCEL
            print("FROM_PATH_TO_PARCEL")
            if ccs1 == self.path_to_parcel_color:
                print("Right")
                self._tmp_side_flag = Side.RIGHT
            else:
                print("Left")
                self._tmp_side_flag = Side.LEFT
        if self.current_mission == Mission.FROM_PATH_TO_PARCEL and \
                (ccs1 == self.parcel_zone_color and ccs2 == self.parcel_zone_color):
            self.current_mission = Mission.PICK_UP
            print("PICK_UP")

    def update_data(self, col_sens_1, col_sens_2):
        self.col_sens_1 = col_sens_1
        self.col_sens_2 = col_sens_2
        self.event_check()

    def run_events(self):
        if self.current_mission is Mission.PATH_TO_PARCEL:
            self.normal_following(param=60)  # black
        if self.current_mission is Mission.FROM_PATH_TO_PARCEL:
            self.from_path_to_parcel()
            # ToDo should be param for specific color depends on path_to_parcel_color and for black also 
            self.normal_following(param=40)
        if self.current_mission is Mission.PICK_UP:
            self.pick_up()
            exit()


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    WHITE = 4


class Side(Enum):
    LEFT = 1
    RIGHT = 2


class Mission(Enum):
    PICK_UP = 1  # pick up the parcel with medium motor only
    DELIVERY = 2
    # line following until find spesial color(RED GREEN) with ONE of the sensors
    PATH_TO_PARCEL = 3
    # line following until find spesial color(RED GREEN) with TWO of the sensors
    FROM_PATH_TO_PARCEL = 4
    # line following until find spesial color(RED GREEN)depends which one was first
    RETURN_TO_PATH = 3


def check_color(cs):
    r, g, b = cs.raw
    # print(r, g, b)
    if r < 80 and g < 80 and b > 100:
        return Color.BLUE, (r+g+b)/3
    if r > 100 and g < 80 and b < 80:
        return Color.RED, (r+g+b)/3
    if r < 80 and g > 100 and b < 100:
        return Color.GREEN, (r+g+b)/3
    if r > 150 and g > 150 and b > 150:
        return Color.GREEN, (r+g+b)/3
    return None, (r+g+b)/3


def run_loop(tasks: TaskExecution):
    while (True):
        ccs1, rgbcs1 = check_color(cs1)
        ccs2, rgbcs2 = check_color(cs2)
        tasks.update_data((ccs1, rgbcs1), (ccs2, rgbcs2))
        tasks.run_events()


def main():
    parcel_zone_color = Color.GREEN
    delivery_zone_color = Color.BLUE
    path_to_parcel_color = Color.RED
    path_to_delivery_color = Color.BLUE
    tasks = TaskExecution(mission=Mission.PATH_TO_PARCEL,
                          col_sens_1=None, col_sens_2=None,
                          parcel_zone_color=parcel_zone_color,
                          delivery_zone_color=delivery_zone_color,
                          path_to_parcel_color=path_to_parcel_color,
                          path_to_delivery_color=path_to_delivery_color,)
    print("init Tasks")
    run_loop(tasks)


if __name__ == '__main__':
    print("start")
    main()

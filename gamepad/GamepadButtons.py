from enum import Enum


class GamepadButtons(Enum):
    # AXIS_LEFT_STICK_X = 0
    # AXIS_LEFT_STICK_Y = 1
    # AXIS_RIGHT_STICK_X = 2
    # AXIS_RIGHT_STICK_Y = 3
    # AXIS_R2 = 5
    # AXIS_L2 = 4

    CROSS = 0  # correct
    CIRCLE = 1  # correct
    TRIANGLE = 2  # correct
    SQUARE = 3  # correct

    L1 = 4  # correct
    R1 = 5  # correct
    L2 = 6
    R2 = 7

    SHARE = 8  # correct
    OPTIONS = 9  # correct
    PS = 10  # correct

    LEFT_STICK = 11  # correct
    RIGHT_STICK = 12  # correct

    LEFT_ARROW = 13  # correct
    RIGHT_ARROW = 14  # correct
    DOWN_ARROW = 15
    UP_ARROW = 16
    CENTER=17


class GamepadDpad:
    @classmethod
    def get_direction(cls, dpad_signals):
        if dpad_signals[0] | dpad_signals[1] == 0:
            return 17
        if dpad_signals[0] != 0:
            if dpad_signals[0] == 1:
                return 14
            else:
                return 13
        if dpad_signals[1] != 0:
            if dpad_signals[1] == 1:
                return 16
            else:
                return 15

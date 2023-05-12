from enum import Enum


class GamepadButtons(Enum):
    CROSS = 0  # correct
    CIRCLE = 1  # correct
    TRIANGLE = 2  # correct
    SQUARE = 3  # correct

    L1 = 4  # correct
    R1 = 5  # correct
    L2_BUTTON = 6
    R2_BUTTON = 7

    SHARE = 8  # correct
    OPTIONS = 9  # correct
    PS = 10  # correct

    LEFT_STICK = 11  # correct
    RIGHT_STICK = 12  # correct

    LEFT_ARROW = 13  # correct
    RIGHT_ARROW = 14  # correct
    DOWN_ARROW = 15
    UP_ARROW = 16
    CENTER = 17


class GamepadSticks(Enum):
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1
    L2_TRIGGER = 2

    RIGHT_STICK_X = 3
    RIGHT_STICK_Y = 4
    R2_TRIGGER = 5


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

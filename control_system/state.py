from gamepad import ControlsFile
from commands import ThreadSafeMetaSingleton
from enum import Enum
from route import Route, RouteBuilder


class ControlModes(Enum):
    REMOTE = 1
    AUTO = 2
    MANUAL = 3


class ControlSystemState(metaclass=ThreadSafeMetaSingleton):

    def __init__(self):
        self.__control_mode = "REMOTE"
        self.__control_configuration = ControlsFile.read_configuration()
        self.__learning_route: Route = None
        self.__is_learning = 0

    @property
    def control_mode(self):
        return self.__control_mode

    @control_mode.setter
    def control_mode(self, control_mode):
        control_mode_name = ControlModes(control_mode).name
        self.__control_mode = control_mode_name

    @property
    def control_configuration(self):
        return self.__control_configuration

    @control_configuration.setter
    def control_configuration(self, control_configuration):
        self.__control_configuration = control_configuration

    @property
    def learning_route(self):
        return self.__learning_route

    @learning_route.setter
    def learning_route(self, learning_route):
        self.__learning_route = learning_route

    @property
    def is_learning(self):
        return self.__is_learning

    @is_learning.setter
    def is_learning(self, is_learning):
        self.__is_learning = self.__is_learning ^ is_learning
        # if is_learning 0 -> save learning route

    def mode_is_set(self, control_mode: int) -> bool:
        if self.control_mode == ControlModes(control_mode).name:
            return True
        else:
            return False

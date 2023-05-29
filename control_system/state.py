from gamepad import ControlsFile
from commands import ThreadSafeMetaSingleton


class ControlSystemState(metaclass=ThreadSafeMetaSingleton):

    def __init__(self):
        self.control_mode = "remote"
        self.control_configuration = ControlsFile.read_configuration()

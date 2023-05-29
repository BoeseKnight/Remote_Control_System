from commands import *
# from gamepad import *


class ControlsFile:
    file_path = 'control_config.txt'

    @classmethod
    def write_configuration(cls, control_configuration: dict):
        with open(cls.file_path, 'w+') as file:
            for key, value in control_configuration.items():
                file.write('%s:%s\n' % (key, value))

    @classmethod
    def read_configuration(cls) -> dict:
        control_configuration = {}
        with open(cls.file_path, 'r') as file:
            list_configuration = file.read().splitlines()
            for control in list_configuration:
                key_value = control.split(':')
                control_configuration.update({key_value[0]: key_value[1]})
            # print(control_configuration)
            return control_configuration


class ControlConfiguration:
    commands_sequence = [command.name for command in ControlCommands]

    def __init__(self, controls_sequence: list = ("UP_ARROW", 'TRIANGLE', 'SQUARE', 'RIGHT_ARROW', 'LEFT_ARROW', 'CROSS', 'DOWN_ARROW')):
        self.controls_sequence = controls_sequence
        self.__create_control_configuration()

    def __create_control_configuration(self) -> dict:
        temporary_configuration = zip(self.controls_sequence, self.commands_sequence, )
        list_configuration = list(temporary_configuration)
        self.control_configuration = dict(list_configuration)
        ControlsFile.write_configuration(self.control_configuration)
        print(self.control_configuration)
        return self.control_configuration


# a = "gas"
# b = "arrow"
# dictik = {ControlCommands.GAS.name: GamepadButtons.CROSS.name}
# dict.update({ControlCommands.GAS.name: GamepadButtons.CROSS.name})
# c = ControlConfiguration()
# print(dict)
# print(type(dict))

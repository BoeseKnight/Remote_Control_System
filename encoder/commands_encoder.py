from control_system import ControlSystemState
from gamepad import ControlsFile, InnerCommand, ControlCommands
from window import *


class Encoder:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def encode_command(self):
        pass


class GamepadEncoder(Encoder):
    def __init__(self):
        super().__init__()

    @app_log
    def encode_command(self):
        control_configuration = ControlSystemState().control_configuration
        print(self.command.button_name)
        gamepad_command = control_configuration.get(self.command.button_name)
        try:
            inner_command = InnerCommand(gamepad_command, command_id=ControlCommands[gamepad_command].value)
            print("AAAAAAA ENCOOOOODE")
            # app.console.insert('1.0', f"{inner_command}\n")
            return inner_command
        except Exception as e:
            return None


class CommandEncoder(Encoder):
    def __init__(self):
        super().__init__()

    def encode_command(self):
        pass

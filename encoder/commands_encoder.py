import window.main_window
from commands import InnerCommand, ControlCommands, RouteCommands, SendCommandsList
from control_system.state import ControlSystemState
from route.route import Route


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

    @window.main_window.app_log
    def encode_command(self):
        control_configuration = ControlSystemState().control_configuration
        print(self.command.button_name)
        gamepad_command = control_configuration.get(self.command.button_name)
        try:
            inner_command = InnerCommand(gamepad_command, command_type=ControlCommands,
                                         command_id=ControlCommands[gamepad_command].value)
            print("AAAAAAA ENCOOOOODE")
            # app.console.insert('1.0', f"{inner_command}\n")
            return inner_command
        except Exception as e:
            return None


class CommandEncoder(Encoder):
    def __init__(self):
        super().__init__()

    def encode_command(self):
        command_list = SendCommandsList()
        if type(self.command) == Route:
            command_to_send = InnerCommand(command_name=RouteCommands.CREATE_ROUTE.name, command_type=RouteCommands,
                                           command_data=self.command.waypoints)
            command_list.append(command_to_send)
            return command_to_send

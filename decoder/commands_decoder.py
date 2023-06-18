from typing import List

from commands import InnerCommand


class Decoder:
    def __init__(self, outer_command: str = "SPEED:25;POSITION:10,30"):
        self.outer_command = outer_command

    def set_command(self, outer_command):
        self.outer_command = outer_command

    def decode(self):
        pass


class CommandDecoder(Decoder):
    def __init__(self, outer_command: str = "SPEED:25;POSITION:10,30"):
        super().__init__(outer_command)

    def decode(self):
        commands: List[str] = self.outer_command.split(';')
        for outer_command in commands:
            code_and_data = outer_command.split(':')
            command_code = code_and_data[0]
            command_data = code_and_data[1]
            # print(command_code + "   " + command_data)
            inner_command = InnerCommand(command_code, command_data, "in processing")
            return inner_command

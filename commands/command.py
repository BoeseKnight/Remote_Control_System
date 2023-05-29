from enum import Enum


class ControlCommands(Enum):
    START = 1
    GAS = 2
    BRAKE = 3
    RIGHT = 4
    LEFT = 5
    REVERSE = 6
    STOP = 7


class RouteCommands(Enum):
    CREATE_ROUTE = 1
    DELETE_ROUTE = 2
    LEARN_ROUTE = 3
    CURRENT_ROUTE = 4
    ALTER_ROUTE = 5


class CommandsFromOnBoard(Enum):
    SPEED = 1
    POSITION = 2
    WHEEL_POSITION = 3
    WAYPOINT = 4


class Command:
    def __init__(self, command_id, command_state):
        self.command_id = command_id
        self.command_state = command_state


class InnerCommand(Command):
    def __init__(self, command_name, command_data='', command_state='created', command_id=0):
        super().__init__(command_id, command_state)
        self.command_name = command_name
        self.command_data = command_data

    def __str__(self):
        return f"{self.command_name}[{self.command_id}] {self.command_state}"

    def __repr__(self):
        return str(self)


class OuterCommand(Command):
    def __init__(self, command_to_send, command_id, command_state):
        super().__init__(command_id, command_state)
        self.command_to_send = command_to_send


# print(ControlCommands(7).name)
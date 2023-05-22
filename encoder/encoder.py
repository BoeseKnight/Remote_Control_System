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

    def encode_command(self):
        pass


class CommandEncoder(Encoder):
    def __init__(self):
        super().__init__()

    def encode_command(self):
        pass


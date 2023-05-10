import threading


class ThreadSafeMetaSingleton(type):
    """Thread Safe Singleton Metaclass."""

    __instances = {}
    __lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class CommandList(metaclass=ThreadSafeMetaSingleton):
    def __init__(self):
        self._commands = []

    def add_command(self, command):
        self._commands.append(command)

    def get_command(self):
        return self._commands.pop(0)

    def get_commands(self):
        return self._commands


class SendCommandsList(CommandList):
    pass


class ReceiveCommandsList(CommandList):
    pass


commands = CommandList()
send = SendCommandsList()
receive = ReceiveCommandsList()
command2 = CommandList()
send2 = SendCommandsList()
receive2 = ReceiveCommandsList()
print(commands == send)
print(send == receive)
print(commands == command2)
receive2.add_command(5)
receive.add_command(7)
commands.add_command(2)
command2.add_command(1)

print(commands.get_commands())
print(send.get_commands())
print(receive.get_commands())

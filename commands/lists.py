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

    def append(self, command):
        self._commands.append(command)

    def pop(self):
        return self._commands.pop(0)

    def get_list(self):
        return self._commands


class SendCommandsList(CommandList):
    pass


class ReceiveCommandsList(CommandList):
    pass


class FramesList(CommandList):
    pass

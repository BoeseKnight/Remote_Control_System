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
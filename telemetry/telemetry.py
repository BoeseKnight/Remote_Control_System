from route import Position


class Speed:
    def __init__(self, speed_value: float = 0.0, speed_unit: str = 'km/h'):
        self.__speed_value = speed_value
        self.__speed_unit = speed_unit

    @property
    def speed_value(self):
        return self.__speed_value

    @speed_value.setter
    def speed_value(self, speed_value):
        self.__speed_value = float(speed_value)

    @property
    def speed_unit(self):
        return self.__speed_unit

    @speed_unit.setter
    def speed_unit(self, speed_unit):
        self.__speed_unit = float(speed_unit)


class WheelPosition:
    def __init__(self, wheel_position: float = 0.0):
        self.__wheel_position = wheel_position

    @property
    def wheel_position(self):
        return self.__wheel_position

    @wheel_position.setter
    def wheel_position(self, wheel_position):
        self.__wheel_position = float(wheel_position)


class TelemetryObject:
    def __init__(self):
        self.__objects = {'SPEED': Speed(), 'WHEEL_POSITION': WheelPosition(), 'POSITTION': Position()}


class Telemetry:
    def __init__(self, speed: Speed, position: Position, wheel_position: WheelPosition):
        self.speed = speed
        self.wheel_position = wheel_position
        self.position = position

    def __str__(self):
        return f"Position: {self.position.x}; {self.position.y}; {self.position.z}\nSpeed:"

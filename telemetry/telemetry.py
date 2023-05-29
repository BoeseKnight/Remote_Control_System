from route import *


class Speed:
    def __init__(self, speed_value: float = 0.0, speed_unit: str = 'km/h'):
        self.speed_value = speed_value
        self.speed_unit = speed_unit


class WheelPosition:
    def __init__(self, wheel_position: float = 0.0):
        self.wheel_position = wheel_position


class Telemetry:
    def __init__(self, speed: Speed, position: Position, wheel_position: WheelPosition):
        self.speed = speed
        self.wheel_position = wheel_position
        self.position = position

    def __str__(self):
        return f"Position: {self.position.x}; {self.position.y}; {self.position.z}\nSpeed:"

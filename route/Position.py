from .Dot import *


class Position(Dot):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z


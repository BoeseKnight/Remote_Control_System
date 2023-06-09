from .dot import *


class Position(Dot):
    def __init__(self, x, y, z=10):
        super().__init__(x, y)
        self.z = z

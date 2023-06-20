from .dot import *


class Position(Dot):
    def __init__(self, x=0, y=0, z=10):
        super().__init__(x, y)
        self.z = z

    def __repr__(self):
        return f"{self.x},{self.y},{self.z}"

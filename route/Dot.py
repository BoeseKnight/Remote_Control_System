class Dot:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class GraphicalDot(Dot):
    def __init__(self, x: float, y: float, colour='black'):
        super().__init__(x, y)
        self.colour = colour

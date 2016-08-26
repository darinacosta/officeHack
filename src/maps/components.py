class Tile:
    # map tile and properties
    def __init__(self, blocked, block_sight = None):
        self.explored = False
        self.blocked = blocked
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class RectRoom:
    # rectangular room
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        return (self.x1 < other.x2 and self.x2 >= other.x1 and
            self.y1 <= other.y2 and self.y2 >= other.y1)

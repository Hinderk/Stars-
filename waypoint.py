
from defines import Task


class Waypoint:

    def __init__(self, x, y):
        self.Task = Task.IDLE
        self.warp = 0
        self.xo = x
        self.yo = y
        self.next = None
        self.previous = None
        self.track = None

from defines import Task


class Waypoint:

    def __init__(self, x, y, p=None):
        self.task = Task.IDLE
        self.warp = 0
        self.planet = p
        self.xo = x
        self.yo = y
        self.next = None
        self.previous = None
        self.retain = False


    def at(self, wp):
        return self.xo == wp.xo and self.yo == wp.yo

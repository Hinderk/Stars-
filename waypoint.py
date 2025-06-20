
""" This module implements waypoints for travelling star fleets """

from math import sqrt
from defines import Task


class Waypoint:

    """ This class implements waypoints for travelling star fleets """

    def __init__(self, x, y, p=None):
        self.task = Task.MOVE
        self.turns = 0
        self.warp = 0
        self.planet = p
        self.xo = x
        self.yo = y
        self.next = None
        self.previous = None
        self.retain = False


    def at(self, wp):
        """ Check whether two points coincide """
        return self.xo == wp.xo and self.yo == wp.yo


    def dist(self, x, y):
        """ Compute the distance towards the point (x,y) """
        return sqrt((self.xo - x) * (self.xo - x) + (self.yo - y) * (self.yo - y))

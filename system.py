
""" This module implements the various systems a ship may carry into combat """

from enum import Enum


class SystemType(Enum):
    """ Categories of technichal equipment """
    EMPTY = 0
    BEAMWEAPON = 1
    MISSILE = 2
    BOMB = 3
    MINEDISPENSER = 4
    SCANNER = 5
    MININGROBOT = 6
    MECHANICAL = 7
    ELECTRICAL = 8
    SHIELDS = 9
    ARMOR = 10


class System:

    """ This class specifies the properties of a piece of equipment """

    def __init__(self):

        self.domain = SystemType.EMPTY
        self.item_type = None
        self.item_count = 0

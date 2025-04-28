
from enum import Enum


class SystemType(Enum):
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

    def __init__(self):

        self.domain = SystemType.EMPTY
        self.item_type = None
        self.item_count = 0


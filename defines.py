
""" This module defines various enumerations used throughout the code """

from enum import Enum



class MapView(Enum):
    """ List of display modes for the planets on the star map """
    DEFAULT = 0
    SURFACE = 1
    CRUST = 2
    POPULATION = 3
    NETWORTH = 4
    MINIMAL = 5


class Stance(Enum):
    """ Possible attitudes of factions towards each other """
    IGNORE = 0
    ALLIED = 1
    FRIENDLY = 2
    NEUTRAL = 4
    HOSTILE = 8
    ACCEPT = 15


class ShipClass(Enum):
    """ Categories of ship designs available in the game """
    COL = "Colony Ship"
    FRT = "Freighter"
    SCT = "Scout"
    WAR = "Warship"
    UTL = "Utility Vessel"
    MLY = "Mine Layer"
    BMB = "Bomber"
    MIN = "Mining Rig"
    FLT = "Fuel Transport"


class Feature(Enum):
    """ Features or prerequisites for specific items """
    NONE = 0         # No specific features
    CROB = 1         # Cargo stealing scanner
    HIDE = 2         # Improved ship cloaking
    OSSC = 3         # Only simple scanners allowed


class Task(Enum):
    """ List of waypoint tasks to be performed by fleets """
    IDLE = 'None'
    MOVE = 'Travel'
    HAUL = 'Transport'
    MINE = 'Mining'


class PlayerType(Enum):
    """ Types of slots available for the game roster """
    AIP = 'AI Antagonist'
    EXP = 'Expansion Slot'
    HUP = 'Human Player'
    REX = 'Random Expansion Slot'
    RNG = 'Random Player'


class AIMode(Enum):
    """ Levels of aggressiveness of the enenmy AI """
    AI0 = 'Easy'
    AI1 = 'Standard'
    AI2 = 'Tough'
    AI3 = 'Expert'
    AIR = 'Random'

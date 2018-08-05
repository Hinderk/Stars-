"""This module holds all the preferences evaluated when drawing the star map"""

from enum import Enum



class RenderMode(Enum):
    """Possible options which information to display when rendering the star map"""
    Plain = 1
    PlanetValue = 2
    Orbiting = 3
    Minerals = 4
    Settlements = 5
    Deposits = 6



class FleetFilter(Enum):
    """Possible filter settings for the fleets in planetary orbit"""
    Friend = 1
    Foe = 2
    Neutral = 3
    Freighter = 4
    DropShips = 5
    Trader = 6
    Pirate = 7
    Armed = 8


    
class MineFieldFilter(Enum):
    """Switch to decide which sorts of mine-fields to display"""
    Friend = 1
    Foe = 2
    Neutral = 3
    Off = 4


class MapSettings(object):
    """Collect settings which content to display on the star map"""
    
    def __init__(self):
        self.Mode = RenderMode.Plain 
        self.InOrbit = FleetFilter.Friend
        self.ShowMines = MineFieldFilter.Off
        self.ShowFleets = True
        self.ShowScanner = True
        
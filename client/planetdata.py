"""This module maintains all star system data"""

import sys


class PlanetData(object):
    """Collect & maintain all pertinent data for a star system."""

    def __init__(self):
        self.Radius = 8000.0         # in km 
        self.Temperature = 274.0     # in Kelvin
        self.Gravity = 1.0           # in g resp. 9.81 m/s^2
        self.Radiation = 200.0       # in Watt per square meter
        self.Factories = 0
        self.Mines = 0               # simple counter
        self.Defenses = 0
        self.TechLevel = 1           # generation of defense tech
        self.Boranium = 200.0        # in Megatons
        self.Ironium = 500.0         # in Megatons
        self.Thoridium = 1.0         # in Megatons
        self.totalBoranium = 1800.0  # in Megatons 
        self.totalIronium = 4000.0   # in Megatons
        self.totalThoridium = 20.0   # in Megatons
        self.Settlers = 0            # in Thousands



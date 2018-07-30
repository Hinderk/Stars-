"""This module maintains all star system data"""


# from speciesdata import SpeciesData


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


    def PlanetValue(self, mySpecies):
        """Compute the value of a star system for a given species"""
        value = 1.0
        if self.Temperature < mySpecies.minTemperature:
            value = 1.0 - (mySpecies.minTemperature - self.Temperature) / 50.0
        if mySpecies.maxTemperature < self.Temperature:
            value = 1.0 - (self.Temperature - mySpecies.maxTemperature) / 50.0
        if self.Radiation < mySpecies.minRadiation:
            value = value - (mySpecies.minRadiation - self.Radiation) / 1000.0
        if mySpecies.maxRadiation < self.Radiation:
            value = value - (self.Radiation - mySpecies.maxRadiation) / 1000.0
        if self.Gravity < mySpecies.minGravity:
            value = value - (mySpecies.minGravity - self.Gravity) / 2.0
        if mySpecies.maxGravity < self.Gravity:
            value = value - (self.Gravity - mySpecies.maxGravity) / 2.0
        return max( 0.0, value )


    def CarryingCapacity(self, mySpecies):
        """Compute the maximal number of settlers for a given species"""
        return mySpecies.maxSettlers * self.PlanetValue(mySpecies)
    
    
    def PopulationLevel(self, mySpecies):
        """Compute an indicator for the current size of the population"""
        return self.Settlers / mySpecies.maxSettlers
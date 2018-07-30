"""This module maintains the biological traits of space-faring species"""



class SpeciesData(object):
    """Maintain the biological parameters of a space-faring species""" 
    
    def __init__(self):
        self.minTemperature = 240.0     # in Kelvin 
        self.maxTemperature = 320.0     # in Kelvin
        self.minGravity = 0.0
        self.maxGravity = 2.5           # in g resp. 9.81 m/s^2
        self.minRadiation = 100.0       # in Watt per square meter
        self.maxRadiation = 500.0       # in Watt per square meter
        self.maxSettlers = 10000000     # in Thousands


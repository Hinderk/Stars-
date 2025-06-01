
""" This module implements a mechanism to specify planetary environments """

from minerals import Minerals
from defines import Stance



class PlanetData:

    """ This class is used to store the biome data as reported by visiting fleets """

    def __init__(self):

        self.radioactivity = 0                             # These parameters may be modified via
        self.gravity = 0                                   # terraforming technologies and influence
        self.temperature = 0                               # population density & growth

        self.radioactivity_rate = 0.0                      # TODO: Create a viable terraforming
        self.gravity_rate = 0.0                            # model to compute these rates.
        self.temperature_rate = 0.0

        self.colonists = 0

        self.relation = Stance.NEUTRAL
        self.space_station = False

        self.crust = Minerals()
        self.surface = Minerals()

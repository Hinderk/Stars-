
from minerals import Minerals
from defines import Stance



class PlanetData:

    def __init__(self):

        self.Radioactivity = 0                             # These parameters may be modified via
        self.Gravity = 0                                   # terraforming technologies and influence
        self.Temperature = 0                               # population density & growth

        self.RadioactivityRate = 0.0                       # TODO: Create a viable terraforming
        self.GravityRate = 0.0                             # model to compute this rates.
        self.TemperatureRate = 0.0

        self.Colonists = 0

        self.Relation = Stance.neutral
        self.SpaceStation = False

        self.Crust = Minerals()
        self.Surface = Minerals()

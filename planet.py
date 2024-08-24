
class Minerals:

  def __init__(self, Rules=None, Scale=1.0):
    if Rules:
      MinVal = Scale * Rules.GetMinResources()
      MaxVal = Scale * Rules.GetMaxResources()
      OptVal = Scale * Rules.GetResources()
      self.Ironium = Rules.Random(MinVal, MaxVal, OptVal)
      self.Boranium = Rules.Random(MinVal, MaxVal, OptVal)
      self.Germanium = Rules.Random(MinVal, MaxVal, OptVal)
    else:
      self.Ironium = 0      # Three types of resources are Mined. These
      self.Boranium = 0     # stand in for minerals, energy and food.
      self.Germanium = 0
      

# This class represents the solar systems of the Stars universe each of
# which is represented by just one of its planets and named after its sun.

class Planet:

  def __init__(self, Rules, HomeWorld=False):

    self.Name = Rules.FindName()      # The name of the solar system

    self.Radioactivity = Rules.Random(0, 100, 50)      # These parameters may be modified via
    self.Gravity = 64.0 ** Rules.Random(-0.5, 0.5, 0)  # terraforming technologies and influence
    self.Temperature = Rules.Random(-200, 200, 0)      # population density & growth

    self.RadioactivityRate = 0.0                       # TODO: Create a viable terraforming
    self.GravityRate = 0.0                             # model to compute this rates.
    self.TemperatureRate = 0.0

    self.Crust = Minerals(Rules)                       # Create a random amount of minerals
    self.Explored = Minerals()                         # inside the planet's crust and - for
    self.Mined = Minerals()                            # the homeworld - on its surface
    if HomeWorld:
      self.Surface = Minerals(Rules, 0.1)
    else:
      self.Surface = Minerals()
    self.Explore(Rules.FirstYear())                    # Start with the first game year ...
    
    
  def Explore(self, year):
    self.Mined.Boranium = self.Surface.Boranium
    self.Mined.Ironium = self.Surface.Ironium
    self.Mined.Germanium = self.Surface.Germanium
    self.Explored.Boranium = self.Crust.Boranium
    self.Explored.Ironium = self.Crust.Ironium
    self.Explored.Germanium = self.Crust.Germanium
    self.LastVisit = year
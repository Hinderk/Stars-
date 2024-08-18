
# This class facilities the generation of a random "Stars!" universe ...

class Ruleset :

  Name = 'Standard'

  Planet = 'dummy'
  Surface = "dummy"

  def Random(self, MinVal, MaxVal, Optimum):
    return(Optimum)

  def FindName(self):
    return 'No Name'

  def FirstYear(self):
    return 2400

  def GetMaxResources(self):
    return 100.0

  def GetMinResources(self):
    return 5.0

  def GetResources(self):
    return 70.0

  def PlanetCount(self):
    return 20
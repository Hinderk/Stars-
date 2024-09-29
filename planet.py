
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

    self.Name = Rules.FindName()                       # The name of the solar system

    self.Radioactivity = Rules.Random(0, 100, 50)      # These parameters may be modified via
    self.Gravity = 64.0 ** Rules.Random(-0.5, 0.5, 0)  # terraforming technologies and influence
    self.Temperature = Rules.Random(-200, 200, 0)      # population density & growth

    self.RadioactivityRate = 0.0                       # TODO: Create a viable terraforming
    self.GravityRate = 0.0                             # model to compute this rates.
    self.TemperatureRate = 0.0

    self.orbit = None                                  # The following class members will be
    self.starbase = None                               # used to render planets on the star
    self.neutral = None                                # map in different ways depending on
    self.foes = None                                   # player choices & the game state ...
    self.friends = None
    self.attackers = None
    self.core = None
    self.body = None
    self.ships = None
    self.others = None
    self.flag = None
    self.diagram = None

    self.TotalFriends = 0
    self.TotalFoes = 0
    self.TotalOthers = 0
    self.TotalOrbit = 0
    self.Colonists = 0

    self.Discovered = HomeWorld                      # Obviously, the home world is settled
    self.ShipTracking = HomeWorld                    # from the first turn of the game ...

    self.Friendly = HomeWorld
    self.Hostile = False
    self.SpaceStation = False

    self.Crust=Minerals(Rules)                       # Create a random amount of minerals
    self.Explored=Minerals()                         # inside the planet's crust and - for
    self.Mined = Minerals()                          # the home world - on its surface
    if HomeWorld:
      self.Surface=Minerals(Rules, 0.1)
      self.Explore(Rules.FirstYear())                # Start with the first game year ...
    else:
      self.Surface = Minerals()


  def Explore(self, year):
    self.Mined.Boranium = self.Surface.Boranium
    self.Mined.Ironium = self.Surface.Ironium
    self.Mined.Germanium = self.Surface.Germanium
    self.Explored.Boranium = self.Crust.Boranium
    self.Explored.Ironium = self.Crust.Ironium
    self.Explored.Germanium = self.Crust.Germanium
    self.LastVisit = year
    self.Discovered = True


  def UpdateFriends(self, count=0):
    self.TotalFriends += count
    self.TotalOrbit += count
    if self.TotalFriends > 0:
      self.friends.setVisible(True)
      self.orbit.setVisible(True)
      w0 = self.ships.boundingRect().width()
      x0 = self.ships.x()
      self.ships.setText(str(self.TotalFriends))
      w = self.ships.boundingRect().width()
      self.ships.setX(x0 - w + w0)
      self.ships.setVisible(True)
    else:
      self.TotalFriends = 0
      self.ships.setVisible(False)
      self.friends.setVisible(False)
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
      self.orbit.setVisible(False)
    else:
      self.orbit.setVisible(self.ShipTracking)


  def UpdateFoes(self, count=0):
    self.TotalFoes += count
    self.TotalOrbit += count
    if self.TotalFoes > 0:
      self.foes.setVisible(self.ShipTracking)
      self.orbit.setVisible(self.ShipTracking)
      w0 = self.attackers.boundingRect().width()
      x0 = self.attackers.x()
      self.attackers.setText(str(self.TotalFoes))
      w = self.attackers.boundingRect().width()
      self.attackers.setX(x0 - w + w0)
      self.attackers.setVisible(self.ShipTracking)
    else:
      self.TotalFoes = 0
      self.attackers.setVisible(False)
      self.foes.setVisible(False)
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
      self.orbit.setVisible(False)
    else:
      self.orbit.setVisible(self.ShipTracking)


  def UpdateOthers(self, count=0):
    self.TotalOthers += count
    self.TotalOrbit += count
    if self.TotalOthers > 0:
      self.neutral.setVisible(self.ShipTracking)
      self.orbit.setVisible(self.ShipTracking)
      self.others.setText(str(self.TotalOthers))
      self.others.setVisible(self.ShipTracking)
    else:
      self.TotalOthers = 0
      self.others.setVisible(False)
      self.neutral.setVisible(False)
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
      self.orbit.setVisible(False)
    else:
      self.orbit.setVisible(self.ShipTracking)


  def RevealStarbase(self):
    show = self.ShipTracking and self.SpaceStation
    self.orbit.setVisible(show)
    self.starbase.setVisible(show)


  def BuildStarbase(self):
    if not self.SpaceStation:
      self.TotalOrbit += 1
      self.SpaceStation = True
    self.RevealStarbase()


  def DestroyStarbase(self):
    if self.OrbitingBase:
      self.TotalOrbit -= 1
      self.OrbitingBase = False
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
      self.orbit.setVisible(False)
    self.starbase.setVisible(False)


  def HideDiagram(self):
    for element in self.diagram:
      element.setVisible(False)


  def ShowNormalView(self):
    self.RevealStarbase()
    self.UpdateFoes()
    self.UpdateOthers()
    self.UpdateFriends()
    self.core.setVisible(self.Friendly)
    if self.Friendly:
      self.body.setVisible(self.TotalOrbit < 1)
    else:
      self.body.setVisible(False)
    self.flag.setVisible(False)
    self.HideDiagram()

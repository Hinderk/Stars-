
import random

from minerals import Minerals
from planetdata import PlanetData
from defines import Stance
from diagram import Diagram


# This class represents the solar systems of the Stars universe each of
# which is represented by just one of its planets and named after its sun.

class Planet(PlanetData):

  GameYear = 2400                  # Modify this date prior to creating the user interface ...

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
    self.center = None
    self.core = None
    self.body = None
    self.ships = None
    self.others = None
    self.flag = None
    self.population = None

    self.scanner = None
    self.diagram = Diagram()

    self.orbitVisible = False
    self.starbaseVisible = False
    self.foesVisible = False
    self.friendsVisible = False
    self.othersVisible = False
    self.coreVisible = False
    self.bodyVisible = False
    self.flagVisible = False

    self.fleets_in_orbit = []
    self.mine_fields = []

    self.TotalFriends = 0
    self.IdleFriends = 0
    self.TotalFoes = 0
    self.TotalOthers = 0
    self.TotalOrbit = 0
    self.Colonists = 0

    self.Discovered = HomeWorld                      # Obviously, the home world is settled
    self.ShipTracking = HomeWorld                    # from the first turn of the game ...
    self.showIdleOnly = False
    self.strengthVisible = False

    self.SpaceStation = False

    self.Crust = Minerals(Rules)                     # Create a random amount of minerals
    self.Explored = PlanetData()                     # inside the planet's crust and - for
    if HomeWorld:                                    # the home world - on its surface
      self.Surface = Minerals(Rules, 0.1)
      self.Explore(Planet.GameYear)                  # Start with the first game year ...
      self.Relation = Stance.allied
    else:
      self.Surface = Minerals()
      self.Relation = Stance.neutral


  def Explore(self, year):
    self.Explored = self
    self.LastVisit = year
    self.Discovered = True


  def Value(self):  # TODO : Compute the planet value ...

    return random.triangular(0.0, 1.0, 0.5)


  def UpdateShipTracking(self):
    if self.Relation == Stance.allied:
      if self.SpaceStation or self.Colonists > 0:
        self.ShipTracking = True
    if self.TotalFriends > 0:
      for f in self.fleets_in_orbit:
        if f.FriendOrFoe == Stance.allied:
          self.ShipTracking = True
          break
    if self.ShipTracking:
      self.Explore(Planet.GameYear)


  def EnterOrbit(self, fleet):
    ships = fleet.ShipCounter
    if ships > 0:
      if fleet.FriendOrFoe == Stance.allied:
        self.UpdateFriends(ships)
      elif fleet.FriendOrFoe == Stance.hostile:
        self.UpdateFoes(ships)
      else:
        self.UpdateOthers(ships)
    fleet.Orbiting = self


  def ClearOrbit(self):
    self.TotalFriends = 0
    self.TotalFoes = 0
    self.TotalOthers = 0
    self.friendsVisible = False
    self.foesVisible = False
    self.othersVisible = False


  def UpdateFriends(self, count=0):
    self.TotalFriends += count
    self.TotalOrbit += count
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
    if self.TotalFriends > 0:
      self.friendsVisible = True
      self.orbitVisible = True
      w0 = self.ships.boundingRect().width()
      x0 = self.ships.x()
      self.ships.setText(str(self.TotalFriends))
      w = self.ships.boundingRect().width()
      self.ships.setX(x0 - w + w0)
    else:
      self.TotalFriends = 0
      self.friendsVisible = False


  def UpdateFoes(self, count=0):
    self.TotalFoes += count
    self.TotalOrbit += count
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
    if self.TotalFoes > 0:
      self.foesVisible |= self.ShipTracking
      w0 = self.attackers.boundingRect().width()
      x0 = self.attackers.x()
      self.attackers.setText(str(self.TotalFoes))
      w = self.attackers.boundingRect().width()
      self.attackers.setX(x0 - w + w0)
    else:
      self.TotalFoes = 0
      self.foesVisible = False


  def UpdateOthers(self, count=0):
    self.TotalOthers += count
    self.TotalOrbit += count
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
    if self.TotalOthers > 0:
      self.othersVisible |= self.ShipTracking
      self.others.setText(str(self.TotalOthers))
    else:
      self.TotalOthers = 0
      self.othersVisible = False


  def BuildStarbase(self):
    if not self.SpaceStation:
      self.TotalOrbit += 1
      self.SpaceStation = True


  def DestroyStarbase(self):
    if self.OrbitingBase:
      self.TotalOrbit -= 1
      self.OrbitingBase = False
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
      self.orbitVisible = False
    self.starbaseVisible = False


  def UpdatePlanetView(self):
    self.UpdateShipTracking()
    self.UpdateFoes()
    self.UpdateOthers()
    self.UpdateFriends()
    if self.SpaceStation:
      self.starbaseVisible = self.ShipTracking
    if self.TotalOrbit < 1:
      self.orbitVisible = False
    else:
      self.orbitVisible |= self.ShipTracking
    self.coreVisible = self.ShipTracking or self.Discovered
    if self.Colonists > 0:
      self.bodyVisible = (self.Relation == Stance.allied)
      self.flagVisible = self.coreVisible
    else:
      self.flagVisible = False


  def ShowDefaultView(self, showNumbers):
    self.center.setVisible(True)
    self.core.setVisible(self.coreVisible)
    self.body.setVisible(False)
    self.orbit.setVisible(self.orbitVisible)
    self.starbase.setVisible(self.starbaseVisible)
    self.neutral.setVisible(self.othersVisible)
    self.foes.setVisible(self.foesVisible)
    self.friends.setVisible(self.friendsVisible)
    self.ships.setVisible(self.friendsVisible and showNumbers)
    self.attackers.setVisible(self.foesVisible and showNumbers)
    self.others.setVisible(self.othersVisible and showNumbers)
    self.population.setVisible(False)
    self.flag.setVisible(False)


  def ShowMinimalView(self):
    self.center.setVisible(True)
    self.core.setVisible(False)
    self.body.setVisible(False)
    self.orbit.setVisible(False)
    self.starbase.setVisible(False)
    self.neutral.setVisible(False)
    self.foes.setVisible(False)
    self.friends.setVisible(False)
    self.ships.setVisible(False)
    self.attackers.setVisible(False)
    self.others.setVisible(False)
    self.population.setVisible(False)
    self.flag.setVisible(False)


  def ShowPercentageView(self):
    self.center.setVisible(False)
    self.core.setVisible(False)
    self.body.setVisible(self.coreVisible)
    self.orbit.setVisible(False)
    self.starbase.setVisible(False)
    self.neutral.setVisible(False)
    self.foes.setVisible(False)
    self.friends.setVisible(False)
    self.ships.setVisible(False)
    self.attackers.setVisible(False)
    self.others.setVisible(False)
    self.population.setVisible(False)
    self.flag.setVisible(self.flagVisible)


  def ShowPopulationView(self):
    self.center.setVisible(not self.bodyVisible)
    self.core.setVisible(False)
    self.body.setVisible(self.bodyVisible)
    self.orbit.setVisible(False)
    self.starbase.setVisible(False)
    self.neutral.setVisible(False)
    self.foes.setVisible(False)
    self.friends.setVisible(False)
    self.ships.setVisible(False)
    self.attackers.setVisible(False)
    self.others.setVisible(False)
    self.population.setVisible(self.bodyVisible)
    self.flag.setVisible(False)
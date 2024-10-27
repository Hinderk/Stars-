
import random

from minerals import Minerals
from planetdata import PlanetData
from defines import Stance
from diagram import Diagram


# This class represents the solar systems of the Stars universe each of
# which is represented by just one of its planets and named after its sun.

class Planet(PlanetData):

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

    self.scanner = None
    self.diagram = Diagram()

    self.orbitVisible = False
    self.starbaseVisible = False
    self.foesVisible = False
    self.friendsVisible = False
    self.attackersVisible = False
    self.coreVisible = False
    self.bodyVisible = False
    self.shipsVisible = False
    self.othersVisible = False
    self.flagVisible = False

    self.fleets_in_orbit = []

    self.TotalFriends = 0
    self.TotalFoes = 0
    self.TotalOthers = 0
    self.TotalOrbit = 0
    self.Colonists = 0

    self.Discovered = HomeWorld                      # Obviously, the home world is settled
    self.ShipTracking = HomeWorld                    # from the first turn of the game ...

    self.SpaceStation = False

    self.Crust = Minerals(Rules)                     # Create a random amount of minerals
    self.Explored = PlanetData()                     # inside the planet's crust and - for
    if HomeWorld:                                    # the home world - on its surface
      self.Surface = Minerals(Rules, 0.1)
      self.Explore(Rules.FirstYear())                # Start with the first game year ...
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


  def UpdateShipTracking(self):  # FIXME:   Use Explore to set Discovered ...
    if self.Relation == Stance.allied:
      self.ShipTracking = self.SpaceStation or self.Colonists > 0   # FIXME: Don't set value, use or operator instead!
      self.Discovered = True
    if self.TotalFriends > 0:
      self.Discovered = True
      self.ShipTracking = True   # FIXME: requires a scanner on board the ships!


  def UpdateFriends(self, count=0):
    self.TotalFriends += count
    self.TotalOrbit += count
    if self.TotalFriends > 0:
      self.friendsVisible = True
      self.orbitVisible = True
      w0 = self.ships.boundingRect().width()
      x0 = self.ships.x()
      self.ships.setText(str(self.TotalFriends))
      w = self.ships.boundingRect().width()
      self.ships.setX(x0 - w + w0)
      self.shipsVisible = True
    else:
      self.TotalFriends = 0
      self.shipsVisible = False
      self.friendsVisible = False
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
      self.orbitVisible = False
    else:
      self.orbitVisible = self.ShipTracking


  def UpdateFoes(self, count=0):
    self.TotalFoes += count
    self.TotalOrbit += count
    if self.TotalFoes > 0:
      self.foesVisible = self.ShipTracking
      self.orbitVisible = self.ShipTracking
      w0 = self.attackers.boundingRect().width()
      x0 = self.attackers.x()
      self.attackers.setText(str(self.TotalFoes))
      w = self.attackers.boundingRect().width()
      self.attackers.setX(x0 - w + w0)
      self.attackersVisible = self.ShipTracking
    else:
      self.TotalFoes = 0
      self.attackersVisible = False
      self.foesVisible = False
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
      self.orbitVisible = False
    else:
      self.orbitVisible = self.ShipTracking


  def UpdateOthers(self, count=0):
    self.TotalOthers += count
    self.TotalOrbit += count
    if self.TotalOthers > 0:
      self.neutralVisible = self.ShipTracking
      self.orbitVisible = self.ShipTracking
      self.others.setText(str(self.TotalOthers))
      self.othersVisible = self.ShipTracking
    else:
      self.TotalOthers = 0
      self.othersVisible = False
      self.neutralVisible = False
    if self.TotalOrbit < 1:
      self.TotalOrbit = 0
      self.orbitVisible = False
    else:
      self.orbitVisible = self.ShipTracking


  def RevealStarbase(self):
    show = self.ShipTracking and self.SpaceStation
    self.orbitVisible = show
    self.starbaseVisible = show


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
      self.orbitVisible = False
    self.starbaseVisible = False


  def UpdatePlanetView(self):
    self.RevealStarbase()
    self.UpdateFoes()
    self.UpdateOthers()
    self.UpdateFriends()
    self.coreVisible = self.ShipTracking or self.Discovered
    if self.Colonists > 0:
      self.bodyVisible = (self.Relation == Stance.allied)
      self.flagVisible = self.coreVisible
    else:
      self.flagVisible = False


  def ShowDefaultView(self):
    self.center.setVisible(True)
    self.core.setVisible(self.coreVisible)
    self.body.setVisible(False)
    self.orbit.setVisible(self.orbitVisible)
    self.starbase.setVisible(self.starbaseVisible)
    self.neutral.setVisible(self.neutralVisible)
    self.foes.setVisible(self.foesVisible)
    self.friends.setVisible(self.friendsVisible)
    self.ships.setVisible(self.friendsVisible)
    self.attackers.setVisible(self.attackersVisible)
    self.others.setVisible(self.neutralVisible)
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
    self.flag.setVisible(False)

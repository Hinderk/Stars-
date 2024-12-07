
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF

from design import Design
from faction import Faction
from guiprop import GuiProps
from defines import Stance
from colours import Pen, Brush
from math import sqrt
from system import SystemType
from defines import Perks
from ruleset import Ruleset



class Fleet:

  arrow = QPolygonF()
  arrow << QPointF(0, 0)
  arrow << QPointF(-GuiProps.w_vector, -GuiProps.h_vector)
  arrow << QPointF(0, GuiProps.dh_vector - GuiProps.h_vector)
  arrow << QPointF(GuiProps.w_vector, -GuiProps.h_vector)

  def __init__(self, ships, fID):
    self.ShipList = []
    self.ShipCounter = 0
    self.Waypoints = []
    self.WaypointIndex = -1
    self.RepeatSchedule = False
    self.Discovered = True           # TODO: Depends on scanners!
    self.Orbiting = None
    self.TotalWeight = 0
    self.TotalFuel = 0
    self.Fuel = 0
    self.Germanium = 0
    self.Boranium = 0
    self.Ironium = 0
    self.Settlers = 0
    self.CargoSpace = 0
    self.MineLaying = 0
    self.MineSweeping = 0
    self.MaxRange = 0
    self.PenRange = 0
    self.StealCargo = False
    self.Name = None
    self.Index = None
    self.Picture = None
    self.FriendOrFoe = Faction.Stance(Ruleset.fID0, fID)
    for s in ships:
      self.AddShip(s)
    self.Faction = fID
    self.scanner = None
    self.MovingFleet = None
    self.RestingFleet = None
    self.ShipCount = None
    self.CloakingFactor = self.ComputeCloaking()
    self.setFleetNameAndIndex()


  def AddShip(self, ship):
    self.ShipList.append(ship)
    self.TotalWeight += ship.TotalWeight
    self.TotalFuel += ship.TotalFuel
    self.Fuel += ship.Fuel
    self.Germanium += ship.Germanium
    self.Boranium += ship.Boranium
    self.Ironium += ship.Ironium
    self.Settlers += ship.Settlers
    self.CargoSpace += ship.CargoSpace
    self.MineLaying += ship.MineLaying
    self.MineSweeping += ship.MineSweeping
    self.UpdateScannerData(ship)


  def UpdateScannerData(self, ship):
    maxrange = 0
    penrange = 0
    for s in ship.Design.System:
      if s.domain == SystemType.SCANNER:
        mr = s.itemType.value[0]
        pr = s.itemType.value[1]
        if s.itemType.value[15] == Perks.ROB:
          self.StealCargo = True
        maxrange += s.itemCount * mr * mr * mr * mr
        penrange += s.itemCount * pr * pr * pr * pr
    if maxrange > 0:
      maxrange = sqrt(sqrt(maxrange))
      if maxrange > self.MaxRange:
        self.MaxRange = maxrange
    if penrange > 0:
      penrange = sqrt(sqrt(penrange))
      if penrange > self.PenRange:
        self.PenRange = penrange


  def ComputeCloaking(self):
    total = 0
    cloak = 0
    for s in self.ShipList:
      if s.Cloaking > 0:
        cloak += s.Cloaking * s.EmptyWeight
      total += s.TotalWeight
    return Ruleset.CloakingRatio(cloak, total)


  def setFleetNameAndIndex(self):
    designs = [s.Design.Index for s in self.ShipList]
    val = -1
    for d in set(designs):
      n = designs.count(d)
      SD = Design.getDesign(d)
      r = SD.ComputeBattleRating()
      if val < n * r:
        self.Picture = SD.getPictureIndex()
        self.Name = SD.getDesignName()
        val = n * r


  def ApplyFilter(self, select):
    self.ShipCounter = 0
    for s in self.ShipList:
      if select[s.Design.Hull.value[2].name]:
        self.ShipCounter += 1


  def getColours(self):
    if self.FriendOrFoe == Stance.allied:
      return (Pen.blue_p, Brush.blue_p)
    elif self.FriendOrFoe == Stance.friendly:
      return (Pen.green_p, Brush.green_p)
    elif self.FriendOrFoe == Stance.neutral:
      return (Pen.yellow_p, Brush.yellow_p)
    else:
      return (Pen.red_p, Brush.red_p)

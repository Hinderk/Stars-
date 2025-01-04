
from PyQt6.QtGui import QPen

import math

from universe import Universe
from design import Design
from faction import Faction
from defines import Stance
from colours import Pen, Brush
from system import SystemType
from defines import Perks
from ruleset import Ruleset
from guiprop import GuiProps as GP



class Fleet:

  Counter = dict()

  def getDelta(dx, dy):
    length = math.sqrt(dx * dx + dy * dy)
    if length > 0:
      scale = GP.Xscale * 100.0 / length   # Warp 10
      return scale * dx, scale * dy
    return 0, 0


  def __init__(self, ships, fID):
    self.xc = 0
    self.yc = 0
    self.ShipList = []
    self.ShipCounter = 0
    self.WarpSpeed = 0
    self.Heading = 0.0
    self.FirstWaypoint = None
    self.ActiveWaypoint = []
    self.LastWaypoint = None
    self.NextWaypoint = None
    self.MineFields = []
    self.RepeatSchedule = False
    self.Idle = True
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
    self.ShipCounter = len(ships)
    for s in ships:
      self.AddShip(s)
    self.Faction = fID
    self.scanner = None
    self.MovingFleet = None
    self.RestingFleet = None
    self.ShipCount = None
    self.Course = None
    self.CloakingFactor = self.ComputeCloaking()
    self.setFleetNameAndIndex()
    if self.Name in Fleet.Counter:
      Fleet.Counter[self.Name] += 1
    else:
      Fleet.Counter[self.Name] = 1
    self.id = Fleet.Counter[self.Name]


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
      maxrange = math.sqrt(math.sqrt(maxrange))
      if maxrange > self.MaxRange:
        self.MaxRange = maxrange
    if penrange > 0:
      penrange = math.sqrt(math.sqrt(penrange))
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


  def ApplyFoeFilter(self, select):
    self.ShipCounter = 0
    for s in self.ShipList:
      if select[s.Design.Hull.value[2].name]:
        self.ShipCounter += 1


  def ApplyMyFilter(self, idle, select):
    self.ShipCounter = 0
    if self.Idle or not idle:
      for s in self.ShipList:
        if select[s.Design.Name]:
          self.ShipCounter += 1


  def GetColours(self, selected=False):
    if self.FriendOrFoe == Stance.allied:
      if selected:
        return (QPen(Pen.blue_h), Brush.blue)
      else:
        return (QPen(Pen.blue_l), Brush.blue)
    elif self.FriendOrFoe == Stance.hostile:
      return (QPen(Pen.red_l), Brush.red)
    else:
      return (QPen(Pen.green), Brush.green)


  def UpdateShipCount(self):
    self.ShipCount.setText(str(self.ShipCounter))
    h = self.ShipCount.boundingRect().height() - 2
    xs = GP.Xscale * self.xc
    ys = GP.Xscale * self.yc
    if abs(self.Heading) > 0.5 * math.pi:
      xs += GP.f_radius + GP.f_dist
    else:
      w = self.ShipCount.boundingRect().width()
      xs -= GP.f_radius + GP.f_dist + w
    self.ShipCount.setPos(xs, ys - h / 2)


  def ShowCourse(self, show):
    if self.Orbiting:
      visible = False
    else:
      visible = show
    wp = self.FirstWaypoint
    while wp.segment and wp != self.NextWaypoint:
      wp.segment.setVisible(False)
      wp = wp.next
    while wp and wp.segment:
      wp.segment.setVisible(visible)
      wp = wp.next
    self.Course.setVisible(visible)


  def ColourCourse(self, selected=False):
    pen, brush = self.GetColours(selected)
    if self.MovingFleet:
      self.MovingFleet.setPen(pen)
      self.MovingFleet.setBrush(brush)
    self.RestingFleet.setPen(pen)
    self.RestingFleet.setBrush(brush)
    pen.setWidthF(Universe.CurrentPathWidth)
    wp = self.FirstWaypoint
    while wp and wp.segment:
      wp.segment.setPen(pen)
      wp = wp.next
    self.Course.setPen(pen)


  def GetOffset(self, wp):
    dx = self.xc - wp.xo
    dy = self.yc - wp.yo
    dist = GP.Xscale * GP.c_dist * math.sqrt(dx * dx + dy * dy)
    if dist > GP.max_dist:
      dist = GP.max_dist
    dx = dist * math.cos(self.Heading)
    dy = dist * math.sin(self.Heading)
    return dx, dy

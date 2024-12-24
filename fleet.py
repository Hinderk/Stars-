
from PyQt6.QtCore import QPointF
from PyQt6.QtCore import QLineF
from PyQt6.QtGui import QPolygonF

import math

from design import Design
from faction import Faction
from guiprop import GuiProps
from defines import Stance, Task
from colours import Pen, Brush
from math import sqrt
from system import SystemType
from defines import Perks
from ruleset import Ruleset
from waypoint import Waypoint
from guiprop import GuiProps as GP



class Fleet:

  arrow = QPolygonF()
  arrow << QPointF(GuiProps.h_vector - GuiProps.dh_vector, 0)
  arrow << QPointF(-GuiProps.dh_vector, -GuiProps.w_vector)
  arrow << QPointF(0, 0)
  arrow << QPointF(-GuiProps.dh_vector, GuiProps.w_vector)


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
    self.ActiveWaypoint = None
    self.LastWaypoint = None
    self.CurrentWaypoint = None
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
    self.Universe = None
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


  def ApplyFoeFilter(self, idle, select):
    self.ShipCounter = 0
    if self.Idle or not idle:
      for s in self.ShipList:
        if select[s.Design.Hull.value[2].name]:
          self.ShipCounter += 1


  def ApplyMyFilter(self, idle, select):
    self.ShipCounter = 0
    if self.Idle or not idle:
      for s in self.ShipList:
        if select[s.Design.Name]:
          self.ShipCounter += 1


  def getColours(self):
    if self.FriendOrFoe == Stance.allied:
      return (Pen.blue_l, Brush.blue)
    elif self.FriendOrFoe == Stance.hostile:
      return (Pen.red_l, Brush.red)
    else:
      return (Pen.green, Brush.green)


  def addWaypoint(self, x, y):
    wa = Waypoint(x, y)
    if self.FirstWaypoint:
      xa = GP.Xscale * wa.xo
      ya = GP.Xscale * wa.yo
      if self.FriendOrFoe == Stance.allied:
        pen = Pen.blue_l
        pen.setWidthF(self.Universe.CurrentPathWidth)
      else:
        pen = None
      w0 = self.ActiveWaypoint
      x0 = GP.Xscale * w0.xo
      y0 = GP.Xscale * w0.yo
      wa.warp = w0.warp
      if w0.next:
        wa.task = Task.MOVE
        if w0.segment:
          self.Universe.removeItem(w0.segment)
          w0.segment = None
        w1 = w0.next
        x1 = GP.Xscale * w1.xo
        y1 = GP.Xscale * w1.yo
        w1.previous = wa
        wa.next = w1
        wa.previous = w0
        w0.next = wa
        if pen:
          line = QLineF(xa, ya, x1, y1)
          wa.segment = self.Universe.addLine(line)
          wa.segment.setPen(pen)
          wa.segment.setZValue(-1)
      else:
        self.LastWaypoint = wa
        w0.next = wa
        wa.previous = w0
      if pen:
        line = QLineF(x0, y0, xa, ya)
        w0.segment = self.Universe.addLine(line)
        w0.segment.setPen(pen)
        w0.segment.setZValue(-1)
    else:
      self.FirstWaypoint = wa
      self.LastWaypoint = wa
      self.CurrentWaypoint = wa
    self.ActiveWaypoint = wa


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

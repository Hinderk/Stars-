
from faction import Faction
from math import sqrt
from system import SystemType
from defines import Perks
from ruleset import Ruleset



class Fleet:


  def __init__(self, ship, fID):
    self.ShipList = [ship]
    self.TotalWeight = ship.TotalWeight
    self.TotalFuel = ship.TotalFuel
    self.Fuel = ship.Fuel
    self.Germanium = ship.Germanium
    self.Boranium = ship.Boranium
    self.Ironium = ship.Ironium
    self.Settlers = ship.Settlers
    self.CargoSpace = ship.CargoSpace
    self.MineLaying = ship.MineLaying
    self.MineSweeping = ship.MineSweeping
    self.FriendOrFoe = Faction.Stance(Ruleset.fID0, fID)
    self.Name = ship.Name
    self.Design = ship.Design
    self.Faction = fID
    self.scanner = None
    self.StealCargo = False
    self.CloakingFactor = self.ComputeCloaking()
    self.MaxRange = 0
    self.PenRange = 0
    self.UpdateScannerData(ship)


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
#    self.UpdateShipDesign(ship)  # TODO: Rank battle rating & modify flagship if necessary
    self.UpdateScannerData(ship)


  def UpdateScannerData(self, ship):
    maxrange = 0
    penrange = 0
    for s in ship.System:
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

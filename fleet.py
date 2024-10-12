
from defines import Stance



class Fleet:

  def __init__(self, ship, faction, fof=Stance.friendly):
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
    self.FriendOrFoe = fof
    self.Name = ship.Name
    self.Faction = faction


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


  def DestroyShip(self, ship):
    if ship in self.ShipList:
      self.TotalWeight -= ship.TotalWeight
      self.TotalFuel -= ship.TotalFuel
      self.Fuel -= ship.Fuel
      self.Germanium -= ship.Germanium
      self.Boranium -= ship.Boranium
      self.Ironium -= ship.Ironium
      self.Settlers -= ship.Settlers
      self.CargoSpace -= ship.CargoSpace
      self.MineLaying -= ship.MineLaying
      self.MineSweeping -= ship.MineSweeping
      self.ShipList.remove(ship)



class Fleet:

  def __init__(self, ship):
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


    
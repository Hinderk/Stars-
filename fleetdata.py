
from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from guiprop import GuiProps as GP
from colours import Brush, Pen
from defines import Stance



class Fleetdata(QGraphicsView):

  xOffset = 150
  yOffset = 110
  yDelta = 35
  ySize = 27
  xWidth = 550
  xText = 100
  IconWidth = 120
  DataOffset = 180
  FlagOffset = 20
  TopOffset = 10


  def __init__(self):
    super(self.__class__, self).__init__()
    self.Freight = []
    self.HullLogo = dict()
    self.Scene = QGraphicsScene(self)
    self.AddStaticText()
    self.AddInfoText()
    self.InitCargo()
    self.AddLogos()
    self.setScene(self.Scene)
    self.setMaximumHeight(325)
    self.FleetPicture = 0
    self.CurrentBanner = 0


  def AddStaticText(self):
    ShipCount = self.Scene.addSimpleText("Ship count:", GP.infoFont)
    xpos = self.xOffset
    ypos = 0
    ShipCount.moveBy(xpos, ypos)
    FuelLoad = self.Scene.addSimpleText("Fuel:", GP.infoFont)
    ypos += self.yDelta + 5
    FuelLoad.moveBy(xpos, ypos)
    Cargo = self.Scene.addSimpleText("Cargo:", GP.infoFont)
    ypos += self.yDelta
    Cargo.moveBy(xpos, ypos)
    FleetMass = self.Scene.addSimpleText("Fleet Mass:", GP.infoFont)
    ypos += self.yDelta + 5
    FleetMass.moveBy(xpos, ypos)
    Waypoint = self.Scene.addSimpleText("Next Waypoint:", GP.infoFont)
    ypos += self.yDelta
    Waypoint.moveBy(xpos, ypos)
    Task = self.Scene.addSimpleText("Waypoint Task:", GP.infoFont)
    ypos += self.yDelta
    Task.moveBy(xpos, ypos)
    Speed = self.Scene.addSimpleText("Warp Speed:", GP.infoFont)
    ypos += self.yDelta
    Speed.moveBy(xpos, ypos)
#    self.Mines = self.Scene.addSimpleText("", GP.infoFont)
#    ypos += self.yDelta
#    self.Mines.moveBy(xpos, ypos)
    self.Sweeps = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.Sweeps.moveBy(xpos, ypos)


  def AddInfoText(self):
    self.ShipCount = self.Scene.addSimpleText("", GP.infoFont)
    xpos = self.xOffset + self.DataOffset
    ypos = 0
    self.ShipCount.moveBy(xpos, ypos)
    ypos += 2 * self.yDelta + 10
    self.Mass = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.Mass.moveBy(xpos, ypos)
    self.Waypoint = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.Waypoint.moveBy(xpos, ypos)
    self.Task = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.Task.moveBy(xpos, ypos)
    self.Speed = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.Speed.moveBy(xpos, ypos)


  def InitCargo(self):
    brush = [Brush.white, Brush.yellow, Brush.green, Brush.blue_f, Brush.red]
    xp = self.xOffset + self.xText
    yp = self.yDelta + 5
    box = QRectF(xp, yp, self.xWidth, self.ySize)
    self.Scene.addRect(box, Pen.black_2, Brush.grey)
    box = QRectF(xp, yp, self.xWidth / 2, self.ySize)
    self.Fuel = self.Scene.addRect(box, Pen.black_2, brush[4])
    self.FuelWeight = self.Scene.addSimpleText("", GP.cargoFont)
    yp += self.yDelta + 2
    box = QRectF(xp, yp, self.xWidth, self.ySize)
    self.Scene.addRect(box, Pen.black_2, Brush.grey)
    for n in (0, 1, 2, 3):
      box = QRectF(xp, yp, self.xWidth, self.ySize)
      self.Freight.append(self.Scene.addRect(box, Pen.black_2, brush[n]))
    self.Cargo = self.Scene.addSimpleText("", GP.cargoFont)


  def UpdateCargo(self, fleet):
    self.FactionBanner[self.CurrentBanner].setVisible(False)
    self.HullLogo[self.FleetPicture].setVisible(False)
    self.CurrentBanner = fleet.BannerIndex
    self.FleetPicture = fleet.Picture
    self.FactionBanner[self.CurrentBanner].setVisible(True)
    self.HullLogo[self.FleetPicture].setVisible(True)
    fraction = []
    fuel = self.xWidth * fleet.Fuel / fleet.TotalFuel
    xp = self.xOffset + self.xText
    yp = self.yDelta + 5
    self.Fuel.setRect(xp, yp, fuel, self.ySize)
    self.FuelWeight.setText(str(fleet.Fuel) + " of " + str(fleet.TotalFuel) + "mg")
    x = self.xWidth - self.FuelWeight.boundingRect().width()
    self.FuelWeight.setPos(xp + x / 2, yp + 2)
    fraction.append(fleet.Ironium / fleet.CargoSpace)
    fraction.append(fleet.Boranium / fleet.CargoSpace)
    fraction.append(fleet.Germanium / fleet.CargoSpace)
    fraction.append(fleet.Settlers / fleet.CargoSpace)
    total = fleet.Germanium + fleet.Boranium + fleet.Ironium + fleet.Settlers
    self.Mass.setText(str(total + fleet.TotalWeight))
    for n in (1, 2, 3):
      fraction[n] += fraction[n - 1]
    text = " of " + str(fleet.CargoSpace) + "kT"
    yp += self.yDelta + 2
    for n in (0, 1, 2, 3):
      self.Freight[3 - n].setRect(xp, yp, self.xWidth * fraction[n], self.ySize)
    self.Cargo.setText(str(total) + text)
    x = self.xWidth - self.Cargo.boundingRect().width()
    self.Cargo.setPos(xp + x / 2, yp + 2)
    if fleet.FriendOrFoe == Stance.allied:
      self.backdrop.setBrush(Brush.blue_p)
    elif fleet.FriendOrFoe == Stance.friendly:
      self.backdrop.setBrush(Brush.green_p)
    elif fleet.FriendOrFoe == Stance.neutral:
      self.backdrop.setBrush(Brush.yellow_p)
    else:
      self.backdrop.setBrush(Brush.red_p)
#    if fleet.MineLaying > 0:
#      text = 'This fleet can lay up to ' + str(fleet.MineLaying)
#      self.Mines.setText(text + ' mines per year.')
#    else:
#      self.Mines.setText('')
    if fleet.MineSweeping > 0:
      text = 'This fleet can destroy up to ' + str(fleet.MineSweeping)
      self.Sweeps.setText(text + ' mines per year.')
    else:
      self.Sweeps.setText('')
    if fleet.NextWaypoint:
      if fleet.NextWaypoint.planet:
        self.Waypoint.setText(fleet.NextWaypoint.planet.Name)
      else:
        x = str(fleet.NextWaypoint.xo)
        y = str(fleet.NextWaypoint.yo)
        self.Waypoint.setText('(' + x + ',' + y + ')')
      self.Task.setText(fleet.NextWaypoint.task.value)
    else:
      self.Waypoint.setText('None')
    if fleet.WarpSpeed > 0:
      self.Speed.setText(str(fleet.WarpSpeed))
    else:
      self.Speed.setText('Stopped')
      self.Task.setText(fleet.Task.value)
    self.ShipCount.setText(str(len(fleet.ShipList)))


  def UpdateInfo(self, speed, wp):
    if wp:
      if wp.planet:
        self.Waypoint.setText(wp.planet.Name)
      else:
        self.Waypoint.setText('(' + str(wp.xo) + ',' + str(wp.yo) + ')')
    if speed > 0:
      self.Speed.setText(str(speed))
    else:
      self.Speed.setText('Stopped')


  def AddLogos(self):
    self.HullLogo = []
    yp = self.TopOffset
    rectangle = QRectF(1, yp + 1, self.IconWidth - 2, self.IconWidth - 2)
    self.backdrop = self.Scene.addRect(rectangle)
    for e1 in "abcdefghi":
      for e2 in "123456":
        resource = "Design/Images/Graphics/ship-" + e1 + e2 + ".svg"
        image = QGraphicsSvgItem(resource)
        width = image.boundingRect().width()
        if width > 0:
          image.setScale(self.IconWidth / width)
          image.setPos(0, yp)
          image.setVisible(False)
          self.Scene.addItem(image)
          self.HullLogo.append(image)
    yp += self.FlagOffset + self.IconWidth
    self.FactionBanner = []
    for faction in "ABCDEFGHIJKLMNOPQRST":
      resource = ":/Factions/Faction-" + faction
      banner = QGraphicsSvgItem(resource)
      width = banner.boundingRect().width()
      banner.setScale(0.5 * self.IconWidth / width)
      banner.setPos(0.25 * self.IconWidth, yp)
      banner.setVisible(False)
      self.Scene.addItem(banner)
      self.FactionBanner.append(banner)
    self.Scene.addRect(QRectF(800, 315, 5, 5), Pen.noshow)

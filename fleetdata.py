
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPen, QBrush, QColor, QFont
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6 import QtSvgWidgets



class Fleetdata(QGraphicsView):

  xOffset = 150
  yOffset = 110
  yDelta = 35
  ySize = 27
  xWidth = 550
  xText = 100
  IconWidth = 120
  DataOffset = 150
  FlagOffset = 20
  TopOffset = 10


  def __init__(self):
    super(self.__class__, self).__init__()

    self.Freight = []

    self.Scene = QGraphicsScene(self)

    self.AddStaticText()
    self.AddInfoText()
    self.SetupColors()
    self.InitCargo()
    self.AddLogos()
    self.setScene(self.Scene)
    self.setMaximumHeight(325)


  def AddStaticText(self):
    font = QFont('Segoe', pointSize=16, weight=400)
    ShipCount = self.Scene.addSimpleText("Ship count:", font)
    xpos = self.xOffset
    ypos = 0
    ShipCount.moveBy(xpos, ypos)
    FuelLoad = self.Scene.addSimpleText("Fuel:", font)
    ypos += self.yDelta + 5
    FuelLoad.moveBy(xpos, ypos)
    Cargo = self.Scene.addSimpleText("Cargo:", font)
    ypos += self.yDelta
    Cargo.moveBy(xpos, ypos)
    FleetMass = self.Scene.addSimpleText("Fleet Mass:", font)
    ypos += self.yDelta + 5
    FleetMass.moveBy(xpos, ypos)
    Waypoint = self.Scene.addSimpleText("Next Waypoint:", font)
    ypos += self.yDelta
    Waypoint.moveBy(xpos, ypos)
    Task = self.Scene.addSimpleText("Waypoint Task:", font)
    ypos += self.yDelta
    Task.moveBy(xpos, ypos)
    Speed = self.Scene.addSimpleText("Warp Speed:", font)
    ypos += self.yDelta
    Speed.moveBy(xpos, ypos)
    text = "This fleet can lay up to 100 mines per year."
    self.Mines = self.Scene.addSimpleText(text, font)
    ypos += self.yDelta
    self.Mines.moveBy(xpos, ypos)
    text = "This fleet can destroy up to 100 mines per year."
    self.Sweeps = self.Scene.addSimpleText(text, font)
    ypos += self.yDelta
    self.Sweeps.moveBy(xpos, ypos)


  def AddInfoText(self):
    font = QFont('Segoe', pointSize=16, weight=400)
    self.ShipCount = self.Scene.addSimpleText("1", font)
    xpos = self.xOffset + self.DataOffset
    ypos = 0
    self.ShipCount.moveBy(xpos, ypos)
    ypos += 2 * self.yDelta + 10
    self.Mass = self.Scene.addSimpleText("999kT", font)
    ypos += self.yDelta
    self.Mass.moveBy(xpos, ypos)
    self.Waypoint = self.Scene.addSimpleText("none", font)
    ypos += self.yDelta
    self.Waypoint.moveBy(xpos, ypos)
    self.Task = self.Scene.addSimpleText("none", font)
    ypos += self.yDelta
    self.Task.moveBy(xpos, ypos)
    self.Speed = self.Scene.addSimpleText("12", font)
    ypos += self.yDelta
    self.Speed.moveBy(xpos, ypos)


  def InitCargo(self):
    font = QFont('Segoe', pointSize=14, weight=800)
    pen = QPen(QColor(0, 0, 0))
    pen.setWidthF(2.3)
    xp = self.xOffset + self.xText
    yp = self.yDelta + 5
    box = QRectF(xp, yp, self.xWidth / 2, self.ySize)
    self.Fuel = self.Scene.addRect(box, QPen(), self.brush[4])
    self.FuelWeight = self.Scene.addSimpleText("50 of 100kT", font)
    x = self.xWidth - self.FuelWeight.boundingRect().width()
    self.FuelWeight.setPos(xp + x / 2, yp + 2)
    box = QRectF(xp, yp, self.xWidth, self.ySize)
    self.Scene.addRect(box, pen)
    yp += self.yDelta + 2
    width = self.xWidth
    for n in (0, 1, 2, 3):
      width *= 0.75
      box = QRectF(xp, yp, width, self.ySize)
      self.Freight.append(self.Scene.addRect(box, QPen(), self.brush[n]))
    self.Cargo = self.Scene.addSimpleText("75 of 100kT", font)
    x = self.xWidth - self.Cargo.boundingRect().width()
    self.Cargo.setPos(xp + x / 2, yp + 2)
    box = QRectF(xp, yp, self.xWidth, self.ySize)
    self.Scene.addRect(box, pen)


  def UpdateCargo(self, fleet):
    fraction = []
    fuel = self.xWidth * fleet.Fuel / fleet.TotalFuel
    xp = self.xOffset + self.xText
    yp = self.yDelta + 5
    self.Fuel.setRect(xp, yp, fuel, self.ySize)
    self.FuelWeight.setText(str(fleet.Fuel) + " of " + str(fleet.TotalFuel) + "kT")
    x = self.xWidth - self.FuelWeight.boundingRect().width()
    self.FuelWeight.setPos(xp + x / 2, yp + 2)
    fraction.append(fleet.Ironium / fleet.CargoSpace)
    fraction.append(fleet.Boranium / fleet.CargoSpace)
    fraction.append(fleet.Germanium / fleet.CargoSpace)
    fraction.append(fleet.Settlers / fleet.CargoSpace)
    total = fleet.Germanium + fleet.Boranium + fleet.Ironium + fleet.Settlers
    for n in (1, 2, 3):
      fraction[n] += fraction[n - 1]
    text = " of " + str(fleet.CargoSpace) + "kT"
    yp += self.yDelta + 2
    for n in (0, 1, 2, 3):
      self.Freight[3 - n].setRect(xp, yp, self.xWidth * fraction[n], self.ySize)
    self.Cargo.setText(str(total) + text)
    x = self.xWidth - self.Cargo.boundingRect().width()
    self.Cargo.setPos(xp + x / 2, yp + 2)


  def SetupColors(self):
    blue = QColor(40, 40, 255)
    green = QColor(0, 255, 0)
    yellow = QColor(255, 255, 0)
    red = QColor(255, 0, 0)
    white = QColor(255, 255, 255)
    self.brush = [QBrush(white), QBrush(yellow), QBrush(green), QBrush(blue), QBrush(red)]


  def AddLogos(self):
    self.FleetImage = QtSvgWidgets.QGraphicsSvgItem(":/Graphics/Enigma")
    width = self.FleetImage.boundingRect().width()
    self.FleetImage.setScale(self.IconWidth / width)
    yp = self.TopOffset
    self.FleetImage.setPos(0, yp)
    self.Scene.addItem(self.FleetImage)
    self.FlagImage = QtSvgWidgets.QGraphicsSvgItem(":/Graphics/Enigma")
    width = self.FlagImage.boundingRect().width()
    self.FlagImage.setScale(0.5 * self.IconWidth / width)
    yp += self.FlagOffset + self.IconWidth
    self.FlagImage.setPos(0.25 * self.IconWidth, yp)
    self.Scene.addItem(self.FlagImage)

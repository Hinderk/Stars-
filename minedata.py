
from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
# from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from math import sqrt

from guiprop import GuiProps as GP
from colours import Brush
from minefield import Minefield
from defines import Stance



class Minedata(QGraphicsView):

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
    self.Scene = QGraphicsScene(self)
    self.AddStaticText()
    self.AddInfoText()
    self.AddLogos()
    self.setScene(self.Scene)
    self.setMaximumHeight(325)
    self.CurrentFaction = 0


  def AddStaticText(self):
    Location = self.Scene.addSimpleText("Location:", GP.infoFont)
    xpos = self.xOffset
    ypos = 0
    Location.moveBy(xpos, ypos)
    FieldType = self.Scene.addSimpleText("Field Type:", GP.infoFont)
    ypos += self.yDelta
    FieldType.moveBy(xpos, ypos)
    FieldRadius = self.Scene.addSimpleText("Field Radius:", GP.infoFont)
    ypos += self.yDelta
    FieldRadius.moveBy(xpos, ypos)
    MineCount = self.Scene.addSimpleText("Live Mines:", GP.infoFont)
    ypos += self.yDelta
    MineCount.moveBy(xpos, ypos)
    DecayRate = self.Scene.addSimpleText("Decay Rate:", GP.infoFont)
    ypos += self.yDelta
    DecayRate.moveBy(xpos, ypos)
    self.IndexLabel = self.Scene.addSimpleText("Field:", GP.infoFont)
    ypos += 2 * self.yDelta
    self.IndexLabel.moveBy(xpos, ypos)
    Spacer = self.Scene.addSimpleText(" ", GP.infoFont)
    ypos += 2 * self.yDelta
    Spacer.moveBy(xpos + 640, ypos)


  def AddInfoText(self):
    self.Location = self.Scene.addSimpleText("", GP.infoFont)
    xpos = self.xOffset + self.DataOffset
    ypos = 0
    self.Location.moveBy(xpos, ypos)
    self.FieldType = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.FieldType.moveBy(xpos, ypos)
    self.FieldRadius = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.FieldRadius.moveBy(xpos, ypos)
    self.MineCount = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.MineCount.moveBy(xpos, ypos)
    self.DecayRate = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.DecayRate.moveBy(xpos, ypos)
    self.FieldIndex = self.Scene.addSimpleText("", GP.infoFont)
    ypos += 2 * self.yDelta
    self.FieldIndex.moveBy(xpos, ypos)


  def UpdateData(self, field: Minefield, index, maxindex):
    self.FactionBanner[self.CurrentFaction].setVisible(False)
    self.CurrentFaction = field.faction
    self.FactionBanner[field.faction].setVisible(True)
    text = '(' + str(field.x) + ',' + str(field.y) + ')'
    self.Location.setText(text)
    self.FieldType.setText(field.model.value)
    radius = round(10 * sqrt(field.mines) + 0.5) / 10
    self.FieldRadius.setText(str(radius))
    self.MineCount.setText(str(field.mines))
    rate = round(field.mines * field.rate_of_decay + 0.5)
    self.DecayRate.setText(str(rate) + ' / year')
    if maxindex > 1:
      self.FieldIndex.setText(str(index) + ' of ' + str(maxindex))
      self.FieldIndex.setVisible(True)
      self.IndexLabel.setVisible(True)
    else:
      self.IndexLabel.setVisible(False)
      self.FieldIndex.setVisible(False)
    if field.fof == Stance.allied:
      self.backdrop.setBrush(Brush.blue_p)
    elif field.fof == Stance.friendly:
      self.backdrop.setBrush(Brush.yellow_p)
    else:
      self.backdrop.setBrush(Brush.red_p)


  def AddLogos(self):
    yp = self.TopOffset
    rectangle = QRectF(1, yp + 1, self.IconWidth - 2, self.IconWidth - 2)
    self.backdrop = self.Scene.addRect(rectangle)
    image = QGraphicsSvgItem(":/Graphics/Mines")
    width = image.boundingRect().width()
    image.setScale(self.IconWidth / width)
    image.setPos(0, yp)
    self.Scene.addItem(image)
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
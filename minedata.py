
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPen, QBrush, QColor, QFont # , QPixmap
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
# from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from guiprop import GuiProps as GP
from colours import Brush



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
    DecayRate = self.Scene.addSimpleText("Decay Rate:", GP.infoFont)
    ypos += self.yDelta
    DecayRate.moveBy(xpos, ypos)
    FieldIndex = self.Scene.addSimpleText("Field:", GP.infoFont)
    ypos += self.yDelta
    FieldIndex.moveBy(xpos, ypos)


  def AddInfoText(self):
    self.Location = self.Scene.addSimpleText("", GP.infoFont)
    xpos = self.xOffset + self.DataOffset
    ypos = 0
    self.Location.moveBy(xpos, ypos)
    ypos += self.yDelta
    self.FieldType = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.FieldType.moveBy(xpos, ypos)
    self.FieldRadius = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.FieldRadius.moveBy(xpos, ypos)
    self.DecayRate = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.DecayRate.moveBy(xpos, ypos)
    self.FieldIndex = self.Scene.addSimpleText("", GP.infoFont)
    ypos += self.yDelta
    self.FieldIndex.moveBy(xpos, ypos)


  def UpdateData(self, field):
    self.FactionBanner[self.CurrentFaction].setVisible(False)
    self.CurrentFaction = field.faction
    self.FactionBanner[field.faction].setVisible(True)
    text = '(' + str(field.x) + ',' + str(field.y) + ')'
    self.Location.setText(text)



  def AddLogos(self):
    yp = self.TopOffset
    resource = "Design/Images/Graphics/ship-a.svg"
    image = QGraphicsSvgItem(resource)
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
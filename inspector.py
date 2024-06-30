
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPen, QBrush, QColor, QPolygon
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PyQt6.QtWidgets import QGraphicsSimpleTextItem



class Inspector(QGraphicsScene):

  xMinerals = 0
  yMinerals = 0
  xWidth = 1000
  yWidth = 120
  xOffset = 40
  TextOffset = 2

  def __init__(self, planet):
    super(self.__class__, self).__init__()

    self.sConc = []
    self.sText = []
    sConc = []

    sConc.append(planet.Available.Ironium)
    sConc.append(planet.Available.Boranium)
    sConc.append(planet.Available.Germanium)
    black = QColor(0, 0, 0)
    white = QColor(255, 255, 255)
    blue = QColor(0, 0, 255)
    green = QColor(0, 255, 0)
    yellow = QColor(255, 255, 0)
    whitePen = QPen(white)
    blackPen = QPen(black)
    tpen = (QPen(white), blackPen, blackPen)
    pen = (QPen(blue), QPen(green), QPen(yellow))
    brush = (QBrush(blue), QBrush(green), QBrush(yellow))
    caret = QPolygon()
    blackBrush = QBrush(black)
    whitePen.setWidth(2)
    deltaX = self.xWidth / 10
    deltaY = self.yWidth / 17
    Minerals = QRectF(self.xMinerals, self.yMinerals, self.xWidth, self.yWidth)
    
    self.addRect(Minerals, blackPen, blackBrush)
    xp = 0
    for n in range(0, 10):
      xp += deltaX
      self.addLine(xp, 0, xp, self.yWidth, whitePen)
    yp = self.yMinerals + 2 * deltaY
    for n in (0, 1, 2):
      xlen = self.xWidth * sConc[n] / 5000.0
      show = False
      if xlen > self.xWidth:
        show = True
        xlen = self.xWidth
      box = QRectF(self.xMinerals, yp, xlen, 3 * deltaY)
      self.sConc.append( self.addRect(box, pen[n], brush[n]))
      label = self.addSimpleText(str(sConc[n]))
      label.setPos(self.xMinerals + self.xOffset, yp + self.TextOffset)
      label.setPen(tpen[n])
      label.setVisible(show)
      self.sText.append(label)
      yp += 5 * deltaY
      
      
  def Update(self, planet):
    sConc = []
    sConc.append(planet.Available.Ironium)
    sConc.append(planet.Available.Boranium)
    sConc.append(planet.Available.Germanium)
    deltaY = self.yWidth / 17
    yp = self.yMinerals + 2 * deltaY
    for n in (0, 1, 2):
      xlen = self.xWidth * sConc[n] / 5000.0
      show = False
      if xlen > self.xWidth:
        show = True
        xlen = self.xWidth
      self.sConc[n].setRect(self.xMinerals, yp, xlen, 3 * deltaY)
      self.sText[n].setVisible(show)
      self.sText[n].setText(str(sConc[n]))
      yp += 5 * deltaY
      
    

from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QPolygonF, QFont
from PyQt6.QtWidgets import QGraphicsScene

import math



class Inspector(QGraphicsScene):

  xInfo = 130
  yInfo = 60
  xMinerals = 130
  yMinerals = 180
  xWidth = 1000
  yWidth = 100
  xOffset = 40
  TextOffset = 1
  LeftOffset = 10
  BottomOffset = 5
  RightOffset = 10
  TopOffset = 5


  def __init__(self, people):
    super(self.__class__, self).__init__()

    self.mConc = []
    self.sConc = []
    self.sText = []
    self.Biome = []

#    Data = []
#    Data.append(0.5 + math.log2(planet.Gravity) / 3.0)
#    Data.append(0.5 + planet.Temperature / 400.0)
#    Data.append(planet.Radioactivity / 100.0)

    self.AddStaticText()
    self.SetupColors()
    self.PaintBackdrop(people)
    self.InitBiome()
    self.InitMinerals()


  def AddStaticText(self):
    font = QFont('Segoe', pointSize=16, weight=400)
    self.ReportAge = self.addSimpleText("Report is current.", font)
    self.ReportAge.moveBy(self.xInfo, (self.yInfo-self.TopOffset) / 2 )
    self.PlanetValue = self.addSimpleText("Value: 100%", font)
    self.PlanetValue.moveBy(self.xInfo, 0)
    self.Population = self.addSimpleText("Uninhabited", font)
    width = self.xWidth - self.Population.boundingRect().width()
    self.Population.moveBy(self.xInfo + width, 0)
    xp = self.xInfo + self.xWidth + self.RightOffset
    deltaY = self.yWidth / 3
    Gravity = self.addSimpleText("Gravity", font)
    width = Gravity.boundingRect().width() + self.LeftOffset
    height = self.yWidth - 3 * Gravity.boundingRect().height()
    yp = self.yInfo + height / 6.0
    Gravity.moveBy(self.xInfo - width, yp)
    self.Gravity = self.addSimpleText("8.00g", font)
    self.Gravity.moveBy(xp, yp)
    yp += deltaY
    Temperature = self.addSimpleText(" Temperature", font)
    width = Temperature.boundingRect().width() + self.LeftOffset
    Temperature.moveBy(self.xInfo - width, yp)
    self.Temperature = self.addSimpleText("-250\u00B0CC", font)
    self.Temperature.moveBy(xp, yp)
    yp += deltaY
    Radiation = self.addSimpleText("Radiation", font)
    width = Radiation.boundingRect().width() + self.LeftOffset
    Radiation.moveBy(self.xInfo - width, yp)
    self.Radiation = self.addSimpleText("100mR", font)
    self.Radiation.moveBy(xp, yp)
    deltaY = self.yWidth / 17
    yp = self.yMinerals + deltaY
    Ironium = self.addSimpleText("Ironium", font)
    width = Ironium.boundingRect().width() + self.LeftOffset
    Ironium.moveBy(self.xMinerals - width, yp)
    yp += 5 * deltaY
    Boranium = self.addSimpleText("Boranium", font)
    width = Boranium.boundingRect().width() + self.LeftOffset
    Boranium.moveBy(self.xMinerals - width, yp)
    yp += 5 * deltaY
    Germanium = self.addSimpleText("Germanium", font)
    width = Germanium.boundingRect().width() + self.LeftOffset
    Germanium.moveBy(self.xMinerals - width, yp)
    kt = 0
    xp = self.xMinerals
    yp = self.yMinerals + self.yWidth + self.BottomOffset
    for i in range(11):
      label = self.addSimpleText(str(kt), font)
      kt += 500
      dx = label.boundingRect().width() / 2
      label.moveBy(xp - dx, yp)
      xp += self.xWidth / 10
    label = self.addSimpleText("kt", font)
    xp = label.boundingRect().width() + 3 * self.LeftOffset
    label.moveBy(self.xMinerals - xp, yp)


  def InitBiome(self):
    caret = QPolygonF()
    dy = self.yWidth / 12.0
    caret << QPointF(0, 0) << QPointF(dy, dy)
    caret << QPointF(0, dy + dy) << QPointF(-dy, dy)
    yp = self.yInfo + dy
    for n in (0, 1, 2):
      xp = self.xWidth * 0.5
      mark = caret.translated(xp, yp)
      self.Biome.append(self.addPolygon(mark, self.pen[n + 6], self.brush[n + 6]))
      yp += 4 * dy


  def InitMinerals(self):
    textPen = QPen(QColor(255, 255, 255))
    caret = QPolygonF()
    dy = self.yWidth / 12.0
    caret << QPointF(0, 0) << QPointF(dy, dy)
    caret << QPointF(0, dy + dy) << QPointF(-dy, dy)
    deltaY = self.yWidth / 17
    yp = self.yMinerals + 2 * deltaY
    for n in (0, 1, 2):
      xlen = self.xWidth / 2
      xp = self.xWidth
      show = False
      if xlen > self.xWidth:
        show = True
        xlen = self.xWidth
      box = QRectF(self.xMinerals, yp, xlen, 3 * deltaY)
      mark = caret.translated(xp, yp)
      self.sConc.append(self.addRect(box, self.pen[n + 3], self.brush[n + 3]))
      self.mConc.append(self.addPolygon(mark, self.pen[n + 9], self.brush[n + 9]))
      label = self.addSimpleText(str(1000))
      label.setPos(self.xMinerals + self.xOffset, yp + self.TextOffset)
      label.setPen(textPen)
      label.setVisible(show)
      self.sText.append(label)
      yp += 5 * deltaY


  def UpdateMinerals(self, planet):
    sConc = []
    mConc = []
    mConc.append(planet.Crust.Ironium / 100.0)
    mConc.append(planet.Crust.Boranium / 100.0)
    mConc.append(planet.Crust.Germanium / 100.0)
    sConc.append(planet.Mined.Ironium)
    sConc.append(planet.Mined.Boranium)
    sConc.append(planet.Mined.Germanium)
    deltaY = self.yWidth / 17
    yp = self.yMinerals + 2 * deltaY
    for n in (0, 1, 2):
      caret = self.mConc[n].polygon()
      dx = self.xWidth * mConc[n] - caret.first().x()
      caret.translate(self.xMinerals + dx, 0)
      self.mConc[n].setPolygon(caret)
      show = False
      xlen = self.xWidth * sConc[n] / 5000.0
      if xlen > self.xWidth:
        show = True
        xlen = self.xWidth - 1
      self.sConc[n].setRect(self.xMinerals, yp, xlen, 3 * deltaY)
      self.sText[n].setVisible(show)
      self.sText[n].setText(str(sConc[n]))
      yp += 5 * deltaY


  def UpdateBiome(self, planet):
    Data = []
    Data.append(0.5 + math.log2(planet.Gravity) / 6.0)
    Data.append(0.5 + planet.Temperature / 400.0)
    Data.append(planet.Radioactivity / 100.0)
    for n in (0, 1, 2):
      caret = self.Biome[n].polygon()
      dx = self.xWidth * Data[n] - caret.first().x()
      caret.translate(self.xInfo + dx, 0)
      self.Biome[n].setPolygon(caret)
    g = int(planet.Gravity * 100 + 0.5) / 100
    t = int(planet.Temperature + 300.5) - 300
    r = int(planet.Radioactivity + 0.5)
    self.Gravity.setText(str(g) + "g")
    self.Temperature.setText(str(t) + "\u00B0C")
    self.Radiation.setText(str(r) + "mR")


  def SetupColors(self):
    blue = QColor(0, 0, 255, 120)
    green = QColor(0, 255, 0, 140)
    yellow = QColor(255, 255, 0, 160)
    red = QColor(255, 0, 0, 180)
    self.pen = [QPen(blue), QPen(red), QPen(green), QPen(blue), QPen(green), QPen(yellow)]
    self.brush = [QBrush(blue), QBrush(red), QBrush(green), QBrush(blue), QBrush(green), QBrush(yellow)]
    blue = QColor(0, 0, 255)
    green = QColor(0, 255, 0)
    yellow = QColor(255, 255, 0)
    red = QColor(255, 0, 0)
    self.pen.append(QPen(blue))
    self.pen.append(QPen(red))
    self.pen.append(QPen(green))
    self.pen.append(QPen(blue))
    self.pen.append(QPen(green))
    self.pen.append(QPen(yellow))
    self.brush.append(QBrush(blue))
    self.brush.append(QBrush(red))
    self.brush.append(QBrush(green))
    self.brush.append(QBrush(blue))
    self.brush.append(QBrush(green))
    self.brush.append(QBrush(yellow))


  def PaintBackdrop(self, people):
    black = QColor(0, 0, 0)
    white = QColor(255, 255, 255, 150)
    whitePen = QPen(white)
    blackPen = QPen(black)
    blackBrush = QBrush(black)
    whitePen.setWidth(2)
    deltaX = self.xWidth / 10
    deltaY = self.yWidth / 3
    Info = QRectF(self.xInfo, self.yInfo, self.xWidth, self.yWidth)
    self.addRect(Info, blackPen, blackBrush)
    xp = self.xInfo + self.xWidth
    yp = self.yInfo + deltaY
    self.addLine(self.xInfo, yp, xp, yp, whitePen)
    yp += deltaY
    self.addLine(self.xInfo, yp, xp, yp, whitePen)
    Minerals = QRectF(self.xMinerals, self.yMinerals, self.xWidth, self.yWidth)
    self.addRect(Minerals, blackPen, blackBrush)
    xp = self.xMinerals
    yp = self.yMinerals + self.yWidth
    for n in range(0, 10):
      xp += deltaX
      self.addLine(xp, self.yMinerals, xp, yp, whitePen)
    MinVal = []
    MaxVal = []
    MinVal.append(0.5 + math.log2(people.MinGravity) / 6.0)
    MinVal.append(0.5 + people.MinTemperatur / 400.0)
    MinVal.append(people.MinRadioactivity / 100.0)
    MaxVal.append(0.5 + math.log2(people.MaxGravity) / 6.0)
    MaxVal.append(0.5 + people.MaxTemperatur / 400.0)
    MaxVal.append(people.MaxRadioactivity / 100.0)
    deltaY = self.yWidth / 12
    yp = self.yInfo + deltaY
    for n in (0, 1, 2):
      xp = self.xInfo + self.xWidth * MinVal[n]
      xlen = self.xWidth * (MaxVal[n] - MinVal[n])
      box = QRectF(xp, yp, xlen, 2 * deltaY)
      self.addRect(box, self.pen[n], self.brush[n])
      yp += 4 * deltaY
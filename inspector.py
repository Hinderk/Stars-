
from PyQt6.QtCore import QRectF, QPointF, QLineF
from PyQt6.QtGui import QPen, QBrush, QColor, QPolygonF, QFont
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene

import math



class Inspector(QGraphicsView):

  xInfo = 110
  yInfo = 60
  xMinerals = 110
  yMinerals = 180
  xWidth = 610
  yWidth = 100
  xOffset = 40
  TextOffset = 1
  LeftOffset = 15
  BottomOffset = 5
  RightOffset = 10
  TopOffset = 5


  def __init__(self, faction):
    super(self.__class__, self).__init__()

    self.mConc = []
    self.sConc = []
    self.sText = []
    self.Biome = []
    self.Rates = []

    self.Scene = QGraphicsScene(self)

    self.AddStaticText()
    self.SetupColors()
    self.PaintBackdrop(faction)
    self.InitBiome()
    self.InitMinerals()
    self.setScene(self.Scene)
    self.setMaximumHeight(325)


  def AddStaticText(self):
    font = QFont('Segoe', pointSize=16, weight=400)
    self.ReportAge = self.Scene.addSimpleText("Report is current.", font)
    self.ReportAge.moveBy(self.xInfo, (self.yInfo-self.TopOffset) / 2 )
    self.PlanetValue = self.Scene.addSimpleText("Value: 100%", font)
    self.PlanetValue.moveBy(self.xInfo, 0)
    self.Population = self.Scene.addSimpleText("Uninhabited", font)
    width = self.xWidth - self.Population.boundingRect().width()
    self.Population.moveBy(self.xInfo + width, 0)
    xp = self.xInfo + self.xWidth + self.RightOffset
    deltaY = self.yWidth / 3
    Gravity = self.Scene.addSimpleText("Gravity", font)
    width = Gravity.boundingRect().width() + self.LeftOffset
    height = self.yWidth - 3 * Gravity.boundingRect().height()
    yp = self.yInfo + height / 6.0
    Gravity.moveBy(self.xInfo - width, yp)
    self.Gravity = self.Scene.addSimpleText("8.00g", font)
    self.Gravity.moveBy(xp, yp)
    yp += deltaY
    Temperature = self.Scene.addSimpleText(" Temperature", font)
    width = Temperature.boundingRect().width() + self.LeftOffset
    Temperature.moveBy(self.xInfo - width, yp)
    self.Temperature = self.Scene.addSimpleText("-250\u00B0CC", font)
    self.Temperature.moveBy(xp, yp)
    yp += deltaY
    Radiation = self.Scene.addSimpleText("Radiation", font)
    width = Radiation.boundingRect().width() + self.LeftOffset
    Radiation.moveBy(self.xInfo - width, yp)
    self.Radiation = self.Scene.addSimpleText("100mR", font)
    self.Radiation.moveBy(xp, yp)
    deltaY = self.yWidth / 17
    yp = self.yMinerals + deltaY
    Ironium = self.Scene.addSimpleText("Ironium", font)
    width = Ironium.boundingRect().width() + self.LeftOffset
    Ironium.moveBy(self.xMinerals - width, yp)
    yp += 5 * deltaY
    Boranium = self.Scene.addSimpleText("Boranium", font)
    width = Boranium.boundingRect().width() + self.LeftOffset
    Boranium.moveBy(self.xMinerals - width, yp)
    yp += 5 * deltaY
    Germanium = self.Scene.addSimpleText("Germanium", font)
    width = Germanium.boundingRect().width() + self.LeftOffset
    Germanium.moveBy(self.xMinerals - width, yp)
    kt = 0
    xp = self.xMinerals
    yp = self.yMinerals + self.yWidth + self.BottomOffset
    for i in range(11):
      label = self.Scene.addSimpleText(str(i * 500), font)
      kt += 500
      dx = label.boundingRect().width() / 2
      label.moveBy(xp - dx, yp)
      xp += self.xWidth / 10
    label = self.Scene.addSimpleText("kt", font)
    xp = label.boundingRect().width() + 3 * self.LeftOffset
    label.moveBy(self.xMinerals - xp, yp)


  def InitBiome(self):
    caret = QPolygonF()
    dy = self.yWidth / 12.0
    caret << QPointF(0, 0) << QPointF(dy, dy)
    caret << QPointF(0, dy + dy) << QPointF(-dy, dy)
    line = QLineF(0, dy, 40, dy)
    yp = self.yInfo + dy
    for n in (0, 1, 2):
      xp = self.xInfo + self.xWidth * 0.5
      mark = caret.translated(xp, yp)
      rate = line.translated(xp, yp)
      self.Rates.append(self.Scene.addLine(rate, self.pen[n + 12]))
      self.Biome.append(self.Scene.addPolygon(mark, self.pen[n + 6], self.brush[n + 6]))
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
      self.sConc.append(self.Scene.addRect(box, self.pen[n + 3], self.brush[n + 3]))
      self.mConc.append(self.Scene.addPolygon(mark, self.pen[n + 9], self.brush[n + 9]))
      label = self.Scene.addSimpleText(str(1000))
      label.setPos(self.xMinerals + self.xOffset, yp + self.TextOffset)
      label.setPen(textPen)
      label.setVisible(show)
      self.sText.append(label)
      yp += 5 * deltaY


  def UpdateMinerals(self, planet):
    sConc = []
    mConc = []
    mConc.append(planet.Explored.Crust.Ironium / 100.0)
    mConc.append(planet.Explored.Crust.Boranium / 100.0)
    mConc.append(planet.Explored.Crust.Germanium / 100.0)
    sConc.append(planet.Explored.Surface.Ironium)
    sConc.append(planet.Explored.Surface.Boranium)
    sConc.append(planet.Explored.Surface.Germanium)
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
    g = planet.Gravity + planet.GravityRate
    t = planet.Temperature + planet.TemperatureRate
    r = planet.Radioactivity + planet.RadioactivityRate
    Data.append(0.5 + math.log2(g) / 6.0 - Data[0])
    Data.append(0.5 + t / 400.0 - Data[1])
    Data.append(r / 100.0 - Data[2])
    for n in (0, 1, 2):
      caret = self.Biome[n].polygon()
      dx = self.xWidth * Data[n] - caret.first().x()
      caret.translate(self.xInfo + dx, 0)
      line = self.Rates[n].line()
      line.translate(self.xInfo + dx, 0)
      line.setLength(self.xWidth * Data[3 + n])
      self.Biome[n].setPolygon(caret)
      self.Rates[n].setLine(line)
    g = int(planet.Gravity * 100 + 0.5) / 100
    t = int(planet.Temperature + 300.5) - 300
    r = int(planet.Radioactivity + 0.5)
    self.Gravity.setText(str(g) + "g")
    self.Temperature.setText(str(t) + "\u00B0C")
    self.Radiation.setText(str(r) + "mR")


  def UpdateText(self, year, planet):
    age = year - planet.LastVisit
    self.ReportAge.setText('Report is ' + str(age) + ' years old.')
    val = round(100 * planet.Value())
    self.PlanetValue.setText('Value: ' + str(val))
    pos = self.Population.pos()
    if planet.Colonists > 0:
      self.Population.setText('Population: ' + str(planet.Colonists))
    else:
      self.Population.setText('Uninhabited')
    width = self.xWidth - self.Population.boundingRect().width()
    pos.setX(self.xInfo + width)
    self.Population.setPos(pos)


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
    WidePen = QPen(QColor(80, 80, 255))
    WidePen.setWidthF(2.5)
    self.pen.append(WidePen)
    WidePen = QPen(QColor(255, 80, 80))
    WidePen.setWidthF(2.5)
    self.pen.append(WidePen)
    WidePen = QPen(QColor(80, 200, 80))
    WidePen.setWidthF(2.5)
    self.pen.append(WidePen)


  def PaintBackdrop(self, faction):
    black = QColor(0, 0, 0)
    white = QColor(255, 255, 255, 150)
    whitePen = QPen(white)
    blackPen = QPen(black)
    blackBrush = QBrush(black)
    whitePen.setWidth(2)
    deltaX = self.xWidth / 10
    deltaY = self.yWidth / 3
    Info = QRectF(self.xInfo, self.yInfo, self.xWidth, self.yWidth)
    self.Scene.addRect(Info, blackPen, blackBrush)
    xp = self.xInfo + self.xWidth
    yp = self.yInfo + deltaY
    self.Scene.addLine(self.xInfo, yp, xp, yp, whitePen)
    yp += deltaY
    self.Scene.addLine(self.xInfo, yp, xp, yp, whitePen)
    Minerals = QRectF(self.xMinerals, self.yMinerals, self.xWidth, self.yWidth)
    self.Scene.addRect(Minerals, blackPen, blackBrush)
    xp = self.xMinerals
    yp = self.yMinerals + self.yWidth
    for n in range(0, 10):
      xp += deltaX
      self.Scene.addLine(xp, self.yMinerals, xp, yp, whitePen)
    MinVal = []
    MaxVal = []
    MinVal.append(0.5 + math.log2(faction.MinGravity) / 6.0)
    MinVal.append(0.5 + faction.MinTemperatur / 400.0)
    MinVal.append(faction.MinRadioactivity / 100.0)
    MaxVal.append(0.5 + math.log2(faction.MaxGravity) / 6.0)
    MaxVal.append(0.5 + faction.MaxTemperatur / 400.0)
    MaxVal.append(faction.MaxRadioactivity / 100.0)
    deltaY = self.yWidth / 12
    yp = self.yInfo + deltaY
    for n in (0, 1, 2):
      xp = self.xInfo + self.xWidth * MinVal[n]
      xlen = self.xWidth * (MaxVal[n] - MinVal[n])
      box = QRectF(xp, yp, xlen, 2 * deltaY)
      self.Scene.addRect(box, self.pen[n], self.brush[n])
      yp += 4 * deltaY
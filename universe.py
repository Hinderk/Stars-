
import math

from PyQt6.QtGui import QPolygonF, QFont
from PyQt6.QtCore import QPointF, QLineF, QRectF
from PyQt6.QtWidgets import QGraphicsScene

from PyQt6.QtCore import pyqtSignal as Signal

from planet import Planet
from colours import Pen
from colours import Brush



class Universe(QGraphicsScene):

  fontsize = 14
  font = QFont('Courier', pointSize=fontsize, weight=50)

  xScale = 1.0
  yScale = 1.0

  dy_label = 10
  dy_pointer = 10
  d_radius = 8
  p_radius = 8
  flag_height = 25
  flag_width = 10
  flag_stem = 2
  scale_length = 30
  pointer_size = 20

  ChangeFocus = Signal(Planet)


  def __init__(self, rules):
    super(self.__class__, self).__init__()

    self.planets = []
    self.fleets = []
    self.minefields = []
    self.debris = []

    self.CreatePlanets(rules)
    self.ColonizePlanets(rules)
    self.CreateIndicator()

    self.setBackgroundBrush(Brush.black)


  def ColonizePlanets(self, rules):
    for p in self.planets:
      print(p)


  def mousePressEvent(self, mouseClick):
    pos = mouseClick.scenePos()
    xo = pos.x()
    yo = pos.y()
    po = None
    dist = 1e20
    for p in self.planets:
      d = (p.x - xo) * (p.x - xo) + (p.y - yo) * (p.y - yo)
      if d < dist:
        po = p
        dist = d
    self.HighlightPlanet(po)


  def CreateIndicator(self):
    w = - self.pointer_size * math.sqrt(3.0) / 2
    triangle = QPolygonF()
    triangle << QPointF(0, 0) << QPointF(self.pointer_size / 2, w)
    triangle << QPointF(- self.pointer_size / 2, w)
    self.pointer = self.addPolygon(triangle, Pen.white_08, Brush.yellow)


  def HighlightPlanet(self, p):
    yp = p.y - self.p_radius - self.dy_pointer
    self.pointer.setPos(p.x + self.p_radius, yp)
    self.ChangeFocus.emit(p)


  def CreatePlanets(self, rules):
    for _ in range(rules.PlanetCount()):
      p = self.CreatePlanet(rules, False)
      self.planets.append(p)
    p = self.CreatePlanet(rules, True)       # Home world ...
    self.planets.append(p)


  def CreateOrbitLabel(self, x, y):
    label = self.addSimpleText("", self.font)
    label.setPen(Pen.white)
    label.setBrush(Brush.white)
    label.setPos(x, y)
    label.setVisible(False)
    return label


  def CreateDiagram(self, x, y, w):
    line = QLineF(0, -self.scale_length, 0, 0)
    line.translate(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    diagram_v = self.addLine(line, Pen.white_08)
    d = self.scale_length / 13
    box = QRectF(d, 0, 3 * d, -self.scale_length)
    blue = self.addRect(box, Pen.black, Brush.blue)
    blue.setPos(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    box = QRectF(5 * d, 0, 3 * d, -self.scale_length)
    green = self.addRect(box, Pen.black, Brush.green)
    green.setPos(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    box = QRectF(9 * d, 0, 3 * d, -self.scale_length)
    yellow = self.addRect(box, Pen.black, Brush.yellow)
    yellow.setPos(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    line = QLineF(self.scale_length, 0, 0, 0)
    line.translate(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    diagram_h = self.addLine(line, Pen.white_08)
    return [blue, green, yellow, diagram_h, diagram_v]


  def CreatePlanet(self, rules, homeworld):
    p = Planet(rules, homeworld)
    [x, y] = rules.FindPosition()
    p.x = x * self.xScale
    p.y = y * self.yScale
    x = p.x + self.p_radius / 2
    y = p.y + self.p_radius / 2
    self.addEllipse(x, y, self.p_radius, self.p_radius, Pen.white, Brush.white)
    w = 2 * self.p_radius
    p.core = self.addEllipse(p.x, p.y, w, w, Pen.brown, Brush.brown)
    p.core.setVisible(False)
    x = p.x - self.d_radius
    y = p.y - self.d_radius
    w += 2 * self.d_radius
    c = 0.3 * w
    dc = w - 7 * c / 8
    p.body = self.addEllipse(x, y, w, w, Pen.brown, Brush.brown)
    p.orbit = self.addEllipse(x, y, w, w, Pen.white_2)
    p.orbit.setVisible(False)
    p.starbase = self.addEllipse(x + dc, y - c / 8, c, c, Pen.yellow, Brush.yellow)
    p.neutral = self.addEllipse(x + dc, y + dc, c, c, Pen.neutral, Brush.neutral)
    p.friends = self.addEllipse(x - c / 8, y + dc, c, c, Pen.blue, Brush.blue)
    p.foes = self.addEllipse(x - c / 8, y - c / 8, c, c, Pen.red, Brush.red)
    p.starbase.setVisible(False)
    p.neutral.setVisible(False)
    p.foes.setVisible(False)
    p.friends.setVisible(False)
    p.label = self.addSimpleText(p.Name, self.font)
    p.label.setPen(Pen.white)
    p.label.setBrush(Brush.white)
    w0 = p.label.boundingRect().width()
    p.label.setPos(x - w0 / 2 + w / 2, y + w + self.dy_label)
    p.ships = self.CreateOrbitLabel(x - c / 2, y + w - self.fontsize)
    p.attackers = self.CreateOrbitLabel(x - c / 2, y - self.fontsize / 2)
    p.others = self.CreateOrbitLabel(x + w + c / 2, y + w - self.fontsize)
    flag = QPolygonF()
    flag << QPointF(0, 0) << QPointF(0, - self.flag_height - self.flag_width)
    flag << QPointF(self.flag_width + self.flag_stem, -self.flag_height - self.flag_width)
    flag << QPointF(self.flag_width + self.flag_stem, -self.flag_height)
    flag << QPointF(self.flag_stem, -self.flag_height)
    flag << QPointF(self.flag_stem, 0)
    p.flag = self.addPolygon(flag, Pen.blue, Brush.blue)
    p.flag.setPos(x + w / 2 - self.flag_stem / 2, y + w / 2)
    p.flag.setVisible(False)
    p.diagram = self.CreateDiagram(x, y, w)
    p.HideDiagram()
    return p


  def ShowCrustDiagram(self, planet):
    minerals = planet.Explored.Ironium + planet.Explored.Boranium + planet.Explored.Germanium
    if planet.Discovered and minerals > 0:
      for element in planet.diagram:
        element.setVisible(True)
      box = planet.diagram[0].rect()
      box.setBottom(-self.scale_length * planet.Explored.Ironium / 100.0)
      planet.diagram[0].setRect(box)
      box = planet.diagram[1].rect()
      box.setBottom(-self.scale_length * planet.Explored.Boranium / 100.0)
      planet.diagram[1].setRect(box)
      box = planet.diagram[2].rect()
      box.setBottom(-self.scale_length * planet.Explored.Germanium / 100.0)
      planet.diagram[2].setRect(box)


  def ShowSurfaceDiagram(self, planet):
    minerals = planet.Mined.Ironium + planet.Mined.Boranium + planet.Mined.Germanium
    if planet.Discovered and minerals > 0:
      for element in planet.diagram:
        element.setVisible(True)
      val = [1.2, 1.2, 1.2]
      if planet.Mined.Ironium < 120:
        val[0] = planet.Mined.Ironium / 100.0
      if planet.Mined.Boranium < 120:
        val[1] = planet.Mined.Boranium / 100.0
      if planet.Mined.Germanium < 120:
        val[2] = planet.Mined.Germanium / 100.0
      for n in (0, 1, 2):
        box = planet.diagram[n].rect()
        box.setBottom(-self.scale_length * val[n])
        planet.diagram[n].setRect(box)


  def CheckShipTracking(self, p):
    if p.Friendly:
      p.ShipTracking = p.SpaceStation or p.Colonists > 0
    if p.TotalFriends > 0:
      p.ShipTracking = True


  def ComputeTurn(self):
    for p in self.planets:
      self.CheckShipTracking(p)

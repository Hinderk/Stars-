
from PyQt6.QtGui import QPolygonF, QFont
from PyQt6.QtCore import QPointF, QLineF, QRectF
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene

from PyQt6 import QtWidgets

from planet import Planet
from colours import Pen
from colours import Brush



class Universe(QGraphicsView):

  fontsize = 12
  font = QFont('Courier', pointSize=fontsize, weight=50)

  xScale = 1.0
  yScale = 1.0

  dy_label = 10
  d_radius = 6
  p_radius = 8
  flag_height = 25
  flag_width = 10
  flag_stem = 2
  scale_length = 30


  def __init__(self, rules):
    super(self.__class__, self).__init__()

    self.planets = []
    self.fleets = []
    self.minefields = []
    self.debris = []

    self.Scene = QGraphicsScene()
    self.CreatePlanets(rules)
    self.ColonizePlanets(rules)

    self.Scene.setBackgroundBrush(Brush.black)
    self.setScene(self.Scene)
    policy = QtWidgets.QSizePolicy()
    policy.setHorizontalPolicy(policy.Policy.MinimumExpanding)
    policy.setVerticalPolicy(policy.Policy.MinimumExpanding)
    self.setSizePolicy(policy)


  def ColonizePlanets(self, rules):
    for p in self.planets:
      print(p)


  def CreatePlanets(self, rules):
    for _ in range(rules.PlanetCount()):
      self.CreatePlanet(rules, False)
    self.CreatePlanet(rules, True)


  def CreateOrbitLabel(self, x, y):
    label = self.Scene.addSimpleText("", self.font)
    label.setPen(Pen.white)
    label.setBrush(Brush.white)
    label.setPos(x, y)
    label.setVisible(False)
    return label


  def CreateDiagram(self, x, y, w):
    line = QLineF(0, -self.scale_length, 0, 0)
    line.translate(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    diagram_v = self.Scene.addLine(line, Pen.white_08)
    d = self.scale_length / 13
    box = QRectF(d, 0, 3 * d, -self.scale_length)
    blue = self.Scene.addRect(box, Pen.black, Brush.blue)
    blue.setPos(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    box = QRectF(5 * d, 0, 3 * d, -self.scale_length)
    green = self.Scene.addRect(box, Pen.black, Brush.green)
    green.setPos(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    box = QRectF(9 * d, 0, 3 * d, -self.scale_length)
    yellow = self.Scene.addRect(box, Pen.black, Brush.yellow)
    yellow.setPos(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    line = QLineF(self.scale_length, 0, 0, 0)
    line.translate(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    diagram_h = self.Scene.addLine(line, Pen.white_08)
    return [blue, green, yellow, diagram_h, diagram_v]


  def CreatePlanet(self, rules, homeworld):
    p = Planet(rules, homeworld)
    [x, y] = rules.FindPosition()
    p.x = x * self.xScale
    p.y = y * self.yScale
    w = 2 * self.p_radius
    p.planet = self.Scene.addEllipse(p.x, p.y, w, w, Pen.brown, Brush.brown)
    w += 2 * self.d_radius
    x -= self.d_radius
    y -= self.d_radius
    c = 0.3 * w
    dc = w - 7 * c / 8
    p.orbit = self.Scene.addEllipse(x, y, w, w, Pen.white_2)
    p.orbit.setVisible(False)
    p.starbase = self.Scene.addEllipse(x + dc, y - c / 8, c, c, Pen.yellow, Brush.yellow)
    p.neutral = self.Scene.addEllipse(x + dc, y + dc, c, c, Pen.neutral, Brush.neutral)
    p.friends = self.Scene.addEllipse(x - c / 8, y + dc, c, c, Pen.blue, Brush.blue)
    p.foes = self.Scene.addEllipse(x - c / 8, y - c / 8, c, c, Pen.red, Brush.red)
    p.starbase.setVisible(False)
    p.neutral.setVisible(False)
    p.foes.setVisible(False)
    p.friends.setVisible(False)
    p.label = self.Scene.addSimpleText(p.Name, self.font)
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
    p.flag = self.Scene.addPolygon(flag, Pen.blue, Brush.blue)
    p.flag.setPos(x + w / 2 - self.flag_stem / 2, y + w / 2)
    p.flag.setVisible(False)
    p.diagram = self.CreateDiagram(x, y, w)
    p.HideDiagram()
    self.planets.append(p)

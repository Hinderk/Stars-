
import math

from PyQt6.QtGui import QPolygonF, QFont
from PyQt6.QtCore import QPointF, QLineF, QRectF
from PyQt6.QtWidgets import QGraphicsScene

from PyQt6.QtCore import pyqtSignal as QSignal

from scanner import Scanner
from planet import Planet
from colours import Pen
from colours import Brush
from defines import Stance, GuiProps



class Universe(QGraphicsScene, GuiProps):

  ChangeFocus = QSignal(Planet)


  def __init__(self, rules):
    super(self.__class__, self).__init__()

    self.planets = []
    self.fleets = []
    self.minefields = []
    self.debris = []

    self.FieldsVisible = False
    self.ShowField = dict()
    self.ShowField[Stance.allied] = True
    self.ShowField[Stance.friendly] = True
    self.ShowField[Stance.neutral] = True
    self.ShowField[Stance.hostile] = True

    self.PopulationCeiling = rules.GetPopulationCeiling()

    self.CreateIndicator()
    self.NamesVisible = False
    self.CreatePlanets(rules)
    self.ColonizePlanets(rules)

    self.setBackgroundBrush(Brush.black)


  def ColonizePlanets(self, rules):
#    for p in self.planets:
    pass


  def mousePressEvent(self, mouseClick):
    pos = mouseClick.scenePos()
    xo = pos.x() / self.Xscale
    yo = pos.y() / self.Xscale
    po = None
    dist = 1e20
    for p in self.planets:
      d = (p.x - xo) * (p.x - xo) + (p.y - yo) * (p.y - yo)
      if d < dist:
        po = p
        dist = d
    self.HighlightPlanet(po)


  def CreateIndicator(self):
    w = self.pointer_size * math.sqrt(3.0) / 2
    triangle = QPolygonF()
    triangle << QPointF(0, 0) << QPointF(self.pointer_size / 2, w)
    triangle << QPointF(- self.pointer_size / 2, w)
    self.pointer = self.addPolygon(triangle, Pen.white_08, Brush.yellow)


  def HighlightPlanet(self, p):
    self.LastPlanet.label.setPen(Pen.white_l)
    self.LastPlanet.label.setBrush(Brush.white_l)
    if self.NamesVisible:
      p.label.setPen(Pen.white)
      p.label.setBrush(Brush.white)
    else:
      xp = self.Xscale * p.x
      yp = self.Xscale * p.y + self.p_radius + self.dy_pointer
      self.pointer.setPos(xp, yp)
    self.LastPlanet = p
    self.ChangeFocus.emit(p)


  def ShowMines(self, switch, fof):
    old = self.ShowField[fof]
    self.ShowField[fof] = switch
    if self.FieldsVisible and old != switch:
      self.ShowFields(True)


  def ShowFields(self, show):
    if show:
      for field in self.minefields:
        switch = self.ShowField[field.fof]
        field.area.setVisible(switch)
        field.center.setVisible(switch)
    else:
      for field in self.minefields:
        field.area.setVisible(False)
        field.center.setVisible(False)
    self.FieldsVisible = show


  def ShowScannerRanges(self, switch):
    for p in self.planets:
      if p.scanner:
        p.scanner.ShowRanges(switch)
    for f in self.fleets:
      if f.scanner:
        f.scanner.ShowRanges(switch)


  def ShowPlanetNames(self, switch):
    self.NamesVisible = switch
    self.HighlightPlanet(self.LastPlanet)
    self.pointer.setVisible(not switch)
    for p in self.planets:
      p.label.setVisible(switch)


  def ShowCrustDiagrams(self):
    for p in self.planets:
      p.ShowDefaultView()
      p.diagram.ShowCrustDiagram(p)
    self.update()


  def ShowSurfaceDiagrams(self):
    for p in self.planets:
      p.ShowDefaultView()
      p.diagram.ShowSurfaceDiagram(p)
    self.update()


  def RemoveDiagrams(self):
    for p in self.planets:
      p.diagram.Show(False)
    self.update()


  def ShowDefaultView(self):
    for p in self.planets:
      p.ShowDefaultView()
    self.update()


  def ShowMinimalView(self):
    for p in self.planets:
      p.ShowMinimalView()
    self.update()


  def ShowPopulationView(self):
    for p in self.planets:
      p.ShowPopulationView()
      if p.bodyVisible:
        q = math.sqrt(p.Colonists / self.PopulationCeiling)
        if q > 1.0:
          q = 1.0
        rnew = self.p_radius * (1 + q) / 2 + q * self.d_radius
        x = self.Xscale * p.x - rnew
        y = self.Xscale * p.y - rnew
        w = 2 * rnew
        p.body.setRect(QRectF(x, y, w, w))
        p.body.setPen(Pen.brown)
        p.body.setBrush(Brush.brown)
        p.population.setText(str(p.Colonists))
    self.update()


  def ScaleRadarRanges(self, factor):
    f = factor / 100.0
    for p in self.planets:
      if p.scanner:
        p.scanner.ScaleRanges(f)
    for fleet in self.fleets:
      if fleet.scanner:
        fleet.scanner.ScaleRanges(f)
    self.update()


  def ShowPercentageView(self):
    for p in self.planets:
      p.ShowPercentageView()
      if p.coreVisible:
        q = p.Value()
        if q < 0.33:
          p.body.setPen(Pen.red)
          p.body.setBrush(Brush.red)
          q = 3 * q
        elif q < 0.66:
          p.body.setPen(Pen.yellow)
          p.body.setBrush(Brush.yellow)
          q = 3 * (q - 0.33)
        else:
          p.body.setPen(Pen.green)
          p.body.setBrush(Brush.green)
          q = 3 * (q - 0.66)
        rnew = self.p_radius * (1 + q) / 2 + q * self.d_radius
        x = self.Xscale * p.x - rnew
        y = self.Xscale * p.y - rnew
        w = 2 * rnew
        p.body.setRect(QRectF(x, y, w, w))
      if p.flagVisible:
        if p.Relation == Stance.allied:
          p.flag.setPen(Pen.blue_l)
          p.flag.setBrush(Brush.blue)
        elif p.Relation == Stance.friendly:
          p.flag.setPen(Pen.green_d)
          p.flag.setBrush(Brush.green)
        elif p.Relation == Stance.neutral:
          p.flag.setPen(Pen.yellow_d)
          p.flag.setBrush(Brush.yellow)
        else:
          p.flag.setPen(Pen.red_l)
          p.flag.setBrush(Brush.red)
    self.update()


  def CreatePlanets(self, rules):
    x = []
    y = []
    n = rules.PlanetCount()
    while n > 0:
      n -= 1
      p = self.CreatePlanet(rules, n < 1)
      x.append(p.x)
      y.append(p.y)
      self.planets.append(p)
    xmin = self.Xscale * min(x) - self.map_frame
    xmax = self.Xscale * max(x) + self.map_frame
    ymin = self.Xscale * min(y) - self.map_frame
    ymax = self.Xscale * max(y) + self.map_frame
    self.setSceneRect(xmin, ymin, xmax - xmin, ymax - ymin)
    model = rules.FirstScanner()
    if model:
      p.scanner = self.CreateScanner(p.x, p.y, model.value)
    self.LastPlanet = p
    self.HighlightPlanet(p)


  def CreateScanner(self, xo, yo, ranges):
    s = Scanner(xo, yo, ranges)
    r = ranges[0] * self.Xscale
    x = self.Xscale * xo
    y = self.Xscale * yo
    if r > 0:
      box = QRectF(x - r, y - r, r + r, r + r)
      s.detection = self.addEllipse(box, Pen.red_s, Brush.red_s)
      s.detection.setZValue(-10)
      s.detection.setVisible(False)
    r = ranges[1] * self.Xscale
    if r > 0:
      box = QRectF(x - r, y - r, r + r, r + r)
      s.penetration = self.addEllipse(box, Pen.yellow_s, Brush.yellow_s)
      s.penetration.setZValue(-8)
      s.penetration.setVisible(False)
    return s


  def RegisterFleet(self, fleet, p, y=None):
    r = fleet.MaxRange
    if y:
      if fleet.FriendOrFoe == Stance.allied and r > 0:
        fleet.scanner = self.CreateScanner(p, y, [r, fleet.PenRange])
    else:
      if fleet.FriendOrFoe == Stance.allied and r > 0:
        fleet.scanner = self.CreateScanner(p.x, p.y, [r, fleet.PenRange])
      p.fleets_in_orbit.append(fleet)
      p.EnterOrbit(fleet)
    self.fleets.append(fleet)


  def CreateOrbitLabel(self, x, y):
    label = self.addSimpleText("", self.mapFont)
    label.setPen(Pen.white_l)
    label.setBrush(Brush.white_l)
    label.setPos(x, y)
    label.setVisible(False)
    return label


  def CreateDiagram(self, diagram, x, y, w):
    line = QLineF(0, -self.scale_length, 0, 0)
    line.translate(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    diagram.VAxis = self.addLine(line, Pen.white_08)
    d = self.scale_length / 13
    box = QRectF(d, 0, 3 * d, -self.scale_length)
    diagram.BlueBox = self.addRect(box, Pen.blue, Brush.blue)
    diagram.BlueBox.setPos(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    box = QRectF(5 * d, 0, 3 * d, -self.scale_length)
    diagram.GreenBox = self.addRect(box, Pen.green, Brush.green)
    diagram.GreenBox.setPos(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    box = QRectF(9 * d, 0, 3 * d, -self.scale_length)
    diagram.YellowBox = self.addRect(box, Pen.yellow, Brush.yellow)
    diagram.YellowBox.setPos(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    line = QLineF(self.scale_length, 0, 0, 0)
    line.translate(x + w / 2 - self.scale_length / 2, y - self.dy_label)
    diagram.HAxis = self.addLine(line, Pen.white_08)
    diagram.ScaleLength = self.scale_length
    diagram.Show(False)


  def CreatePlanet(self, rules, homeworld):
    p = Planet(rules, homeworld)
    [p.x, p.y] = rules.FindPosition()
    w = self.p_radius
    xo = p.x * self.Xscale - w
    yo = p.y * self.Xscale - w
    x = xo + w / 2
    y = yo + w / 2
    p.center = self.addEllipse(x, y, w, w, Pen.white, Brush.white)
    w += self.p_radius
    p.core = self.addEllipse(xo, yo, w, w, Pen.brown, Brush.brown)
    p.core.setVisible(False)
    x = xo - self.d_radius
    y = yo - self.d_radius
    w += 2 * self.d_radius
    c = 0.3 * w
    dc = w - 7 * c / 8
    p.body = self.addEllipse(x, y, w, w)
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
    p.label = self.addSimpleText(p.Name, self.mapFont)
    p.label.setPen(Pen.white_l)
    p.label.setBrush(Brush.white_l)
    p.label.setVisible(False)
    w0 = p.label.boundingRect().width()
    p.label.setPos(x - w0 / 2 + w / 2, y + w + self.dy_label)
    p.ships = self.CreateOrbitLabel(x - c / 2, y + w - self.fontsize)
    p.attackers = self.CreateOrbitLabel(x - c / 2, y - self.fontsize / 2)
    p.others = self.CreateOrbitLabel(x + w + c / 2, y + w - self.fontsize)
    p.population = self.CreateOrbitLabel(x + w + c / 2, y - self.fontsize / 2)
    flag = QPolygonF()
    flag << QPointF(0, 0) << QPointF(0, - self.flag_height - self.flag_width)
    flag << QPointF(self.flag_width + self.flag_stem, -self.flag_height - self.flag_width)
    flag << QPointF(self.flag_width + self.flag_stem, -self.flag_height)
    flag << QPointF(self.flag_stem, -self.flag_height)
    flag << QPointF(self.flag_stem, 0)
    p.flag = self.addPolygon(flag)
    p.flag.setPos(x + w / 2 - self.flag_stem / 2, y + w / 2)
    p.flag.setVisible(False)
    self.CreateDiagram(p.diagram, x, y, w)
    return p


  def ComputeTurn(self):
    for p in self.planets:
      p.UpdateShipTracking()


import math

from PyQt6.QtGui import QPolygonF
from PyQt6.QtCore import QPointF, QLineF, QRectF, Qt
from PyQt6.QtWidgets import QMenu
from PyQt6.QtWidgets import QGraphicsScene

from PyQt6.QtCore import pyqtSignal as QSignal

from guidesign import GuiDesign
from fleet import Fleet
from scanner import Scanner
from ruleset import Ruleset
from planet import Planet
from colours import Pen
from colours import Brush
from defines import Stance
from guiprop import GuiProps as GP



class ItemSelector(QMenu):

  def __init__(self, pos):
    super(self.__class__, self).__init__()
    self.xo = pos.x()
    self.yo = pos.y()


  def mousePressEvent(self, mouseClick):
    pos = mouseClick.localPos()
    print(pos)




class Universe(QGraphicsScene):

  ChangeFocus = QSignal(Planet)
  SelectField = QSignal(bool, int, list)

  flag = QPolygonF()
  flag << QPointF(0, 0)
  flag << QPointF(0, - GP.flag_height - GP.flag_width)
  flag << QPointF(GP.flag_width + GP.flag_stem, -GP.flag_height - GP.flag_width)
  flag << QPointF(GP.flag_width + GP.flag_stem, -GP.flag_height)
  flag << QPointF(GP.flag_stem, -GP.flag_height)
  flag << QPointF(GP.flag_stem, 0)

  def __init__(self, rules):
    super(self.__class__, self).__init__()

    self.planets = []
    self.fleets = []
    self.minefields = []
    self.debris = []

    self.SelectedPlanet = None
    self.DefaultView = False
    self.ShowFleetStrength = False
    self.ActiveFoeFilter = None

    self.PopulationCeiling = Ruleset.GetPopulationCeiling()

    self.CreateIndicator()
    self.SetupMinefields()
    self.NamesVisible = False
    self.CreatePlanets(rules)
    self.ColonizePlanets()

    self.setBackgroundBrush(Brush.black)


  def ColonizePlanets(self):
#    for p in self.planets:
    pass


  def contextMenuEvent(self, mouseClick):
    print(self.Context)
    Select = QMenu()
    Select.setStyleSheet(GuiDesign.getMapStyle())
    n = 0
    if self.Context[1]:
      for f in self.Context[1]:
        a = Select.addAction(f.name)
        a.setData((1, n))
        n += 1
    elif self.Context[0]:
      a = Select.addAction(self.Context[0].Name)
      a.setData((0, 0))
      if self.Context[0].mine_fields:
        Select.addSeparator()
        for f in self.Context[0].mine_fields:
          a = Select.addAction(f.name)
          a.setData((1, n))
          n += 1
      if self.Context[2]:
        Select.addSeparator()
    selected = Select.exec(mouseClick.screenPos())
    if selected:
      itemtype, item = selected.data()
      if itemtype == 1 and self.Context[1]:
        self.HighlightMinefield(self.Context[1], item, False)
      elif itemtype == 1:
        po = self.Context[0]
        self.HighlightPlanet(po)
        self.SelectField.emit(True, item, po.mine_fields)
      else:
        self.HighlightPlanet(self.Context[0])


  def mousePressEvent(self, mouseClick):
    pos = mouseClick.scenePos()
    xo = round(0.5 + pos.x() / GP.Xscale)
    yo = round(0.5 + pos.y() / GP.Xscale)
    m_list = None
    dist = 1e20
    for p in self.planets:
      d = (p.x - xo) * (p.x - xo) + (p.y - yo) * (p.y - yo)
      if d < dist:
        po = p
        dist = d
    po.mine_fields = []
    for m in self.minefields:
      if m.Detected:
        if self.FieldsVisible:
          d = (m.x - xo) * (m.x - xo) + (m.y - yo) * (m.y - yo)
          if d < dist:
            m_list = [m]
            dist = d
          elif m_list and d == dist:
            m_list.append(m)
        d = (m.x - po.x) * (m.x - po.x) + (m.y - po.y) * (m.y - po.y)
        if d < m.mines:
          po.mine_fields.append(m)
    self.Context = (po, m_list, None)
    if mouseClick.buttons() == Qt.MouseButton.LeftButton:
      if m_list:
        self.HighlightMinefield(m_list, 0, False)
      else:
        self.HighlightPlanet(po)


  def CreateIndicator(self):
    w = GP.pointer_size * math.sqrt(3.0) / 2
    triangle = QPolygonF()
    triangle << QPointF(0, 0) << QPointF(GP.pointer_size / 2, w)
    triangle << QPointF(- GP.pointer_size / 2, w)
    self.pointer = self.addPolygon(triangle, Pen.white_08, Brush.yellow)
    self.pointer.setZValue(8)


  def HighlightPlanet(self, p):
    if self.SelectedPlanet:
      self.SelectedPlanet.label.setPen(Pen.white_l)
      self.SelectedPlanet.label.setBrush(Brush.white_l)
    if self.NamesVisible:
      p.label.setPen(Pen.white)
      p.label.setBrush(Brush.white)
      self.pointer.setVisible(False)
    else:
      xp = GP.Xscale * p.x
      yp = GP.Xscale * p.y + GP.p_radius + GP.dy_pointer
      self.pointer.setPos(xp, yp)
    self.SelectedPlanet = p
    self.ChangeFocus.emit(p)


  def HighlightMinefield(self, m_list, index, planet):
    if self.SelectedPlanet:
      self.SelectedPlanet.label.setPen(Pen.white_l)
      self.SelectedPlanet.label.setBrush(Brush.white_l)
    xp = GP.Xscale * m_list[0].x
    yp = GP.Xscale * m_list[0].y + GP.dy_pointer
    self.pointer.setPos(xp, yp)
    self.pointer.setVisible(True)
    self.SelectedPlanet = None
    self.SelectField.emit(planet, index, m_list)


  def SetupMinefields(self):
    self.FieldsVisible = False
    self.ShowField = dict()
    self.ShowField[Stance.allied] = True
    self.ShowField[Stance.friendly] = True
    self.ShowField[Stance.neutral] = True
    self.ShowField[Stance.hostile] = True


  def ShowMines(self, switch, fof):
    old = self.ShowField[fof]
    self.ShowField[fof] = switch
    if self.FieldsVisible and old != switch:
      self.ShowFields(True)


  def ShowFields(self, show):
    if show:
      for field in self.minefields:
        switch = self.ShowField[field.fof] and field.Detected
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
    if self.SelectedPlanet:
      self.HighlightPlanet(self.SelectedPlanet)
      self.pointer.setVisible(not switch)
    for p in self.planets:
      p.label.setVisible(switch)


  def ShowCrustDiagrams(self):
    for p in self.planets:
      p.ShowDefaultView(self.ShowFleetStrength)
      p.diagram.ShowCrustDiagram(p)
    self.update()
    self.DefaultView = True


  def ShowSurfaceDiagrams(self):
    for p in self.planets:
      p.ShowDefaultView(self.ShowFleetStrength)
      p.diagram.ShowSurfaceDiagram(p)
    self.update()
    self.DefaultView = True


  def RemoveDiagrams(self):
    for p in self.planets:
      p.diagram.Show(False)
    self.update()


  def ShowDefaultView(self):
    for p in self.planets:
      p.ShowDefaultView(self.ShowFleetStrength)
    self.update()
    self.DefaultView = True


  def ShowMinimalView(self):
    for p in self.planets:
      p.ShowMinimalView()
    self.update()
    self.DefaultView = False


  def ShowPopulationView(self):
    for p in self.planets:
      p.ShowPopulationView()
      if p.bodyVisible:
        q = math.sqrt(p.Colonists / self.PopulationCeiling)
        if q > 1.0:
          q = 1.0
        rnew = GP.p_radius * (1 + q) / 2 + q * GP.d_radius
        x = GP.Xscale * p.x - rnew
        y = GP.Xscale * p.y - rnew
        w = 2 * rnew
        p.body.setRect(QRectF(x, y, w, w))
        p.body.setPen(Pen.brown)
        p.body.setBrush(Brush.brown)
        p.population.setText(str(p.Colonists))
    self.update()
    self.DefaultView = False


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
        rnew = GP.p_radius * (1 + q) / 2 + q * GP.d_radius
        x = GP.Xscale * p.x - rnew
        y = GP.Xscale * p.y - rnew
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
    self.DefaultView = False


  def CreatePlanets(self, rules):
    x = []
    y = []
    n = Ruleset.PlanetCount()
    while n > 0:
      n -= 1
      p = self.CreatePlanet(rules, n < 1)
      x.append(p.x)
      y.append(p.y)
      self.planets.append(p)
    xmin = GP.Xscale * min(x) - GP.map_frame
    xmax = GP.Xscale * max(x) + GP.map_frame
    ymin = GP.Xscale * min(y) - GP.map_frame
    ymax = GP.Xscale * max(y) + GP.map_frame
    self.setSceneRect(xmin, ymin, xmax - xmin, ymax - ymin)
    model = rules.FirstScanner()
    if model:
      p.scanner = self.CreateScanner(p.x, p.y, model.value)
    self.SelectedPlanet = p
    self.HighlightPlanet(p)


  def CreateScanner(self, xo, yo, ranges):
    s = Scanner(xo, yo, ranges)
    r = ranges[0] * GP.Xscale
    x = GP.Xscale * xo
    y = GP.Xscale * yo
    if r > 0:
      box = QRectF(x - r, y - r, r + r, r + r)
      s.detection = self.addEllipse(box, Pen.red_s, Brush.red_s)
      s.detection.setZValue(-10)
      s.detection.setVisible(False)
    r = ranges[1] * GP.Xscale
    if r > 0:
      box = QRectF(x - r, y - r, r + r, r + r)
      s.penetration = self.addEllipse(box, Pen.yellow_s, Brush.yellow_s)
      s.penetration.setZValue(-8)
      s.penetration.setVisible(False)
    return s


  def RegisterFleet(self, fleet, p, y=None):
    r = fleet.MaxRange
    pen, brush = fleet.getColours()
    fleet.MovingFleet = self.addPolygon(Fleet.arrow, pen, brush)
    fleet.MovingFleet.setVisible(False)
    if y:
      xo = p
      yo = y
    else:
      xo = p.x
      yo = p.y
      p.fleets_in_orbit.append(fleet)
      p.EnterOrbit(fleet)
    if fleet.FriendOrFoe == Stance.allied and r > 0:
      fleet.scanner = self.CreateScanner(xo, yo, [r, fleet.PenRange])
    w = 2 * GP.f_radius
    xs = xo * GP.Xscale - GP.f_radius
    ys = yo * GP.Xscale - GP.f_radius
    fleet.RestingFleet = self.addEllipse(xs, ys, w, w, pen, brush)
    fleet.RestingFleet.setVisible(False)
    fleet.MovingFleet.setPos(xo * GP.Xscale, yo * GP.Xscale)
    fleet.ShipCount = self.CreateOrbitLabel(0, 0)
    fleet.ShipCount.setText(str(fleet.ShipCounter))
    h = fleet.ShipCount.boundingRect().height() - 2
    fleet.ShipCount.setPos(xs + w + GP.f_dist, yo * GP.Xscale - h / 2)
    fleet.ShipCount.setVisible(False)
    self.fleets.append(fleet)


  def CreateOrbitLabel(self, x, y):
    label = self.addSimpleText("", GP.mapFont)
    label.setPen(Pen.white_l)
    label.setBrush(Brush.white_l)
    label.setPos(x, y)
    label.setVisible(False)
    return label


  def CreateDiagram(self, diagram, x, y, w):
    line = QLineF(0, -GP.scale_length, 0, 0)
    line.translate(x + w / 2 - GP.scale_length / 2, y - GP.dy_label)
    diagram.VAxis = self.addLine(line, Pen.white_08)
    d = GP.scale_length / 13
    box = QRectF(d, 0, 3 * d, -GP.scale_length)
    diagram.BlueBox = self.addRect(box, Pen.blue, Brush.blue)
    diagram.BlueBox.setPos(x + w / 2 - GP.scale_length / 2, y - GP.dy_label)
    box = QRectF(5 * d, 0, 3 * d, -GP.scale_length)
    diagram.GreenBox = self.addRect(box, Pen.green, Brush.green)
    diagram.GreenBox.setPos(x + w / 2 - GP.scale_length / 2, y - GP.dy_label)
    box = QRectF(9 * d, 0, 3 * d, -GP.scale_length)
    diagram.YellowBox = self.addRect(box, Pen.yellow, Brush.yellow)
    diagram.YellowBox.setPos(x + w / 2 - GP.scale_length / 2, y - GP.dy_label)
    line = QLineF(GP.scale_length, 0, 0, 0)
    line.translate(x + w / 2 - GP.scale_length / 2, y - GP.dy_label)
    diagram.HAxis = self.addLine(line, Pen.white_08)
    diagram.ScaleLength = GP.scale_length
    diagram.Show(False)


  def CreatePlanet(self, rules, homeworld):
    p = Planet(rules, homeworld)
    [p.x, p.y] = rules.FindPosition()
    w = GP.p_radius
    xo = p.x * GP.Xscale - w
    yo = p.y * GP.Xscale - w
    x = xo + w / 2
    y = yo + w / 2
    p.center = self.addEllipse(x, y, w, w, Pen.white, Brush.white)
    w += GP.p_radius
    p.core = self.addEllipse(xo, yo, w, w, Pen.brown, Brush.brown)
    p.core.setVisible(False)
    x = xo - GP.d_radius
    y = yo - GP.d_radius
    w += 2 * GP.d_radius
    c = 2 * GP.o_radius
    w0 = w / math.sqrt(8.0)
    xm = x + w / 2 - w0 - GP.o_radius
    xp = x + w / 2 + w0 - GP.o_radius
    ym = y + w / 2 - w0 - GP.o_radius
    yp = y + w / 2 + w0 - GP.o_radius
    p.body = self.addEllipse(x, y, w, w)
    p.orbit = self.addEllipse(x, y, w, w, Pen.white_2)
    p.orbit.setVisible(False)
    p.starbase = self.addEllipse(xp, ym, c, c, Pen.yellow, Brush.yellow)
    p.neutral = self.addEllipse(xp, yp, c, c, Pen.neutral, Brush.neutral)
    p.friends = self.addEllipse(xm, yp, c, c, Pen.blue, Brush.blue)
    p.foes = self.addEllipse(xm, ym, c, c, Pen.red, Brush.red)
    p.starbase.setVisible(False)
    p.neutral.setVisible(False)
    p.foes.setVisible(False)
    p.friends.setVisible(False)
    p.label = self.addSimpleText(p.Name, GP.mapFont)
    p.label.setPen(Pen.white_l)
    p.label.setBrush(Brush.white_l)
    p.label.setVisible(False)
    w0 = p.label.boundingRect().width()
    p.label.setPos(x - w0 / 2 + w / 2, y + w + GP.dy_label)
    p.ships = self.CreateOrbitLabel(x - c / 2, y + w - GP.fontsize)
    p.attackers = self.CreateOrbitLabel(x - c / 2, y - GP.fontsize / 2)
    p.others = self.CreateOrbitLabel(x + w + c / 2, y + w - GP.fontsize)
    p.population = self.CreateOrbitLabel(x + w + c / 2, y - GP.fontsize / 2)
    p.flag = self.addPolygon(Universe.flag)
    p.flag.setPos(x + w / 2 - GP.flag_stem / 2, y + w / 2)
    p.flag.setVisible(False)
    self.CreateDiagram(p.diagram, x, y, w)
    return p


  def ShowShipCount(self, event):
    if self.DefaultView:
      for p in self.planets:
        p.ShowDefaultView(event)
    for f in self.fleets:
      if f.Discovered and not f.Orbiting:
        f.ShipCount.setVisible(event and f.ShipCounter > 0)
    self.ShowFleetStrength = event


  def FilterFoes(self, disabled, select):
    if select:
      self.ActiveFoeFilter = select
    if disabled:
      for f in self.fleets:
        if f.FriendOrFoe == Stance.hostile:
          f.ShipCounter = len(f.ShipList)
          f.ShipCount.setText(str(f.ShipCounter))
    else:
      for f in self.fleets:
        if f.FriendOrFoe == Stance.hostile:
          f.ApplyFilter(select)
          f.ShipCount.setText(str(f.ShipCounter))
    for p in self.planets:
      p.TotalFoes = 0
      for f in p.fleets_in_orbit:
        if f.FriendOrFoe == Stance.hostile:
          p.TotalFoes += f.ShipCounter
        p.UpdateFoes()
    self.ShowShipCount(self.ShowFleetStrength)
    self.update()


  def EnableFoeFilter(self, event):
    if event and self.ActiveFoeFilter:
      self.FilterFoes(False, self.ActiveFoeFilter)
    else:
      self.FilterFoes(True, None)


  def ComputeTurn(self):
    for p in self.planets:
      p.UpdateShipTracking()

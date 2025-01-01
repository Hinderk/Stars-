
import math

from PyQt6.QtGui import QPolygonF, QPen
from PyQt6.QtGui import QTransform
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
from defines import Stance, Task
from waypoint import Waypoint
from guiprop import GuiProps as GP




class Universe(QGraphicsScene):

  SelectPlanet = QSignal(Planet)
  UpdatePlanet = QSignal(Planet)
  UpdateFilter = QSignal(dict)
  SelectFleet = QSignal(object, int, list, list)
  SelectField = QSignal(object, int, list)

  flag = QPolygonF()
  flag << QPointF(0, 0)
  flag << QPointF(0, - GP.flag_height - GP.flag_width)
  flag << QPointF(GP.flag_width + GP.flag_stem, -GP.flag_height - GP.flag_width)
  flag << QPointF(GP.flag_width + GP.flag_stem, -GP.flag_height)
  flag << QPointF(GP.flag_stem, -GP.flag_height)
  flag << QPointF(GP.flag_stem, 0)


  def SetupMineFilter():
    fields = dict()
    fields[Stance.allied] = True
    fields[Stance.friendly] = True
    fields[Stance.neutral] = True
    fields[Stance.hostile] = True
    return fields


  def __init__(self, rules):
    super(self.__class__, self).__init__()

    self.planets = []
    self.fleets = []
    self.minefields = []
    self.debris = []

    self.SelectedPlanet = None
    self.SelectedFleet = None
    self.SelectedWaypoint = None
    self.WaypointIndex = 0
    self.WaypointOffset = 0
    self.FleetIndex = 0
    self.FleetOffset = 0
    self.SelectedFleets = []
    self.DefaultView = False
    self.ShowFleetStrength = False
    self.ShowIdleFleetsOnly = False
    self.ShowFleetMovements = False
    self.FoeFilterEnabled = False
    self.FriendFilterEnabled = False
    self.ActiveFoeFilter = None
    self.ActiveFriendFilter = None
    self.FieldsVisible = False
    self.WaypointSelected = False

    self.ShowField = Universe.SetupMineFilter()
    self.PopulationCeiling = Ruleset.GetPopulationCeiling()
    self.CurrentPathWidth = GP.fp_width[100]

    self.pointer = None
    self.select = None
    self.wpselect = None

    self.CreateIndicator()
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
    if self.Context[2]:
      pass
    # deal with fleets
    elif self.Context[1]:
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
        self.HighlightMinefield(self.Context[1], item)
      elif itemtype == 1:
        po = self.Context[0]
        self.HighlightPlanet(po)
        self.SelectField.emit(po, item, po.mine_fields)
      else:
        self.HighlightPlanet(self.Context[0])


  def mouseReleaseEvent(self, mouseClick):
    self.WaypointSelected = False


  def mousePressEvent(self, mouseClick):
    self.WaypointSelected = False
    pos = mouseClick.scenePos()
    xo = round(0.5 + pos.x() / GP.Xscale)
    yo = round(0.5 + pos.y() / GP.Xscale)
    dist = 1e20
    for p in self.planets:
      d = (p.x - xo) * (p.x - xo) + (p.y - yo) * (p.y - yo)
      if d < dist:
        po = p
        dist = d
    f_list = []
    w_list = []
    for f in self.fleets:
      if f.Discovered and f.ShipCounter > 0 and not f.Orbiting:
        d = (f.xc - xo) * (f.xc - xo) + (f.yc - yo) * (f.yc - yo)
        if d < dist:
          dist = d
          f_list = [f]
        elif f_list and d == dist:
          f_list.append(f)
        if self.ShowFleetMovements or f == self.SelectedFleet:
          if f.FriendOrFoe != Stance.allied:
            continue
          wp = f.FirstWaypoint
          n = 1
          while wp:
            d = (wp.xo - xo) * (wp.xo - xo) + (wp.yo - yo) * (wp.yo - yo)
            if d < dist:
              n = 1
              w_list = [(wp, n)]
              f_list = [f]
              f.ActiveWaypoint = [wp]
              dist = d
            elif w_list and d == dist:
              f.ActiveWaypoint.append(wp)
              f_list.append(f)
              w_list.append((wp, n))
              n += 1
            wp = wp.next
    m_list = []
    for m in self.minefields:
      if m.Detected:
        if self.FieldsVisible:
          d = (m.x - xo) * (m.x - xo) + (m.y - yo) * (m.y - yo)
          if d < dist:
            m_list = [m]
            dist = d
          elif m_list and d == dist:
            m_list.append(m)
    self.Context = (po, m_list, f_list, w_list)
    if mouseClick.buttons() == Qt.MouseButton.LeftButton:
      if w_list:
        self.HighlightWaypoint(w_list, f_list)
      elif m_list:
        self.WaypointOffset = 0
        self.FleetOffset = 0
        self.HighlightMinefield(m_list, 0)
      elif f_list:
        self.WaypointOffset = 0
        self.HighlightFleet(f_list)
      else:
        self.WaypointOffset = 0
        self.FleetOffset = 0
        self.HighlightPlanet(po)


  def mouseMoveEvent(self, event):
    if self.WaypointSelected:
      w0 = self.SelectedWaypoint[0]
      wp = w0.previous
      p0 = event.scenePos()
      w0.xo = round(0.5 + p0.x() / GP.Xscale)
      w0.yo = round(0.5 + p0.y() / GP.Xscale)
      p0 = QPointF(GP.Xscale * w0.xo, GP.Xscale * w0.yo)
      s0 = wp.segment.line()
      s0.setP2(p0)
      wp.segment.setLine(s0)
      if w0.segment:
        s1 = w0.segment.line()
        s1.setP1(p0)
        w0.segment.setLine(s1)
      f = self.SelectedFleet
      if f.NextWaypoint == w0:
        f.Heading = math.atan2(w0.yo - f.yc, w0.xo - f.xc)
        pen, brush = f.getColours()
        self.PlotCourse(f, pen, brush)
      self.wpselect.setPos(p0)


  def CreateIndicator(self):
    w = GP.pointer_size * math.sqrt(3.0) / 2
    triangle = QPolygonF()
    triangle << QPointF(0, 0) << QPointF(GP.pointer_size / 2, w)
    triangle << QPointF(- GP.pointer_size / 2, w)
    self.pointer = self.addPolygon(triangle, Pen.white_08, Brush.yellow)
    self.pointer.setZValue(8)
    w = GP.fp_radius
    self.select = self.addEllipse(-w, -w, w + w, w + w, Pen.white_08, Brush.yellow)
    self.select.setZValue(-2)
    w = GP.wp_radius
    pen = QPen(Pen.yellow)
    pen.setWidthF(GP.wp_width)
    self.wpselect = self.addEllipse(-w, -w, w + w, w + w, pen)
    self.wpselect.setZValue(-2)


  def HighlightPlanet(self, p):
    self.select.setVisible(False)
    self.wpselect.setVisible(False)
    if self.SelectedPlanet:
      self.SelectedPlanet.label.setPen(Pen.white_l)
      self.SelectedPlanet.label.setBrush(Brush.white_l)
    if self.SelectedFleet:
      self.SelectedFleet.ShowCourse(self.ShowFleetMovements)
    self.SelectedWaypoint = None
    self.SelectedFleet = None
    self.SelectedFleets = None
    if self.NamesVisible:
      p.label.setPen(Pen.white)
      p.label.setBrush(Brush.white)
      self.pointer.setVisible(False)
    else:
      xp = GP.Xscale * p.x
      yp = GP.Xscale * p.y + GP.p_radius + GP.dy_pointer
      self.pointer.setPos(xp, yp)
      self.pointer.setVisible(True)
    self.SelectedPlanet = p
    self.SelectPlanet.emit(p)


  def HighlightFleet(self, f_list, index=-1):
    self.wpselect.setVisible(False)
    self.pointer.setVisible(False)
    if self.SelectedPlanet:
      self.SelectedPlanet.label.setPen(Pen.white_l)
      self.SelectedPlanet.label.setBrush(Brush.white_l)
    self.SelectedPlanet = None
    self.SelectedWaypoint = None
    if self.SelectedFleet:
      self.SelectedFleet.ShowCourse(self.ShowFleetMovements)
    if index < 0:
      index = (self.FleetIndex + self.FleetOffset) % len(f_list)
    f0 = f_list[index]
    self.select.setPos(GP.Xscale * f0.xc, GP.Xscale * f0.yc)
    self.select.setVisible(True)
    f0.ShowCourse(True)
    self.SelectedFleet = f0
    self.FleetIndex = index
    self.FleetOffset = 1
    self.SelectedFleets = f_list
    self.SelectFleet.emit(None, index, f_list, f0.MineFields)


  def HighlightMinefield(self, m_list, index):
    self.select.setVisible(False)
    if self.SelectedPlanet:
      self.SelectedPlanet.label.setPen(Pen.white_l)
      self.SelectedPlanet.label.setBrush(Brush.white_l)
    if self.SelectedFleet:
      self.SelectedFleet.ShowCourse(self.ShowFleetMovements)
    self.SelectedWaypoint = None
    self.SelectedFleet = None
    self.SelectedFleets = None
    self.SelectedPlanet = None
    xp = GP.Xscale * m_list[0].x
    yp = GP.Xscale * m_list[0].y + GP.dy_pointer
    self.pointer.setPos(xp, yp)
    self.pointer.setVisible(True)
    self.SelectField.emit(None, index, m_list)


  def HighlightWaypoint(self, w_list, f_list, index=-1):
    self.pointer.setVisible(False)
    if self.SelectedPlanet:
      self.SelectedPlanet.label.setPen(Pen.white_l)
      self.SelectedPlanet.label.setBrush(Brush.white_l)
    self.SelectedPlanet = None
    if self.SelectedFleet:
      self.SelectedFleet.ShowCourse(self.ShowFleetMovements)
    if index < 0:
      index = (self.WaypointIndex + self.WaypointOffset) % len(w_list)
    w0, n0 = w_list[index]
    f0 = f_list[index]
    self.wpselect.setPos(GP.Xscale * w0.xo, GP.Xscale * w0.yo)
    self.select.setPos(GP.Xscale * f0.xc, GP.Xscale * f0.yc)
    self.wpselect.setVisible(True)
    self.select.setVisible(True)
    f0.ShowCourse(True)
    self.SelectedWaypoint = (w0, n0)
    self.SelectedFleet = f0
    self.WaypointIndex = index
    self.FleetIndex = index
    self.WaypointOffset = 1
    self.SelectedFleets = f_list
    self.WaypointSelected = True
    self.SelectFleet.emit(None, index, f_list, [])


  def ShowMines(self, switch, fof):
    self.ShowField[fof] = switch
    if self.FieldsVisible:
      self.ShowFields(True)
      self.UpdateFilter.emit(self.ShowField)


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


  def ShowMovements(self, show):
    for f in self.fleets:
      if f.ShipCounter > 0 and f.Discovered and not f.Orbiting:
        f.ShowCourse(show)
    if self.SelectedFleet:
      self.SelectedFleet.ShowCourse(self.SelectedFleet.ShipCounter > 0)
    self.ShowFleetMovements = show


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
      if switch:
        self.SelectedPlanet.label.setPen(Pen.white)
        self.SelectedPlanet.label.setBrush(Brush.white)
        self.pointer.setVisible(False)
      else:
        xp = GP.Xscale * self.SelectedPlanet.x
        yp = GP.Xscale * self.SelectedPlanet.y + GP.p_radius + GP.dy_pointer
        self.pointer.setPos(xp, yp)
        self.pointer.setVisible(True)
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
      p.scanner = self.CreateScanner(p.x, p.y, model.value[0], model.value[1])


  def CreateScanner(self, xo, yo, rmax, rpen=0):
    s = Scanner(xo, yo, rmax, rpen)
    x = GP.Xscale * xo
    y = GP.Xscale * yo
    if rmax > 0:
      r = rmax * GP.Xscale
      box = QRectF(x - r, y - r, r + r, r + r)
      s.detection = self.addEllipse(box, Pen.red_s, Brush.red_s)
      s.detection.setZValue(-10)
      s.detection.setVisible(False)
    if rpen > 0:
      r = rpen * GP.Xscale
      box = QRectF(x - r, y - r, r + r, r + r)
      s.penetration = self.addEllipse(box, Pen.yellow_s, Brush.yellow_s)
      s.penetration.setZValue(-8)
      s.penetration.setVisible(False)
    return s


  def RegisterFleet(self, fleet, p, y=None):
    w = GP.f_radius + GP.f_radius
    fleet.RestingFleet = self.addEllipse(-GP.f_radius, -GP.f_radius, w, w)
    fleet.RestingFleet.setVisible(False)
    fleet.Course = self.addLine(0, 0, 0, 1)
    if y:
      xo = p
      yo = y
    else:
      xo = p.x
      yo = p.y
    self.addWaypoint(fleet, xo, yo)
    if fleet.FriendOrFoe == Stance.allied and fleet.MaxRange > 0:
      fleet.scanner = self.CreateScanner(xo, yo, fleet.MaxRange, fleet.PenRange)
    fleet.ShipCount = self.CreateOrbitLabel(0, 0)
    fleet.xc = xo
    fleet.yc = yo
    self.fleets.append(fleet)


  def SetWaypointMode(self, event):
    self.WaypointMode = event


  def addWaypoint(self, fleet, x, y, index=0):
    wa = Waypoint(x, y)
    if fleet.FirstWaypoint:
      xa = GP.Xscale * wa.xo
      ya = GP.Xscale * wa.yo
      if fleet.FriendOrFoe == Stance.allied:
        pen = QPen(Pen.blue_l)
        pen.setWidthF(self.CurrentPathWidth)
      else:
        pen = None
      w0 = fleet.ActiveWaypoint[index]
      x0 = GP.Xscale * w0.xo
      y0 = GP.Xscale * w0.yo
      wa.warp = w0.warp
      if w0.next:
        wa.task = Task.MOVE
        if w0.segment:
          self.removeItem(w0.segment)
          w0.segment = None
        w1 = w0.next
        x1 = GP.Xscale * w1.xo
        y1 = GP.Xscale * w1.yo
        w1.previous = wa
        wa.next = w1
        if w1 == fleet.NextWaypoint:
          fleet.NextWaypoint = wa
        if pen:
          line = QLineF(xa, ya, x1, y1)
          wa.segment = self.addLine(line)
          wa.segment.setPen(pen)
          wa.segment.setZValue(-1)
      elif fleet.NextWaypoint:
        fleet.LastWaypoint = wa
      else:
        fleet.NextWaypoint = wa
        fleet.LastWaypoint = wa
      w0.next = wa
      wa.previous = w0
      if pen:
        line = QLineF(x0, y0, xa, ya)
        w0.segment = self.addLine(line)
        w0.segment.setPen(pen)
        w0.segment.setZValue(-1)
    else:
      fleet.FirstWaypoint = wa
      fleet.LastWaypoint = wa
    fleet.ActiveWaypoint = [wa]


  def CreateOrbitLabel(self, x, y):
    label = self.addSimpleText("", GP.mapFont)
    label.setPen(Pen.white_l)
    label.setBrush(Brush.white_l)
    label.setPos(x, y)
    label.setVisible(False)
    label.setZValue(4)
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
    w0 = w / math.sqrt(8.0) + 0.5
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
    self.update()
    self.ShowFleetStrength = event


  def ApplyFleetFilter(self):
    for f in self.fleets:
      if f.Discovered and not f.Orbiting:
        if f.ShipCounter > 0:
          if f.WarpSpeed > 0:
            f.MovingFleet.setVisible(True)
          else:
            f.RestingFleet.setVisible(True)
          f.ShipCount.setVisible(self.ShowFleetStrength)
          f.ShowCourse(self.ShowFleetMovements)
        else:
          if f.WarpSpeed > 0:
            f.MovingFleet.setVisible(False)
          f.ShipCount.setVisible(False)
          f.ShowCourse(False)
          f.RestingFleet.setVisible(False)
    if self.SelectedFleets:
      total = 0
      for f in self.SelectedFleets:
        total += f.ShipCounter
      if total > 0:
        if self.SelectedWaypoint:
          self.wpselect.setVisible(True)
        self.select.setVisible(True)
      else:
        self.wpselect.setVisible(False)
        self.select.setVisible(False)
      self.SelectFleet.emit(self.SelectedPlanet, self.FleetIndex, self.SelectedFleets, self.SelectedFleet.MineFields)
    self.update()


  def FilterFoes(self, enabled, select):
    self.FoeFilterEnabled = enabled
    if select:
      self.ActiveFoeFilter = select
    if enabled:
      for f in self.fleets:
        if f.FriendOrFoe != Stance.allied:
          f.ApplyFoeFilter(select)
          f.UpdateShipCount()
    else:
      for f in self.fleets:
        if f.FriendOrFoe != Stance.allied:
          f.ShipCounter = len(f.ShipList)
          f.UpdateShipCount()
    for p in self.planets:
      TotalOthers = 0
      TotalFoes = 0
      for f in p.fleets_in_orbit:
        if f.FriendOrFoe == Stance.hostile:
          TotalFoes += f.ShipCounter
        elif f.FriendOrFoe != Stance.allied:
          TotalOthers += f.ShipCounter
      p.UpdateFoes(TotalFoes - p.TotalFoes)
      p.UpdateOthers(TotalOthers - p.TotalOthers)
      if self.DefaultView:
        p.ShowDefaultView(self.ShowFleetStrength)
    self.ApplyFleetFilter()
    if self.SelectedPlanet:
      self.UpdatePlanet.emit(self.SelectedPlanet)
    self.update()


  def FilterFriendlies(self, enabled, select):
    self.FriendFilterEnabled = enabled
    if select:
      self.ActiveFriendFilter = select
    if enabled:
      for f in self.fleets:
        if f.FriendOrFoe == Stance.allied:
          f.ApplyMyFilter(self.ShowIdleFleetsOnly, select)
          f.UpdateShipCount()
    elif self.ShowIdleFleetsOnly:
      for f in self.fleets:
        if f.FriendOrFoe == Stance.allied:
          if f.Idle:
            f.ShipCounter = len(f.ShipList)
            f.UpdateShipCount()
          else:
            f.ShipCounter = 0
    else:
      for f in self.fleets:
        if f.FriendOrFoe == Stance.allied:
          f.ShipCounter = len(f.ShipList)
          f.UpdateShipCount()
    for p in self.planets:
      TotalFriends = 0
      for f in p.fleets_in_orbit:
        if f.FriendOrFoe == Stance.allied:
          TotalFriends += f.ShipCounter
      p.UpdateFriends(TotalFriends - p.TotalFriends)
      if self.DefaultView:
        p.ShowDefaultView(self.ShowFleetStrength)
    self.ApplyFleetFilter()
    if self.SelectedPlanet:
      self.UpdatePlanet.emit(self.SelectedPlanet)
    self.update()


  def EnableFoeFilter(self, event):
    if event and self.ActiveFoeFilter:
      self.FilterFoes(True, self.ActiveFoeFilter)
    else:
      self.FilterFoes(False, None)


  def EnableFriendFilter(self, event):
    if event and self.ActiveFriendFilter:
      self.FilterFriendlies(True, self.ActiveFriendFilter)
    else:
      self.FilterFriendlies(False, None)


  def FilterIdleFleets(self, event):
    self.ShowIdleFleetsOnly = event
    self.FilterFoes(self.FoeFilterEnabled, self.ActiveFoeFilter)
    self.FilterFriendlies(self.FriendFilterEnabled, self.ActiveFriendFilter)


  def ResizeFlightPaths(self, width):
    for f in self.fleets:
      pen = f.getColours()[0]
      pen.setWidthF(width)
      wp = f.FirstWaypoint
      while wp and wp.segment:
        wp.segment.setPen(pen)
        wp = wp.next
#      if f.FriendOrFoe != Stance.allied:
#        pen.setDashPattern((6, 10))
      f.Course.setPen(pen)
    self.CurrentPathWidth = width


  def PlotCourse(self, f, pen, brush):
    x0 = GP.Xscale * f.xc
    y0 = GP.Xscale * f.yc
    if f.WarpSpeed > 0:
      if f.MovingFleet:
        self.removeItem(f.MovingFleet)
      Q0 = QTransform()
      Q0.translate(x0, y0)
      Q0.rotateRadians(f.Heading)
      f.MovingFleet = self.addPolygon(Q0.map(Fleet.arrow), pen, brush)
    else:
      f.RestingFleet.setPos(x0, y0)
      f.RestingFleet.setPen(pen)
      f.RestingFleet.setBrush(brush)
      f.RestingFleet.setVisible(True)
    wp = f.NextWaypoint
    if wp and f.FriendOrFoe == Stance.allied:
      dx, dy = f.getOffset(wp)
      x0 += dx
      y0 += dy
      x1 = GP.Xscale * wp.xo
      y1 = GP.Xscale * wp.yo
    elif f.WarpSpeed > 0:
      length = f.WarpSpeed * f.WarpSpeed * GP.Xscale
      dist = GP.c_dist * length
      if dist > GP.max_dist:
        dist = GP.max_dist
      dx = length * math.cos(f.Heading)
      dy = length * math.sin(f.Heading)
      x1 = x0 + dx
      y1 = y0 + dy
      x0 += dx * dist / length
      y0 += dy * dist / length
    else:
      x1 = x0
      y1 = y0
#    if f.FriendOrFoe != Stance.allied:
#      pen.setDashPattern((6, 10))
    pen.setWidthF(self.CurrentPathWidth)
    f.Course.setPen(pen)
    f.Course.setLine(x0, y0, x1, y1)


  def ComputeTurn(self):
    for p in self.planets:
      p.ClearOrbit()
      p.fleets_in_orbit = []
    for f in self.fleets:
      f.Orbiting = None
      for p in self.planets:
        if p.x == f.xc and p.y == f.yc:
          p.EnterOrbit(f)
          p.fleets_in_orbit.append(f)
          break
    for f in self.fleets:
      if f.MovingFleet:
        self.removeItem(f.MovingFleet)
        f.MovingFleet = None
      f.RestingFleet.setVisible(False)
      f.ShipCount.setVisible(False)
      f.ShowCourse(False)
      if f.ShipCounter > 0 and f.Discovered and not f.Orbiting:
        pen, brush = f.getColours()
        f.Heading = math.pi
        if f.NextWaypoint.previous:
          x0 = f.NextWaypoint.previous.xo
          y0 = f.NextWaypoint.previous.yo
          x1 = f.NextWaypoint.xo
          y1 = f.NextWaypoint.yo
          f.Heading = math.atan2(y1 - y0, x1 - x0)
        self.PlotCourse(f, pen, brush)
        f.UpdateShipCount()
        f.ShipCount.setVisible(self.ShowFleetStrength)
        f.ShowCourse(self.ShowFleetMovements)
    for p in self.planets:
      p.UpdateShipTracking()
      p.mine_fields = []
      for m in self.minefields:
        d = (m.x - p.x) * (m.x - p.x) + (m.y - p.y) * (m.y - p.y)
        if d < m.mines:
          p.mine_fields.append(m)
    for f in self.fleets:
      f.MineFields = []
      for m in self.minefields:
        d = (f.xc - m.x) * (f.xc - m.x) + (f.yc - m.y) * (f.yc - m.y)
        if d < m.mines:
          f.MineFields.append(m)
    self.update()

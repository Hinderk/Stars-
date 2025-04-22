
from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPolygonF

from enum import Enum
from math import sqrt
from ruleset import Ruleset
from faction import Faction
from colours import Pen, Brush
from defines import Stance
from guiprop import GuiProps



class Model(Enum):
  Normal = 'Standard'
  Heavy = 'Heavy'
  SpeedTrap = 'Speed Trap'



class Minefield:

  caret = QPolygonF()
  caret << QPointF(0, - GuiProps.center_size)
  caret << QPointF(GuiProps.center_size, 0)
  caret << QPointF(0, GuiProps.center_size)
  caret << QPointF(-GuiProps.center_size, 0)

  Counter = dict()
  for m in Model:
    Counter[m] = 0

  def __init__(self, scene, x, y, m, model, fID, people):

    r = sqrt(m) * GuiProps.Xscale
    Minefield.Counter[model] += 1

    self.id = Minefield.Counter[model]
    self.fleets_en_route = []
    self.TotalFriends = 0
    self.TotalFoes = 0
    self.TotalOthers = 0
    self.Detected = True # False    -- FIXME: Test feature
    self.ShipTracking = False
    self.fof = people.getStance(Ruleset.fID0, fID)
    self.faction = fID
    self.x = x
    self.y = y
    self.mines = m
    self.model = model
    self.rate_of_decay = Ruleset.MinefieldDecay(fID)
    self.countdown = 0

    x *= GuiProps.Xscale
    y *= GuiProps.Xscale
    box = QRectF(x - r, y - r, r + r, r + r)
    if self.fof == Stance.allied:
      self.area = scene.addEllipse(box, Pen.blue_m, Brush.blue_m)
      self.area.setZValue(-6)
      self.center = scene.addPolygon(self.caret, Pen.blue_l, Brush.blue)
    elif self.fof == Stance.friendly:
      self.area = scene.addEllipse(box, Pen.yellow_m, Brush.yellow_m)
      self.area.setZValue(-5)
      self.center = scene.addPolygon(self.caret, Pen.noshow, Brush.yellow)
    else:
      self.area = scene.addEllipse(box, Pen.red_m, Brush.red_m)
      self.area.setZValue(-4)
      self.center = scene.addPolygon(self.caret, Pen.noshow, Brush.red)
    self.center.setZValue(4)
    self.center.setPos(x, y)
    self.area.setVisible(False)
    self.center.setVisible(False)

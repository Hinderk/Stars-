
from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPolygonF

from enum import Enum
from colours import Pen, Brush
from defines import Stance, GuiProps as GP



class Model(Enum):
  Normal = 0
  Heavy = 1
  SpeedTrap = 2



class Minefield:

  caret = QPolygonF()
  caret << QPointF(0, - GP.center_size) << QPointF(GP.center_size, 0)
  caret << QPointF(0, GP.center_size) << QPointF(-GP.center_size, 0)

  def __init__(self, scene, x, y, m, model, fof):

    r = 600 #  TODO: determine size of minefield as function of mine count

    self.xo = x
    self.yo = y
    self.radius = r
    self.mines = m
    self.model = model
    self.fof = fof
    self.rate_of_decay = 0.01
    self.countdown = 0

    box = QRectF(x - r, y - r, r + r, r + r)
    if fof == Stance.allied:
      brush = Brush.blue
      pen = Pen.blue_l
      self.area = scene.addEllipse(box, Pen.blue_m, Brush.blue_m)
      self.area.setZValue(-6)
    elif fof == Stance.friendly:
      brush = Brush.yellow
      pen = Pen.noshow
      self.area = scene.addEllipse(box, Pen.yellow_m, Brush.yellow_m)
      self.area.setZValue(-5)
    else:
      brush = Brush.red
      pen = Pen.noshow
      self.area = scene.addEllipse(box, Pen.red_m, Brush.red_m)
      self.area.setZValue(-4)
    self.center = scene.addPolygon(self.caret)
    self.center.setPen(pen)
    self.center.setBrush(brush)
    self.center.setZValue(2)
    self.center.setPos(x, y)
    self.area.setVisible(False)
    self.center.setVisible(False)

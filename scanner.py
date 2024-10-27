
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor

from enum import Enum
from defines import Perks as P
from defines import Traits as T
from colours import Pen, Brush




class Model(Enum):
  Bat = [0, -1, 2, True, 0, 0, 0, 0, 0, 0, T.NO, 1, 0, 1, 1, P.NONE]
  Rhino = [50, -1, 5, True, 0, 0, 0, 0, 1, 0, T.NO, 3, 0, 2, 3, P.NONE]
  Viewer50 = [50, -1, -1, False, 0, 0, 0, 0, 0, 0, T.NO, 10, 10, 70, 100, P.NONE]
  Viewer90 = [90, -1, -1, False, 0, 0, 0, 0, 1, 0, T.NO, 10, 10, 70, 100, P.NONE]
  Scoper150 = [150, -1, -1, False, 0, 0, 0, 0, 3, 0, T.NO, 10, 10, 70, 100, P.NONE]
  Mole = [100, -1, 2, True, 0, 0, 0, 0, 4, 0, T.NO, 2, 0, 2, 9, P.NONE]
  PickPocket = [80, -1, 15, True, 4, 0, 0, 0, 4, 4, T.ST, 8, 10, 6, 35, P.ROB]
  Possum = [150, -1, 3, True, 0, 0, 0, 0, 5, 0, T.NO, 3, 0, 3, 18, P.NONE]
  Chameleon = [160, 45, 6, True, 3, 0, 0, 0, 6, 0, T.ST, 4, 6, 4, 25, P.HIDE]
  Scoper220 = [220, -1, -1, False, 0, 0, 0, 0, 6, 0, T.NO, 10, 10, 70, 100, P.NONE]
  DNA = [125, -1, 2, True, 0, 0, 3, 0, 0, 6, T.NO, 1, 1, 1, 5, P.NONE]
  Ferret = [185, 50, 2, True, 3, 0, 0, 0, 7, 2, T.NO, 2, 0, 8, 36, P.NAS]
  Gazelle = [225, -1, 5, True, 4, 0, 0, 0, 8, 0, T.NO, 4, 0, 5, 24, P.NONE]
  Scoper280 = [280, -1, -1, False, 0, 0, 0, 0, 8, 0, T.NO, 10, 10, 70, 100, P.NONE]
  Dolphin = [220, 100, 4, True, 5, 0, 0, 0, 10, 4, T.NO, 5, 5, 10, 40, P.NAS]
  Snooper320X = [320, 160, -1, False, 3, 0, 0, 0, 10, 3, T.AR, 10, 10, 70, 100, P.NONE]
  RNA = [230, -1, 2, True, 0, 0, 5, 0, 0, 10, T.NO, 1, 1, 2, 20, P.NONE]
  Cheetah = [275, -1, 4, True, 5, 0, 0, 0, 11, 0, T.NO, 3, 1, 13, 50, P.NONE]
  Snooper400X = [400, 200, -1, False, 4, 0, 0, 0, 13, 6, T.AR, 10, 10, 70, 100, P.NONE]
  EagleEye = [335, -1, 3, True, 6, 0, 0, 0, 14, 0, T.NO, 3, 2, 21, 64, P.NONE]
  RobberBaron = [220, 120, 20, True, 10, 0, 0, 0, 24, 10, T.ST, 10, 10, 10, 90, P.ROB]
  Elephant = [300, 200, 6, True, 6, 0, 0, 0, 16, 7, T.NO, 8, 5, 14, 70, P.NAS]
  Snooper500X = [500, 250, -1, False, 5, 0, 0, 0, 16, 7, T.AR, 10, 10, 70, 100, P.NONE]
  Snooper620X = [620, 310, -1, False, 7, 0, 0, 0, 23, 9, T.AR, 10, 10, 70, 100, P.NONE]
  Peerless = [500, -1, 4, True, 7, 0, 0, 0, 24, 0, T.NO, 3, 2, 30, 90, P.NONE]



class Scanner:

  def __init__(self, x, y, model, scene):
    r = model.value[0] * scene.Xscale
    self.range = r
    self.xo = x + scene.p_radius /2
    self.yo = y + scene.p_radius /2
    if r > 0:
      box = QRectF(self.xo - r, self.yo - r, r + r, r + r)
      self.range = scene.addEllipse(box, Pen.red_s, Brush.red_s)
      self.range.setZValue(-10)
      self.range.setVisible(False)
    else:
      self.range = None
    r = model.value[1] * scene.Xscale
    self.penrange = r
    if r > 0:
      box = QRectF(self.xo - r, self.yo - r, r + r, r + r)
      self.penetration = scene.addEllipse(box, Pen.yellow_s, Brush.yellow_s)
      self.penetration.setZValue(-5)
      self.penetration.setVisible(False)
    else:
      self.penetration = None


  def ShowRanges(self, toggle):
    if self.penetration:
      self.penetration.setVisible(toggle)
    if self.range:
      self.range.setVisible(toggle)


from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPen, QBrush, QColor, QPolygonF, QFont
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene

import math

from PyQt6 import QtWidgets

##from ruleset import Ruleset



class Universe(QGraphicsView):

  def __init__(self, rules):
    super(self.__class__, self).__init__()

    self.planets = []
    self.fleets = []
    self.minefields = []
    self.debris = []

    self.Scene = QGraphicsScene()

    self.CreatePlanets(rules)
    self.ColonizePlanets(rules)

    black = QColor(0, 0, 0)
    blackBrush = QBrush(black)
    self.Scene.setBackgroundBrush(blackBrush)
    self.setScene(self.Scene)
    policy = QtWidgets.QSizePolicy()
    policy.setHorizontalPolicy(policy.Policy.MinimumExpanding)
    policy.setVerticalPolicy(policy.Policy.MinimumExpanding)
    self.setSizePolicy(policy)


  def ColonizePlanets(self, rules):
    for p in self.planets:
      print(p)


  def CreatePlanets(self, rules):
    for n in range(0, rules.PlanetCount()):
      print(n)

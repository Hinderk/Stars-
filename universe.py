
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPen, QBrush, QColor, QPolygonF, QFont
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene

import math
##from ruleset import Ruleset



class Universe(QGraphicsView):

  Width = 1024
  Height = 768

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
    self.setMinimumSize(QSize(800, 850))


  def ColonizePlanets(self, rules):
    for p in self.planets:
      print(p)


  def CreatePlanets(self, rules):
    for n in range(0, rules.PlanetCount()):
      print(n)
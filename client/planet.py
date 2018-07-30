"""This module implements a star system & its graphical representation"""

import sys

from planetdata import PlanetData

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsEllipseItem

from PyQt5.QtGui import QFont, QPen
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPaintEvent

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QSizeF
from PyQt5.QtCore import QPointF




class Planet(QGraphicsEllipseItem, PlanetData):
    """This class represents a star system as shown on the star map."""
    PlanetColor = QColor(255, 255, 255, 255)
    PlanetFont = QFont('Calibri', 32, 25, True)
    PlanetRadius = 25


    def __init__(self, x, y, starName):
        super(QGraphicsEllipseItem, self).__init__()
        self.initSystem(x, y, starName)


    def initSystem(self, x, y, starName):
        """Initialize the star system and name it."""
        self.x = x
        self.y = y
        self.Name = starName
        self.Friendlies = 0
        self.Foes = 0


    def setPlanetData(self, data):
        """Assign planet parameters to an existing star system"""
        self.Radius = data.Radius
        self.Temperature = data.Temperature
        self.Gravity = data.Gravity
        self.Radiation = data.Radiation
        self.Factories = data.Factories
        self.Mines = data.Mines
        self.Defenses = data.Defenses
        self.TechLevel = data.TechLevel
        self.Boranium = data.Boranium
        self.Ironium = data.Ironium
        self.Thoridium = data.Thoridium
        self.totalBoranium = data.totalBoranium
        self.totalIronium = data.totalIronium
        self.totalThoridium = data.totalThoridium
        self.Settlers = data.Settlers


    def mousePressEvent(self, event):
        """Intercept mouse clicks to select a star system."""
        print( 'Mouse click on planet: ', self.Name, 'at:', event.scenePos() )
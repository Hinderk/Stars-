"""This module implements a star system & its graphical representation"""

import sys

from planetdata import PlanetData

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtGui import QFont, QPen
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPaintEvent

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QSize




class Planet(QGraphicsItem, PlanetData):
    """This class represents a star system as shown on the star map."""
    PlanetColor = QColor(255, 255, 255, 255)
    PlanetFont = QFont('Calibri', 32, 25, True)

    def __init__(self, starName):
        super(QGraphicsItem, self).__init__()
        self.initSystem(starName)

    def initSystem(self, starName):
        """Initialise the star system and name it."""
        self.x = 0
        self.y = 0
        self.Name = starName

    def moveTo(self, xval, yval):
        self.x = xval
        self.y = yval
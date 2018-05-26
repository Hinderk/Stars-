"""This module maintains the list of star systems comprising the game universe"""

import sys

from planet import Planet

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtGui import QFont, QPen, QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPaintEvent

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QSizeF




class Starmap(object):
    """This class maintains a list of star systems."""

    def __init__(self):
        super().__init__()
        self.Star = dict()
        self.createMap()


    def createMap(self):
        """Populate the star map with various types of objects."""
        self.X0 = 0
        self.Y0 = 0
        p0 = Planet('Earth')
        p0.moveTo(200, 500)
        self.Star['Earth'] = p0
        p1 = Planet('Alpha Centauri')
        p1.moveTo(600, 1400)
        self.Star['Alpha Centauri'] = p1
        p2 = Planet('Tau Ceti')
        p2.moveTo(1200,750)
        self.Star['Tau Ceti'] = p2


    def createScene(self, PpiScene):
        """Populate the universe with the stars in the map."""
        PlanetList = self.Star.values()
        for p in PlanetList:
            brush = QBrush(p.PlanetColor)
            pen = QPen(p.PlanetColor)
            size = QSizeF(50, 50)
            loc = QPointF(p.x - self.X0, p.y - self.Y0)
            pos = QRectF(loc, size)
            PpiScene.addEllipse(pos, pen, brush)
            Name = PpiScene.addSimpleText(p.Name)
            Name.setBrush(brush)
            Name.setPen(pen)
            Name.setFont(p.PlanetFont)
            bounds = Name.boundingRect()
            Name.setX( size.width() / 2 + loc.x() - bounds.width() / 2 )
            Name.setY( loc.y() + size.height() / 2 + 40 )
            
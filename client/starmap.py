"""This module maintains the list of star systems comprising the game universe"""

import sys

from planet import Planet

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtGui import QFont, QPen, QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPaintEvent

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QSizeF




class Starmap(QGraphicsScene):
    """This class maintains a list of star systems."""

    def __init__(self):
        super().__init__()
        self.Star = dict()
        self.createMap()


    def createMap(self):
        """Populate the star map with various types of objects."""
        self.X0 = 0
        self.Y0 = 0
        p0 = Planet(200, 500, 'Earth')
        self.Star['Earth'] = p0
        p1 = Planet(600, 1400, 'Alpha Centauri')
        self.Star['Alpha Centauri'] = p1
        p2 = Planet(1200, 750, 'Tau Ceti')
        self.Star['Tau Ceti'] = p2
        self.addItem(p0)
        self.addItem(p1)
        self.addItem(p2)


    def renderPlanets(self):
        """Populate the universe with the stars in the map."""
        PlanetList = self.Star.values()
        brush = QBrush(Planet.PlanetColor)
        pen = QPen(Planet.PlanetColor)
        for p in PlanetList:
            p.setBrush(brush)
            p.setPen(pen)
            loc = QPointF(p.x, p.y)
            name = self.addSimpleText(p.Name)
            name.setBrush(brush)
            name.setPen(pen)
            name.setFont(p.PlanetFont)
            bounds = name.boundingRect()
            name.setX( loc.x() - bounds.width() / 2 )
            name.setY( loc.y() + Planet.PlanetRadius + 20 )



#    def mousePressEvent(self, event):
#        """Intercept mouse klicks to select space objects."""
#        print( 'Mouse klick on item: ', event.scenePos() )
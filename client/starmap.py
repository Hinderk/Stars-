"""This module maintains the list of star systems comprising the game universe"""

import sys
from enum import Enum

from planet import Planet
from planetdata import PlanetData
from speciesdata import SpeciesData

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




class RenderMode(Enum):
    """Possible options which information to display when rendering the star map"""
    Plain = 1
    PlanetValue = 2
    Orbiting = 3
    Minerals = 4
    Settlements = 5
    Deposits = 6




class Starmap(QGraphicsScene):
    """This class maintains a list of star systems."""
    
    neutralbrush = QBrush(Planet.PlanetColor)
    redbrush = QBrush(QColor(255,0,0))
    yellowbrush = QBrush(QColor(255,255,0))
    greenbrush = QBrush(QColor(0,255,0))
    neutralpen = QPen(Planet.PlanetColor)
    redpen = QPen(QColor(255,0,0))
    yellowpen = QPen(QColor(255,255,0))
    greenpen = QPen(QColor(0,255,0))


    def __init__(self):
        super().__init__()
        self.Star = dict()
        self.createMap()


    def createMap(self):
        """Populate the star map with various types of objects."""
        specs = PlanetData()
        specs.Temperature = 300.0
        specs.Settlers = 7000000
        specs.Factories = 5000000
        specs.Mines = 100000
        p0 = Planet(200, 500, 'Earth')
        p0.setPlanetData(specs)
        self.Star['Earth'] = p0
        specs.Temperature = 120.0
        specs.Settlers = 3
        specs.Factories = 80
        specs.Mines = 10
        p1 = Planet(600, 1400, 'Alpha Centauri')
        p1.setPlanetData(specs)
        self.Star['Alpha Centauri'] = p1
        specs.Temperature = 340.0
        specs.Settlers = 25000
        specs.Factories = 90000
        specs.Mines = 4000
        p2 = Planet(1200, 750, 'Tau Ceti')
        p2.setPlanetData(specs)
        self.Star['Tau Ceti'] = p2
        self.addItem(p0)
        self.addItem(p1)
        self.addItem(p2)



    def SelectColorAndSize(self,value):
        """Determine the size and the color of a system on the star map"""
        if value < 0.0 :
            self.pen = neutralpen
            self.brush = neutralbrush
            self.radius = 1.0
        elif 3 * value < 1 :
            self.brush = Starmap.redbrush
            self.pen = Starmap.redpen
            self.radius = 0.4 + 1.8 * value
        elif 3 * value < 2 :
            self.brush = Starmap.yellowbrush
            self.pen = Starmap.yellowpen
            self.radius = 1.8 * value - 0.2
        else:
            self.brush = Starmap.greenbrush
            self.pen = Starmap.greenpen
            self.radius = 1.8 * value - 0.8   
        


    def renderPlanets(self, mode, species):
        """Populate the universe with the stars in the map."""
        PlanetList = self.Star.values() 
        for p in PlanetList:
            if mode == RenderMode.PlanetValue:
                value = p.PlanetValue(species)
            elif mode == RenderMode.Settlements:
                value = p.PopulationLevel(species)    
            else:
                value = -1.0
            self.SelectColorAndSize(value)
            r = self.radius * p.PlanetRadius 
            d = 2 * r
            p.setRect( p.x - r, p.y - r, d, d)
            p.setBrush(self.brush)
            p.setPen(self.pen)
            loc = QPointF(p.x, p.y)
            name = self.addSimpleText(p.Name)
            name.setBrush(Starmap.neutralbrush)
            name.setPen(Starmap.neutralpen)
            name.setFont(p.PlanetFont)
            bounds = name.boundingRect()
            name.setX( loc.x() - bounds.width() / 2 )
            name.setY( loc.y() + r + 20 )
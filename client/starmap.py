"""This module maintains the list of star systems comprising the game universe"""

import sys

from enum import Enum

from planet import Planet
from planetdata import PlanetData
from speciesdata import SpeciesData
from mapsettings import RenderMode 
from mapsettings import MapSettings
from mapsettings import FleetFilter

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
    
    FleetFont = QFont('Cambria', 24, 25, False)
    
    bluebrush = QBrush(QColor(0,0,255))
    neutralbrush = QBrush(QColor(255,255,255))
    planetbrush = QBrush(Planet.PlanetColor)
    redbrush = QBrush(QColor(255,0,0))
    yellowbrush = QBrush(QColor(255,255,0))
    greenbrush = QBrush(QColor(0,255,0))
    bluepen = QPen(QColor(0,0,255))
    neutralpen = QPen(QColor(255,255,255))
    planetpen = QPen(Planet.PlanetColor)
    redpen = QPen(QColor(255,0,0))
    yellowpen = QPen(QColor(255,255,0))
    greenpen = QPen(QColor(0,255,0))


    def __init__(self):
        super().__init__()
        self.Star = dict()
        self.createMap()
        Starmap.neutralpen.setWidthF(3.5)


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
        p1.Foes = 1
        p1.Friendlies = 5
        self.Star['Alpha Centauri'] = p1
        specs.Temperature = 340.0
        specs.Settlers = 25000
        specs.Factories = 90000
        specs.Mines = 4000
        p2 = Planet(1200, 750, 'Tau Ceti')
        p2.Friendlies = 20
        p2.Foes = 3000
        p2.setPlanetData(specs)
        self.Star['Tau Ceti'] = p2
        self.addItem(p0)
        self.addItem(p1)
        self.addItem(p2)



    def SelectColorAndSize(self,value):
        """Determine the size and the color of a system on the star map"""
        if value < 0.0 :
            self.pen = Starmap.planetpen
            self.brush = Starmap.planetbrush
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
        


    def renderPlanets(self, settings, species):
        """Populate the universe with the stars in the map."""
        PlanetList = self.Star.values() 
        for p in PlanetList:
            if settings.Mode == RenderMode.PlanetValue:
                value = p.PlanetValue(species)
            elif settings.Mode == RenderMode.Settlements:
                value = p.PopulationLevel(species)    
            else:
                value = -1.0
            self.SelectColorAndSize(value)
            r = self.radius * p.PlanetRadius 
            d = 2 * r
            p.setRect( p.x - r, p.y - r, d, d)
            p.setBrush(self.brush)
            name = self.addSimpleText(p.Name)
            name.setBrush(Starmap.planetbrush)
            name.setFont(p.PlanetFont)
            bounds = name.boundingRect()
            name.setX( p.x - bounds.width() / 2 )
            name.setY( p.y + r + 20 )
            if settings.Mode == RenderMode.Orbiting:
                ShowFriends = ( settings.InOrbit == FleetFilter.Friend ) or ( settings.InOrbit == FleetFilter.Armed )
                ShowFoes = ( settings.InOrbit == FleetFilter.Foe ) or ( settings.InOrbit == FleetFilter.Armed )
                d = d + 30
                r = r + 15
                if ShowFriends and p.Friendlies > 0:
                    self.addEllipse( p.x - r, p.y - r, d, d, Starmap.neutralpen)
                    backdrop = self.addRect(0, 0, 10, 10 )
                    backdrop.setBrush(Starmap.planetbrush)             
                    counter = self.addSimpleText(str(p.Friendlies))
                    counter.setBrush(Starmap.bluebrush)
                    counter.setFont(Starmap.FleetFont)
                    bounds = counter.boundingRect()
                    x0 = p.x + r + 20
                    y0 = p.y - bounds.height() / 2
                    counter.setX( x0 )
                    counter.setY( y0 )  
                    backdrop.setRect( x0 - 5, y0, bounds.width() + 10, bounds.height() )
                if ShowFoes and p.Foes > 0:
                    self.addEllipse( p.x - r, p.y - r, d, d, Starmap.neutralpen)
                    backdrop = self.addRect(0, 0, 0, 0 )
                    backdrop.setBrush(Starmap.planetbrush)             
                    counter = self.addSimpleText(str(p.Foes))
                    counter.setBrush(Starmap.redbrush)
                    counter.setFont(Starmap.FleetFont)
                    bounds = counter.boundingRect()
                    x0 = p.x - r - 20 - bounds.width()
                    y0 = p.y - bounds.height() / 2
                    counter.setX( x0 )
                    counter.setY( y0 )  
                    backdrop.setRect( x0 - 5, y0, bounds.width() + 10, bounds.height() )
"""This module maintains the list of star systems comprising the game universe"""

import sys

from enum import Enum

from planet import Planet
from starcolors import StarColors
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

    def __init__(self):
        super().__init__()
        self.Star = dict()
        self.Sector = QRectF()
        self.createMap()
        self.ComputeBoundingBox()



    def createMap(self):
        """Populate the star map with various types of objects."""
        specs = PlanetData()
        specs.Temperature = 300.0
        specs.Settlers = 7000000
        specs.Factories = 5000000
        specs.Mines = 100000
        p0 = Planet(200, 500, 'Earth')
        p0.Friendlies = 1
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
        specs.Temperature = 180.0
        specs.Settlers = 3
        specs.Factories = 500
        specs.Mines = 100
        p3 = Planet(150, 3000, 'Ursa Major')
        p3.setPlanetData(specs)
        p3.Foes = 30
        p3.Friendlies = 0
        self.Star['Ursa Major'] = p3
        specs.Temperature = 320.0
        specs.Settlers = 3000
        specs.Factories = 2500
        specs.Mines = 1200
        p4 = Planet(3800, 4000, 'Canis Minor')
        p4.setPlanetData(specs)
        p4.Foes = 0
        p4.Friendlies = 0
        self.Star['Canis Minor'] = p4
        self.addItem(p0)
        self.addItem(p1)
        self.addItem(p2)
        self.addItem(p3)
        self.addItem(p4)


    def ComputeBoundingBox(self):
        """Compute the coordinates of the corners of the visible sector"""
        initialize = True
        PlanetList = self.Star.values()
        for p in PlanetList:
            if initialize:
                x_nw = p.x
                y_nw = p.y
                x_se = p.x
                y_se = p.y
                initialize = False
                continue
            if p.x < x_nw :
                x_nw = p.x
            if p.y < y_nw :
                y_nw = p.y
            if p.x > x_se :
                x_se = p.x
            if p.y > y_se :
                y_se = p.y
        self.Sector.adjust( x_nw - 200, y_nw - 200, x_se + 200, y_se + 200 )



    def SelectColorAndSize(self,value):
        """Determine the size and the color of a system on the star map"""
        if value < 0.0 :
            self.pen = StarColors.PlanetPen
            self.brush = StarColors.PlanetBrush
            self.radius = 1.0
        elif 3 * value < 1 :
            self.brush = StarColors.RedBrush
            self.pen = StarColors.RedPen
            self.radius = 0.4 + 1.8 * value
        elif 3 * value < 2 :
            self.brush = StarColors.YellowBrush
            self.pen = StarColors.YellowPen
            self.radius = 1.8 * value - 0.2
        else:
            self.brush = StarColors.GreenBrush
            self.pen = StarColors.GreenPen
            self.radius = 1.8 * value - 0.8   
        


    def renderPlanets(self, settings, species):
        """Populate the universe with the stars in the map."""
        self.addRect(self.Sector, StarColors.DarkPen)
        PlanetList = self.Star.values() 
        for p in PlanetList :
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
            name.setBrush(StarColors.PlanetBrush)
            name.setFont(StarColors.PlanetFont)
            bounds = name.boundingRect()
            name.setX( p.x - bounds.width() / 2 )
            name.setY( p.y + r + 20 )
            if settings.Mode == RenderMode.Orbiting :
                ShowFriends = ( settings.InOrbit == FleetFilter.Friend ) or ( settings.InOrbit == FleetFilter.Armed )
                ShowFoes = ( settings.InOrbit == FleetFilter.Foe ) or ( settings.InOrbit == FleetFilter.Armed )
                d = d + 30
                r = r + 15
                if ShowFriends and p.Friendlies > 0 :
                    self.addEllipse( p.x - r, p.y - r, d, d, StarColors.NeutralPen)
                    backdrop = self.addRect(0, 0, 10, 10 )
                    backdrop.setBrush(StarColors.BlueBrush)             
                    counter = self.addSimpleText(str(p.Friendlies))
                    counter.setBrush(StarColors.PlanetBrush)
                    counter.setFont(StarColors.FleetFont)
                    bounds = counter.boundingRect()
                    x0 = p.x + r + 20
                    y0 = p.y - bounds.height() / 2
                    counter.setX( x0 )
                    counter.setY( y0 )  
                    backdrop.setRect( x0 - 5, y0, bounds.width() + 10, bounds.height() )
                if ShowFoes and p.Foes > 0 :
                    self.addEllipse( p.x - r, p.y - r, d, d, StarColors.NeutralPen)
                    backdrop = self.addRect(0, 0, 0, 0 )
                    backdrop.setBrush(StarColors.RedBrush)             
                    counter = self.addSimpleText(str(p.Foes))
                    counter.setBrush(StarColors.PlanetBrush)
                    counter.setFont(StarColors.FleetFont)
                    bounds = counter.boundingRect()
                    x0 = p.x - r - 20 - bounds.width()
                    y0 = p.y - bounds.height() / 2
                    counter.setX( x0 )
                    counter.setY( y0 )  
                    backdrop.setRect( x0 - 5, y0, bounds.width() + 10, bounds.height() )
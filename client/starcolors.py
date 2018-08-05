"""This file implements a class which contains color definitions, pens & brushes used to draw the star map."""


from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor



class StarColors(object):
    """Define the container for various colors, pens & brushes."""
    
    FleetFont = QFont('Cambria', 24, 25, False)
    PlanetFont = QFont('Calibri', 32, 25, True)
    
    SpaceColor = QColor(0, 0, 0, 240)
    PlanetColor = QColor(255, 255, 255, 255)
    
    BlueBrush = QBrush(QColor(0,0,255))
    NeutralBrush = QBrush(QColor(255,255,255))
    PlanetBrush = QBrush(PlanetColor)
    RedBrush = QBrush(QColor(255,0,0))
    YellowBrush = QBrush(QColor(255,255,0))
    GreenBrush = QBrush(QColor(0,255,0))
    BluePen = QPen(QColor(0,0,255))
    NeutralPen = QPen(QColor(255,255,255))
    PlanetPen = QPen(PlanetColor)
    RedPen = QPen(QColor(255,0,0))
    YellowPen = QPen(QColor(255,255,0))
    GreenPen = QPen(QColor(0,255,0))
    DarkPen = QPen(SpaceColor)

    NeutralPen.setWidthF(3.5)
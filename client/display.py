"""This module renders the plan position indicater"""

import sys

from starmap import Starmap

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene

from PyQt5.QtGui import QFont, QPen
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPaintEvent

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QSize




class Display(QWidget):
    """This class implements the plan position indicator."""
    SpaceColor = QColor(0, 0, 0, 240)

    def __init__(self, Stars):
        super().__init__()
        self.initPPI(Stars)

    def initPPI(self, Stars):
        """Initialise the plan position indicator."""
        self.Universe = Stars
        self.Layout = QVBoxLayout(self)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.setSpacing(0)
        self.setLayout(self.Layout)
        self.setMinimumHeight(600)
        self.setMinimumWidth(600)
        self.Scene = QGraphicsScene()
        self.View = QGraphicsView(self.Scene)
        self.View.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.View.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Scene.setBackgroundBrush(self.SpaceColor)
        self.Universe.createScene(self.Scene)
        self.Layout.addWidget(self.View)
        self.setObjectName("Universe")


    def paintEvent(self, event):
        """Paint the contents of the plan position indicator"""
   #     self.PPIpainter.begin(self)
   #     self.PPIpainter.setBrush(self.SpaceColor)
   #     self.PPIpainter.drawRect(self.rect())
   #     self.PPIpainter.setFont(QFont("Arial", 30))
   #     self.PPIpainter.setPen(self.PlanetColor)
   #     self.PPIpainter.drawText(event.rect(), Qt.AlignCenter, "Map")
   #     self.PPIpainter.end()

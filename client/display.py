
import sys

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QAction

from PyQt5.QtGui import QFont, QPen
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPaintEvent

from PyQt5.QtCore import Qt


from PyQt5.QtWidgets import QLabel



class Display(QWidget):
    """This class implements the plan position indicator."""
    PlanetColor = QColor(255,255,255,255)
    SpaceColor = QColor(0, 0, 0, 240)

    def __init__(self):
        super().__init__()
        self.initPPI()

    def initPPI(self):
        """Initialise the plan position indicator."""
        self.PPIpainter = QPainter()
        self.setMinimumHeight(800)
        self.setMinimumWidth(800)
        self.layout = QVBoxLayout(self)
        self.setObjectName("Universe")


    def paintEvent(self, event):
        """Paint the contents of the plan position indicator"""
        self.PPIpainter.begin(self)
        self.PPIpainter.setBrush(self.SpaceColor)
        self.PPIpainter.drawRect(event.rect())
        self.PPIpainter.setFont(QFont("Arial", 30))
        self.PPIpainter.setPen(self.PlanetColor)
        self.PPIpainter.drawText(event.rect(), Qt.AlignCenter, "Map")
        self.PPIpainter.end()

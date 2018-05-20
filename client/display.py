
import sys

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
#from PyQt5.QtWidgets import QAction

from PyQt5.QtGui import QFont, QPen
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPaintEvent

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize




class Display(QWidget):
    """This class implements the plan position indicator."""
    PlanetColor = QColor(255,255,255,255)
    SpaceColor = QColor(0, 0, 0, 240)

    def __init__(self):
        super().__init__()
        self.initPPI()

    def initPPI(self):
        """Initialise the plan position indicator."""
        self.Layout = QVBoxLayout(self)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.setSpacing(0)
        self.setLayout(self.Layout)
        self.PPIpainter = QPainter()
        self.setMinimumHeight(600)
        self.setMinimumWidth(600)
        self.setObjectName("Universe")

    #def sizeHint(self):
    #    return QSize(self.height(),self.height())


    def paintEvent(self, event):
        """Paint the contents of the plan position indicator"""
        self.PPIpainter.begin(self)
        self.PPIpainter.setBrush(self.SpaceColor)
        self.PPIpainter.drawRect(self.rect())
        self.PPIpainter.setFont(QFont("Arial", 30))
        self.PPIpainter.setPen(self.PlanetColor)
        self.PPIpainter.drawText(event.rect(), Qt.AlignCenter, "Map")
        self.PPIpainter.end()


#    def resizeEvent(self,event):
#        """Resize the plan position indicator & keeping it square"""
#        NewWidth = self.height()
#        print( 'new height :', NewWidth  )

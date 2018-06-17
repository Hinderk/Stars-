"""This module implements the main control panel."""

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter

from PyQt5.QtCore import Qt




class ControlArea(QWidget):
    """This class implements the game control panel."""
    
    PColor = QColor(255,0,0,255)
    SColor = QColor(0, 0, 0, 120)

    def __init__(self):
        super().__init__()
        self.initControlArea()

    def initControlArea(self):
        """Initialize the game control panel."""
        self.Layout = QVBoxLayout(self)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.setSpacing(0)
        self.setLayout(self.Layout)
        self.setMinimumWidth(40)
        self.AreaPainter = QPainter()
        self.lbl1 = QLabel('Interactive Area', self)
        self.layout().addWidget(self.lbl1)
        self.setObjectName("ControlArea")



    def paintEvent(self, event):
        """Paint the contents of the plan position indicator"""
        self.AreaPainter.begin(self)
        self.AreaPainter.setBrush(self.SColor)
        self.AreaPainter.drawRect(event.rect())
        self.AreaPainter.setFont(QFont("Arial", 30))
        self.AreaPainter.setPen(self.PColor)
        self.AreaPainter.drawText(event.rect(), Qt.AlignCenter, "Controls")
        self.AreaPainter.end()
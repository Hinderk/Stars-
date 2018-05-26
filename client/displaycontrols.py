
import sys

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QToolBox
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon


from PyQt5.QtCore import Qt




class DisplayControls(QWidget):
    """This class implements the button panel used to configure PPI settings."""
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        """Initialise the control panel for the plan position indicator."""
        self.Layout = QVBoxLayout()
        self.ZoomIn = QPushButton("Zoom\nIn")
        self.ZoomOut = QPushButton("Zoom\nOut")
        self.Center = QPushButton("Center\nPPI")
        self.Layout.addWidget(self.ZoomIn)
        self.Layout.addWidget(self.ZoomOut)
        self.Layout.addWidget(self.Center)
        self.Layout.addStretch(1)
        self.Layout.setContentsMargins(5, 10, 5, 0)
        self.Layout.setSpacing(0)
        self.setMaximumWidth(70)
        self.setLayout(self.Layout)


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
        """Initialise the plan position indicator."""
        Layout = QVBoxLayout()
        ZoomIn = QPushButton("Zoom\nIn")
        ZoomOut = QPushButton("Zoom\nOut")
        Center = QPushButton("Center\nPPI")
        Layout.addWidget(ZoomIn)
        Layout.addWidget(ZoomOut)
        Layout.addWidget(Center)
        Layout.addStretch(1)
        self.setLayout(Layout)

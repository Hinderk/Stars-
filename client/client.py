
import sys

from display import Display
from displaycontrols import DisplayControls
from controlarea import ControlArea
from square import Square

from PyQt5 import QtCore

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QAction, qApp

from PyQt5.QtGui import QFont, QIcon

from PyQt5.QtWidgets import QLabel





class Client(QMainWindow):
    """This class implements the graphical 'Stars!' client."""

    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        """Initialise the graphical user interface."""
        self.resize(1600, 900)
        self.setWindowTitle('Stars!')
        self.setWindowIcon(QIcon('resources/stars.png'))
        self.center()
        self.createMenubar()
        self.Statusbar = self.statusBar()
        self.Statusbar.showMessage('Initializing the Client ...')
        self.CentralWidget = QWidget(self)
        self.CentralWidget.setObjectName('CentralWidget')
        self.Layout = QHBoxLayout(self.CentralWidget)
        self.Layout.setObjectName('MainHorizontalLayout')
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Area = ControlArea()
        self.PpI = Display()
        self.Controls = DisplayControls()
        self.Layout.addWidget(self.Area)      
        self.Layout.addWidget(self.PpI)
        self.Layout.addWidget(self.Controls)
        self.setCentralWidget(self.CentralWidget)
    #
    #    QtCore.QMetaObject.connectSlotsByName(self.CentralWidget)



    def resizeEvent(self, event):
        """Recompute spacings to keep the plan position indicator square"""
        TotalHeight = self.CentralWidget.height()
        TotalWidth = self.CentralWidget.width() - self.Controls.width() - 10
        self.Layout.setStretch(0,TotalWidth-TotalHeight)
        self.Layout.setStretch(1,TotalHeight)


    def center(self):
        """Center the client widget on the desktop."""
        ClientFrame = self.frameGeometry()
        ScreenCenter = QDesktopWidget().availableGeometry().center()
        ClientFrame.moveCenter(ScreenCenter)
        self.move(ClientFrame.topLeft())


    def createMenubar(self):
        """Create the menubar of the client"""
        loadAction = QAction(QIcon('resources/load.png'), '&Open', self)
        saveAction = QAction(QIcon('resources/save.png'), '&Save', self)
        exitAction = QAction(QIcon('resources/exit.png'), 'E&xit', self)
        loadAction.setShortcut('Ctrl+o')
        saveAction.setShortcut('Ctrl+s')
        exitAction.setShortcut('Ctrl+x')
        loadAction.setStatusTip('Open a saved game file.')
        saveAction.setStatusTip('Save the current state of the game.')
        exitAction.setStatusTip("""Terminate the 'Stars!' client.""")
        exitAction.triggered.connect(qApp.quit)
        Menubar = self.menuBar()
        FileMenu = Menubar.addMenu('File')
        FileMenu.addAction(loadAction)
        FileMenu.addAction(saveAction)
        FileMenu.addSeparator()
        FileMenu.addAction(exitAction)

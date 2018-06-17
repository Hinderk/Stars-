"""The module creates the graphical user interface for the game client"""

import sys
import resources

from speciesdata import SpeciesData
from starmap import Starmap
from display import Display
from displaycontrols import DisplayControls
from controlarea import ControlArea

from PyQt5 import QtCore

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QAction, qApp

from PyQt5.QtGui import QFont, QIcon

#from PyQt5.QtWidgets import QLabel





class Client(QMainWindow):
    """This class implements the graphical 'Stars!' client."""

    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        """Initialise the graphical user interface."""
        self.resize(1600, 900)
        self.setWindowTitle('Stars!')
        self.setWindowIcon(QIcon(':icons/stars.png'))
        self.center()
        self.createMenubar()
        self.Statusbar = self.statusBar()
        self.Statusbar.showMessage('Initializing the Client ...')
        self.CentralWidget = QWidget(self)
        self.CentralWidget.setObjectName('CentralWidget')
        self.Layout = QHBoxLayout(self.CentralWidget)
        self.Layout.setObjectName('MainHorizontalLayout')
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.setSpacing(0)
        self.Stars = Starmap()
        self.Species = SpeciesData()
        self.Area = ControlArea()
        self.PpI = Display(self.Stars, self.Species)
        self.Controls = DisplayControls()
        self.Layout.addWidget(self.Area)      
        self.Layout.addWidget(self.PpI)
        self.Layout.addWidget(self.Controls)
        self.setCentralWidget(self.CentralWidget)
        self.Controls.ZoomIn.clicked.connect(self.PpI.ZoomIn)
        self.Controls.ZoomOut.clicked.connect(self.PpI.ZoomOut)
        
    #
    #    QtCore.QMetaObject.connectSlotsByName(self.CentralWidget)



    def resizeEvent(self, event):
        """Recompute spacings to keep the plan position indicator square"""
        TotalHeight = self.CentralWidget.height()
        TotalWidth = self.CentralWidget.width() - self.Controls.width()
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
        loadAction = QAction(QIcon(':icons/load.png'), '&Open', self)
        saveAction = QAction(QIcon(':icons/save.png'), '&Save', self)
        exitAction = QAction(QIcon(':icons/exit.png'), 'E&xit', self)
        loadAction.setShortcut('Ctrl+o')
        saveAction.setShortcut('Ctrl+s')
        exitAction.setShortcut('Ctrl+x')
        loadAction.setStatusTip('Open a saved game file.')
        saveAction.setStatusTip('Save the current state of the game.')
        exitAction.setStatusTip("""Terminate the 'Stars!' client.""")
        exitAction.triggered.connect(self.exitGame)
        loadAction.triggered.connect(self.openFile)
        saveAction.triggered.connect(self.saveFile)
        Menubar = self.menuBar()
        FileMenu = Menubar.addMenu('File')
        FileMenu.addAction(loadAction)
        FileMenu.addAction(saveAction)
        FileMenu.addSeparator()
        FileMenu.addAction(exitAction)


    def exitGame(self,event):
        """Terminate the game client"""
        qApp.quit()


    def saveFile(self,event):
        """Save the current state of the game in a file"""
        fileFilter='Game Files (*.trn);;All Files (*.*)'
        gameFile, _ = QFileDialog.getSaveFileName(self, 'Save Game', '', fileFilter)
        print(gameFile)




    def openFile(self, event):
        """Load a new state for the game from a file"""
        fileFilter='Game Files (*.trn);;All Files (*.*)'
        newGame, _ = QFileDialog.getOpenFileName(self, 'Open Saved Game', '', fileFilter)
        print(newGame)

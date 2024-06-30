
from PyQt6 import QtWidgets, QtGui, QtCore
from fonts import LoadFonts

import stars_rc
#import os



class Gui(QtWidgets.QMainWindow):
    
    def __init__(self, design):
        
        super(Gui, self).__init__()
        self.SetupUI(design)


    def DefineZoomLevel( self, Menu, Level ) :
     
        for NewLevel in Level :
            NewAction = Menu.addAction( NewLevel + '%' )
            NewAction.setCheckable( True )
            self.Action['Zoom' + NewLevel] = NewAction
            

    def SetupUI(self, design):

        LoadFonts("Design/Fonts")
        FontDB = QtGui.QFontDatabase()

        styles = FontDB.styles("Playfair Display")
        print(styles)
        MenuFont = FontDB.font("Playfair Display", "Medium", design.MenuFontSize)
        MenuFont.setPointSize(design.MenuFontSize)

        self.setObjectName('Stars')
        self.setWindowTitle('Stars!')
   #     self.resize(1920, 1080)
        # Policy = QtWidgets.QSizePolicy()
        # self.setSizePolicy( Policy )
        Icon = QtGui.QIcon(':/Icons/Stars')
        self.setWindowIcon(Icon)
        self.CentralWidget=QtWidgets.QWidget(self)
        self.CentralWidget.setEnabled(True)
        GridLayout = QtWidgets.QGridLayout(self.CentralWidget)
        self.Inspector=QtWidgets.QGraphicsView(self.CentralWidget)
        self.Inspector.setMinimumHeight(200)
        GridLayout.addWidget(self.Inspector, 1, 1)

        MessageLayout = QtWidgets.QGridLayout(self.CentralWidget)
        MessageLabel = QtWidgets.QLabel(self.CentralWidget)
        MessageLabel.setText("This is a message!")
        MessageLayout.addWidget(MessageLabel, 0, 0)
  
  
        CurrentMessage = QtWidgets.QTextEdit(self.CentralWidget)
        CurrentMessage.insertPlainText("This is a very simple message that requires Your attention!")
        
        scrollArea = QtWidgets.QScrollArea(self.CentralWidget)
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        scrollArea.setWidget(CurrentMessage)
        MessageLayout.addWidget(scrollArea, 1, 0)

        GridLayout.addLayout(MessageLayout, 1, 0)

        self.Universe = QtWidgets.QGraphicsView(self.CentralWidget)
        self.Universe.setMinimumSize(1440, 1080)
        GridLayout.addWidget(self.Universe, 0, 1)


        self.setCentralWidget(self.CentralWidget)

        self.MenuBar = QtWidgets.QMenuBar(self)
        self.MenuBar.setFont(MenuFont)
        self.MenuFile = QtWidgets.QMenu(self.MenuBar)
        self.MenuView = QtWidgets.QMenu(self.MenuBar)
        self.MenuLayout=QtWidgets.QMenu(self.MenuView)
        self.MenuZoom=QtWidgets.QMenu(self.MenuView)
        self.MenuTurn=QtWidgets.QMenu(self.MenuBar)
        self.MenuCommands=QtWidgets.QMenu(self.MenuBar)
        self.MenuReport=QtWidgets.QMenu(self.MenuBar)
        self.MenuHelp=QtWidgets.QMenu(self.MenuBar)
        self.MenuExport=QtWidgets.QMenu(self.MenuBar)
        self.setMenuBar(self.MenuBar)
        self.MenuBar.addAction(self.MenuFile.menuAction())
        self.MenuBar.addAction(self.MenuView.menuAction())
        self.MenuBar.addAction(self.MenuTurn.menuAction())
        self.MenuBar.addAction(self.MenuCommands.menuAction())
        self.MenuBar.addAction(self.MenuReport.menuAction())
        self.MenuBar.addAction(self.MenuHelp.menuAction())
        self.MenuFile.setTitle('File')
        self.MenuView.setTitle('View')
        self.MenuLayout.setTitle('Layout')
        self.MenuZoom.setTitle('Zoom')
        self.MenuTurn.setTitle('Turn')
        self.MenuCommands.setTitle('Commands')
        self.MenuReport.setTitle('Report')
        self.MenuHelp.setTitle('Help')
        self.MenuExport.setTitle('Save a report')

        self.PlanetInfo=QtWidgets.QToolBar(self)
        self.PlanetInfo.setFloatable(True)
        self.PlanetInfo.setWindowTitle('Planetary Data')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.PlanetInfo)
        self.SpaceInfo=QtWidgets.QToolBar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.SpaceInfo)
        self.SpaceInfo.setWindowTitle('Minefields & Fleets')

        self.Action=dict()

        NewAction=QtWidgets.QAction(self)
        Icon = QtGui.QIcon(':/Menu/NewGame')
        NewAction.setIcon(Icon)
        NewAction.setText('New')
        NewAction.setToolTip('Create an new game')
        NewAction.setShortcut('Ctrl+N')
        self.MenuFile.addAction(NewAction)
        self.Action['New Game']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Open')
        Icon=QtGui.QIcon(':/Menu/OpenGame')
        NewAction.setIcon(Icon)
        NewAction.setToolTip('Open a saved game')
        NewAction.setShortcut('Ctrl+O')
        self.MenuFile.addAction(NewAction)
        self.Action['Open Game']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Close')
        NewAction.setToolTip('Close the current game')
        self.MenuFile.addAction(NewAction)
        self.Action['Close Game']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Save')
        Icon=QtGui.QIcon(':/Menu/SaveGame')
        NewAction.setIcon(Icon)
        NewAction.setToolTip('Save the current game')
        NewAction.setShortcut('Ctrl+S')
        self.MenuFile.addAction(NewAction)
        self.Action['Save Game']=NewAction
        self.MenuFile.addSeparator()

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Exit')
        NewAction.setToolTip('Exit the game')
        NewAction.setShortcut('Ctrl+X')
        self.MenuFile.addAction(NewAction)
        self.Action['Exit Game']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Toolbar')
        NewAction.setToolTip('Show the toolbar')
        NewAction.setCheckable(True)
        NewAction.setChecked(True)
        self.MenuView.addAction(NewAction)
        self.Action['Toolbar']=NewAction
        self.MenuView.addSeparator()

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Find')
        NewAction.setShortcut('Ctrl+F')
        NewAction.setToolTip('Find planet or fleet by name or number')
        self.MenuView.addAction(NewAction)
        self.Action['Find']=NewAction

        self.MenuView.addAction(self.MenuZoom.menuAction())
        self.MenuView.addAction(self.MenuLayout.menuAction())
        Level=['25', '38', '50', '75', '100', '125', '150', '200', '400']
        self.DefineZoomLevel(self.MenuZoom, Level)
        self.Action['Zoom100'].setChecked(True)

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Player Colours')
        NewAction.setToolTip('Display player colours')
        NewAction.setCheckable(True)
        NewAction.setChecked(True)
        self.MenuView.addAction(NewAction)
        self.Action['Traits']=NewAction
        self.MenuView.addSeparator()

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Traits')
        NewAction.setToolTip('Display the perks of the civilisation')
        NewAction.setShortcut('F8')
        self.MenuView.addAction(NewAction)
        self.Action['Traits']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Parameters')
        NewAction.setToolTip('Display the setup parameters of the game')
        self.MenuView.addAction(NewAction)
        self.Action['Parameters']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Generate')
        NewAction.setToolTip('Compute a new turn for the game')
        NewAction.setShortcut('F9')
        self.MenuTurn.addAction(NewAction)
        self.Action['Generate']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Ship Design')
        NewAction.setToolTip('Manage the ship designs')
        NewAction.setShortcut('F4')
        self.MenuCommands.addAction(NewAction)
        self.Action['Design']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Research')
        NewAction.setToolTip('Allocate spending on research')
        NewAction.setShortcut('F5')
        self.MenuCommands.addAction(NewAction)
        self.Action['Research']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Battle Plans')
        NewAction.setToolTip('Modifiy the programming of the battle computers')
        NewAction.setShortcut('F6')
        self.MenuCommands.addAction(NewAction)
        self.Action['Battle Plan']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Player Relations')
        NewAction.setToolTip('Declare war or negotiate peace')
        NewAction.setShortcut('F7')
        NewAction.setDisabled(True)
        self.MenuCommands.addAction(NewAction)
        self.Action['Diplomacy']=NewAction
        self.MenuCommands.addSeparator()

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Manage Keys')
        NewAction.setToolTip('Protect the game data')
        self.MenuCommands.addAction(NewAction)
        self.Action['Security']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Planets ...')
        NewAction.setToolTip('Review planetary data')
        NewAction.setShortcut('F3')
        self.MenuReport.addAction(NewAction)
        self.Action['Planets']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Fleets ...')
        NewAction.setToolTip('Review fleet movements')
        NewAction.setShortcut('F3')
        self.MenuReport.addAction(NewAction)
        self.Action['Fleets']=NewAction

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Others\' Fleets ...')
        NewAction.setToolTip('Review fleet intelligence')
        NewAction.setShortcut('F3')
        self.MenuReport.addAction(NewAction)
        self.Action['Enemies']=NewAction
        self.MenuReport.addSeparator()

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Battles ...')
        NewAction.setToolTip('Review battle outcomes')
        NewAction.setShortcut('F1')
        self.MenuReport.addAction(NewAction)
        self.Action['Battles']=NewAction
        self.MenuReport.addSeparator()

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('Score')
        NewAction.setToolTip('Review the current game score')
        NewAction.setShortcut('F10')
        self.MenuReport.addAction(NewAction)
        self.Action['Score']=NewAction
        self.MenuReport.addSeparator()

        self.MenuReport.addAction(self.MenuExport.menuAction())

        NewAction=QtWidgets.QAction(self)
        Icon=QtGui.QIcon(':/Menu/Science')
        NewAction.setIcon(Icon)
        NewAction.setText('Technology Browser')
        NewAction.setToolTip('Review research options')
        NewAction.setShortcut('F2')
        self.MenuHelp.addAction(NewAction)
        self.Action['Science']=NewAction
        self.MenuHelp.addSeparator()

        NewAction=QtWidgets.QAction(self)
        NewAction.setText('About')
        NewAction.setToolTip('About this clone of Stars!')
        self.MenuHelp.addAction(NewAction)
        self.Action['About']=NewAction

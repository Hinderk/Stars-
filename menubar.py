
from PyQt6 import QtWidgets, QtGui, QtCore



class Menu(QtWidgets.QMenuBar):
    
    def __init__(self, form):

        super(self.__class__, self).__init__(form)
        self.actionZoom = dict()

        MenuFile = QtWidgets.QMenu(self)
        MenuView = QtWidgets.QMenu(self)
        MenuToolbar = QtWidgets.QMenu(MenuView)
        MenuLayout = QtWidgets.QMenu(MenuView)
        MenuZoom = QtWidgets.QMenu(MenuView)
        MenuTurn = QtWidgets.QMenu(self)
        MenuCommands = QtWidgets.QMenu(self)
        MenuReport = QtWidgets.QMenu(self)
        MenuDumpTextFile = QtWidgets.QMenu(MenuReport)
        MenuHelp = QtWidgets.QMenu(self)

        self.actionNewGame = QtGui.QAction(self)
        self.actionNewGame.setText("New")
        self.actionNewGame.setStatusTip("Start a new game ...")
        self.actionNewGame.setShortcut("Ctrl+N")
        self.actionNewGame.setAutoRepeat(False)

        self.actionOpenGame = QtGui.QAction(self)
        self.actionOpenGame.setAutoRepeat(False)
        self.actionOpenGame.setText("Open")
        self.actionOpenGame.setStatusTip("Open a set of game files ...")
        self.actionOpenGame.setShortcut("Ctrl+O")

        self.actionCloseGame = QtGui.QAction(self)
        self.actionCloseGame.setText("Close")
        self.actionCloseGame.setStatusTip("Close the current game ...")
        self.actionCloseGame.setAutoRepeat(False)

        self.actionSaveGame = QtGui.QAction(self)
        self.actionSaveGame.setText("Save")
        self.actionSaveGame.setStatusTip("Save the current turn to a set of game files ...")
        self.actionSaveGame.setShortcut("Ctrl+S")
        self.actionSaveGame.setAutoRepeat(False)

        self.actionExportMap = QtGui.QAction(self)
        self.actionExportMap.setText("Export Map")
        self.actionExportMap.setStatusTip("Print the current star map to a file ...")
        self.actionExportMap.setAutoRepeat(False)

        self.actionSaveGameAs = QtGui.QAction(self)
        self.actionSaveGameAs.setText("Save Game as ...")
        self.actionSaveGameAs.setStatusTip("Save the current game under a new name ...")
        self.actionSaveGameAs.setAutoRepeat(False)

        self.actionExit = QtGui.QAction(self)
        self.actionExit.setText("Exit")
        self.actionExit.setToolTip("Exit the current game ...")
        self.actionExit.setStatusTip("Leave the current turn behind & close the game client ...")
        self.actionExit.setShortcut("Ctrl+X")
        self.actionExit.setAutoRepeat(False)

        self.actionGameParameters = QtGui.QAction(self)
        self.actionGameParameters.setText("Game Parameters ...")
        self.actionGameParameters.setAutoRepeat(False)

        self.actionGenerate = QtGui.QAction(self)
        self.actionGenerate.setText("Generate")
        self.actionGenerate.setToolTip("Generate a new turn ...")
        self.actionGenerate.setStatusTip("Generate a new turn ...")
        self.actionGenerate.setShortcut("F9")
        self.actionGenerate.setAutoRepeat(False)

        self.actionToolbarOn = QtGui.QAction(self)
        self.actionToolbarOn.setText("On")
        self.actionToolbarOn.setToolTip("Show the toolbar ...")
        self.actionToolbarOn.setStatusTip("Show the toolbar ...")
        self.actionToolbarOn.setCheckable(True)
        self.actionToolbarOn.setChecked(True)

        self.actionToolbarOff = QtGui.QAction(self)
        self.actionToolbarOff.setText("Off")
        self.actionToolbarOff.setToolTip("Hide the toolbar ...")
        self.actionToolbarOff.setStatusTip("Hide the toolbar ...")
        self.actionToolbarOff.setCheckable(True)

        MenuToolbar.setTitle("Toolbar")
        MenuToolbar.setStatusTip("Modify the tool bar of the game ...")
        MenuToolbar.setStyleSheet("QMenu::item{padding: 5px 20px 5px 0px}")

        MenuToolbar.addAction(self.actionToolbarOn)
        MenuToolbar.addAction(self.actionToolbarOff)

        self.actionDefault=QtGui.QAction(self)
        self.actionDefault.setText("Default")
        self.actionDefault.setCheckable(True)
        self.actionDefault.setChecked(True)

        self.actionRace=QtGui.QAction(self)
        self.actionRace.setText("Race ...")
        self.actionRace.setShortcut("F8")
        self.actionRace.setAutoRepeat(False)

        self.actionSaveSubmit=QtGui.QAction(self)
        self.actionSaveSubmit.setText("Save and Submit")
        self.actionSaveSubmit.setStatusTip("Save Game & submit Your turn ...")
        self.actionSaveSubmit.setShortcut("Ctrl+A")
        self.actionSaveSubmit.setAutoRepeat(False)

        self.actionShipDesign=QtGui.QAction(self)
        self.actionShipDesign.setText("Ship Design ...")
        self.actionShipDesign.setShortcut("F4")

        self.actionBattlePlans=QtGui.QAction(self)
        self.actionBattlePlans.setText("Battle Plans ...")
        self.actionBattlePlans.setShortcut("F6")

        self.actionPlayerRelations=QtGui.QAction(self)
        self.actionPlayerRelations.setText("Player Relations ...")
        self.actionPlayerRelations.setShortcut("F7")
        self.actionPlayerRelations.setIconVisibleInMenu(False)

        self.actionResearch=QtGui.QAction(self)
        self.actionResearch.setText("Research ...")
        self.actionResearch.setShortcut("F5")

        self.actionChangePassword=QtGui.QAction(self)
        self.actionChangePassword.setText("Change Password ...")

        self.actionPlanets=QtGui.QAction(self)
        self.actionPlanets.setShortcut("F3")
        self.actionPlanets.setAutoRepeat(False)
        self.actionPlanets.setIconVisibleInMenu(False)
        self.actionPlanets.setText("Planets ...")

        self.actionFleets=QtGui.QAction(self)
        self.actionFleets.setAutoRepeat(False)
        self.actionFleets.setIconVisibleInMenu(False)
        self.actionFleets.setText("Fleets ...")
        self.actionFleets.setShortcut("F3")

        self.actionOtherFleets=QtGui.QAction(self)
        self.actionOtherFleets.setShortcut("F3")
        self.actionOtherFleets.setAutoRepeat(False)
        self.actionOtherFleets.setIconVisibleInMenu(False)
        self.actionOtherFleets.setText("Others\' Fleets ...")

        self.actionBattles=QtGui.QAction(self)
        self.actionBattles.setShortcut("F3")
        self.actionBattles.setAutoRepeat(False)
        self.actionBattles.setIconVisibleInMenu(False)
        self.actionBattles.setText("Battles ...")

        self.actionScore=QtGui.QAction(self)
        self.actionScore.setShortcut("F10")
        self.actionScore.setAutoRepeat(False)
        self.actionScore.setIconVisibleInMenu(False)
        self.actionScore.setText("Score ...")

        self.actionUniverseDefinition=QtGui.QAction(self)
        self.actionUniverseDefinition.setText("Universe Defintion")

        self.actionPlanetInformation=QtGui.QAction(self)
        self.actionPlanetInformation.setText("Planet Information")

        self.actionFleetInformation = QtGui.QAction(self)
        self.actionFleetInformation.setText("Fleet Information")

        MenuFile.addAction(self.actionNewGame)
        MenuFile.addAction(self.actionOpenGame)
        MenuFile.addAction(self.actionCloseGame)
        MenuFile.addAction(self.actionSaveGameAs)
        MenuFile.addAction(self.actionSaveGame)
        MenuFile.addAction(self.actionSaveSubmit)
        MenuFile.addSeparator()
        MenuFile.addAction(self.actionExportMap)
        MenuFile.addSeparator()
        MenuFile.addAction(self.actionExit)
        MenuFile.setTitle("File")
        self.DefineZoomLevel(MenuZoom, ['25%', '50%', '75%', '100%', '125%', '150%', '200%', '400%'])
        self.actionZoom['100%'].setChecked(True)
        MenuZoom.setStyleSheet("QMenu::item { padding: 5px 30px 5px 0px }")
        MenuZoom.setTitle("Zoom")
        MenuLayout.addAction(self.actionDefault)
        MenuLayout.setTitle("Layout")
        MenuLayout.setStyleSheet("QMenu::item { padding: 5px 30px 5px 0px }")
        MenuView.addAction(MenuToolbar.menuAction())
        MenuView.addAction(MenuZoom.menuAction())
        MenuView.addAction(MenuLayout.menuAction())
        MenuView.addSeparator()
        MenuView.addAction(self.actionRace)
        MenuView.addAction(self.actionGameParameters)
        MenuView.setTitle("View")
        MenuTurn.addAction(self.actionGenerate)
        MenuTurn.setTitle("Turn")
        MenuCommands.addAction(self.actionShipDesign)
        MenuCommands.addAction(self.actionResearch)
        MenuCommands.addAction(self.actionBattlePlans)
        MenuCommands.addAction(self.actionPlayerRelations)
        MenuCommands.addSeparator()
        MenuCommands.addAction(self.actionChangePassword)
        MenuCommands.setTitle("Commands")
        MenuDumpTextFile.addAction(self.actionUniverseDefinition)
        MenuDumpTextFile.addAction(self.actionPlanetInformation)
        MenuDumpTextFile.addAction(self.actionFleetInformation)
        MenuDumpTextFile.setTitle("Dump to Text File")
        MenuReport.addAction(self.actionPlanets)
        MenuReport.addAction(self.actionFleets)
        MenuReport.addAction(self.actionOtherFleets)
        MenuReport.addAction(self.actionBattles)
        MenuReport.addSeparator()
        MenuReport.addAction(self.actionScore)
        MenuReport.addSeparator()
        MenuReport.addAction(MenuDumpTextFile.menuAction())
        MenuReport.setTitle("Report")
        MenuHelp.setTitle("Help")

        self.addAction(MenuFile.menuAction())
        self.addAction(MenuView.menuAction())
        self.addAction(MenuTurn.menuAction())
        self.addAction(MenuCommands.menuAction())
        self.addAction(MenuReport.menuAction())
        self.addAction(MenuHelp.menuAction())

    def DefineZoomLevel(self, Menu, LevelSet):

        for Level in LevelSet:
            NewAction = Menu.addAction(Level)
            NewAction.setCheckable( True )
            NewAction.setText(Level)
            NewAction.setToolTip('Set magnification level to: ' + Level)
            NewAction.setStatusTip('Set magnification level to: ' + Level)
            self.actionZoom[Level] = NewAction

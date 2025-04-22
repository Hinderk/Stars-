
from PyQt6.QtWidgets import QMenu
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QActionGroup
from PyQt6.QtCore import pyqtSignal as QSignal



class Menu(QMenuBar):

    ChangeZoom = QSignal(bool, int)


    def __init__(self, form):

        super(self.__class__, self).__init__(form)

        MenuFile = QMenu(self)
        MenuView = QMenu(self)
        MenuToolbar = QMenu(MenuView)
        MenuLayout = QMenu(MenuView)
        self.MenuZoom = QMenu(MenuView)
        MenuTurn = QMenu(self)
        MenuCommands = QMenu(self)
        MenuReport = QMenu(self)
        MenuDumpTextFile = QMenu(MenuReport)
        MenuHelp = QMenu(self)

        self.actionNewGame = QAction(self)
        self.actionNewGame.setText("New")
        self.actionNewGame.setStatusTip("Start a new game ...")
        self.actionNewGame.setShortcut("Ctrl+N")
        self.actionNewGame.setAutoRepeat(False)

        self.actionWizard = QAction(self)
        self.actionWizard.setAutoRepeat(False)
        self.actionWizard.setText("Custom Faction Wizard ...")
        self.actionWizard.setStatusTip("Launch the custom faction wizard ...")

        self.actionOpenGame = QAction(self)
        self.actionOpenGame.setAutoRepeat(False)
        self.actionOpenGame.setText("Open")
        self.actionOpenGame.setStatusTip("Open a set of game files ...")
        self.actionOpenGame.setShortcut("Ctrl+O")

        self.actionCloseGame = QAction(self)
        self.actionCloseGame.setText("Close")
        self.actionCloseGame.setStatusTip("Close the current game ...")
        self.actionCloseGame.setAutoRepeat(False)

        self.actionSaveGame = QAction(self)
        self.actionSaveGame.setText("Save")
        self.actionSaveGame.setStatusTip("Save the current turn to a set of game files ...")
        self.actionSaveGame.setShortcut("Ctrl+S")
        self.actionSaveGame.setAutoRepeat(False)

        self.actionExportMap = QAction(self)
        self.actionExportMap.setText("Export Map")
        self.actionExportMap.setStatusTip("Print the current star map to a file ...")
        self.actionExportMap.setAutoRepeat(False)

        self.actionSaveGameAs = QAction(self)
        self.actionSaveGameAs.setText("Save Game as ...")
        self.actionSaveGameAs.setStatusTip("Save the current game under a new name ...")
        self.actionSaveGameAs.setAutoRepeat(False)

        self.actionExit = QAction(self)
        self.actionExit.setText("Exit")
        self.actionExit.setToolTip("Exit the current game ...")
        self.actionExit.setStatusTip("Leave the current turn behind & close the game client ...")
        self.actionExit.setShortcut("Ctrl+X")
        self.actionExit.setAutoRepeat(False)

        self.actionGameParameters = QAction(self)
        self.actionGameParameters.setText("Game Parameters ...")
        self.actionGameParameters.setAutoRepeat(False)

        self.actionGenerate = QAction(self)
        self.actionGenerate.setText("Generate")
        self.actionGenerate.setToolTip("Generate a new turn ...")
        self.actionGenerate.setStatusTip("Generate a new turn ...")
        self.actionGenerate.setShortcut("F9")
        self.actionGenerate.setAutoRepeat(False)

        self.actionToolbarOn = QAction(self)
        self.actionToolbarOn.setText("On")
        self.actionToolbarOn.setToolTip("Show the toolbar ...")
        self.actionToolbarOn.setStatusTip("Show the toolbar ...")
        self.actionToolbarOn.setCheckable(True)
        self.actionToolbarOn.setChecked(True)

        self.actionToolbarOff = QAction(self)
        self.actionToolbarOff.setText("Off")
        self.actionToolbarOff.setToolTip("Hide the toolbar ...")
        self.actionToolbarOff.setStatusTip("Hide the toolbar ...")
        self.actionToolbarOff.setCheckable(True)

        MenuToolbar.setTitle("Toolbar")
        MenuToolbar.setStatusTip("Modify the tool bar of the game ...")
        MenuToolbar.setStyleSheet("QMenu::item{padding: 5px 20px 5px 0px}")

        MenuToolbar.addAction(self.actionToolbarOn)
        MenuToolbar.addAction(self.actionToolbarOff)
        ToolbarActions = QActionGroup(self)
        ToolbarActions.addAction(self.actionToolbarOn)
        ToolbarActions.addAction(self.actionToolbarOff)

        self.actionDefault = QAction(self)
        self.actionDefault.setText("Default")
        self.actionDefault.setCheckable(True)
        self.actionDefault.setChecked(True)

        self.actionFaction = QAction(self)
        self.actionFaction.setText("Faction ...")
        self.actionFaction.setShortcut("F8")
        self.actionFaction.setAutoRepeat(False)

        self.actionSaveSubmit = QAction(self)
        self.actionSaveSubmit.setText("Save and Submit")
        self.actionSaveSubmit.setStatusTip("Save Game & submit Your turn ...")
        self.actionSaveSubmit.setShortcut("Ctrl+A")
        self.actionSaveSubmit.setAutoRepeat(False)

        self.actionShipDesign = QAction(self)
        self.actionShipDesign.setText("Ship Design ...")
        self.actionShipDesign.setShortcut("F4")

        self.actionBattlePlans = QAction(self)
        self.actionBattlePlans.setText("Battle Plans ...")
        self.actionBattlePlans.setShortcut("F6")

        self.actionPlayerRelations = QAction(self)
        self.actionPlayerRelations.setText("Player Relations ...")
        self.actionPlayerRelations.setShortcut("F7")
        self.actionPlayerRelations.setIconVisibleInMenu(False)

        self.actionResearch = QAction(self)
        self.actionResearch.setText("Research ...")
        self.actionResearch.setShortcut("F5")

        self.actionChangePassword = QAction(self)
        self.actionChangePassword.setText("Change Password ...")

        self.actionPlanets = QAction(self)
        self.actionPlanets.setShortcut("F3")
        self.actionPlanets.setAutoRepeat(False)
        self.actionPlanets.setIconVisibleInMenu(False)
        self.actionPlanets.setText("Planets ...")

        self.actionFleets = QAction(self)
        self.actionFleets.setAutoRepeat(False)
        self.actionFleets.setIconVisibleInMenu(False)
        self.actionFleets.setText("Fleets ...")
        self.actionFleets.setShortcut("F3")

        self.actionOtherFleets = QAction(self)
        self.actionOtherFleets.setShortcut("F3")
        self.actionOtherFleets.setAutoRepeat(False)
        self.actionOtherFleets.setIconVisibleInMenu(False)
        self.actionOtherFleets.setText("Others\' Fleets ...")

        self.actionBattles = QAction(self)
        self.actionBattles.setShortcut("F3")
        self.actionBattles.setAutoRepeat(False)
        self.actionBattles.setIconVisibleInMenu(False)
        self.actionBattles.setText("Battles ...")

        self.actionScore = QAction(self)
        self.actionScore.setShortcut("F10")
        self.actionScore.setAutoRepeat(False)
        self.actionScore.setIconVisibleInMenu(False)
        self.actionScore.setText("Score ...")

        MenuDumpTextFile.setTitle("Dump to Text File")
        self.actionPlanetInformation = QAction(self)
        self.actionPlanetInformation.setText("Planet Information")
        MenuDumpTextFile.addAction(self.actionPlanetInformation)
        self.actionFleetInformation = QAction(self)
        self.actionFleetInformation.setText("Fleet Information")
        MenuDumpTextFile.addAction(self.actionFleetInformation)
        self.actionUniverseDefinition = QAction(self)
        self.actionUniverseDefinition.setText("Universe Definition")
        MenuDumpTextFile.addAction(self.actionUniverseDefinition)

        MenuFile.addAction(self.actionNewGame)
        MenuFile.addAction(self.actionWizard)
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
        self.DefineZoomLevel(self.MenuZoom, [25, 50, 75, 100, 125, 150, 200, 400])
        self.MenuZoom.setStyleSheet("QMenu::item { padding: 5px 30px 5px 0px }")
        self.MenuZoom.setTitle("Zoom")
        MenuLayout.addAction(self.actionDefault)
        MenuLayout.setTitle("Layout")
        MenuLayout.setStyleSheet("QMenu::item { padding: 5px 30px 5px 0px }")
        MenuView.addAction(MenuToolbar.menuAction())
        MenuView.addAction(self.MenuZoom.menuAction())
        MenuView.addAction(MenuLayout.menuAction())
        MenuView.addSeparator()
        MenuView.addAction(self.actionFaction)
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

        class ZoomAction(QAction):

            def __init__(self, level):
                super(self.__class__, self).__init__()
                self.ZoomLevel = level

        zoomActions = QActionGroup(Menu)
        for level in LevelSet:
            NewAction = ZoomAction(level)
            Menu.addAction(NewAction)
            NewAction.setCheckable( True )
            label = str(level) + '%'
            NewAction.setText(label)
            NewAction.setToolTip('Set magnification level: ' + label)
            NewAction.setStatusTip('Set magnification level: ' + label)
            zoomActions.addAction(NewAction)
            NewAction.setChecked(level == 100)
            NewAction.toggled.connect(self.ResizeStarmap)


    def ResizeStarmap(self, event):
        self.ChangeZoom.emit(event, self.sender().ZoomLevel)

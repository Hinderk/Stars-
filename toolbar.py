
from PyQt6.QtWidgets import QMenu, QToolButton
from PyQt6.QtWidgets import QToolBar, QSpinBox
from PyQt6.QtGui import QActionGroup
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
from PyQt6.QtCore import pyqtSignal as QSignal

from defines import Stance, ShipClass


Instant = QToolButton.ToolButtonPopupMode.InstantPopup
Delayed = QToolButton.ToolButtonPopupMode.DelayedPopup



class ToolBar(QToolBar):

    ShowMines = QSignal(bool, Stance)
    FilterMyFleets = QSignal(bool, dict)
    FilterEnemyFleets = QSignal(bool, dict)


    def __init__(self):

        super(self.__class__, self).__init__()

        self.DesignNames = []
        self.MyDesigns = dict()
        self.AlienDesigns = dict()
        for sc in ShipClass:
            self.AlienDesigns[sc.name] = True
        self.MineFilter = dict()
        self.MineFilter[Stance.allied] = True
        self.MineFilter[Stance.friendly] = True
        self.MineFilter[Stance.neutral] = True
        self.MineFilter[Stance.hostile] = True

        Icon = QIcon(":/Toolbar/Mine")
        self.Mines = QToolButton(self)
        self.Mines.setIcon(Icon)
        self.Mines.setCheckable(True)
        self.Mines.setAutoRepeat(False)
        self.Mines.setToolTip('Show mine fields ...')
        self.Mines.setStatusTip('Show mine fields ...')
        self.DefineMineMenu(self.Mines)

        Icon = QIcon(":/Toolbar/Default")
        self.actionDefaultView = QAction(self)
        self.actionDefaultView.setCheckable(True)
        self.actionDefaultView.setIcon(Icon)
        self.actionDefaultView.setAutoRepeat(False)
        self.actionDefaultView.setToolTip("Normal View")
        self.actionDefaultView.setStatusTip("Normal View")

        Icon = QIcon(":/Toolbar/Percent")
        self.actionPercentView = QAction(self)
        self.actionPercentView.setCheckable(True)
        self.actionPercentView.setIcon(Icon)
        self.actionPercentView.setAutoRepeat(False)
        self.actionPercentView.setToolTip("Planet Value View")
        self.actionPercentView.setStatusTip("Planet Value View")

        Icon = QIcon(":/Toolbar/People")
        self.actionPopulationView = QAction(self)
        self.actionPopulationView.setCheckable(True)
        self.actionPopulationView.setIcon(Icon)
        self.actionPopulationView.setAutoRepeat(False)
        self.actionPopulationView.setToolTip("Population View")
        self.actionPopulationView.setStatusTip("Population View")

        Icon = QIcon(":/Toolbar/Surface")
        self.actionSurfaceMineralView = QAction(self)
        self.actionSurfaceMineralView.setCheckable(True)
        self.actionSurfaceMineralView.setIcon(Icon)
        self.actionSurfaceMineralView.setAutoRepeat(False)
        self.actionSurfaceMineralView.setToolTip("Surface Mineral View")
        self.actionSurfaceMineralView.setStatusTip("Surface Mineral View")

        Icon = QIcon(":/Toolbar/Minerals")
        self.actionConcentrationView = QAction(self)
        self.actionConcentrationView.setCheckable(True)
        self.actionConcentrationView.setIcon(Icon)
        self.actionConcentrationView.setAutoRepeat(False)
        self.actionConcentrationView.setToolTip("Mineral Concentration View")
        self.actionConcentrationView.setStatusTip("Mineral Concentration View")

        Icon = QIcon(":/Toolbar/Cancel")
        self.actionNoInfoView = QAction(self)
        self.actionNoInfoView.setCheckable(True)
        self.actionNoInfoView.setIcon(Icon)
        self.actionNoInfoView.setAutoRepeat(False)
        self.actionNoInfoView.setToolTip("No Player Info View")
        self.actionNoInfoView.setStatusTip("Remove information about players ...")

        Icon = QIcon(":/Toolbar/Waypoint")
        self.actionAddWaypoint = QAction(self)
        self.actionAddWaypoint.setCheckable(True)
        self.actionAddWaypoint.setIcon(Icon)
        self.actionAddWaypoint.setAutoRepeat(False)
        self.actionAddWaypoint.setStatusTip("Add way points to the flight path ...")
        self.actionAddWaypoint.setToolTip("Add way points ...")

        Icon = QIcon(":/Toolbar/Waiting")
        self.actionWaitingFleets = QAction(self)
        self.actionWaitingFleets.setCheckable(True)
        self.actionWaitingFleets.setIcon(Icon)
        self.actionWaitingFleets.setAutoRepeat(False)
        self.actionWaitingFleets.setToolTip("Show idle fleets only ...")
        self.actionWaitingFleets.setStatusTip("Show fleets without any task to complete ...")

        Icon = QIcon(":/Toolbar/Orbiting")
        self.actionShipCount = QAction(self)
        self.actionShipCount.setCheckable(True)
        self.actionShipCount.setIcon(Icon)
        self.actionShipCount.setAutoRepeat(False)
        self.actionShipCount.setToolTip("Show fleet strengths ...")
        self.actionShipCount.setStatusTip("Show the strength of all fleets within scanner range ...")

        Icon = QIcon(":/Toolbar/Friendlies")
        self.actionFriendlies = QToolButton(self)
        self.actionFriendlies.setCheckable(False)
        self.actionFriendlies.setPopupMode(Instant)
        self.actionFriendlies.setIcon(Icon)
        self.actionFriendlies.setToolTip("Show friendly fleets ...")
        self.actionFriendlies.setStatusTip("Show only friendly fleets on the star map ...")
        self.actionFriendlies.setAutoRepeat(False)
        self.DefineMyDesignMenu(self.actionFriendlies)

        Icon = QIcon(":/Toolbar/Foes")
        self.actionFoes = QToolButton(self)
        self.actionFoes.setCheckable(False)
        self.actionFoes.setPopupMode(Instant)
        self.actionFoes.setIcon(Icon)
        self.actionFoes.setToolTip("Show enemy fleets ...")
        self.actionFoes.setStatusTip("Show only enemy fleets on the star map ...")
        self.actionFoes.setAutoRepeat(False)
        self.DefineEnemyDesignMenu(self.actionFoes)

        Icon = QIcon(":/Toolbar/Zoomlevel")
        self.Zoom = QToolButton(self)
        self.Zoom.setPopupMode(Instant)
        self.Zoom.setIcon(Icon)
        self.Zoom.setAutoRepeat(False)
        self.Zoom.setToolTip("Define the level of magnification ...")
        self.Zoom.setStatusTip("Define the level of magnification ...")

        Icon = QIcon(":/Toolbar/Paths")
        self.actionPathOverlay = QAction(self)
        self.actionPathOverlay.setCheckable(True)
        self.actionPathOverlay.setIcon(Icon)
        self.actionPathOverlay.setAutoRepeat(False)
        self.actionPathOverlay.setToolTip("Show fleet paths")
        self.actionPathOverlay.setStatusTip("Show the flight paths of all fleets within scanner range ...")

        Icon = QIcon(":/Toolbar/Names")
        self.actionPlanetNames = QAction(self)
        self.actionPlanetNames.setCheckable(True)
        self.actionPlanetNames.setIcon(Icon)
        self.actionPlanetNames.setAutoRepeat(False)
        self.actionPlanetNames.setToolTip("Show planet names ...")
        self.actionPlanetNames.setStatusTip("Show planet names ...")

        self.RadarRange = QSpinBox()
        self.RadarRange.setSuffix('%')
        self.RadarRange.setRange(10, 100)
        self.RadarRange.setValue(100)
        self.RadarRange.setSingleStep(10)
        self.RadarRange.setMinimumSize(QSize(100, 40))
        self.RadarRange.setAlignment(Qt.AlignmentFlag.AlignRight)

        Icon = QIcon(":/Toolbar/Scanner")
        self.actionRadarView = QAction(self)
        self.actionRadarView.setCheckable(True)
        self.actionRadarView.setIcon(Icon)
        self.actionRadarView.setAutoRepeat(False)
        self.actionRadarView.setToolTip("Scanner coverage overlay ...")
        self.actionRadarView.setStatusTip("Show scanner coverage on the star map ...")

        self.ViewMode = QActionGroup(self)
        self.ViewMode.addAction(self.actionDefaultView)
        self.ViewMode.addAction(self.actionSurfaceMineralView)
        self.ViewMode.addAction(self.actionConcentrationView)
        self.ViewMode.addAction(self.actionPercentView)
        self.ViewMode.addAction(self.actionPopulationView)
        self.ViewMode.addAction(self.actionNoInfoView)

        self.addAction(self.actionDefaultView)
        self.addAction(self.actionSurfaceMineralView)
        self.addAction(self.actionConcentrationView)
        self.addAction(self.actionPercentView)
        self.addAction(self.actionPopulationView)
        self.addAction(self.actionNoInfoView)
        self.addAction(self.actionAddWaypoint)
        self.addAction(self.actionRadarView)
        self.addWidget(self.RadarRange)
        self.addWidget(self.Mines)
        self.addAction(self.actionPathOverlay)
        self.addAction(self.actionPlanetNames)
        self.addAction(self.actionShipCount)
        self.addAction(self.actionWaitingFleets)
        self.addWidget(self.actionFriendlies)
        self.addWidget(self.actionFoes)
        self.addWidget(self.Zoom)


    def UpdateMyDesigns(self, DesignData):

        class MyAction(QAction):

            def __init__(self, name):
                super(self.__class__, self).__init__()
                self.ShipDesign = name

        @staticmethod
        def addAction(menu, action, label):
            action.setText(label)
            action.setCheckable(True)
            action.setChecked(True)
            action.toggled.connect(self.ShowMyFleets)
            menu.addAction(action)

        Menu = self.actionFriendlies.menu()
        for design in self.DesignNames:
            Menu.removeAction(self.MyFilter[design])
        self.MyFilter.clear()
        DesignData.sort()
        NewDesigns = dict()
        for name in DesignData:
            if name in self.DesignNames:
                NewDesigns[name] = self.MyDesigns[name]
            else:
                NewDesigns[name] = True
            NewAction = MyAction(name)
            addAction(Menu, NewAction, name)
            self.MyFilter[name] = NewAction
        self.MyDesigns = NewDesigns
        self.DesignNames = DesignData


    def DefineMyDesignMenu(self, DesignMenu):
        self.DesignNames = []
        self.MyDesigns = dict()
        self.MyFilter = dict()
        Menu = QMenu(self)
        Menu.setStyleSheet("QMenu::item{padding: 5px 40px 5px 0px}")
        self.AllMyDesigns = Menu.addAction('   All Designs')
        self.AllMyDesigns.setCheckable(False)
        self.AllMyDesigns.triggered.connect(self.ShowAllMyDesigns)
        self.InvertMyDesigns = Menu.addAction('   Invert Filter')
        self.InvertMyDesigns.setCheckable(False)
        self.InvertMyDesigns.triggered.connect(self.InvertMyDisplay)
        self.HideMyDesigns = Menu.addAction('   No Designs')
        self.HideMyDesigns.setCheckable(False)
        self.HideMyDesigns.triggered.connect(self.HideAllMyDesigns)
        Menu.addSeparator()
        DesignMenu.setMenu(Menu)


    def DefineEnemyDesignMenu(self, DesignMenu):

        class EnemyAction(QAction):

            def __init__(self, design):
                super(self.__class__, self).__init__()
                self.ShipDesign = design.name

        @staticmethod
        def addAction(menu, action, label):
            action.setText(label)
            action.setCheckable(True)
            action.setChecked(True)
            action.toggled.connect(self.ShowEnemyFleets)
            menu.addAction(action)

        self.FoeFilter = dict()
        Menu = QMenu(self)
        Menu.setStyleSheet("QMenu::item{padding: 5px 40px 5px 0px}")
        self.AllEnemyDesigns = Menu.addAction('   All Designs')
        self.AllEnemyDesigns.setCheckable(False)
        self.AllEnemyDesigns.triggered.connect(self.ShowAllEnemyDesigns)
        self.InvertEnemyDesigns = Menu.addAction('   Invert Filter')
        self.InvertEnemyDesigns.setCheckable(False)
        self.InvertEnemyDesigns.triggered.connect(self.InvertEnemyDisplay)
        self.HideEnemyDesigns = Menu.addAction('   No Designs')
        self.HideEnemyDesigns.setCheckable(False)
        self.HideEnemyDesigns.triggered.connect(self.HideAllEnemyDesigns)
        Menu.addSeparator()
        for design in ShipClass:
            action = EnemyAction(design)
            addAction(Menu, action, design.value)
            self.FoeFilter[design] = action
        DesignMenu.setMenu(Menu)


    def DefineMineMenu(self, Mines):

        class MineAction(QAction):

            def __init__(self, stance):
                super(self.__class__, self).__init__()
                self.MineView = stance

        @staticmethod
        def addAction(menu, action, label, tick=True):
            action.setText(label)
            action.setCheckable(tick)
            action.setChecked(True)
            if tick:
                action.toggled.connect(self.ShowMinefields)
            else:
                action.triggered.connect(self.ChangeMineDisplay)
            menu.addAction(action)

        Menu = QMenu(self)
        Menu.setStyleSheet("QMenu::item{padding: 5px 40px 5px 0px}")
        self.AllMines = MineAction(Stance.accept)
        self.NoMines = MineAction(Stance.none)
        self.AlliedMines = MineAction(Stance.allied)
        self.FriendlyMines = MineAction(Stance.friendly)
        self.NeutralMines = MineAction(Stance.neutral)
        self.HostileMines = MineAction(Stance.hostile)
        addAction(Menu, self.AllMines, '   All Mine Fields', False)
        addAction(Menu, self.NoMines, '   No Mine Fields', False)
        Menu.addSeparator()
        addAction(Menu, self.AlliedMines, 'Mine Fields of Yours')
        addAction(Menu, self.FriendlyMines, 'Mine Fields of Friends')
        addAction(Menu, self.NeutralMines, 'Mine Fields of Neutrals')
        addAction(Menu, self.HostileMines, 'Mine Fields of Enemies')
        Mines.setMenu(Menu)


    def ChangeMineDisplay(self, event):
        show = (self.sender().MineView == Stance.accept)
        if not show:
            self.Mines.setChecked(False)
        self.AlliedMines.setChecked(show)
        self.FriendlyMines.setChecked(show)
        self.NeutralMines.setChecked(show)
        self.HostileMines.setChecked(show)


    def ShowMinefields(self, event):
        fof = self.sender().MineView
        self.MineFilter[fof] = event
        show = False
        for b in self.MineFilter.values():
            show = show or b
        if show:
            self.Mines.setCheckable(True)
            self.Mines.setChecked(True)
            self.Mines.setPopupMode(Delayed)
        else:
            self.Mines.setChecked(False)
            self.Mines.setCheckable(False)
            self.Mines.setPopupMode(Instant)
        self.ShowMines.emit(event, fof)


    def ShowEnemyFleets(self, event):
        sc = self.sender().ShipDesign
        self.AlienDesigns[sc] = event
        disabled = True
        for b in self.AlienDesigns.values():
            disabled = disabled and b
        if disabled:
            self.actionFoes.setChecked(False)
            self.actionFoes.setCheckable(False)
            self.actionFoes.setPopupMode(Instant)
        else:
            self.actionFoes.setCheckable(True)
            self.actionFoes.setChecked(True)
            self.actionFoes.setPopupMode(Delayed)
        self.FilterEnemyFleets.emit(not disabled, self.AlienDesigns)


    def ShowMyFleets(self, event):
        sc = self.sender().ShipDesign
        self.MyDesigns[sc] = event
        disabled = True
        for b in self.MyDesigns.values():
            disabled = disabled and b
        if disabled:
            self.actionFriendlies.setChecked(False)
            self.actionFriendlies.setCheckable(False)
            self.actionFriendlies.setPopupMode(Instant)
        else:
            self.actionFriendlies.setCheckable(True)
            self.actionFriendlies.setChecked(True)
            self.actionFriendlies.setPopupMode(Delayed)
        self.FilterMyFleets.emit(not disabled, self.MyDesigns)


    def ShowAllMyDesigns(self):
        for design in self.DesignNames:
            self.MyFilter[design].setChecked(True)


    def InvertMyDisplay(self):
        for design in self.DesignNames:
            show = self.MyFilter[design].isChecked()
            self.MyFilter[design].setChecked(not show)


    def HideAllMyDesigns(self):
        for design in self.DesignNames:
            self.MyFilter[design].setChecked(False)


    def ShowAllEnemyDesigns(self):
        for design in ShipClass:
            self.FoeFilter[design].setChecked(True)


    def InvertEnemyDisplay(self):
        for design in ShipClass:
            show = self.FoeFilter[design].isChecked()
            self.FoeFilter[design].setChecked(not show)


    def HideAllEnemyDesigns(self):
        for design in ShipClass:
            self.FoeFilter[design].setChecked(False)
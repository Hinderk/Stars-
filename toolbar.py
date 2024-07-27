
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize



class ToolBar(QtWidgets.QToolBar):

    def __init__(self, form):

        super(self.__class__, self).__init__()
        self.EnemyDesigns = dict()
        self.FriendlyDesigns = dict()
        Instant = QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup

        MineFilter = QtWidgets.QMenu(self)
        self.AllMines = MineFilter.addAction('All Mine Fields')
        self.NoMines = MineFilter.addAction('No Mine Fields')
        MineFilter.addSeparator()
        self.YourMines = MineFilter.addAction('Mine Fields of Yours')
        self.FriendlyMines = MineFilter.addAction('Mine Fields of Friends')
        self.NeutralMines = MineFilter.addAction('Mine Fields of Neutrals')
        self.EnemyMines = MineFilter.addAction('Mine Fields of Enemies')
        self.YourMines.setCheckable(True)
        self.FriendlyMines.setCheckable(True)
        self.NeutralMines.setCheckable(True)
        self.EnemyMines.setCheckable(True)
        self.YourMines.setChecked(True)
        self.FriendlyMines.setChecked(True)
        self.NeutralMines.setChecked(True)
        self.EnemyMines.setChecked(True)

        Icon = QtGui.QIcon(":/Toolbar/Mine")
        self.MineOverlay = QtWidgets.QToolButton(self)
        self.MineOverlay.setIcon(Icon)
        self.MineOverlay.setPopupMode(Instant)
        self.MineOverlay.setCheckable(False)
        self.MineOverlay.setChecked(True)
        self.MineOverlay.setAutoRepeat(False)
        self.MineOverlay.setMenu(MineFilter)
        self.MineOverlay.setToolTip('Show mine fields ...')
        self.MineOverlay.setStatusTip('Show mine fields ...')

        Icon = QtGui.QIcon(":/Toolbar/Default")
        self.actionDefaultView = QtGui.QAction(self)
        self.actionDefaultView.setCheckable(True)
        self.actionDefaultView.setIcon(Icon)
        self.actionDefaultView.setAutoRepeat(False)
        self.actionDefaultView.setToolTip("Normal View")
        self.actionDefaultView.setStatusTip("Normal View")

        Icon = QtGui.QIcon(":/Toolbar/Percent")
        self.actionPercentView=QtGui.QAction(self)
        self.actionPercentView.setCheckable(True)
        self.actionPercentView.setIcon(Icon)
        self.actionPercentView.setAutoRepeat(False)
        self.actionPercentView.setToolTip("Planet Value View")
        self.actionPercentView.setStatusTip("Planet Value View")

        Icon = QtGui.QIcon(":/Toolbar/People")
        self.actionPopulationView = QtGui.QAction(self)
        self.actionPopulationView.setCheckable(True)
        self.actionPopulationView.setIcon(Icon)
        self.actionPopulationView.setAutoRepeat(False)
        self.actionPopulationView.setToolTip("Population View")
        self.actionPopulationView.setStatusTip("Population View")

        Icon = QtGui.QIcon(":/Toolbar/Surface")
        self.actionSurfaceMineralView = QtGui.QAction(self)
        self.actionSurfaceMineralView.setCheckable(True)
        self.actionSurfaceMineralView.setIcon(Icon)
        self.actionSurfaceMineralView.setAutoRepeat(False)
        self.actionSurfaceMineralView.setToolTip("Surface Mineral View")
        self.actionSurfaceMineralView.setStatusTip("Surface Mineral View")

        Icon = QtGui.QIcon(":/Toolbar/Minerals")
        self.actionConcentrationView = QtGui.QAction(self)
        self.actionConcentrationView.setCheckable(True)
        self.actionConcentrationView.setIcon(Icon)
        self.actionConcentrationView.setAutoRepeat(False)
        self.actionConcentrationView.setToolTip("Mineral Concentration View")
        self.actionConcentrationView.setStatusTip("Mineral Concentration View")

        Icon = QtGui.QIcon(":/Toolbar/Cancel")
        self.actionNoInfoView = QtGui.QAction(self)
        self.actionNoInfoView.setCheckable(True)
        self.actionNoInfoView.setIcon(Icon)
        self.actionNoInfoView.setAutoRepeat(False)
        self.actionNoInfoView.setToolTip("No Player Info View")
        self.actionNoInfoView.setStatusTip("Remove information about players ...")

        Icon = QtGui.QIcon(":/Toolbar/Waypoint")
        self.actionAddWaypoint = QtGui.QAction(self)
        self.actionAddWaypoint.setCheckable(True)
        self.actionAddWaypoint.setIcon(Icon)
        self.actionAddWaypoint.setAutoRepeat(False)
        self.actionAddWaypoint.setStatusTip("Add way points to the flight path ...")
        self.actionAddWaypoint.setToolTip("Add way points ...")

        Icon = QtGui.QIcon(":/Toolbar/Waiting")
        self.actionWaitingFleets = QtGui.QAction(self)
        self.actionWaitingFleets.setCheckable(True)
        self.actionWaitingFleets.setIcon(Icon)
        self.actionWaitingFleets.setAutoRepeat(False)
        self.actionWaitingFleets.setToolTip("Show idle fleets only ...")
        self.actionWaitingFleets.setStatusTip("Show fleets without any task to complete ...")

        Icon = QtGui.QIcon(":/Toolbar/Orbiting")
        self.actionShipCount = QtGui.QAction(self)
        self.actionShipCount.setCheckable(True)
        self.actionShipCount.setIcon(Icon)
        self.actionShipCount.setAutoRepeat(False)
        self.actionShipCount.setToolTip("Show fleet strengths ...")
        self.actionShipCount.setStatusTip("Show the strength of all fleets within scanner range ...")

        Icon = QtGui.QIcon(":/Toolbar/Friendlies")
        self.actionFriendlies = QtWidgets.QToolButton(self)
        self.actionFriendlies.setCheckable(True)
        self.actionFriendlies.setIcon(Icon)
        self.actionFriendlies.setAutoRepeat(False)
        self.actionFriendlies.setToolTip("Show friendly fleets ...")
        self.actionFriendlies.setStatusTip("Show only friendly fleets on the star map ...")
        self.FriendFilter = QtWidgets.QMenu(self)
        self.actionFriendlies.setMenu(self.FriendFilter)

        Icon = QtGui.QIcon(":/Toolbar/Foes")
        self.FoeFilter = QtWidgets.QMenu(self)
        self.actionFoes = QtWidgets.QToolButton(self)
        self.actionFoes.setCheckable(True)
        self.actionFoes.setIcon(Icon)
        self.actionFoes.setToolTip("Show enemy fleets ...")
        self.actionFoes.setStatusTip("Show only enemy fleets on the star map ...")
        self.actionFoes.setAutoRepeat(False)
        self.actionFoes.setMenu(self.FoeFilter)

        Icon = QtGui.QIcon(":/Toolbar/Zoomlevel")
        Zoom = QtWidgets.QToolButton(self)
        Zoom.setPopupMode(Instant)
        Zoom.setIcon(Icon)
        Zoom.setAutoRepeat(False)
        Zoom.setToolTip("Define the level of magnification ...")
        Zoom.setStatusTip("Define the level of magnification ...")
        self.actionZoom = dict()
        Menu = QtWidgets.QMenu(self)
        self.DefineZoomLevel(Menu, ['25%', '50%', '75%', '100%', '125%', '150%', '200%', '400%'])
        Zoom.setMenu(Menu)
        self.actionZoom['100%'].setChecked(True)

        Icon = QtGui.QIcon(":/Toolbar/Paths")
        self.actionPathOverlay = QtGui.QAction(self)
        self.actionPathOverlay.setCheckable(True)
        self.actionPathOverlay.setIcon(Icon)
        self.actionPathOverlay.setAutoRepeat(False)
        self.actionPathOverlay.setToolTip("Show fleet paths")
        self.actionPathOverlay.setStatusTip("Show the flight paths of all fleets within scanner range ...")

        Icon = QtGui.QIcon(":/Toolbar/Names")
        self.actionPlanetNames = QtGui.QAction(self)
        self.actionPlanetNames.setCheckable(True)
        self.actionPlanetNames.setIcon(Icon)
        self.actionPlanetNames.setAutoRepeat(False)
        self.actionPlanetNames.setToolTip("Show planet names ...")
        self.actionPlanetNames.setStatusTip("Show planet names ...")

        self.RadarRange = QtWidgets.QSpinBox()
        self.RadarRange.setSuffix('%')
        self.RadarRange.setRange(10, 100)
        self.RadarRange.setValue(100)
        self.RadarRange.setSingleStep(10)
        self.RadarRange.setMinimumSize(QSize(100, 40))
        self.RadarRange.setAlignment(Qt.AlignmentFlag.AlignRight)

        Icon = QtGui.QIcon(":/Toolbar/Scanner")
        self.actionRadarView = QtGui.QAction(self)
        self.actionRadarView.setCheckable(True)
        self.actionRadarView.setIcon(Icon)
        self.actionRadarView.setAutoRepeat(False)
        self.actionRadarView.setToolTip("Scanner coverage overlay ...")
        self.actionRadarView.setStatusTip("Show scanner coverage on the star map ...")

        self.addAction(self.actionDefaultView)
        self.addAction(self.actionSurfaceMineralView)
        self.addAction(self.actionConcentrationView)
        self.addAction(self.actionPercentView)
        self.addAction(self.actionPopulationView)
        self.addAction(self.actionNoInfoView)
        self.addAction(self.actionAddWaypoint)
        self.addAction(self.actionRadarView)
        self.addWidget(self.RadarRange)
        self.addWidget(self.MineOverlay)
        self.addAction(self.actionPathOverlay)
        self.addAction(self.actionPlanetNames)
        self.addAction(self.actionShipCount)
        self.addAction(self.actionWaitingFleets)
        self.addWidget(self.actionFriendlies)
        self.addWidget(self.actionFoes)
        self.addWidget(Zoom)


    def UpdateFriendlyDesigns(self, DesignData):

        self.FriendFilter.clear()
        self.AllFriends = self.FriendFilter.addAction( 'All Designs' )
        self.InvertFriends = self.FriendFilter.addAction( 'Invert Filter' )
        self.NoFriends = self.FriendFilter.addAction( 'No Designs' )
        self.FriendFilter.addSeparator()
        self.FriendlyDesigns.clear()
        for NewDesign in DesignData:
            NewAction = self.FriendFilter.addAction(NewDesign)
            NewAction.setCheckable(True)
            NewAction.setChecked(True)
            self.FriendlyDesigns[NewDesign] = NewAction


    def UpdateEnemyDesigns(self, DesignData):

        self.FoeFilter.clear()
        self.AllFoes = self.FoeFilter.addAction('All Designs')
        self.InvertFoes = self.FoeFilter.addAction('Invert Filter')
        self.NoFoes = self.FoeFilter.addAction('No Designs')
        self.FoeFilter.addSeparator()
        self.EnemyDesigns.clear()
        for NewDesign in DesignData:
            NewAction = self.FoeFilter.addAction(NewDesign)
            NewAction.setCheckable(True)
            NewAction.setChecked(True)
            self.EnemyDesigns[NewDesign] = NewAction


    def DefineZoomLevel(self, Menu, LevelSet):

        for Level in LevelSet:
            NewAction = Menu.addAction(Level)
            NewAction.setCheckable( True )
            NewAction.setText(Level)
            NewAction.setToolTip('Set magnification level: ' + Level)
            self.actionZoom[Level] = NewAction

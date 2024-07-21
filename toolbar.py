
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize



class ToolBar(QtWidgets.QToolBar):

    def __init__(self, form):

        super(self.__class__, self).__init__()
#
        MineFilter = QtWidgets.QMenu(self)
        form.AllMines = MineFilter.addAction('All Mine Fields')
        form.NoMines = MineFilter.addAction('No Mine Fields')
        MineFilter.addSeparator()
        form.YourMines = MineFilter.addAction('Mine Fields of Yours')
        form.FriendlyMines = MineFilter.addAction('Mine Fields of Friends')
        form.NeutralMines = MineFilter.addAction('Mine Fields of Neutrals')
        form.EnemyMines = MineFilter.addAction('Mine Fields of Enemies')
        form.YourMines.setCheckable(True)
        form.FriendlyMines.setCheckable(True)
        form.NeutralMines.setCheckable(True)
        form.EnemyMines.setCheckable(True)
        form.YourMines.setChecked(True)
        form.FriendlyMines.setChecked(True)
        form.NeutralMines.setChecked(True)
        form.EnemyMines.setChecked(True)

        Icon = QtGui.QIcon(':/Toolbar/Mine')
        form.MineOverlay = QtWidgets.QToolButton(self)
        form.MineOverlay.setToolTip('Show mine fields ...')
        form.MineOverlay.setCheckable(False)
        form.MineOverlay.setChecked(True)
        form.MineOverlay.setIcon(Icon)
        form.MineOverlay.setMenu(MineFilter)
#
        Icon = QtGui.QIcon(":/Toolbar/Default")
        form.actionDefaultView = QtGui.QAction(self)
        form.actionDefaultView.setCheckable(True)
        form.actionDefaultView.setIcon(Icon)
        form.actionDefaultView.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/Percent")
        form.actionPercentView=QtGui.QAction(self)
        form.actionPercentView.setCheckable(True)
        form.actionPercentView.setIcon(Icon)
        form.actionPercentView.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/People")
        form.actionPopulationView = QtGui.QAction(self)
        form.actionPopulationView.setCheckable(True)
        form.actionPopulationView.setIcon(Icon)
        form.actionPopulationView.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/Surface")
        form.actionSurfaceMineralView = QtGui.QAction(self)
        form.actionSurfaceMineralView.setCheckable(True)
        form.actionSurfaceMineralView.setIcon(Icon)
        form.actionSurfaceMineralView.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/Minerals")
        form.actionConcentrationView = QtGui.QAction(self)
        form.actionConcentrationView.setCheckable(True)
        form.actionConcentrationView.setIcon(Icon)
        form.actionConcentrationView.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/Cancel")
        form.actionNoInfoView = QtGui.QAction(self)
        form.actionNoInfoView.setCheckable(True)
        form.actionNoInfoView.setIcon(Icon)
        form.actionNoInfoView.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/Waypoint")
        form.actionAddWaypoint = QtGui.QAction(self)
        form.actionAddWaypoint.setCheckable(True)
        form.actionAddWaypoint.setIcon(Icon)
        form.actionAddWaypoint.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/Waiting")
        form.actionWaitingFleets = QtGui.QAction(self)
        form.actionWaitingFleets.setCheckable(True)
        form.actionWaitingFleets.setIcon(Icon)
        form.actionWaitingFleets.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/Orbiting")
        form.actionShipCount = QtGui.QAction(self)
        form.actionShipCount.setCheckable(True)
        form.actionShipCount.setIcon(Icon)
        form.actionShipCount.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/Friendlies")
        form.actionFriendlies = QtWidgets.QToolButton(self)
        form.actionFriendlies.setCheckable(True)
        form.actionFriendlies.setIcon(Icon)
        form.actionFriendlies.setAutoRepeat(False)
        form.FriendFilter = QtWidgets.QMenu(self)
        form.actionFriendlies.setMenu(form.FriendFilter)
#
        Icon = QtGui.QIcon(":/Toolbar/Foes")
        form.actionFoes = QtWidgets.QToolButton(self)
        form.actionFoes.setCheckable(True)
        form.actionFoes.setIcon(Icon)
        form.actionFoes.setAutoRepeat(False)
        form.FoeFilter = QtWidgets.QMenu(self)
        form.actionFoes.setMenu(form.FoeFilter)
#
        Icon = QtGui.QIcon(":/Toolbar/Zoomlevel")
        form.actionZoom = QtGui.QAction(self)
        form.actionZoom.setIcon(Icon)
        form.actionZoom.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/Paths")
        form.actionPathOverlay = QtGui.QAction(self)
        form.actionPathOverlay.setCheckable(True)
        form.actionPathOverlay.setIcon(Icon)
        form.actionPathOverlay.setAutoRepeat(False)
#
        Icon = QtGui.QIcon(":/Toolbar/Names")
        form.actionPlanetNames = QtGui.QAction(self)
        form.actionPlanetNames.setCheckable(True)
        form.actionPlanetNames.setIcon(Icon)
        form.actionPlanetNames.setAutoRepeat(False)
#
        form.RadarRange = QtWidgets.QSpinBox()
        form.RadarRange.setSuffix('%')
        form.RadarRange.setRange(10, 100)
        form.RadarRange.setValue(100)
        form.RadarRange.setSingleStep(10)
        form.RadarRange.setMinimumSize(QSize(100, 40))
        form.RadarRange.setAlignment(Qt.AlignmentFlag.AlignRight)
#
        self.addAction(form.actionDefaultView)
        self.addAction(form.actionSurfaceMineralView)
        self.addAction(form.actionConcentrationView)
        self.addAction(form.actionPercentView)
        self.addAction(form.actionPopulationView)
        self.addAction(form.actionNoInfoView)
        self.addAction(form.actionAddWaypoint)
        self.addWidget(form.RadarRange)
        self.addWidget(form.MineOverlay)
        self.addAction(form.actionPathOverlay)
        self.addAction(form.actionPlanetNames)
        self.addAction(form.actionShipCount)
        self.addAction(form.actionWaitingFleets)
        self.addWidget(form.actionFriendlies)
        self.addWidget(form.actionFoes)
        self.addAction(form.actionZoom)

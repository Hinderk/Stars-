
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QWidget
from design import Design
from menubar import Menu
from toolbar import ToolBar

import stars_rc
#import os



class Gui(QtWidgets.QMainWindow):

    def __init__(self):

        super(self.__class__, self).__init__()
        design = Design()
        self.setStyleSheet(design.getStyle())
        self.Action = dict()
        self.SetupUI(design)


    def retranslateUi(self, GUI):

        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(_translate("GUI", "GroupBox"))
        self.PreviousMessage.setText(_translate("GUI", "Previous"))
        self.FollowMessage.setText(_translate("GUI", "Goto"))
        self.SelectedObject.setText(_translate("GUI", "Selected Object"))
        self.actionLoadGame.setText(_translate("GUI", "Load Turn"))
        self.actionLoadGame.setShortcut(_translate("GUI", "Ctrl+L"))
        self.actionSaveGameAs.setText(_translate("GUI", "Save Turn as ..."))
        self.actionSaveGameAs.setShortcut(_translate("GUI", "Ctrl+A"))
        self.actionOpenGame.setShortcut(_translate("GUI", "Ctrl+O"))
        self.actionComputeNewTurn.setText(_translate("GUI", "Compute new Turn"))
        self.actionComputeNewTurn.setToolTip(_translate("GUI", "Compute the Next Turn"))
        self.actionComputeNewTurn.setShortcut(_translate("GUI", "Ctrl+F12"))
        self.actionShowToolbar.setText(_translate("GUI", "Toolbar"))
        self.actionGameParameters.setText(_translate("GUI", "Game Parameters"))
        self.actionCompute.setText(_translate("GUI", "Compute "))
        self.actionGenerate.setShortcut(_translate("GUI", "F9"))
        self.actionToolbar.setText(_translate("GUI", "Toolbar"))
        self.actionDefault.setText(_translate("GUI", "Default"))
        self.actionRace.setText(_translate("GUI", "Race"))
        self.actionRace.setShortcut(_translate("GUI", "F8"))
        self.action25.setText(_translate("GUI", "25%"))
        self.action50.setText(_translate("GUI", "50%"))
        self.action75.setText(_translate("GUI", "75%"))
        self.action100.setText(_translate("GUI", "100%"))
        self.action125.setText(_translate("GUI", "125%"))
        self.action150.setText(_translate("GUI", "150%"))
        self.action200.setText(_translate("GUI", "200%"))
        self.action400.setText(_translate("GUI", "400%"))
        self.actionDefaultView.setText(_translate("GUI", "DefaultView"))
        self.actionDefaultView.setToolTip(_translate("GUI", "Normal View"))
        self.actionPercentView.setText(_translate("GUI", "PercentView"))
        self.actionPercentView.setToolTip(_translate("GUI", "Planet Value View"))
        self.actionPopulationView.setText(_translate("GUI", "PopulationView"))
        self.actionPopulationView.setToolTip(_translate("GUI", "Population View"))
        self.actionSurfaceMineralView.setText(_translate("GUI", "SurfaceMineralView"))
        self.actionSurfaceMineralView.setToolTip(_translate("GUI", "Surface Mineral View"))
        self.actionConcentrationView.setText(_translate("GUI", "ConcentrationView"))
        self.actionConcentrationView.setToolTip(_translate("GUI", "Mineral Concentration View"))
        self.actionNoInfoView.setText(_translate("GUI", "NoPlayerInfoView"))
        self.actionNoInfoView.setToolTip(_translate("GUI", "No Player Info View"))
        self.actionShipDesign.setText(_translate("GUI", "Ship Design ..."))
        self.actionShipDesign.setShortcut(_translate("GUI", "F4"))
        self.actionBattlePlans.setText(_translate("GUI", "Battle Plans ..."))
        self.actionBattlePlans.setShortcut(_translate("GUI", "F6"))
        self.actionPlayerRelations.setText(_translate("GUI", "Player Relations ..."))
        self.actionPlayerRelations.setShortcut(_translate("GUI", "F7"))
        self.actionResearch.setText(_translate("GUI", "Research ..."))
        self.actionResearch.setShortcut(_translate("GUI", "F5"))
        self.actionChangePassword.setText(_translate("GUI", "Change Password ..."))
        self.actionPlanets.setText(_translate("GUI", "Planets ..."))
        self.actionFleets.setText(_translate("GUI", "Fleets ..."))
        self.actionFleets.setShortcut(_translate("GUI", "F3"))
        self.actionOtherFleets.setText(_translate("GUI", "Other\'s Fleets ..."))
        self.actionBattles.setText(_translate("GUI", "Battles ..."))
        self.actionScore.setText(_translate("GUI", "Score ..."))
        self.actionUniverseDefinition.setText(_translate("GUI", "Universe Defintion"))
        self.actionPlanetInformation.setText(_translate("GUI", "Planet Information"))
        self.actionFleetInformation.setText(_translate("GUI", "Fleet Information"))
        self.actionAddWaypoint.setText(_translate("GUI", "Add way points mode"))
        self.actionAddWaypoint.setIconText(_translate("GUI", "Add way points mode"))
        self.actionAddWaypoint.setToolTip(_translate("GUI", "Add way points mode"))
        self.actionWaitingFleets.setText(_translate("GUI", "Idle fleets filter"))
        self.actionWaitingFleets.setToolTip(_translate("GUI", "Idle fleets filter"))
        self.actionShipCount.setText(_translate("GUI", "ShipCount"))
        self.actionShipCount.setToolTip(_translate("GUI", "Ship counts overlay"))
        self.actionFriendlies.setText(_translate("GUI", "Friendlies"))
        self.actionFriendlies.setToolTip(_translate("GUI", "Show friendly fleets"))
        self.actionFoes.setText(_translate("GUI", "Foes"))
        self.actionFoes.setToolTip(_translate("GUI", "Show enemy ships"))
        self.actionZoom.setText(_translate("GUI", "Zoom"))
        self.actionPathOverlay.setText(_translate("GUI", "PathOverlay"))
        self.actionPathOverlay.setToolTip(_translate("GUI", "Show fleet paths"))


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


    def SetupUI(self, design):

        ExpandSize = QtWidgets.QSizePolicy.Policy.Expanding
        MaxSize = QtWidgets.QSizePolicy.Policy.Maximum
        MinSize = QtWidgets.QSizePolicy.Policy.Minimum
        FixedSize = QtWidgets.QSizePolicy.Policy.Fixed

        self.resize(1600, 1200)
        sizePolicy = QtWidgets.QSizePolicy(MaxSize, MaxSize)  # TODO: Query design for details!
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle("My Stars!")
        Icon = QtGui.QIcon()
        Icon.addPixmap(QtGui.QPixmap(":/Icons/Stars"))
        self.setWindowIcon(Icon)
        self.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.Europe))
        self.setIconSize(QtCore.QSize(60, 60))
        self.CentralWidget = QWidget(self)
        self.CentralWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(ExpandSize, ExpandSize)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.CentralWidget.setSizePolicy(sizePolicy)
        self.CentralWidget.setMinimumSize(QtCore.QSize(800, 600))  # TODO: Query design!

        GridLayout = QtWidgets.QGridLayout(self.CentralWidget)
        self.groupBox = QtWidgets.QGroupBox(self.CentralWidget)
        GridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.Universe = QtWidgets.QGraphicsView(self.CentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(ExpandSize, ExpandSize)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.Universe.setSizePolicy(sizePolicy)
        self.Universe.setSceneRect(QtCore.QRectF(0.0, 0.0, 100.0, 100.0))
        GridLayout.addWidget(self.Universe, 0, 1, 1, 1)
        Filter_HL = QtWidgets.QHBoxLayout(self.CentralWidget)
        self.FilterMessage = QtWidgets.QCheckBox(self.CentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(MinSize, FixedSize)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.FilterMessage.setSizePolicy(sizePolicy)
        self.FilterMessage.setMinimumSize(QtCore.QSize(20, 20))
        self.FilterMessage.setToolTip("Show the likes of the current message ...")
        self.FilterMessage.setChecked(True)
        Filter_HL.addWidget(self.FilterMessage)
        self.CurrentGameYear = QtWidgets.QLabel(self.CentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(ExpandSize, FixedSize)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.CurrentGameYear.setSizePolicy(sizePolicy)
        self.CurrentGameYear.setToolTip("Current Age of the Galaxy ...")
        self.CurrentGameYear.setText("Year 2400 - Message: 1 of 10")  # TODO: Fix messages!
        self.CurrentGameYear.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        Filter_HL.addWidget(self.CurrentGameYear)
        Spacer = QtWidgets.QSpacerItem(100, 20, FixedSize, MinSize)
        Filter_HL.addItem(Spacer)
        Messages_VL = QtWidgets.QVBoxLayout()
        Messages_VL.addLayout(Filter_HL)
        CurrentMessage_HL = QtWidgets.QHBoxLayout()
        self.CurrentMessage = QtWidgets.QPlainTextEdit(self.CentralWidget)
        self.CurrentMessage.setMinimumSize(QtCore.QSize(0, 0))
        self.CurrentMessage.setUndoRedoEnabled(False)
        self.CurrentMessage.setReadOnly(True)
#
        self.CurrentMessage.setPlainText("This is a very simple message that requires Your attention!")
#
        CurrentMessage_HL.addWidget(self.CurrentMessage)
        NewsButtons_VL = QtWidgets.QVBoxLayout()
        NewsButtons_VL.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        Spacer = QtWidgets.QSpacerItem(20, 40, MinSize, ExpandSize)
        NewsButtons_VL.addItem(Spacer)
        self.PreviousMessage = QtWidgets.QPushButton(self.CentralWidget)
        self.PreviousMessage.setToolTip("Read previous message ...")
        NewsButtons_VL.addWidget(self.PreviousMessage)
        self.FollowMessage = QtWidgets.QPushButton(self.CentralWidget)
        self.FollowMessage.setToolTip("Follow up on current message ...")
        NewsButtons_VL.addWidget(self.FollowMessage)
        self.NextMessage = QtWidgets.QPushButton(self.CentralWidget)
        self.NextMessage.setText("Next")
        self.NextMessage.setToolTip("Read next message ...")
        NewsButtons_VL.addWidget(self.NextMessage)
        Spacer = QtWidgets.QSpacerItem(20, 40, MinSize, ExpandSize)
        NewsButtons_VL.addItem(Spacer)
        CurrentMessage_HL.addLayout(NewsButtons_VL)
        Messages_VL.addLayout(CurrentMessage_HL)
        GridLayout.addLayout(Messages_VL, 1, 0, 1, 1)
        Inspector_VL = QtWidgets.QVBoxLayout()
        SelectedObject_HL = QtWidgets.QHBoxLayout()
        SelectedObject_HL.setSpacing(0)
        Spacer = QtWidgets.QSpacerItem(32, 20, FixedSize, MinSize)
        SelectedObject_HL.addItem(Spacer)
        Spacer = QtWidgets.QSpacerItem(40, 20, ExpandSize, MinSize)
        SelectedObject_HL.addItem(Spacer)
        self.SelectedObject = QtWidgets.QLabel(self.CentralWidget)
#        self.SelectedObject.setScaledContents(False)
#        self.SelectedObject.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        SelectedObject_HL.addWidget(self.SelectedObject)
        Spacer = QtWidgets.QSpacerItem(40, 20, ExpandSize, MinSize)
        SelectedObject_HL.addItem(Spacer)
        self.SelectNextObject = QtWidgets.QPushButton(self.CentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(FixedSize, FixedSize)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.SelectNextObject.setSizePolicy(sizePolicy)
        self.SelectNextObject.setMinimumSize(QtCore.QSize(20, 20))
        SelectedObject_HL.addWidget(self.SelectNextObject)
        Inspector_VL.addLayout(SelectedObject_HL)
#
        Icon = QtGui.QIcon()
        Icon.addPixmap(QtGui.QPixmap(":/Toolbar/Percent"))
        self.SelectNextObject.setIcon(Icon)
        self.SelectNextObject.setIconSize(QtCore.QSize(20, 20))
        self.SelectNextObject.setFlat(True)
        self.Inspector = QtWidgets.QGraphicsView(parent=self.CentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.Inspector.setSizePolicy(sizePolicy)
        self.Inspector.setMaximumSize(QtCore.QSize(1200, 450))
        self.Inspector.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        Inspector_VL.addWidget(self.Inspector)
        GridLayout.addLayout(Inspector_VL, 1, 1, 1, 1)
        self.setCentralWidget(self.CentralWidget)
#
        self.FriendlyDesigns = dict()
        self.EnemyDesigns = dict()
#
        Buttons = ToolBar(self)
#        Buttons.setAutoFillBackground(True)
        Buttons.setMovable(False)
        Buttons.setIconSize(QtCore.QSize(40, 40))
        self.addToolBar(Buttons)
        self.setMenuBar(Menu(self))
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
#
        self.UpdateFriendlyDesigns([])
        self.UpdateEnemyDesigns(
            ['Colony Ships', 'Freighters', 'Scouts', 'Warships', 'Utility Ships',
              'Bombers', 'Mining Ships', 'Fuel Transports']
        )
#

        self.retranslateUi(self)

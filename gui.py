
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QWidget, QStackedLayout
from PyQt6.QtWidgets import QGraphicsView, QVBoxLayout
from design import Design
from menubar import Menu
from toolbar import ToolBar
from ruleset import Ruleset
from inspector import Inspector
from universe import Universe

#import stars_rc
#import os



def _CreateButton(name):
  Style = "padding: 5px 5px 5px 5px;border-width: 0px;background-color: transparent"
  Icon = QtGui.QIcon(name)
  Button = QtWidgets.QPushButton()
  Button.setIcon(Icon)
  Button.setIconSize(QtCore.QSize(30, 30))
  Button.setStyleSheet(Style)
  Button.setVisible(True)
  return Button



class Gui(QtWidgets.QMainWindow):

    def __init__(self, people):

        super(self.__class__, self).__init__()
        design = Design()
        self.setStyleSheet(design.getStyle())
        self.Action = dict()
        self.SetupUI(design, people, Ruleset())


    def SetupUI(self, design, people, rules):

        self.resize(1800, 1300)                        # TODO: Query design!
        self.setWindowTitle("My Stars!")
        Icon = QtGui.QIcon()
        Icon.addPixmap(QtGui.QPixmap(":/Icons/Stars"))
        self.setWindowIcon(Icon)
        self.CentralWidget = QWidget(self)
        self.setCentralWidget(self.CentralWidget)
        self.CentralWidget.setMinimumSize(1800, 1200)  # TODO: Query design!

        GridLayout = QtWidgets.QGridLayout(self.CentralWidget)
        GroupBox = QtWidgets.QGroupBox(self.CentralWidget)
        GridLayout.addWidget(GroupBox, 0, 0, 1, 1)
        self.Universe = Universe(rules)
        GridLayout.addWidget(self.Universe, 0, 1, 1, 1)
        GridLayout.addLayout(self.SetupNewsReader(), 1, 0, 1, 1)
#
        self.PlanetInfo = Inspector(people)
        h = int(self.PlanetInfo.sceneRect().height() + 1.5)
        w = int(self.PlanetInfo.sceneRect().width() + 4.5)
        InspectorView = QGraphicsView(self.CentralWidget)
        InspectorView.setMinimumSize(QtCore.QSize(w, h))
        InspectorView.setScene(self.PlanetInfo)
        Inspector_VL = QVBoxLayout()
        Inspector_VL.addLayout(self.SetupInspectorTitle(w - 5))
        Inspector_VL.addWidget(InspectorView)
        Inspector_VL.addStretch()

        self.ItemInfo = QStackedLayout(self.CentralWidget)
        PlanetProperties = QWidget()
        PlanetProperties.setLayout(Inspector_VL)
        self.ItemInfo.addWidget(PlanetProperties)

        GridLayout.addLayout(self.ItemInfo, 1, 1, 1, 1)
#
        self.Buttons = ToolBar(self)
#       self.Buttons.setAutoFillBackground(True)
        self.Buttons.setMovable(False)
        self.Buttons.setIconSize(QtCore.QSize(40, 40))
        self.addToolBar(self.Buttons)
        self.Menu = Menu(self)
        self.setMenuBar(self.Menu)
        self.Status = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.Status)
#
        self.Buttons.UpdateFriendlyDesigns([])
        self.Buttons.UpdateEnemyDesigns(
            ['Colony Ships', 'Freighters', 'Scouts', 'Warships', 'Utility Ships',
              'Bombers', 'Mining Ships', 'Fuel Transports']
        )


    def SetupNewsReader(self):
        Filter_HL = QtWidgets.QHBoxLayout(self.CentralWidget)
        self.FilterMessage = QtWidgets.QCheckBox(self.CentralWidget)
        self.FilterMessage.setToolTip("Show the likes of the current message ...")
        self.FilterMessage.setStatusTip("Show the likes of the current message ...")
        self.FilterMessage.setChecked(True)
        Filter_HL.addWidget(self.FilterMessage)
        Filter_HL.addStretch()
        self.CurrentGameYear = QtWidgets.QLabel(self.CentralWidget)
        self.CurrentGameYear.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CurrentGameYear.setToolTip("Current Age of the Galaxy ...")
        self.CurrentGameYear.setText("Year 2400 - Message: 1 of 9999")
        Filter_HL.addWidget(self.CurrentGameYear)
        Filter_HL.addStretch()
        Filter_HL.addSpacing(25)
        self.CurrentMessage = QtWidgets.QPlainTextEdit(self.CentralWidget)
        self.CurrentMessage.setMinimumSize(QtCore.QSize(400, 320))
        self.CurrentMessage.setReadOnly(True)
        NewsButtons_VL = QtWidgets.QVBoxLayout()
        NewsButtons_VL.addStretch()
        self.PreviousMessage = QtWidgets.QPushButton(self.CentralWidget)
        self.PreviousMessage.setText("Previous")
        self.PreviousMessage.setToolTip("Read previous message ...")
        self.PreviousMessage.setStatusTip("Read the previous message ...")
        NewsButtons_VL.addWidget(self.PreviousMessage)
        self.FollowMessage = QtWidgets.QPushButton(self.CentralWidget)
        self.FollowMessage.setText("Goto")
        self.FollowMessage.setToolTip("Follow up on current message ...")
        self.FollowMessage.setStatusTip("Follow up on the current message ...")
        NewsButtons_VL.addSpacing(10)
        NewsButtons_VL.addWidget(self.FollowMessage)
        self.NextMessage = QtWidgets.QPushButton(self.CentralWidget)
        self.NextMessage.setText("Next")
        self.NextMessage.setToolTip("Read next message ...")
        self.NextMessage.setStatusTip("Read the next message ...")
        NewsButtons_VL.addSpacing(10)
        NewsButtons_VL.addWidget(self.NextMessage)
        News_GL = QtWidgets.QGridLayout(self.CentralWidget)
        News_GL.addLayout(Filter_HL, 0, 0, 1, 1)
        News_GL.addWidget(self.CurrentMessage, 1, 0, 1, 1)
        News_GL.addLayout(NewsButtons_VL, 1, 1, 1, 1)
        NewsButtons_VL.addStretch()
        return News_GL


    def SetupInspectorTitle(self, width):
        SelectedObject_HL = QtWidgets.QHBoxLayout(self.CentralWidget)
        SelectedObject_HL.setSpacing(0)
        SelectedObject_HL.addSpacing(Inspector.xInfo + 160)
        self.SelectedObject = QtWidgets.QLabel(self.CentralWidget)
        self.SelectedObject.setMinimumWidth(Inspector.xWidth - 320)
        self.SelectedObject.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SelectedObject.setText("Selected Object")
        SelectedObject_HL.addWidget(self.SelectedObject)
        self.ShowAlienBase = _CreateButton(":/Icons/Fortress")
        self.ShowStarBase = _CreateButton(":/Icons/Starbase")
        self.SelectNextEnemy = _CreateButton(":/Icons/Enemies")
        self.SelectNextFleet = _CreateButton(":/Icons/Fleets")
        SelectedObject_HL.addStretch()
        SelectedObject_HL.addWidget(self.ShowAlienBase)
        SelectedObject_HL.addWidget(self.ShowStarBase)
        SelectedObject_HL.addWidget(self.SelectNextEnemy)
        SelectedObject_HL.addWidget(self.SelectNextFleet)
        SelectedObject_HL.addSpacing(width - Inspector.xInfo - Inspector.xWidth)
        return SelectedObject_HL



    def ChangeInspectorTitle(self, titel, b1=False, b2=False, b3=False, b4=False):
        self.SelectedObject.setText(titel)
        self.ShowAlienBase.setVisible(b1)
        self.ShowStarBase.setVisible(b2)
        self.SelectNextEnemy.setVisible(b3)
        self.SelectNextFleet.setVisible(b4)
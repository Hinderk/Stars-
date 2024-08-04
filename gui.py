
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QWidget
from design import Design
from menubar import Menu
from toolbar import ToolBar
from inspector import Inspector

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
        self.SetupUI(design, people)


    def SetupUI(self, design, people):

        ExpandSize = QtWidgets.QSizePolicy.Policy.Expanding
        MaxSize = QtWidgets.QSizePolicy.Policy.Maximum
        MinSize = QtWidgets.QSizePolicy.Policy.Minimum
        FixedSize = QtWidgets.QSizePolicy.Policy.Fixed

        self.resize(1800, 1350)
        self.setWindowTitle("My Stars!")
        Icon = QtGui.QIcon()
        Icon.addPixmap(QtGui.QPixmap(":/Icons/Stars"))
        self.setWindowIcon(Icon)
        self.CentralWidget = QWidget(self)
        self.setCentralWidget(self.CentralWidget)
        self.CentralWidget.setMinimumSize(640, 480)  # TODO: Query design!

        GridLayout = QtWidgets.QGridLayout(self.CentralWidget)
        GroupBox = QtWidgets.QGroupBox(self.CentralWidget)
        GridLayout.addWidget(GroupBox, 0, 0, 1, 1)
        self.Universe = QtWidgets.QGraphicsView(self.CentralWidget)
        GridLayout.addWidget(self.Universe, 0, 1, 1, 1)
        GridLayout.addLayout(self.SetupNewsReader(), 1, 0, 1, 1)
#
        self.PlanetInfo = Inspector(people)
        h = int(self.PlanetInfo.sceneRect().height() + 1.5)
        w = int(self.PlanetInfo.sceneRect().width() + 4.5)
        Iview = QtWidgets.QGraphicsView(self.CentralWidget)
        Iview.setMinimumSize(QtCore.QSize(w, h))
        Iview.setScene(self.PlanetInfo)
        Inspector_VL = QtWidgets.QVBoxLayout()
        Inspector_VL.addStretch()
        Inspector_VL.addLayout(self.SetupInspectorTitle(w - 5))
        Inspector_VL.addWidget(Iview)
        GridLayout.addLayout(Inspector_VL, 1, 1, 1, 1)
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
        self.CurrentMessage.setMinimumSize(QtCore.QSize(400, 315))
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
        NewsButtons_VL.addStretch()
        News_GL = QtWidgets.QGridLayout(self.CentralWidget)
        News_GL.addLayout(Filter_HL, 0, 0, 1, 1)
        News_GL.addWidget(self.CurrentMessage, 1, 0, 1, 1)
        News_GL.addLayout(NewsButtons_VL, 1, 1, 1, 1)
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
        self.ShowAlienBase = _CreateButton(":/Icons/Starbase")
        self.ShowStarBase = _CreateButton(":/Icons/Starbase")
        self.SelectNextEnemy = _CreateButton(":/Icons/Triangle")
        self.SelectNextFleet = _CreateButton(":/Icons/Triangle")
        SelectedObject_HL.addStretch()
        SelectedObject_HL.addWidget(self.ShowAlienBase)
        SelectedObject_HL.addWidget(self.ShowStarBase)
        SelectedObject_HL.addWidget(self.SelectNextEnemy)
        SelectedObject_HL.addWidget(self.SelectNextFleet)
        SelectedObject_HL.addSpacing(width - Inspector.xInfo - Inspector.xWidth)
        return SelectedObject_HL



    def ChangeInspectorTitle(self, titel, starbase=False, fleets=False):
        self.SelectedObject.setText(titel)
        self.SelectNextFleet.setVisible(fleets)
        self.ShowStarBase.setVisible(starbase)

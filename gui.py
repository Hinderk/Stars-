
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QWidget, QStackedLayout
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from design import Design
from menubar import Menu
from toolbar import ToolBar
from ruleset import Ruleset
from inspector import Inspector
from fleetdata import Fleetdata
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

        self.resize(2400, 1350)                        # TODO: Query design!
        self.setWindowTitle("My Stars!")
        Icon = QtGui.QIcon()
        Icon.addPixmap(QtGui.QPixmap(":/Icons/Stars"))
        self.setWindowIcon(Icon)
        self.CentralWidget = QWidget(self)
        self.setCentralWidget(self.CentralWidget)
        self.CentralWidget.setMinimumSize(2400, 1350)  # TODO: Query design!

        LeftSide = QtWidgets.QWidget()
        LeftSide.setMaximumWidth(875)

        Layout_HL = QtWidgets.QHBoxLayout(self.CentralWidget)
        Layout_HL.setSpacing(0)
        Layout_VL = QtWidgets.QVBoxLayout(LeftSide)
        Layout_VL.setSpacing(0)

        self.Buttons = ToolBar(self)
        self.Buttons.setAutoFillBackground(True)
        self.Buttons.setMovable(False)
        self.Buttons.setIconSize(QtCore.QSize(40, 40))
        Layout_VL.addWidget(self.Buttons)

        InfoBox = QtWidgets.QGroupBox()
        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalPolicy(policy.Policy.MinimumExpanding)
        policy.setVerticalPolicy(policy.Policy.MinimumExpanding)
        InfoBox.setSizePolicy(policy)
        Data_VL = QtWidgets.QVBoxLayout(InfoBox)
        Label_A = QtWidgets.QLabel("Test-A")
        Label_B = QtWidgets.QLabel("Test-B")
        Data_VL.addWidget(Label_A)
        Data_VL.addStretch()
        Data_VL.addWidget(Label_B)

        Layout_VL.addWidget(InfoBox)
        Layout_VL.addWidget(self.SetupNewsReader())
#
        InfoBox = QtWidgets.QGroupBox()
        InfoBox.setMinimumHeight(420)
        InfoBox.setMaximumHeight(420)
        Info_VL = QVBoxLayout(InfoBox)
        Info_VL.setSpacing(0)
        Info_VL.addWidget(self.SetupInspectorTitle())
        self.ItemInfo = QStackedLayout()
        self.PlanetInfo = Inspector(people)
        self.ItemInfo.addWidget(self.PlanetInfo)

        self.FleetInfo = Fleetdata()
        self.ItemInfo.addWidget(self.FleetInfo)

        Enigma = QWidget()
        Enigma_HL = QHBoxLayout(Enigma)
        Enigma_HL.addStretch()
        Image = QSvgWidget(":/Graphics/Enigma")
        Image.setMaximumSize(300, 300)
        Enigma_HL.addWidget(Image)
        Enigma_HL.addStretch()
        self.ItemInfo.addWidget(Enigma)

        Info_VL.addLayout(self.ItemInfo)
        Layout_VL.addWidget(InfoBox)

        self.Universe = Universe(rules)
        Layout_HL.addWidget(LeftSide)
        Layout_HL.addWidget(self.Universe)

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

        Filter_HL = QtWidgets.QHBoxLayout()
        Filter_HL.setSpacing(0)
        self.FilterMessage = QtWidgets.QCheckBox()
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
        Icon = QtGui.QIcon()
        Show = QtGui.QPixmap(":/Icons/ShowNews")
        NoShow = QtGui.QPixmap(":/Icons/NoNews")
        Icon.addPixmap(NoShow, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Icon.addPixmap(Show, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        Filter = QtWidgets.QToolButton(self.CentralWidget)
        Filter.setCheckable(True)
        Filter.setIcon(Icon)
        Filter.setAutoRepeat(False)
        Filter.setToolTip("Show the likes of the current message ...")
        Filter.setStatusTip("Show the likes of the current message ...")
        Filter.setIconSize(QtCore.QSize(30, 30))
        Filter_HL.addWidget(Filter)
        self.CurrentMessage = QtWidgets.QPlainTextEdit(self.CentralWidget)
        self.CurrentMessage.setReadOnly(True)
        self.CurrentMessage.setPlainText("This is a very important message ...")  # DELETE ME!
        NewsButtons_VL = QtWidgets.QVBoxLayout()
        NewsButtons_VL.addStretch()
        self.PreviousMessage = QtWidgets.QPushButton()
        self.PreviousMessage.setText("Prev")
        self.PreviousMessage.setToolTip("Read previous message ...")
        self.PreviousMessage.setStatusTip("Read the previous message ...")
        NewsButtons_VL.addWidget(self.PreviousMessage)
        self.FollowMessage = QtWidgets.QPushButton()
        self.FollowMessage.setText("Goto")
        self.FollowMessage.setToolTip("Follow up on current message ...")
        self.FollowMessage.setStatusTip("Follow up on the current message ...")
        NewsButtons_VL.addWidget(self.FollowMessage)
        self.NextMessage = QtWidgets.QPushButton()
        self.NextMessage.setText("Next")
        self.NextMessage.setToolTip("Read next message ...")
        self.NextMessage.setStatusTip("Read the next message ...")
        NewsButtons_VL.addWidget(self.NextMessage)
        NewsButtons_VL.addStretch()
        News_HL = QtWidgets.QHBoxLayout()
        News_HL.setSpacing(5)
        News_HL.addWidget(self.CurrentMessage)
        News_HL.addLayout(NewsButtons_VL)
        News_VL = QtWidgets.QVBoxLayout()
        News_VL.addLayout(Filter_HL)
        News_VL.addLayout(News_HL)
        News_VL.addSpacing(5)
        NewsReader = QtWidgets.QGroupBox()
        NewsReader.setLayout(News_VL)
        NewsReader.setMaximumHeight(190)
        return NewsReader


    def SetupInspectorTitle(self):

        Title = QtWidgets.QWidget()
        SelectedObject_HL = QtWidgets.QHBoxLayout(Title)
        SelectedObject_HL.setSpacing(0)
        SelectedObject_HL.addSpacing(250)
        self.SelectedObject = QtWidgets.QLabel()
        self.SelectedObject.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SelectedObject.setText("Selected Object")
        SelectedObject_HL.addWidget(self.SelectedObject)
        ButtonBox = QtWidgets.QWidget()
        ButtonBox.setMaximumWidth(180)
        ButtonLayout_HL = QtWidgets.QHBoxLayout(ButtonBox)
        ButtonLayout_HL.setSpacing(0)
        ButtonLayout_HL.addStretch()
        self.ShowAlienBase = _CreateButton(":/Icons/Fortress")
        ButtonLayout_HL.addWidget(self.ShowAlienBase)
        self.ShowStarBase = _CreateButton(":/Icons/Starbase")
        ButtonLayout_HL.addWidget(self.ShowStarBase)
        self.SelectNextEnemy = _CreateButton(":/Icons/Enemies")
        ButtonLayout_HL.addWidget(self.SelectNextEnemy)
        self.SelectNextFleet = _CreateButton(":/Icons/Fleets")
        ButtonLayout_HL.addWidget(self.SelectNextFleet)
        SelectedObject_HL.addWidget(ButtonBox)
        SelectedObject_HL.addSpacing(70)
        Title.setMaximumHeight(70)
        return Title


    def ChangeInspectorTitle(self, titel, b1=False, b2=False, b3=False, b4=False):
        self.SelectedObject.setText(titel)
        self.ShowAlienBase.setVisible(b1)
        self.ShowStarBase.setVisible(b2)
        self.SelectNextEnemy.setVisible(b3)
        self.SelectNextFleet.setVisible(b4)
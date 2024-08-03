
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
        GroupBox = QtWidgets.QGroupBox(self.CentralWidget)
        GridLayout.addWidget(GroupBox, 0, 0, 1, 1)
        self.Universe = QtWidgets.QGraphicsView(self.CentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(ExpandSize, ExpandSize)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.Universe.setSizePolicy(sizePolicy)
        self.Universe.setSceneRect(QtCore.QRectF(0.0, 0.0, 100.0, 100.0))
        GridLayout.addWidget(self.Universe, 0, 1, 1, 1)

        Filter_HL = QtWidgets.QHBoxLayout(self.CentralWidget)
        self.FilterMessage = QtWidgets.QCheckBox(self.CentralWidget)
        self.FilterMessage.setToolTip("Show the likes of the current message ...")
        self.FilterMessage.setStatusTip("Show the likes of the current message ...")
        self.FilterMessage.setChecked(True)
        Filter_HL.addWidget(self.FilterMessage)
        self.CurrentGameYear = QtWidgets.QLabel(self.CentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(ExpandSize, FixedSize)
        self.CurrentGameYear.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CurrentGameYear.setSizePolicy(sizePolicy)
        self.CurrentGameYear.setToolTip("Current Age of the Galaxy ...")
#
        self.CurrentGameYear.setText("Year 2400 - Message: 1 of 9999")  # TODO: Fix messages!
#
        Filter_HL.addWidget(self.CurrentGameYear)
        Spacer = QtWidgets.QSpacerItem(25, 0, FixedSize, MinSize)
        Filter_HL.addItem(Spacer)
#
        self.CurrentMessage = QtWidgets.QPlainTextEdit(self.CentralWidget)
        self.CurrentMessage.setMinimumSize(QtCore.QSize(400, 0))
#        self.CurrentMessage.setUndoRedoEnabled(False)
        self.CurrentMessage.setReadOnly(True)
#
        self.CurrentMessage.setPlainText("This is a very simple message that requires Your attention!")
#
        NewsButtons_VL = QtWidgets.QVBoxLayout()
        Spacer = QtWidgets.QSpacerItem(0, 40, MinSize, ExpandSize)
        Shim = QtWidgets.QSpacerItem(0, 10, MinSize, MinSize)
        NewsButtons_VL.addItem(Spacer)
        self.PreviousMessage = QtWidgets.QPushButton(self.CentralWidget)
        self.PreviousMessage.setText("Previous")
        self.PreviousMessage.setToolTip("Read previous message ...")
        self.PreviousMessage.setStatusTip("Read the previous message ...")
        NewsButtons_VL.addWidget(self.PreviousMessage)
        self.FollowMessage = QtWidgets.QPushButton(self.CentralWidget)
        self.FollowMessage.setText("Goto")
        self.FollowMessage.setToolTip("Follow up on current message ...")
        self.FollowMessage.setStatusTip("Follow up on the current message ...")
        NewsButtons_VL.addItem(Shim)
        NewsButtons_VL.addWidget(self.FollowMessage)
        self.NextMessage = QtWidgets.QPushButton(self.CentralWidget)
        self.NextMessage.setText("Next")
        self.NextMessage.setToolTip("Read next message ...")
        self.NextMessage.setStatusTip("Read the next message ...")
        NewsButtons_VL.addItem(Shim)
        NewsButtons_VL.addWidget(self.NextMessage)
        NewsButtons_VL.addItem(Spacer)
        News_GL = QtWidgets.QGridLayout(self.CentralWidget)
        News_GL.addLayout(Filter_HL, 0, 0, 1, 1)
        News_GL.addWidget(self.CurrentMessage, 1, 0, 1, 1)
        News_GL.addLayout(NewsButtons_VL, 1, 1, 1, 1)
        GridLayout.addLayout(News_GL, 1, 0, 1, 1)
#
        Inspector_VL = QtWidgets.QVBoxLayout()
        SelectedObject_HL = QtWidgets.QHBoxLayout()
        SelectedObject_HL.setSpacing(0)
        Spacer = QtWidgets.QSpacerItem(90, 0, FixedSize, MinSize)
        SelectedObject_HL.addItem(Spacer)
        Spacer = QtWidgets.QSpacerItem(0, 0, ExpandSize, MinSize)
        SelectedObject_HL.addItem(Spacer)
        self.SelectedObject = QtWidgets.QLabel(self.CentralWidget)
#
        self.SelectedObject.setText("Selected Object")
#
        SelectedObject_HL.addWidget(self.SelectedObject)
        SelectedObject_HL.addItem(Spacer)
        NewStyle = "QPushButton { padding: 5px 5px 5px 5px; border-width: 0px;background-color: transparent }"
        Icon = QtGui.QIcon(":/Icons/Starbase")
        self.ShowStarbase = QtWidgets.QPushButton(self.CentralWidget)
        self.ShowStarbase.setIcon(Icon)
        self.ShowStarbase.setIconSize(QtCore.QSize(30, 30))
        self.ShowStarbase.setStyleSheet(NewStyle)
        self.ShowStarbase.setVisible(True)
        self.SelectNextObject = QtWidgets.QPushButton(self.CentralWidget)
        Icon = QtGui.QIcon(":/Icons/Triangle")
        self.SelectNextObject.setIcon(Icon)
        self.SelectNextObject.setIconSize(QtCore.QSize(30, 30))
        self.SelectNextObject.setStyleSheet(NewStyle)
        self.SelectNextObject.setVisible(True)
        self.ButtonSpacer = QtWidgets.QSpacerItem(10, 0, FixedSize, MinSize)
        SelectedObject_HL.addItem(self.ButtonSpacer)
        SelectedObject_HL.addWidget(self.ShowStarbase)
        SelectedObject_HL.addWidget(self.SelectNextObject)
        Inspector_VL.addLayout(SelectedObject_HL)
#
        self.Inspector = QtWidgets.QGraphicsView(self.CentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(ExpandSize, MinSize)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.Inspector.setSizePolicy(sizePolicy)
        self.Inspector.setMaximumSize(QtCore.QSize(1200, 450))
        Inspector_VL.addWidget(self.Inspector)
        GridLayout.addLayout(Inspector_VL, 1, 1, 1, 1)
        self.setCentralWidget(self.CentralWidget)
#
        self.Buttons = ToolBar(self)
#        self.Buttons.setAutoFillBackground(True)
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
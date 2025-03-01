
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QComboBox
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton

from guidesign import GuiDesign



class NewGame(QWidget):

    def __init__(self, people, rules):
        super(self.__class__, self).__init__()
        self.setWindowTitle("New Game")
        self.setStyleSheet(GuiDesign.getSetupStyle())
        Icon = QIcon()
        Icon.addPixmap(QPixmap(":/Icons/Host"))
        self.setWindowIcon(Icon)
        self.setFixedSize(800, 600)
        self.hide()

        LeftSide = QWidget()
        SimpleSetup = QWidget()
        FactionBox = QGroupBox()
        FactionBox.setTitle('Player Faction')
        Faction_VL = QVBoxLayout(FactionBox)
        FactionSelector = QComboBox()
        Faction_VL.addWidget(FactionSelector)
        self.FactionSetup = QPushButton()
        self.FactionSetup.setText('Customize Faction')
        Faction_VL.addWidget(self.FactionSetup)

        GameBox = QGroupBox()
        GameBox.setTitle('Advanced Game')
        Game_VL = QVBoxLayout(GameBox)
        AdvancedGame = QPushButton()
        AdvancedGame.setText('Advanced Game Configuration')
        Explanation = QLabel('This button allows You to configure multi-player games '
                             'and customize advanced game options. You do not need to '
                             'press it to launch standard single player games.')
        Explanation.setWordWrap(True)
        Game_VL.addWidget(Explanation)
        Game_VL.addWidget(AdvancedGame)

        Buttons_HL = QHBoxLayout()
        self.SoloStart = QPushButton()
        self.SoloStart.setText("OK")
        self.SoloStart.setToolTip(" Start a new game with default settings.")
        self.SoloStart.setFixedSize(160, 50)
        Buttons_HL.addWidget(self.SoloStart)
        Cancel = QPushButton()
        Cancel.setText("Cancel")
        Cancel.setToolTip(" Close this dialog.")
        Cancel.setFixedSize(160, 50)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(Cancel)
        self.Help = QPushButton()
        self.Help.setText("Help")
        self.Help.setToolTip(" Read the game manual.")
        self.Help.setFixedSize(160, 50)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(self.Help)

        Right_VL = QVBoxLayout(SimpleSetup)
        Right_VL.addWidget(FactionBox)
        Right_VL.addSpacing(20)
        Right_VL.addWidget(GameBox)
        Right_VL.addStretch()
        Right_VL.addLayout(Buttons_HL)
        Right_VL.addSpacing(15)

        SizeBox = QGroupBox()
        SizeBox.setTitle('Universe Size')
        self.TinyMap = QRadioButton('Tiny')
        self.SmallMap = QRadioButton('Small')
        self.MediumMap = QRadioButton('Medium')
        self.LargeMap = QRadioButton('Large')
        self.HugeMap = QRadioButton('Huge')
        Size_VL = QVBoxLayout(SizeBox)
        Size_VL.setSpacing(0)
        Size_VL.addWidget(self.TinyMap)
        Size_VL.addWidget(self.SmallMap)
        Size_VL.addWidget(self.MediumMap)
        Size_VL.addWidget(self.LargeMap)
        Size_VL.addWidget(self.HugeMap)
        self.SmallMap.setChecked(True)

        ModeBox = QGroupBox()
        ModeBox.setTitle('Difficulty Level')
        self.EasyMode = QRadioButton('Easy')
        self.StandardMode = QRadioButton('Standard')
        self.HarderMode = QRadioButton('Harder')
        self.ExpertMode = QRadioButton('Expert')
        Mode_VL = QVBoxLayout(ModeBox)
        Mode_VL.setSpacing(0)
        Mode_VL.addWidget(self.EasyMode)
        Mode_VL.addWidget(self.StandardMode)
        Mode_VL.addWidget(self.HarderMode)
        Mode_VL.addWidget(self.ExpertMode)
        self.StandardMode.setChecked(True)

        Left_VL = QVBoxLayout(LeftSide)
        Left_VL.setSpacing(0)
        Left_VL.addWidget(ModeBox)
        Left_VL.addSpacing(20)
        Left_VL.addWidget(SizeBox)
        Left_VL.addStretch()

        AdvancedSetup = QWidget()


        self.RightSide = QStackedLayout()
        self.RightSide.addWidget(SimpleSetup)
        self.RightSide.addWidget(AdvancedSetup)

        Layout_HL = QHBoxLayout(self)
        Layout_HL.setSpacing(0)
        Layout_HL.addWidget(LeftSide)
        Layout_HL.addLayout(self.RightSide)

        FactionSelector.addItem('Humanoid')
        FactionSelector.addItem('Rabbitoid')
        FactionSelector.addItem('Insectoid')
        FactionSelector.addItem('Nucletoid')
        FactionSelector.addItem('Silicanoid')
        FactionSelector.addItem('Antetheral')
        FactionSelector.addItem('Random')

        Cancel.clicked.connect(self.Hide)
        AdvancedGame.clicked.connect(self.AdvancedSetup)



    def AdvancedSetup(self):
        self.RightSide.setCurrentIndex(1)
        print('Setup advanced game ...')


    def Launch(self):
        self.RightSide.setCurrentIndex(0)
        self.show()
        print('New Game pressed ...')


    def Hide(self):
        self.hide()
        print('New Game closed ...')

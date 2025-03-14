
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QKeySequence
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QComboBox
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton

from guidesign import GuiDesign, GuiStyle



class NewGame(QWidget):

    def __init__(self, people, rules):
        super(self.__class__, self).__init__()
        self.setWindowTitle('New Game')
        self.setStyleSheet(GuiDesign.getStyle(GuiStyle.SimpleSetup))
        Icon = QIcon()
        Icon.addPixmap(QPixmap(':/Icons/Host'))
        self.setWindowIcon(Icon)
        self.setFixedSize(800, 600)
        self.hide()

        LeftSide = QWidget()
        RightSide = QWidget()
        FactionBox = QGroupBox()
        FactionBox.setTitle('Player Faction')
        Faction_VL = QVBoxLayout(FactionBox)
        self.FactionSelector = QComboBox()
        Faction_VL.addWidget(self.FactionSelector)
        self.FactionSetup = QPushButton()
        self.FactionSetup.setText('Customize &Faction')
        self.FactionSetup.setShortcut(QKeySequence('Ctrl+F'))
        Faction_VL.addWidget(self.FactionSetup)

        GameBox = QGroupBox()
        GameBox.setTitle('Advanced Game')
        Game_VL = QVBoxLayout(GameBox)
        self.AdvancedGame = QPushButton()
        self.AdvancedGame.setText('&Advanced Game Configuration')
        self.AdvancedGame.setShortcut(QKeySequence('Ctrl+A'))
        Explanation = QLabel('This button allows You to configure multi-player games '
                             'and customize advanced game options. You do not need to '
                             'press it to launch standard single player games.')
        Explanation.setWordWrap(True)
        Game_VL.addWidget(Explanation)
        Game_VL.addWidget(self.AdvancedGame)

        ButtonSize = QSize(160, 50)
        Buttons_HL = QHBoxLayout()
        self.SoloStart = QPushButton()
        self.SoloStart.setText('&OK')
        self.SoloStart.setToolTip(' Start a new game with default settings.')
        self.SoloStart.setShortcut(QKeySequence('Ctrl+O'))
        self.SoloStart.setFixedSize(ButtonSize)
        Buttons_HL.addWidget(self.SoloStart)
        Cancel = QPushButton()
        Cancel.setText('&Cancel')
        Cancel.setToolTip(' Close this dialog.')
        Cancel.setShortcut(QKeySequence('Ctrl+C'))
        Cancel.setFixedSize(ButtonSize)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(Cancel)
        self.Help = QPushButton()
        self.Help.setText('&Help')
        self.Help.setToolTip(' Read the game manual.')
        self.Help.setShortcut(QKeySequence('Ctrl+H'))
        self.Help.setFixedSize(ButtonSize)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(self.Help)

        Right_VL = QVBoxLayout(RightSide)
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

        Layout_HL = QHBoxLayout(self)
        Layout_HL.setSpacing(0)
        Layout_HL.addWidget(LeftSide)
        Layout_HL.addWidget(RightSide)

        for ai in people.AIFaction:
            self.FactionSelector.addItem(ai.Species)
        self.FactionSelector.addItem('Random')

        Cancel.clicked.connect(self.hide)


    def ConfigureGame(self):
        self.FactionSelector.setCurrentIndex(0)
        self.SmallMap.setChecked(True)
        self.StandardMode.setChecked(True)
        self.show()

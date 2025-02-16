
from PyQt6.QtWidgets import QWidget
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
        self.setMaximumSize(800, 600)
        self.setMinimumSize(800, 600)
        self.hide()
        Layout_HL = QHBoxLayout(self)
        Layout_HL.setSpacing(0)
        LeftSide = QWidget()
        Left_VL = QVBoxLayout(LeftSide)
        Left_VL.setSpacing(0)
        RightSide = QStackedLayout()
        SimpleSetup = QWidget()
        RightSide.addWidget(SimpleSetup)
        
        Right_VL = QVBoxLayout(SimpleSetup)
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
        self.AdvancedGame = QPushButton()
        self.AdvancedGame.setText('Advanced Game Configuration')
        Game_VL.addWidget(self.AdvancedGame)

        Right_VL.addWidget(FactionBox)
        Right_VL.addSpacing(10)
        Right_VL.addWidget(GameBox)
        Right_VL.addStretch()

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
        
        Left_VL.addWidget(ModeBox)
        Left_VL.addSpacing(20)
        Left_VL.addWidget(SizeBox)
        Left_VL.addStretch()

        Layout_HL.addWidget(LeftSide)
        Layout_HL.addLayout(RightSide)

        FactionSelector.addItem('Humanoid')
        FactionSelector.addItem('Rabbitoid')
        FactionSelector.addItem('Insectoid')
        FactionSelector.addItem('Nucletoid')
        FactionSelector.addItem('Silicanoid')
        FactionSelector.addItem('Antetheral')
        FactionSelector.addItem('Random')
        


    def Launch(self):
        self.show()
        print('New Game pressed ...')
        

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton, QLineEdit

from guidesign import GuiDesign



class GameSetup(QWidget):

    def __init__(self, people, rules):
        super(self.__class__, self).__init__()
        self.setWindowTitle("Advanced New Game Wizard - Step 1 of 3")
        self.setStyleSheet(GuiDesign.getSetupStyle())
        Icon = QIcon()
        Icon.addPixmap(QPixmap(":/Icons/Host"))
        self.setWindowIcon(Icon)
        self.setFixedSize(1000, 750)
        self.hide()
        Layout_VL = QVBoxLayout(self)
        Wizard = QWidget()
        self.Pages = QStackedLayout(Wizard)
        self.SetupUniverse()
        self.SetupPlayers()
        self.SetupVictoryConditions()
        ButtonSize = QSize(140, 50)
        self.CurrentPage = 0

        Buttons_HL = QHBoxLayout()
        self.Finish = QPushButton()
        self.Finish.setText('Finish')
        self.Finish.setToolTip(' Save the game settings.')
        self.Finish.setFixedSize(ButtonSize)
        self.Finish.setShortcut(QKeySequence('Ctrl+F'))
        Cancel = QPushButton()
        Cancel.setText("Cancel")
        Cancel.setToolTip(" Close this dialog.")
        Cancel.setFixedSize(ButtonSize)
        Cancel.setShortcut(QKeySequence('Ctrl+C'))
        self.Help = QPushButton()
        self.Help.setText("Help")
        self.Help.setToolTip(" Read the game manual.")
        self.Help.setFixedSize(ButtonSize)
        self.Help.setShortcut(QKeySequence('Ctrl+H'))
        self.Next = QPushButton()
        self.Next.setText("Next")
        self.Next.setToolTip(" Proceed to the next page.")
        self.Next.setFixedSize(ButtonSize)
        self.Next.setShortcut(QKeySequence('Ctrl+N'))
        self.Back = QPushButton()
        self.Back.setText("Back")
        self.Back.setToolTip(" Return to the previous page.")
        self.Back.setFixedSize(ButtonSize)
        self.Back.setShortcut(QKeySequence('Ctrl+B'))
        self.Back.setEnabled(False)

        Buttons_HL.addSpacing(30)
        Buttons_HL.addWidget(self.Help)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(Cancel)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(self.Back)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(self.Next)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(self.Finish)
        Buttons_HL.addSpacing(30)

        Layout_VL.addWidget(Wizard)
        Layout_VL.addLayout(Buttons_HL)

        self.Finish.clicked.connect(self.SaveGameData)
        self.Back.clicked.connect(self.Revert)
        self.Next.clicked.connect(self.Proceed)
        Cancel.clicked.connect(self.hide)


    def Proceed(self):
        print('Proceed ' + str(self.CurrentPage))
        if self.CurrentPage < 2:
            self.CurrentPage += 1
            self.Pages.setCurrentIndex(self.CurrentPage)
            self.Back.setEnabled(True)
            self.Next.setEnabled(self.CurrentPage < 2)


    def Revert(self):
        print('Revert ' + str(self.CurrentPage))
        if 0 < self.CurrentPage:
            self.CurrentPage -= 1
            self.Pages.setCurrentIndex(self.CurrentPage)
            self.Next.setEnabled(True)
            self.Back.setEnabled(self.CurrentPage > 0)


    def ConfigureGame(self):
        self.CurrentPage = 0
        self.Pages.setCurrentIndex(0)
        self.ModerateDistance.setChecked(True)
        self.NormalMode.setChecked(True)
        self.SmallMap.setChecked(True)
        self.Next.setEnabled(True)
        self.Back.setEnabled(False)
        self.MaxMinerals.setChecked(False)
        self.SlowerTech.setChecked(False)
        self.AcceleratedGame.setChecked(False)
        self.NoRandomEvents.setChecked(False)
        self.AIAlliances.setChecked(False)
        self.PublicScores.setChecked(False)
        self.GalaxyClumping.setChecked(False)
        self.GameName.setText('')
        self.show()


    def SaveGameData(self):
        print('Game data saved to file ...')



    def SetupUniverse(self):
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
        DensityBox = QGroupBox()
        DensityBox.setTitle('Density')
        self.SparseMode = QRadioButton('Sparse')
        self.NormalMode = QRadioButton('Normal')
        self.DenseMode = QRadioButton('Dense')
        self.PackedMode = QRadioButton('Packed')
        Density_VL = QVBoxLayout(DensityBox)
        Density_VL.setSpacing(0)
        Density_VL.addWidget(self.SparseMode)
        Density_VL.addWidget(self.NormalMode)
        Density_VL.addWidget(self.DenseMode)
        Density_VL.addWidget(self.PackedMode)
        self.NormalMode.setChecked(True)
        PlayerBox = QGroupBox()
        PlayerBox.setTitle('Player Positions')
        PlayerBox.setMinimumWidth(300)
        self.CloseDistance = QRadioButton('Close')
        self.ModerateDistance = QRadioButton('Moderate')
        self.FartherDistance = QRadioButton('Farther')
        self.LargeDistance = QRadioButton('Distant')
        Player_VL = QVBoxLayout(PlayerBox)
        Player_VL.setSpacing(0)
        Player_VL.addWidget(self.CloseDistance)
        Player_VL.addWidget(self.ModerateDistance)
        Player_VL.addWidget(self.FartherDistance)
        Player_VL.addWidget(self.LargeDistance)
        self.ModerateDistance.setChecked(True)
        LeftSide = QWidget()
        LeftSide.setMinimumWidth(240)
        Left_VL = QVBoxLayout(LeftSide)
        Left_VL.setSpacing(0)
        Left_VL.addWidget(SizeBox)
        Left_VL.addSpacing(20)
        Left_VL.addWidget(DensityBox)
        Left_VL.addStretch()
        ButtonStyle = 'font-size: 20pt;font-style: oblique;font-weight: 400;'
        self.MaxMinerals = QRadioButton(' &Beginner: Abundance of Minerals')
        self.MaxMinerals.setStyleSheet(ButtonStyle)
        self.MaxMinerals.setShortcut(QKeySequence('Ctrl+B'))
        self.SlowerTech = QRadioButton(' &Slower Advances in Technology')
        self.SlowerTech.setStyleSheet(ButtonStyle)
        self.SlowerTech.setShortcut(QKeySequence('Ctrl+S'))
        self.AcceleratedGame = QRadioButton(' Acclererated &Multi-player Game')
        self.AcceleratedGame.setStyleSheet(ButtonStyle)
        self.AcceleratedGame.setShortcut(QKeySequence('Ctrl+M'))
        self.NoRandomEvents = QRadioButton(' No &Random Events')
        self.NoRandomEvents.setStyleSheet(ButtonStyle)
        self.NoRandomEvents.setShortcut(QKeySequence('Ctrl+R'))
        self.AIAlliances = QRadioButton(' Computer Players form &Alliances')
        self.AIAlliances.setStyleSheet(ButtonStyle)
        self.AIAlliances.setShortcut(QKeySequence('Ctrl+A'))
        self.PublicScores = QRadioButton(' &Public Player Scores')
        self.PublicScores.setStyleSheet(ButtonStyle)
        self.PublicScores.setShortcut(QKeySequence('Ctrl+P'))
        self.GalaxyClumping = QRadioButton(' &Galaxy features Star Clusters')
        self.GalaxyClumping.setStyleSheet(ButtonStyle)
        self.GalaxyClumping.setShortcut(QKeySequence('Ctrl+G'))
        RightSide = QWidget()
        Right_VL = QVBoxLayout(RightSide)
        Right_VL.setSpacing(0)
        Right_VL.addWidget(PlayerBox)
        Right_VL.addSpacing(20)
        Right_VL.addWidget(self.MaxMinerals)
        Right_VL.addWidget(self.SlowerTech)
        Right_VL.addWidget(self.AcceleratedGame)
        Right_VL.addWidget(self.NoRandomEvents)
        Right_VL.addWidget(self.AIAlliances)
        Right_VL.addWidget(self.PublicScores)
        Right_VL.addWidget(self.GalaxyClumping)
        Right_VL.addStretch()
        Layout_HL = QHBoxLayout()
        Layout_HL.setSpacing(0)
        Layout_HL.addWidget(LeftSide)
        Layout_HL.addSpacing(20)
        Layout_HL.addWidget(RightSide)
        Layout_HL.addStretch()
        self.GameName = QLineEdit()
        self.GameName.setPlaceholderText('Silent Running')
        self.GameName.setMaxLength(56)
        self.GameName.setMinimumWidth(670)
        NameLabel = QLabel('Game Name:')
        NameLabel.setStyleSheet('font-size: 20pt;font-style: oblique;font-weight: 600;')
        Game_HL = QHBoxLayout()
        Game_HL.addStretch()
        Game_HL.addWidget(NameLabel)
        Game_HL.addSpacing(20)
        Game_HL.addWidget(self.GameName)
        Game_HL.addSpacing(20)
        GameWorld = QWidget()
        Layout_VL = QVBoxLayout(GameWorld)
        Layout_VL.addLayout(Game_HL)
        Layout_VL.addSpacing(10)
        Layout_VL.addLayout(Layout_HL)
        Layout_VL.addStretch()
        self.Pages.addWidget(GameWorld)


    def SetupPlayers(self):
        PlayerSetup = QWidget()
        self.Pages.addWidget(PlayerSetup)


    def SetupVictoryConditions(self):
        VictorySettings = QWidget()
        self.Pages.addWidget(VictorySettings)


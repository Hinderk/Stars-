
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QHeaderView
from PyQt6.QtWidgets import QTableView, QMenu
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton, QLineEdit

from defines import PlayerType as PT
from defines import AIMode as AI
from guidesign import GuiDesign, GuiStyle
from playerdata import PlayerData




class GameSetup(QWidget):

    AIModes = [AI.AI0, AI.AI1, AI.AI2, AI.AI3, AI.AIR]

    def __init__(self, people, rules):
        super(self.__class__, self).__init__()
        self.setWindowTitle("Advanced New Game Wizard - Step 1 of 3")
        self.setStyleSheet(GuiDesign.getStyle(GuiStyle.AdvancedSetup_1))
        Icon = QIcon()
        Icon.addPixmap(QPixmap(":/Icons/Host"))
        self.setWindowIcon(Icon)
        self.setFixedSize(1000, 750)
        self.hide()
        self.Wizard = QWidget()
        self.Pages = QStackedLayout(self.Wizard)
        self.CurrentPage = 0
        self.NumberOfPlayers = 6              # Where to define these defaults?
        self.Factions = people
        self.SetupUniverse()
        self.SetupPlayers(people)
        self.SetupVictoryConditions()
        self.SetupMenu(people)
        self.SetupButtons()


    def SetupButtons(self):
        ButtonSize = QSize(140, 50)
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
        Layout_VL = QVBoxLayout(self)
        Layout_VL.addWidget(self.Wizard)
        Layout_VL.addLayout(Buttons_HL)
        self.Finish.clicked.connect(self.SaveGameData)
        self.Back.clicked.connect(self.Revert)
        self.Next.clicked.connect(self.Proceed)
        Cancel.clicked.connect(self.hide)


    def Proceed(self):
        if self.CurrentPage < 2:
            self.CurrentPage += 1
            step = 'Step ' + str(1 + self.CurrentPage) + ' of 3'
            self.setWindowTitle('Advanced New Game Wizard - ' + step)
            self.Pages.setCurrentIndex(self.CurrentPage)
            self.Back.setEnabled(True)
            self.Next.setEnabled(self.CurrentPage < 2)


    def Revert(self):
        if 0 < self.CurrentPage:
            self.CurrentPage -= 1
            step = 'Step ' + str(1 + self.CurrentPage) + ' of 3'
            self.setWindowTitle('Advanced New Game Wizard - ' + step)
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


    def SetupMenu(self, people):
        self.Select = QMenu()
        self.Select.setStyleSheet(GuiDesign.getStyle(GuiStyle.PlayerMenu))
        pf = self.Select.addMenu('Predefined Faction ')
        n = 1
        for ai in people.AIFaction:
            a = pf.addAction(ai.Species)
            a.setData((0, n, 0))
            n += 1
        a = pf.addAction('Random')
        a.setData((0, 0, 0))
        cf = self.Select.addMenu('Custom Faction')
        a = cf.addAction('New Faction')
        a.setData((1, 0, 0))
        a = cf.addAction('Open File')
        a.setData((1, 1, 0))
        cf.addSeparator()
        n = 0
        for pc in people.PlayerFaction:
            a = cf.addAction(pc.Name)
            a.setData((1, 2, n))
            n += 1
        self.Select.addSeparator()
        cp = self.Select.addMenu('Computer Player')
        n = 1
        for ai in people.AIFaction:
            cpm = cp.addMenu(ai.Name + ' ')
            m = 0
            for mode in AI:
                a = cpm.addAction(mode.value)
                a.setData((2, n, m))
                m += 1
            n += 1
        cpm = cp.addMenu('Random')
        m = 0
        for mode in AI:
            a = cpm.addAction(mode.value)
            a.setData((2, 0, m))
            m += 1
        self.Select.addSeparator()
        a = self.Select.addAction('Expansion Slot')
        a.setData((3, 0, 0))
        self.Select.addSeparator()
        a = self.Select.addAction('Remove Player')
        a.setData((4, 0, 0))


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


    def SetupPlayers(self, people):
        self.Model = PlayerData()
        self.Players = QTableView()
        self.Players.setShowGrid(False)
        self.Players.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Players.setModel(self.Model)
        align = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        Header_H = self.Players.horizontalHeader()
        Header_H.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        Header_H.setStretchLastSection(True)
        Header_H.resizeSection(0, 200)
        Header_H.resizeSection(1, 200)
        Header_H.setDefaultAlignment(align)
        Header_V = self.Players.verticalHeader()
        Header_V.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        Header_V.setDefaultSectionSize(48)
        Header_V.setDefaultAlignment(align)
        self.Model.AddPlayer(0, PT.HUP, None, people.myFaction())
        n = 1
        while n < self.NumberOfPlayers:
            self.Model.AddPlayer(n, PT.AIP, AI.AI1, people.getAIFaction(n))
            n += 1
        Layout_HL = QHBoxLayout()
        Layout_HL.addSpacing(20)
        Layout_HL.addWidget(self.Players)
        Layout_HL.addSpacing(20)
        PlayerSetup = QWidget()
        PlayerSetup.setStyleSheet(GuiDesign.getStyle(GuiStyle.AdvancedSetup_2))
        Layout_VL = QVBoxLayout(PlayerSetup)
        Layout_VL.addLayout(Layout_HL)
        Layout_VL.addSpacing(10)
        self.Pages.addWidget(PlayerSetup)
        self.Players.clicked.connect(self.SelectPlayer)


    def SelectPlayer(self, select):
        if select.column() < 2:
            here = self.cursor().pos()
            selected = self.Select.exec(here)
            if selected:
                pType = PT.HUP
                pMode = None
                ID, fID, mID = selected.data()
                if ID == 0:
                    if fID > 0:
                        fnew = self.Factions.getAIFaction(fID - 1)
                    else:
                        pType = PT.RNG
                        fnew = self.Factions.randomFaction()
                if ID == 1:
                    fnew = self.Factions.myFaction()   # FIX ME
                    if fID == 0:
                        print('Design New Faction')
                    if fID == 1:
                        print('Load a design file')
                    if fID == 2:
                        fnew = self.Factions.getFaction(mID)
                if ID == 2:
                    if fID > 0:
                        fnew = self.Factions.getAIFaction(fID - 1)
                        pType = PT.AIP
                    else:
                        pType = PT.RNG
                        fnew = self.Factions.randomFaction()
                    pMode = self.AIModes[mID]
                if ID == 3:
                    fnew = self.Factions.myFaction()   # FIX ME
                    pType = PT.EXP
                if ID == 4:
                    self.Model.RemovePlayer(select.row())
                    return
                self.Model.AddPlayer(select.row(), pType, pMode, fnew)


    def SetupVictoryConditions(self):
        VictorySettings = QWidget()
        self.Pages.addWidget(VictorySettings)

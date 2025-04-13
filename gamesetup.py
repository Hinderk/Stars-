
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QHeaderView
from PyQt6.QtWidgets import QTableView, QMenu
from PyQt6.QtWidgets import QStackedLayout, QSpinBox
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton, QLineEdit

from defines import PlayerType as PT
from defines import AIMode as AI
from guidesign import GuiDesign, GuiStyle
from victory import Victory
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
        self.GameFeature = []
        self.NumberOfPlayers = rules.GetNumberOfPlayers()
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


    def ConfigureGame(self, MapSize):
        self.CurrentPage = 0
        self.Pages.setCurrentIndex(0)
        self.PlayerDistance[1].setChecked(True)
        self.StarDensity[1].setChecked(True)
        index = 0
        for m in MapSize:
            if m.isChecked():
                break
            index += 1
        self.MapSize[index].setChecked(True)
        self.Next.setEnabled(True)
        self.Back.setEnabled(False)
        for rb in self.GameFeature:
            rb.setChecked(False)
        self.GameName.setText('')
        self.RestoreVictoryConditions()
        self.Model.ResetModel(self.Factions, self.NumberOfPlayers)
        self.show()


    def SaveGameData(self):
        SaveGame = QFileDialog(self)
        SaveGame.setOption( SaveGame.Option.DontUseNativeDialog)
        SaveGame.setStyleSheet(GuiDesign.getStyle(GuiStyle.FileBrowser))
        SaveGame.setMinimumSize(1000, 750)
        SaveGame.setFileMode(SaveGame.FileMode.AnyFile)
        SaveGame.setViewMode(SaveGame.ViewMode.List)
        SaveGame.setAcceptMode(SaveGame.AcceptMode.AcceptSave)
        SaveGame.setNameFilters(['Game Files (*.xy)', 'All Files (*.*)'])
        SaveGame.setDefaultSuffix('xy')
        if SaveGame.exec():
            Files = SaveGame.selectedFiles()
            try:
                f = open(Files[0], 'wt')
                name = self.GameName.text()
                if not name:
                    name = 'Silent Running'
                f.write('setup.advanced.name: ' + name)
                GameData = [name]
                for rb in self.MapSize:
                    if rb.isChecked():
                        GameData.append(self.MapSize.index(rb))
                        f.write('\nsetup.advanced.size: ' + rb.text())
                for rb in self.StarDensity:
                    if rb.isChecked():
                        GameData.append(self.StarDensity.index(rb))
                        f.write('\nsetup.advanced.density: ' + rb.text())
                for rb in self.PlayerDistance:
                    if rb.isChecked():
                        GameData.append(self.PlayerDistance.index(rb))
                        f.write('\nsetup.advanced.distance: ' + rb.text())
                f.write('\nsetup.advanced.featureset:')
                for rb in self.GameFeature:
                    if rb.isChecked():
                        f.write(' 1')
                        GameData.append(1)
                    else:
                        f.write(' 0')
                        GameData.append(0)

                for vc in Victory:
                    radio, spinner = self.VictoryCondition[vc]
                    f.write('\nsetup.advanced.distance: ' + radio.text())
                    if radio.isChecked():
                        GameData.append(spinner.value())
                    else:
                        GameData.append(0)
                f.close()
            except OSError:
                print('Couldn\'t open file!')

        print(GameData)


    def SetupMenu(self, people):
        self.Select = QMenu()
        self.Select.setStyleSheet(GuiDesign.getStyle(GuiStyle.PlayerMenu))
        pf = self.Select.addMenu('Predefined Faction  ')
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
            cpm = cp.addMenu(ai.Name + '  ')
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


    def AddGameFeature(self, layout, text, hotkey):
        rb = QRadioButton(text)
        rb.setStyleSheet('font-size: 20pt;font-style: oblique;font-weight: 400;')
        rb.setShortcut(QKeySequence(hotkey))
        layout.addWidget(rb)
        self.GameFeature.append(rb)


    def SetupUniverse(self):
        SizeBox = QGroupBox()
        SizeBox.setTitle('Universe Size')
        Tiny = QRadioButton('Tiny')
        Small = QRadioButton('Small')
        Medium = QRadioButton('Medium')
        Large = QRadioButton('Large')
        Huge = QRadioButton('Huge')
        self.MapSize = [Tiny, Small, Medium, Large, Huge]
        Size_VL = QVBoxLayout(SizeBox)
        Size_VL.setSpacing(0)
        Size_VL.addWidget(Tiny)
        Size_VL.addWidget(Small)
        Size_VL.addWidget(Medium)
        Size_VL.addWidget(Large)
        Size_VL.addWidget(Huge)
        Small.setChecked(True)
        DensityBox = QGroupBox()
        DensityBox.setTitle('Density')
        Sparse = QRadioButton('Sparse')
        Normal = QRadioButton('Normal')
        Dense = QRadioButton('Dense')
        Packed = QRadioButton('Packed')
        self.StarDensity = [Sparse, Normal, Dense, Packed]
        Density_VL = QVBoxLayout(DensityBox)
        Density_VL.setSpacing(0)
        Density_VL.addWidget(Sparse)
        Density_VL.addWidget(Normal)
        Density_VL.addWidget(Dense)
        Density_VL.addWidget(Packed)
        Normal.setChecked(True)
        PlayerBox = QGroupBox()
        PlayerBox.setTitle('Player Positions')
        PlayerBox.setMinimumWidth(300)
        Close = QRadioButton('Close')
        Moderate = QRadioButton('Moderate')
        Farther = QRadioButton('Farther')
        Large = QRadioButton('Distant')
        self.PlayerDistance = [Close, Moderate, Farther, Large]
        Player_VL = QVBoxLayout(PlayerBox)
        Player_VL.setSpacing(0)
        Player_VL.addWidget(Close)
        Player_VL.addWidget(Moderate)
        Player_VL.addWidget(Farther)
        Player_VL.addWidget(Large)
        Moderate.setChecked(True)
        LeftSide = QWidget()
        LeftSide.setMinimumWidth(240)
        Left_VL = QVBoxLayout(LeftSide)
        Left_VL.setSpacing(0)
        Left_VL.addWidget(SizeBox)
        Left_VL.addSpacing(20)
        Left_VL.addWidget(DensityBox)
        Left_VL.addStretch()
        RightSide = QWidget()
        Right_VL = QVBoxLayout(RightSide)
        Right_VL.setSpacing(0)
        Right_VL.addWidget(PlayerBox)
        Right_VL.addSpacing(20)
        self.AddGameFeature(Right_VL, ' &Beginner: Abundance of Minerals', 'Ctrl+B')
        self.AddGameFeature(Right_VL, ' &Slower Advances in Technology', 'Ctrl+S')
        self.AddGameFeature(Right_VL, ' Acclererated &Multi-player Game', 'Ctrl+M')
        self.AddGameFeature(Right_VL, ' No &Random Events', 'Ctrl+R')
        self.AddGameFeature(Right_VL, ' Computer Players form &Alliances', 'Ctrl+A')
        self.AddGameFeature(Right_VL, ' &Public Player Scores', 'Ctrl+P')
        self.AddGameFeature(Right_VL, ' &Galaxy features Star Clusters', 'Ctrl+G')
        Right_VL.addStretch()
        Layout_HL=QHBoxLayout()
        Layout_HL.setSpacing(0)
        Layout_HL.addWidget(LeftSide)
        Layout_HL.addSpacing(20)
        Layout_HL.addWidget(RightSide)
        Layout_HL.addStretch()
        self.GameName=QLineEdit()
        self.GameName.setPlaceholderText('Silent Running')
        self.GameName.setMaxLength(56)
        self.GameName.setMinimumWidth(670)
        NameLabel=QLabel('Game Name:')
        NameLabel.setStyleSheet('font-size: 20pt;font-style: oblique;font-weight: 600;')
        Game_HL=QHBoxLayout()
        Game_HL.addStretch()
        Game_HL.addWidget(NameLabel)
        Game_HL.addSpacing(20)
        Game_HL.addWidget(self.GameName)
        Game_HL.addSpacing(20)
        GameWorld=QWidget()
        Layout_VL=QVBoxLayout(GameWorld)
        Layout_VL.addLayout(Game_HL)
        Layout_VL.addSpacing(10)
        Layout_VL.addLayout(Layout_HL)
        Layout_VL.addStretch()
        self.Pages.addWidget(GameWorld)


    def SetupPlayers(self, people):
        self.Model = PlayerData(people, self.NumberOfPlayers)
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


    def AddVictoryCondition(self, vlayout, vc):
        msg, suffix, default, low, high, step, width, select = vc.value
        data = QSpinBox()
        if suffix:
            data.setSuffix(suffix)
        data.setRange(low, high)
        data.setValue(default)
        data.setSingleStep(step)
        data.setMinimumSize(QSize(width, 40))
        data.setAlignment(Qt.AlignmentFlag.AlignLeft)
        radio = QRadioButton('  ' + msg)
        radio.setChecked(select)
        radio.setAutoExclusive(False)
        hlayout = QHBoxLayout()
        hlayout.addWidget(radio)
        hlayout.addWidget(data)
        hlayout.addStretch()
        vlayout.addLayout(hlayout)
        self.VictoryCondition[vc] = (radio, data)
        radio.toggled.connect(self.AdjustConditionCount)


    def AdjustConditionCount(self, enabled):
        if enabled:
            self.ConditionCounter += 1
        else:
            self.ConditionCounter -= 1
        self.ActiveConditions.setRange(0, self.ConditionCounter)


    def SetupVictoryConditions(self):
        Title = QLabel('Victory is declared if some of these conditions are met:')
        VictorySettings = QWidget()
        VictorySettings.setStyleSheet(GuiDesign.getStyle(GuiStyle.AdvancedSetup_3))
        Layout_VL = QVBoxLayout(VictorySettings)
        Layout_VL.setSpacing(0)
        Layout_VL.addWidget(Title)
        Layout_VL.addSpacing(20)
        self.VictoryCondition = dict()
        self.ConditionCounter = 4
        for vc in Victory:
            self.AddVictoryCondition(Layout_VL, vc)
        Layout_VL.addSpacing(40)
        label = QLabel('The following number of selected conditions must be met:')
        self.ActiveConditions = QSpinBox()
        self.ActiveConditions.setRange(0, 4)
        self.ActiveConditions.setValue(1)
        self.ActiveConditions.setMinimumSize(QSize(60, 40))
        self.ActiveConditions.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ActiveConditions.setStyleSheet('font-weight: 600;')
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.ActiveConditions)
        layout.addStretch()
        Layout_VL.addLayout(layout)
        Layout_VL.addSpacing(10)
        label = QLabel('These many years must pass before a winner is declared:')
        self.GameDuration = QSpinBox()
        self.GameDuration.setRange(30, 500)
        self.GameDuration.setSingleStep(10)
        self.GameDuration.setValue(50)
        self.GameDuration.setMinimumSize(QSize(85, 40))
        self.GameDuration.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.GameDuration.setStyleSheet('font-weight: 600;')
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.GameDuration)
        layout.addStretch()
        Layout_VL.addLayout(layout)
        Layout_VL.addStretch()
        self.Pages.addWidget(VictorySettings)


    def RestoreVictoryConditions(self):
        for vc in Victory:
            radio, spinner = self.VictoryCondition[vc]
            spinner.setValue(vc.value[2])
            radio.setChecked(vc.value[7])
        self.ConditionCounter = 4
        self.ActiveConditions.setRange(0, 4)
        self.ActiveConditions.setValue(1)
        self.GameDuration.setValue(50)

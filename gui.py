
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QStackedLayout, QSizePolicy
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QMainWindow, QPushButton, QToolButton
from PyQt6.QtWidgets import QStatusBar, QGroupBox, QCheckBox
from PyQt6.QtWidgets import QPlainTextEdit

from guidesign import GuiDesign
from defines import Stance
from menubar import Menu
from toolbar import ToolBar
from inspector import Inspector
from fleetdata import Fleetdata
from minedata import Minedata
from starmap import Starmap
from universe import Universe
from newgame import NewGame
from gamesetup import GameSetup



def _CreateButton(name):
    Style = "padding: 0px 2px 0px 2px;border-width: 0px;background-color: transparent"
    Icon = QIcon(name)
    Button = QPushButton()
    Button.setIcon(Icon)
    Button.setIconSize(QSize(30, 30))
    Button.setStyleSheet(Style)
    Button.setVisible(False)
    return Button



class Gui(QMainWindow):

    def __init__(self, people, rules):
        super(self.__class__, self).__init__()
        self.CurrentYear = rules.FirstYear()
        self.SelectedPlanet = None
        self.SelectedFleet = None
        self.SelectedFields = []
        self.SelectedFleets = []
        self.MineFilter = Universe.SetupMineFilter()
        self.NumberOfFields = 0
        self.FilteredFields = 0
        self.EnemyFleetIndex = 0
        self.NeutralFleetIndex = 0
        self.FleetIndex = 0
        self.MineIndex = 0
        self.FieldIndex = 0
        self.EnemyFleetOffset = 0
        self.NeutralFleetOffset = 0
        self.FleetOffset = 0
        self.MineOffset = 0
        self.AlliedFleets = 0
        self.NeutralFleets = 0
        self.HostileFleets = 0
        self.ShowFleetMovements = False
        self.WaypointMode = False
        self.setStyleSheet(GuiDesign.getGuiStyle())
        self.Action = dict()
        self.SetupUI(people, rules)
        self.Buttons.Zoom.setMenu(self.Menu.MenuZoom)
        self.Buttons.actionRadarView.toggled.connect(self.Map.Universe.ShowScannerRanges)
        self.Buttons.actionPlanetNames.toggled.connect(self.Map.Universe.ShowPlanetNames)
        self.Buttons.actionConcentrationView.toggled.connect(self.ShowCrustDiagrams)
        self.Buttons.actionSurfaceMineralView.toggled.connect(self.ShowSurfaceDiagrams)
        self.Buttons.actionDefaultView.toggled.connect(self.ShowDefaultView)
        self.Buttons.actionPopulationView.toggled.connect(self.ShowPopulationView)
        self.Buttons.actionNoInfoView.toggled.connect(self.ShowMinimalView)
        self.Buttons.actionPercentView.toggled.connect(self.ShowPercentageView)
        self.Buttons.actionFoes.toggled.connect(self.Map.Universe.EnableFoeFilter)
        self.Buttons.actionFriendlies.toggled.connect(self.Map.Universe.EnableFriendFilter)
        self.Buttons.actionShipCount.toggled.connect(self.Map.Universe.ShowShipCount)
        self.Buttons.actionWaitingFleets.toggled.connect(self.Map.Universe.FilterIdleFleets)
        self.Buttons.actionPathOverlay.toggled.connect(self.ShowMovements)
        self.Buttons.actionAddWaypoint.toggled.connect(self.AddWaypoints)
        self.NextField.clicked.connect(self.ShowNextMineField)
        self.PreviousField.clicked.connect(self.ShowPreviousMineField)
        self.Buttons.actionNoInfoView.setChecked(True)
        self.Buttons.RadarRange.valueChanged.connect(self.Map.Universe.ScaleRadarRanges)
        self.Menu.ChangeZoom.connect(self.Map.ResizeStarmap)
        self.Buttons.Mines.toggled.connect(self.Map.Universe.ShowFields)
        self.Buttons.ShowMines.connect(self.Map.Universe.ShowMines)
        self.Map.Universe.SelectField.connect(self.InspectMineField)
        self.Map.Universe.SelectFleet.connect(self.InspectFleet)
        self.Map.Universe.SelectPlanet.connect(self.InspectPlanet)
        self.Map.Universe.UpdatePlanet.connect(self.UpdatePlanetView)
        self.Map.Universe.UpdateFilter.connect(self.UpdateFields)
        self.Map.Universe.UpdateRoute.connect(self.FleetInfo.UpdateInfo)
        self.ShowPlanet.clicked.connect(self.InspectPlanets)
        self.SelectNextEnemy.clicked.connect(self.InspectHostileFleet)
        self.SelectNextNeutral.clicked.connect(self.InspectNeutralFleet)
        self.SelectNextFleet.clicked.connect(self.InspectAlliedFleet)
        self.ShowFields.clicked.connect(self.InspectMines)
        self.ShowFleets.clicked.connect(self.InspectFleets)
        self.Buttons.FilterEnemyFleets.connect(self.Map.Universe.FilterFoes)
        self.Buttons.FilterMyFleets.connect(self.Map.Universe.FilterFleets)
        self.Menu.actionNewGame.triggered.connect(self.NewGame.ConfigureGame)
        self.NewGame.AdvancedGame.clicked.connect(self.ConfigureGame)
        self.Map.Universe.HighlightPlanet(self.Map.Universe.planets[-1])

    def SetupUI(self, people, rules):

        sx, sy = GuiDesign.getSize()
        self.resize(sx, sy)
        self.setWindowTitle("My Stars!")
        Icon = QIcon()
        Icon.addPixmap(QPixmap(":/Icons/Stars"))
        self.setWindowIcon(Icon)
        self.CentralWidget = QWidget(self)
        self.setCentralWidget(self.CentralWidget)
        self.CentralWidget.setMinimumSize(sx, sy)

        self.GameSetup = GameSetup(people, rules)
        self.NewGame = NewGame(people, rules)
        self.NewGame.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.GameSetup.setWindowModality(Qt.WindowModality.ApplicationModal)

        LeftSide = QWidget()
        LeftSide.setMinimumWidth(875)        # Minimal feasible value ...
        LeftSide.setMaximumWidth(875)

        Layout_HL = QHBoxLayout(self.CentralWidget)
        Layout_HL.setSpacing(0)
        Layout_VL = QVBoxLayout(LeftSide)
        Layout_VL.setSpacing(0)

        self.Buttons = ToolBar()
        self.Buttons.setAutoFillBackground(True)
        self.Buttons.setMovable(False)
        self.Buttons.setIconSize(QSize(40, 40))
        Layout_VL.addWidget(self.Buttons)

        InfoBox = QGroupBox()
        policy = QSizePolicy()
        policy.setHorizontalPolicy(policy.Policy.MinimumExpanding)
        policy.setVerticalPolicy(policy.Policy.MinimumExpanding)
        InfoBox.setSizePolicy(policy)
        Data_VL = QVBoxLayout(InfoBox)
        Label_A = QLabel("Test-A")
        Label_B = QLabel("Test-B")
        Data_VL.addWidget(Label_A)
        Data_VL.addStretch()
        Data_VL.addWidget(Label_B)

        Layout_VL.addWidget(InfoBox)
        Layout_VL.addWidget(self.SetupNewsReader())

        InfoBox = QGroupBox()
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
        self.MineInfo = Minedata()
        self.ItemInfo.addWidget(self.MineInfo)

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

        self.Map = Starmap(rules)
        Layout_HL.addWidget(LeftSide)
        Layout_HL.addWidget(self.Map)

        self.Menu = Menu(self)
        self.setMenuBar(self.Menu)
        self.Status = QStatusBar(self)
        self.setStatusBar(self.Status)


    def SetupNewsReader(self):
        Filter_HL = QHBoxLayout()
        Filter_HL.setSpacing(0)
        self.FilterMessage = QCheckBox()
        self.FilterMessage.setToolTip("Show the likes of the current message ...")
        self.FilterMessage.setStatusTip("Show the likes of the current message ...")
        self.FilterMessage.setChecked(True)
        Filter_HL.addWidget(self.FilterMessage)
        Filter_HL.addStretch()
        self.CurrentGameYear = QLabel(self.CentralWidget)
        self.CurrentGameYear.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.CurrentGameYear.setToolTip("Current Age of the Galaxy ...")
        self.CurrentGameYear.setText("Year 2400 - Message: 1 of 9999")
        Filter_HL.addWidget(self.CurrentGameYear)
        Filter_HL.addStretch()
        Icon = QIcon()
        Show = QPixmap(":/Icons/ShowNews")
        NoShow = QPixmap(":/Icons/NoNews")
        Icon.addPixmap(NoShow, QIcon.Mode.Normal, QIcon.State.Off)
        Icon.addPixmap(Show, QIcon.Mode.Normal, QIcon.State.On)
        Filter = QToolButton(self.CentralWidget)
        Filter.setCheckable(True)
        Filter.setIcon(Icon)
        Filter.setAutoRepeat(False)
        Filter.setToolTip("Show the likes of the current message ...")
        Filter.setStatusTip("Show the likes of the current message ...")
        Filter.setIconSize(QSize(30, 30))
        Filter_HL.addWidget(Filter)
        self.CurrentMessage = QPlainTextEdit(self.CentralWidget)
        self.CurrentMessage.setReadOnly(True)
        self.CurrentMessage.setPlainText("This is a very important message ...")  # DELETE ME!
        NewsButtons_VL = QVBoxLayout()
        NewsButtons_VL.addStretch()
        self.PreviousMessage = QPushButton()
        self.PreviousMessage.setText("Prev")
        self.PreviousMessage.setToolTip("Read previous message ...")
        self.PreviousMessage.setStatusTip("Read the previous message ...")
        NewsButtons_VL.addWidget(self.PreviousMessage)
        self.FollowMessage = QPushButton()
        self.FollowMessage.setText("Goto")
        self.FollowMessage.setToolTip("Follow up on current message ...")
        self.FollowMessage.setStatusTip("Follow up on the current message ...")
        NewsButtons_VL.addWidget(self.FollowMessage)
        self.NextMessage = QPushButton()
        self.NextMessage.setText("Next")
        self.NextMessage.setToolTip("Read next message ...")
        self.NextMessage.setStatusTip("Read the next message ...")
        NewsButtons_VL.addWidget(self.NextMessage)
        NewsButtons_VL.addStretch()
        News_HL = QHBoxLayout()
        News_HL.setSpacing(5)
        News_HL.addWidget(self.CurrentMessage)
        News_HL.addLayout(NewsButtons_VL)
        News_VL = QVBoxLayout()
        News_VL.addLayout(Filter_HL)
        News_VL.addLayout(News_HL)
        News_VL.addSpacing(5)
        NewsReader = QGroupBox()
        NewsReader.setLayout(News_VL)
        NewsReader.setMaximumHeight(190)
        return NewsReader


    def SetupInspectorTitle(self):
        Title = QWidget()
        SelectedObject_HL = QHBoxLayout(Title)
        SelectedObject_HL.setSpacing(0)
        SelectedObject_HL.addSpacing(250)
        self.SelectedObject = QLabel()
        self.SelectedObject.setAlignment(Qt.AlignmentFlag.AlignCenter)
        SelectedObject_HL.addWidget(self.SelectedObject)
        ButtonBox = QWidget()
        ButtonBox.setMaximumWidth(180)
        ButtonLayout_HL = QHBoxLayout(ButtonBox)
        ButtonLayout_HL.setSpacing(0)
        ButtonLayout_HL.addStretch()
        self.PreviousField = _CreateButton(":/Icons/Previous")
        ButtonLayout_HL.addWidget(self.PreviousField)
        self.NextField = _CreateButton(":/Icons/Next")
        ButtonLayout_HL.addWidget(self.NextField)
        self.ShowAlienBase = _CreateButton(":/Icons/Fortress")
        ButtonLayout_HL.addWidget(self.ShowAlienBase)
        self.ShowNeutralBase = _CreateButton(":/Icons/Tradehub")
        ButtonLayout_HL.addWidget(self.ShowNeutralBase)
        self.ShowStarBase = _CreateButton(":/Icons/Starbase")
        ButtonLayout_HL.addWidget(self.ShowStarBase)
        self.SelectNextEnemy = _CreateButton(":/Icons/Enemies")
        ButtonLayout_HL.addWidget(self.SelectNextEnemy)
        self.SelectNextNeutral = _CreateButton(":/Icons/Neutrals")
        ButtonLayout_HL.addWidget(self.SelectNextNeutral)
        self.SelectNextFleet = _CreateButton(":/Icons/Fleets")
        ButtonLayout_HL.addWidget(self.SelectNextFleet)
        SelectedObject_HL.addWidget(ButtonBox)
        SwitchBox = QWidget()
        SwitchBox.setMaximumWidth(70)
        SwitchLayout_HL = QHBoxLayout(SwitchBox)
        SwitchLayout_HL.setSpacing(0)
        SwitchLayout_HL.addStretch(0)
        self.ShowPlanet = _CreateButton(":/Icons/Planet")
        SwitchLayout_HL.addWidget(self.ShowPlanet)
        self.ShowFields = _CreateButton(":/Icons/Mines")
        SwitchLayout_HL.addWidget(self.ShowFields)
        self.ShowFleets = _CreateButton(":/Icons/Ships")
        SwitchLayout_HL.addWidget(self.ShowFleets)
        SelectedObject_HL.addWidget(SwitchBox)
        Title.setMinimumHeight(68)
        return Title


    def DisplayStarbaseIcons(self, p=None):
        if p:
            if p.Relation == Stance.allied:
                self.ShowNeutralBase.setVisible(False)
                self.ShowAlienBase.setVisible(False)
                self.ShowStarBase.setVisible(p.SpaceStation)
            elif p.Relation == Stance.hostile:
                self.ShowNeutralBase.setVisible(False)
                self.ShowStarBase.setVisible(False)
                self.ShowAlienBase.setVisible(p.SpaceStation and p.ShipTracking)
            else:
                self.ShowAlienBase.setVisible(False)
                self.ShowStarBase.setVisible(False)
                self.ShowNeutralBase.setVisible(p.SpaceStation and p.ShipTracking)
        else:
            self.ShowNeutralBase.setVisible(False)
            self.ShowAlienBase.setVisible(False)
            self.ShowStarBase.setVisible(False)


    def DisplayFleetIcons(self):
        self.SelectNextEnemy.setVisible(self.HostileFleets > 0)
        self.SelectNextNeutral.setVisible(self.NeutralFleets > 0)
        self.SelectNextFleet.setVisible(self.AlliedFleets > 0)


    def UpdatePlanetView(self, p):
        if self.ItemInfo.currentIndex() < 2:
            self.AlliedFleets = p.TotalFriends
            if p.ShipTracking:
                self.HostileFleets = p.TotalFoes
                self.NeutralFleets = p.TotalOthers
            else:
                self.HostileFleets = 0
                self.NeutralFleets = 0
            self.DisplayFleetIcons()
        if self.ItemInfo.currentIndex() == 1:
            if self.EnemyFleetOffset > 0 and p.TotalFoes > 0:
                self.EnemyFleetOffset = 0
                self.InspectEnemyFleet()
            elif self.NeutralFleetOffset > 0 and p.TotalOthers > 0:
                self.NeutralFleetOffset = 0
                self.InspectNeutralFleet()
            elif self.FleetOffset > 0 and p.TotalFriends > 0:
                self.FleetOffset = 0
                self.InspectFleets()
            elif p.TotalFoes > 0:
                self.EnemyFleetOffset = 0
                self.InspectEnemyFleet()
            elif p.TotalOthers > 0:
                self.NeutralFleetOffset = 0
                self.InspectNeutralFleet()
            elif p.TotalFriends > 0:
                self.FleetOffset = 0
                self.InspectFleets()
            else:
                self.InspectPlanet(p)


    def InspectPlanet(self, p):
        self.SelectedPlanet = p
        self.SelectedFleets = p.fleets_in_orbit
        self.SelectedFields = p.mine_fields
        self.ApplyMineFilter()
        self.PreviousField.setVisible(False)
        self.NextField.setVisible(False)
        self.ShowPlanet.setVisible(False)
        self.ShowFleets.setVisible(False)
        self.ShowFields.setVisible(self.FilteredFields > 0)
        self.EnemyFleetOffset = 0
        self.NeutralFleetOffset = 0
        self.FleetOffset = 0
        self.MineOffset = 0
        if p.Discovered:
            self.ItemInfo.setCurrentIndex(0)
            self.PlanetInfo.UpdateMinerals(p)
            self.PlanetInfo.UpdateBiome(p)
            self.PlanetInfo.UpdateText(self.CurrentYear, p)
        else:
            self.ItemInfo.setCurrentIndex(3)
        self.AlliedFleets = p.TotalFriends
        if p.ShipTracking:
            self.HostileFleets = p.TotalFoes
            self.NeutralFleets = p.TotalOthers
        else:
            self.HostileFleets = 0
            self.NeutralFleets = 0
        self.DisplayStarbaseIcons(p)
        self.DisplayFleetIcons()
        self.SelectedObject.setText(p.Name)


    def InspectFleet(self, planet, index, f_list, m_list):
        self.EnemyFleetOffset = 0
        self.NeutralFleetOffset = 0
        self.FleetOffset = 0
        self.FleetIndex = index % len(f_list)
        self.SelectedFleets = f_list
        self.SelectedPlanet = planet
        self.SelectedFields = m_list
        self.AlliedFleets = 0
        self.HostileFleets = 0
        self.NeutralFleets = 0
        fleets = 0
        for f in f_list:
            if f.ShipCounter > 0:
                if f.FriendOrFoe == Stance.allied:
                    self.AlliedFleets += 1
                elif f.FriendOrFoe == Stance.hostile:
                    self.HostileFleets += 1
                else:
                    self.NeutralFleets += 1
                fleets += 1
        self.NextField.setVisible(False)
        self.PreviousField.setVisible(False)
        self.ShowFleets.setVisible(False)
        if fleets > 0:
            self.DisplayStarbaseIcons(planet)
            self.ApplyMineFilter()
            self.ShowFields.setVisible(self.FilteredFields > 0)
            fof = f_list[self.FleetIndex].FriendOrFoe
            if fof == Stance.allied:
                self.InspectAlliedFleet()
            elif fof == Stance.hostile:
                self.InspectHostileFleet()
            else:
                self.InspectNeutralFleet()
        elif planet:
            self.InspectPlanet(planet)
        else:
            self.ItemInfo.setCurrentIndex(3)
            self.ShowFields.setVisible(False)
            self.DisplayFleetIcons()
            self.SelectedObject.setText("Deep Space")


    def UpdateFields(self, NewFilter):
        self.MineFilter = NewFilter
        self.ApplyMineFilter()
        if self.ItemInfo.currentIndex() < 2:
            self.ShowFields.setVisible(self.FilteredFields > 0)
        elif self.ItemInfo.currentIndex() < 3:
            if self.FilteredFields > 0:
                self.InspectMines()
            elif self.SelectedPlanet:
                self.InspectPlanets()
            elif self.SelectedFleets:
                self.InspectFleets()
            else:
                self.ItemInfo.setCurrentIndex(3)
                self.PreviousField.setVisible(False)
                self.NextField.setVisible(False)
                self.ShowFleets.setVisible(False)
                self.SelectedObject.setText("Deep Space")


    def InspectMineField(self, planet, index, m_list, f_list):
        self.SelectedFields = m_list
        self.MineIndex = index
        self.SelectedPlanet = planet
        self.SelectedFleets = f_list
        self.InspectMines()


    def NextFleet(self, index, offset, fof):
        if self.SelectedPlanet:
            self.ShowPlanet.setVisible(True)
            self.ShowFields.setVisible(False)
        else:
            self.ShowPlanet.setVisible(False)
        if self.SelectedFleet:
            self.SelectedFleet.ColourCourse(False)
            self.SelectedFleet.ShowCourse(self.ShowFleetMovements)
        self.DisplayFleetIcons()
        self.ItemInfo.setCurrentIndex(1)
        nmax = len(self.SelectedFleets)
        n = (index + offset) % nmax
        while n < nmax:
            f = self.SelectedFleets[n]
            if f.ShipCounter > 0 and f.FriendOrFoe in fof:
                self.SelectedObject.setText(f.Name + ' #' + str(f.id))
                self.FleetInfo.UpdateCargo(f)
                f.ShowCourse(True)
                f.ColourCourse(True)
                self.SelectedFleet = f
                self.Map.Universe.SelectedFleet = f
                self.Map.Universe.FleetIndex = n
                return n
            n += 1
        n = 0
        while n <= index:
            f = self.SelectedFleets[n]
            if f.ShipCounter > 0 and f.FriendOrFoe in fof:
                self.SelectedObject.setText(f.Name + ' #' + str(f.id))
                self.FleetInfo.UpdateCargo(f)
                f.ShowCourse(True)
                f.ColourCourse(True)
                self.Map.Universe.SelectedFleet = f
                self.Map.Universe.FleetIndex = n
                return n
            n += 1


    def NextMinefield(self, i0, offset):
        self.FieldIndex += self.FilteredFields + offset
        self.FieldIndex %= self.FilteredFields
        i = (i0 + self.NumberOfFields + offset) % self.NumberOfFields
        while i < self.NumberOfFields:
            m = self.SelectedFields[i]
            if self.MineFilter[m.fof]:
                self.MineInfo.UpdateData(m, self.FieldIndex + 1, self.FilteredFields)
                self.SelectedObject.setText(m.model.value + ' Mine Field #' + str(m.id))
                return i
            i += 1
        i = 0
        while i <= i0:
            m = self.SelectedFields[i]
            if self.MineFilter[m.fof]:
                self.MineInfo.UpdateData(m, self.FieldIndex + 1, self.FilteredFields)
                self.SelectedObject.setText(m.model.value + ' Mine Field #' + str(m.id))
                return i
            i += 1


    def InspectHostileFleet(self):
        self.HostileFleets -= 1
        self.EnemyFleetIndex = self.NextFleet(self.EnemyFleetIndex, self.EnemyFleetOffset, [Stance.hostile])
        self.HostileFleets += 1
        self.EnemyFleetOffset = 1
        self.NeutralFleetOffset = 0
        self.FleetOffset = 0


    def InspectNeutralFleet(self):
        fof = [Stance.friendly, Stance.neutral]
        self.NeutralFleets -= 1
        self.NeutralFleetIndex = self.NextFleet(self.NeutralFleetIndex, self.NeutralFleetOffset, fof)
        self.NeutralFleets += 1
        self.EnemyFleetOffset = 0
        self.NeutralFleetOffset = 1
        self.FleetOffset = 0


    def InspectAlliedFleet(self):
        self.AlliedFleets -= 1
        self.FleetIndex = self.NextFleet(self.FleetIndex, self.FleetOffset, [Stance.allied])
        self.AlliedFleets += 1
        self.EnemyFleetOffset = 0
        self.NeutralFleetOffset = 0
        self.FleetOffset = 1


    def InspectPlanets(self):
        self.InspectPlanet(self.SelectedPlanet)


    def InspectFleets(self):
        self.ShowFleets.setVisible(False)
        self.InspectFleet(self.SelectedPlanet, self.FleetIndex, self.SelectedFleets, self.SelectedFields)


    def InspectMines(self):
        self.EnemyFleetOffset = 0
        self.NeutralFleetOffset = 0
        self.FleetOffset = 0
        self.SelectNextEnemy.setVisible(False)
        self.SelectNextNeutral.setVisible(False)
        self.SelectNextFleet.setVisible(False)
        self.ShowNeutralBase.setVisible(False)
        self.ShowAlienBase.setVisible(False)
        self.ShowStarBase.setVisible(False)
        if self.SelectedPlanet:
            self.ShowPlanet.setVisible(True)
            self.ShowFleets.setVisible(False)
        elif self.SelectedFleets:
            self.ShowPlanet.setVisible(False)
            self.ShowFleets.setVisible(True)
        else:
            self.ShowPlanet.setVisible(False)
            self.ShowFleets.setVisible(False)
        if self.SelectedFleet:
            self.SelectedFleet.ColourCourse(False)
            self.SelectedFleet.ShowCourse(self.ShowFleetMovements)
        self.ShowFields.setVisible(False)
        self.ApplyMineFilter()
        if self.FilteredFields > 0:
            self.ItemInfo.setCurrentIndex(2)
            self.NextField.setVisible(self.FilteredFields > 1)
            self.PreviousField.setVisible(self.FilteredFields > 1)
            self.NextMinefield(self.MineIndex, 0)
        else:
            print('filtered fields should always be > 0')
            self.SelectedObject.setText('Error : FilteredFields < 1!')
            self.ItemInfo.setCurrentIndex(3)


    def ApplyMineFilter(self):
        self.FilteredFields = 0
        self.NumberOfFields = 0
        if self.SelectedFields:
            self.NumberOfFields = len(self.SelectedFields)
            for m in self.SelectedFields:
                if self.MineFilter[m.fof]:
                    self.FilteredFields += 1


    def ShowNextMineField(self, event):
        self.MineIndex = self.NextMinefield(self.MineIndex, 1)


    def ShowPreviousMineField(self, event):
        self.MineIndex = self.NextMinefield(self.MineIndex, -1)


    def ShowCrustDiagrams(self, event):
        if event:
            self.Map.Universe.ShowCrustDiagrams()
        else:
            self.Map.Universe.RemoveDiagrams()


    def ShowSurfaceDiagrams(self, event):
        if event:
            self.Map.Universe.ShowSurfaceDiagrams()
        else:
            self.Map.Universe.RemoveDiagrams()


    def ShowPopulationView(self, event):
        if event:
            self.Map.Universe.ShowPopulationView()


    def ShowDefaultView(self, event):
        if event:
            self.Map.Universe.ShowDefaultView()


    def ShowMinimalView(self, event):
        if event:
            self.Map.Universe.ShowMinimalView()


    def ShowPercentageView(self, event):
        if event:
            self.Map.Universe.ShowPercentageView()


    def ShowMovements(self, event):
        self.ShowFleetMovements = event
        self.Map.Universe.ShowMovements(event)


    def AddWaypoints(self, event):
        self.WaypointMode = event
        self.Map.Universe.SetWaypointMode(event)


    def ConfigureGame(self):
        self.NewGame.hide()
        self.GameSetup.ConfigureGame()

from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QStackedLayout, QSizePolicy
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QMainWindow, QPushButton, QToolButton
from PyQt6.QtWidgets import QStatusBar, QGroupBox, QCheckBox
from PyQt6.QtWidgets import QPlainTextEdit

from PyQt6.QtCore import Qt
# from PyQt6.QtCore import pyqtSignal as QSignal

from design import Design
from defines import Stance
from menubar import Menu
from toolbar import ToolBar
from inspector import Inspector
from fleetdata import Fleetdata
from starmap import Starmap



def _CreateButton(name):
    Style = "padding: 0px 2px 0px 2px;border-width: 0px;background-color: transparent"
    Icon = QIcon(name)
    Button = QPushButton()
    Button.setIcon(Icon)
    Button.setIconSize(QSize(30, 30))
    Button.setStyleSheet(Style)
    Button.setVisible(True)
    return Button



class Gui(QMainWindow):

    def __init__(self, people, rules):
        super(self.__class__, self).__init__()
        self.CurrentYear = rules.FirstYear()
        self.SelectedPlanet = None
        self.EnemyFleetIndex = 0
        self.NeutralFleetIndex = 0
        self.FleetIndex = 0
        self.EnemyFleetOffset = 0
        self.NeutralFleetOffset = 0
        self.FleetOffset = 0
        design = Design()
        self.setStyleSheet(design.getStyle())
        self.Action = dict()
        self.SetupUI(design, people, rules)
        self.Buttons.actionRadarView.toggled.connect(self.Map.Universe.ShowScannerRanges)
        self.Buttons.actionPlanetNames.toggled.connect(self.Map.Universe.ShowPlanetNames)
        self.Buttons.actionConcentrationView.toggled.connect(self.ShowCrustDiagrams)
        self.Buttons.actionSurfaceMineralView.toggled.connect(self.ShowSurfaceDiagrams)
        self.Buttons.actionDefaultView.toggled.connect(self.ShowDefaultView)
        self.Buttons.actionPopulationView.toggled.connect(self.ShowPopulationView)
        self.Buttons.actionNoInfoView.toggled.connect(self.ShowMinimalView)
        self.Buttons.actionPercentView.toggled.connect(self.ShowPercentageView)
        self.Buttons.actionNoInfoView.setChecked(True)
        self.Buttons.RadarRange.valueChanged.connect(self.Map.Universe.ScaleRadarRanges)
        self.Buttons.ChangeZoom.connect(self.Map.ResizeStarmap)
        self.Map.Universe.ChangeFocus.connect(self.InspectPlanet)
        self.ShowPlanet.clicked.connect(self.InspectPlanets)
        self.SelectNextEnemy.clicked.connect(self.InspectEnemyFleets)
        self.SelectNextNeutral.clicked.connect(self.InspectNeutralFleets)
        self.SelectNextFleet.clicked.connect(self.InspectFleets)


    def SetupUI(self, design, people, rules):

        self.resize(2400, 1350)                        # TODO: Query design!
        self.setWindowTitle("My Stars!")
        Icon = QIcon()
        Icon.addPixmap(QPixmap(":/Icons/Stars"))
        self.setWindowIcon(Icon)
        self.CentralWidget = QWidget(self)
        self.setCentralWidget(self.CentralWidget)
        self.CentralWidget.setMinimumSize(2400, 1350)  # TODO: Query design!

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
#
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
#
        self.Buttons.UpdateFriendlyDesigns([])
        self.Buttons.UpdateEnemyDesigns(
            ['Colony Ships', 'Freighters', 'Scouts', 'Warships', 'Utility Ships',
             'Bombers', 'Mining Ships', 'Fuel Transports']
        )


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
        SelectedObject_HL.addWidget(SwitchBox)
        Title.setMinimumHeight(65)
        return Title


    def InspectPlanet(self, p):
        self.SelectedPlanet = p
        self.ShowPlanet.setVisible(False)
        self.EnemyFleetOffset = 0
        self.NeutralFleetOffset = 0
        self.FleetOffset = 0
        if p.Discovered:
            self.ItemInfo.setCurrentIndex(0)
            self.PlanetInfo.UpdateMinerals(p)
            self.PlanetInfo.UpdateBiome(p)
            self.PlanetInfo.UpdateText(self.CurrentYear, p)
        else:
            self.ItemInfo.setCurrentIndex(2)
        if p.ShipTracking:
            self.SelectNextEnemy.setVisible(p.TotalFoes > 0)
            self.SelectNextNeutral.setVisible(p.TotalOthers > 0)
        else:
            self.SelectNextEnemy.setVisible(False)
            self.SelectNextNeutral.setVisible(False)
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
        self.SelectNextFleet.setVisible(p.TotalFriends > 0)
        self.SelectedObject.setText(p.Name + ' - Summary')


    def InspectNextFleet(self, index, offset, fof):
        self.ShowPlanet.setVisible(True)
        self.ItemInfo.setCurrentIndex(1)
        nmax = len(self.SelectedPlanet.fleets_in_orbit)
        n = (index + offset) % nmax
        while n < nmax:
            f = self.SelectedPlanet.fleets_in_orbit[n]
            if f.FriendOrFoe == fof:
                self.SelectedObject.setText(f.Name + ' - Summary')
                self.FleetInfo.UpdateCargo(f)
                return n
            n += 1
        n = 0
        while n <= index:
            f = self.SelectedPlanet.fleets_in_orbit[n]
            if f.FriendOrFoe == fof:
                self.SelectedObject.setText(f.Name + ' - Summary')
                self.FleetInfo.UpdateCargo(f)
                return n
            n += 1


    def InspectEnemyFleets(self, event):
        self.EnemyFleetIndex = self.InspectNextFleet(self.EnemyFleetIndex, self.EnemyFleetOffset, Stance.hostile)
        self.EnemyFleetOffset = 1
        self.NeutralFleetOffset = 0
        self.FleetOffset = 0


    def InspectNeutralFleets(self, event):
        self.NeutralFleetIndex = self.InspectNextFleet(self.NeutralFleetIndex, self.NeutralFleetOffset, Stance.neutral)
        self.EnemyFleetOffset = 0
        self.NeutralFleetOffset = 1
        self.FleetOffset = 0


    def InspectFleets(self, event):
        self.FleetIndex = self.InspectNextFleet(self.FleetIndex, self.FleetOffset, Stance.friendly)
        self.EnemyFleetOffset = 0
        self.NeutralFleetOffset = 0
        self.FleetOffset = 1


    def InspectPlanets(self, event):
        self.InspectPlanet(self.SelectedPlanet)


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

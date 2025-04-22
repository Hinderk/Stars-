
import copy
import json

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QFileDialog, QGridLayout
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QScrollBar
from PyQt6.QtWidgets import QButtonGroup
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtWidgets import QComboBox, QSpinBox
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton, QLineEdit
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from defines import PlayerType as PT
from defines import AIMode as AI
from guidesign import GuiDesign, GuiStyle
from faction import Faction
from victory import Victory
from playerdata import PlayerData




class FactionWizard(QWidget):

    def __init__(self, people, rules):
        super(self.__class__, self).__init__()
        self.setWindowTitle("Custom Faction Wizard - Step 1 of 6")
        self.setStyleSheet(GuiDesign.getStyle(GuiStyle.FactionSetup_1))
        Icon = QIcon()
        Icon.addPixmap(QPixmap(":/Icons/Host"))
        self.setWindowIcon(Icon)
        self.setFixedSize(1000, 750)
        self.hide()
        self.Wizard = QWidget()
        self.Pages = QStackedLayout(self.Wizard)
        self.RestartGameWizard = False
        self.RestartNewGame = False
        self.Factions = people
        self.SelectedBanner = 0
        self.Template = None
        self.CurrentPage = 0
        self.SetupErrorMessages()
        self.SetupButtonsAndScore()
        self.SetupNamesAndBanner()

        self.SetAdvantagePoints(0)  # Remove me


    def SetupErrorMessages(self):
        self.Error = QMessageBox(self)
        self.Error.setIcon(self.Error.Icon.Warning)
        self.Error.setWindowTitle('Custom Faction Wizard')
        Icon = QIcon()
        Icon.addPixmap(QPixmap(":/Icons/Stars"))
        self.Error.setWindowIcon(Icon)


    def SetupButtonsAndScore(self):
        ButtonSize = QSize(140, 50)
        Buttons_HL = QHBoxLayout()
        self.Finish = QPushButton()
        self.Finish.setText('Finish')
        self.Finish.setToolTip(' Save the game settings.')
        self.Finish.setFixedSize(ButtonSize)
        self.Finish.setShortcut(QKeySequence('Ctrl+F'))
        self.Cancel = QPushButton()
        self.Cancel.setText("Cancel")
        self.Cancel.setToolTip(" Close this dialog.")
        self.Cancel.setFixedSize(ButtonSize)
        self.Cancel.setShortcut(QKeySequence('Ctrl+C'))
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
        Buttons_HL.addWidget(self.Cancel)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(self.Back)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(self.Next)
        Buttons_HL.addStretch()
        Buttons_HL.addWidget(self.Finish)
        Buttons_HL.addSpacing(30)
        Label = QLabel('Advantage Points left: ')
        Label.setStyleSheet('font-size: 24pt;font-weight: 800;padding: 0px;')
        self.Advantage = QLabel()
        AdvantagePoints = QHBoxLayout()
        AdvantagePoints.addStretch()
        AdvantagePoints.addWidget(Label)
        AdvantagePoints.addWidget(self.Advantage)
        AdvantagePoints.addSpacing(20)
        Layout_VL = QVBoxLayout(self)
        Layout_VL.addSpacing(10)
        Layout_VL.addLayout(AdvantagePoints)
        Layout_VL.addSpacing(10)
        Layout_VL.addWidget(self.Wizard)
        Layout_VL.addLayout(Buttons_HL)
        self.Finish.clicked.connect(self.SaveFactionData)
        self.Back.clicked.connect(self.Revert)
        self.Next.clicked.connect(self.Proceed)


    def Proceed(self):
        if self.CurrentPage < 5:
            self.CurrentPage += 1
            step = 'Step ' + str(1 + self.CurrentPage) + ' of 6'
            self.setWindowTitle('Custom Faction Wizard - ' + step)
            self.Pages.setCurrentIndex(self.CurrentPage)
            self.Back.setEnabled(True)
            self.Next.setEnabled(self.CurrentPage < 5)


    def Revert(self):
        if 0 < self.CurrentPage:
            self.CurrentPage -= 1
            step = 'Step ' + str(1 + self.CurrentPage) + ' of 6'
            self.setWindowTitle('Custom Faction Wizard - ' + step)
            self.Pages.setCurrentIndex(self.CurrentPage)
            self.Next.setEnabled(True)
            self.Back.setEnabled(self.CurrentPage > 0)


    def SaveFactionData(self):
        SaveFaction = QFileDialog(self)
        SaveFaction.setOption(SaveFaction.Option.DontUseNativeDialog)
        SaveFaction.setStyleSheet(GuiDesign.getStyle(GuiStyle.FileBrowser))
        SaveFaction.setMinimumSize(1000, 750)
        SaveFaction.setFileMode(SaveFaction.FileMode.AnyFile)
        SaveFaction.setViewMode(SaveFaction.ViewMode.List)
        SaveFaction.setAcceptMode(SaveFaction.AcceptMode.AcceptSave)
        SaveFaction.setNameFilters(['Game Files (*.f1)', 'All Files (*.*)'])
        SaveFaction.setDefaultSuffix('f1')
        if SaveFaction.exec():
            Files = SaveFaction.selectedFiles()
            try:
                f = open(Files[0], 'wt')
                FactionData = ['Content']
                json.dump(FactionData, f)
                f.close()
                if self.RestartNewGame:          # FIX ME
                    nf = Faction()
                    nf.deserialize(FactionData)

                if self.RestartGameWizard:
                    pass
            except:
                self.Error.setText('Failed to save faction data!')
                self.Error.exec()


    def ConfigureWizard(self, simple=False, advanced=False):
        self.RestartNewGame = simple
        self.RestartGameWizard = advanced
        self.Settings.button(0).setChecked(True)
        self.Banners[0].setVisible(True)
        self.Banners[self.SelectedBanner].setVisible(False)
        self.SelectedBanner = 0
        self.DefaultName = 'Humanoid'
        self.FactionSingular.setPlaceholderText('Humanoid')
        self.FactionPlural.setPlaceholderText('Humanoids')
        self.Surplus.setCurrentIndex(0)
        self.show()


    def SetupNamesAndBanner(self):
        Alignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight
        BannerWidth = 180
        Names_GL = QGridLayout()
        spacer = QLabel()
        spacer.setMaximumWidth(35)
        label = QLabel('Faction Name (singular):')
        label.setAlignment(Alignment)
        self.FactionSingular = QLineEdit()
        self.FactionSingular.setMaximumWidth(600)
        self.FactionPlural = QLineEdit()
        self.FactionPlural.setMaximumWidth(600)
        Names_GL.addWidget(spacer, 0, 2)
        Names_GL.addWidget(label, 0, 0)
        Names_GL.addWidget(self.FactionSingular, 0, 1)
        label = QLabel('Faction Name (plural):')
        label.setAlignment(Alignment)
        Names_GL.addWidget(label, 1, 0)
        Names_GL.addWidget(self.FactionPlural, 1, 1)
        self.Settings = QButtonGroup()
        self.Settings.idClicked.connect(self.SwitchFaction)
        FactionBox = QGroupBox()
        FactionBox.setTitle('Predefined Factions')
        Factions_GL = QGridLayout(FactionBox)
        self.Banners = []
        n = 0
        for sp in self.Factions.AIFaction:
            rb = QRadioButton(sp.Species)
            Factions_GL.addWidget(rb, n % 4, n // 4)
            self.Settings.addButton(rb, n)
            n += 1
        rb = QRadioButton('Random')
        Factions_GL.addWidget(rb, 2, 1)
        self.Settings.addButton(rb, 6)
        rb = QRadioButton('Custom')
        Factions_GL.addWidget(rb, 3, 1)
        self.Settings.addButton(rb, 7)
        self.Selector = QScrollBar(Qt.Orientation.Horizontal)
        BannerBox = QGroupBox()
        BannerBox.setTitle('Faction Banner')
        BannerBox.setMaximumWidth(40 + BannerWidth)
        Banner_VL = QVBoxLayout(BannerBox)
        Scene = QGraphicsScene()
        Scene.setSceneRect(0, 0, BannerWidth, BannerWidth)
        for f in "ABCDEFGHIJKLMNOPQRST":
            resource = ":/Factions/Faction-" +f
            banner = QGraphicsSvgItem(resource)
            width = banner.boundingRect().width()
            banner.setScale(0.9 * BannerWidth / width)
            banner.setPos(0.05 * BannerWidth, 0.05 * BannerWidth)
            banner.setVisible(True)
            Scene.addItem(banner)
            self.Banners.append(banner)
        BannerView = QGraphicsView(Scene)
        Banner_VL.addWidget(BannerView)
        Banner_VL.addWidget(self.Selector)
        Banner_HL = QHBoxLayout()
        Banner_HL.addSpacing(40)
        Banner_HL.addWidget(FactionBox)
        Banner_HL.addSpacing(60)
        Banner_HL.addWidget(BannerBox)
        Banner_HL.addSpacing(40)
        self.Surplus = QComboBox()
        SurplusBox = QGroupBox()
        SurplusBox.setTitle('Spent up to 50 leftover advantage points on ')
        SurplusBox.setMinimumHeight(120)
        Surplus_HL = QHBoxLayout(SurplusBox)
        Surplus_HL.addSpacing(10)
        Surplus_HL.addWidget(self.Surplus)
        Surplus_HL.addSpacing(10)
        Surplus_HL = QHBoxLayout()
        Surplus_HL.addSpacing(40)
        Surplus_HL.addWidget(SurplusBox)
        Surplus_HL.addSpacing(40)
        NamesAndBanner = QWidget(self)
        Layout_VL = QVBoxLayout(NamesAndBanner)
        Layout_VL.addSpacing(10)
        Layout_VL.addLayout(Names_GL)
        Layout_VL.addSpacing(20)
        Layout_VL.addLayout(Banner_HL)
        Layout_VL.addSpacing(20)
        Layout_VL.addLayout(Surplus_HL)
        Layout_VL.addStretch()
        self.Pages.addWidget(NamesAndBanner)
        self.Surplus.addItem('Surface Minerals')
        self.Surplus.addItem('Mineral Concentrations')
        self.Surplus.addItem('Mines')
        self.Surplus.addItem('Factories')
        self.Surplus.addItem('Defenses')


    def SwitchFaction(self, buttonid):
        if buttonid < 6:
            self.Next.setEnabled(True)
            name = self.Factions.AIFaction[buttonid].Species
            self.FactionSingular.setPlaceholderText(name)
            self.FactionPlural.setPlaceholderText(name + 's')
            self.DefaultName = name
            self.Template = copy.deepcopy(self.Factions.AIFaction[buttonid])
        elif buttonid < 7:
            self.RandomizeFaction()
        else:
            self.CustomizeFaction()


    def RandomizeFaction(self):
        self.Next.setEnabled(False)
        self.FactionSingular.setPlaceholderText('Random')
        self.FactionPlural.setPlaceholderText('Randoms')
        self.DefaultName = 'Random'


    def CustomizeFaction(self):
        print('-- Customize --')


    def SetAdvantagePoints(self, value):
        style = 'font-size: 24pt;font-weight: 800;padding: 0px;'
        if value < 0:
            self.Advantage.setStyleSheet(style + 'color: red;')
            self.Finish.setEnabled(False)
        else:
            self.Advantage.setStyleSheet(style + 'color: black;')
            self.Finish.setEnabled(True)
        self.Advantage.setText(str(value))
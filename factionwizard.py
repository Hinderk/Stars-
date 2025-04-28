
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
        self.setStyleSheet(GuiDesign.get_style(GuiStyle.FACTIONSETUP_1))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Icons/Host"))
        self.setWindowIcon(icon)
        self.setFixedSize(1000, 750)
        self.hide()
        self.wizard = QWidget()
        self.pages = QStackedLayout(self.wizard)
        self.restart_game_wizard = False
        self.restart_new_game = False
        self.factions = people
        self.selected_banner = 0
        self.template = None
        self.current_page = 0
        self.setup_error_messages()
        self.setup_buttons_and_score()
        self.setup_names_and_banner()

        self.set_advantage_points(0)  # Remove me


    def setup_error_messages(self):
        self.error = QMessageBox(self)
        self.error.setIcon(self.error.Icon.Warning)
        self.error.setWindowTitle('Custom Faction Wizard')
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Icons/Stars"))
        self.error.setWindowIcon(icon)


    def setup_buttons_and_score(self):
        button_size = QSize(140, 50)
        buttons_hl = QHBoxLayout()
        self.finish = QPushButton()
        self.finish.setText('Finish')
        self.finish.setToolTip(' Save the game settings.')
        self.finish.setFixedSize(button_size)
        self.finish.setShortcut(QKeySequence('Ctrl+F'))
        self.cancel = QPushButton()
        self.cancel.setText("Cancel")
        self.cancel.setToolTip(" Close this dialog.")
        self.cancel.setFixedSize(button_size)
        self.cancel.setShortcut(QKeySequence('Ctrl+C'))
        self.help = QPushButton()
        self.help.setText("Help")
        self.help.setToolTip(" Read the game manual.")
        self.help.setFixedSize(button_size)
        self.help.setShortcut(QKeySequence('Ctrl+H'))
        self.next = QPushButton()
        self.next.setText("Next")
        self.next.setToolTip(" Proceed to the next page.")
        self.next.setFixedSize(button_size)
        self.next.setShortcut(QKeySequence('Ctrl+N'))
        self.back = QPushButton()
        self.back.setText("Back")
        self.back.setToolTip(" Return to the previous page.")
        self.back.setFixedSize(button_size)
        self.back.setShortcut(QKeySequence('Ctrl+B'))
        self.back.setEnabled(False)
        buttons_hl.addSpacing(30)
        buttons_hl.addWidget(self.help)
        buttons_hl.addStretch()
        buttons_hl.addWidget(self.cancel)
        buttons_hl.addStretch()
        buttons_hl.addWidget(self.back)
        buttons_hl.addStretch()
        buttons_hl.addWidget(self.next)
        buttons_hl.addStretch()
        buttons_hl.addWidget(self.finish)
        buttons_hl.addSpacing(30)
        label = QLabel('Advantage Points left: ')
        label.setStyleSheet('font-size: 24pt;font-weight: 800;padding: 0px;')
        self.advantage = QLabel()
        advantage_points = QHBoxLayout()
        advantage_points.addStretch()
        advantage_points.addWidget(label)
        advantage_points.addWidget(self.advantage)
        advantage_points.addSpacing(20)
        layout_vl = QVBoxLayout(self)
        layout_vl.addSpacing(10)
        layout_vl.addLayout(advantage_points)
        layout_vl.addSpacing(10)
        layout_vl.addWidget(self.wizard)
        layout_vl.addLayout(buttons_hl)
        self.finish.clicked.connect(self.save_faction_data)
        self.back.clicked.connect(self.revert)
        self.next.clicked.connect(self.proceed)


    def proceed(self):
        if self.current_page < 5:
            self.current_page += 1
            step = 'Step ' + str(1 + self.current_page) + ' of 6'
            self.setWindowTitle('Custom Faction Wizard - ' + step)
            self.pages.setCurrentIndex(self.current_page)
            self.back.setEnabled(True)
            self.next.setEnabled(self.current_page < 5)


    def revert(self):
        if 0 < self.current_page:
            self.current_page -= 1
            step = 'Step ' + str(1 + self.current_page) + ' of 6'
            self.setWindowTitle('Custom Faction Wizard - ' + step)
            self.pages.setCurrentIndex(self.current_page)
            self.next.setEnabled(True)
            self.back.setEnabled(self.current_page > 0)


    def save_faction_data(self):
        save_faction = QFileDialog(self)
        save_faction.setOption(save_faction.Option.DontUseNativeDialog)
        save_faction.setStyleSheet(GuiDesign.get_style(GuiStyle.FILEBROWSER))
        save_faction.setMinimumSize(1000, 750)
        save_faction.setFileMode(save_faction.FileMode.AnyFile)
        save_faction.setViewMode(save_faction.ViewMode.List)
        save_faction.setAcceptMode(save_faction.AcceptMode.AcceptSave)
        save_faction.setNameFilters(['Game Files (*.f1)', 'All Files (*.*)'])
        save_faction.setDefaultSuffix('f1')
        if save_faction.exec():
            files = save_faction.selectedFiles()
            try:
                f = open(files[0], 'wt')
                faction_data = ['Content']
                json.dump(faction_data, f)
                f.close()
                if self.restart_new_game:          # FIX ME
                    nf = Faction()
                    nf.deserialize(faction_data)

                if self.restart_game_wizard:
                    pass
            except:
                self.error.setText('Failed to save faction data!')
                self.error.exec()


    def configure_wizard(self, simple=False, advanced=False):
        self.restart_new_game = simple
        self.restart_game_wizard = advanced
        self.settings.button(0).setChecked(True)
        self.banners[0].setVisible(True)
        self.banners[self.selected_banner].setVisible(False)
        self.selected_banner = 0
        self.default_name = 'Humanoid'
        self.faction_singular.setPlaceholderText('Humanoid')
        self.faction_plural.setPlaceholderText('Humanoids')
        self.surplus.setCurrentIndex(0)
        self.show()


    def setup_names_and_banner(self):
        alignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight
        banner_width = 180
        names_gl = QGridLayout()
        spacer = QLabel()
        spacer.setMaximumWidth(35)
        label = QLabel('Faction Name (singular):')
        label.setAlignment(alignment)
        self.faction_singular = QLineEdit()
        self.faction_singular.setMaximumWidth(600)
        self.faction_plural = QLineEdit()
        self.faction_plural.setMaximumWidth(600)
        names_gl.addWidget(spacer, 0, 2)
        names_gl.addWidget(label, 0, 0)
        names_gl.addWidget(self.faction_singular, 0, 1)
        label = QLabel('Faction Name (plural):')
        label.setAlignment(alignment)
        names_gl.addWidget(label, 1, 0)
        names_gl.addWidget(self.faction_plural, 1, 1)
        self.settings = QButtonGroup()
        self.settings.idClicked.connect(self.switch_faction)
        faction_box = QGroupBox()
        faction_box.setTitle('Predefined Factions')
        factions_gl = QGridLayout(faction_box)
        self.banners = []
        n = 0
        for sp in self.factions.ai_faction:
            rb = QRadioButton(sp.species)
            factions_gl.addWidget(rb, n % 4, n // 4)
            self.settings.addButton(rb, n)
            n += 1
        rb = QRadioButton('Random')
        factions_gl.addWidget(rb, 2, 1)
        self.settings.addButton(rb, 6)
        rb = QRadioButton('Custom')
        factions_gl.addWidget(rb, 3, 1)
        self.settings.addButton(rb, 7)
        self.selector = QScrollBar(Qt.Orientation.Horizontal)
        banner_box = QGroupBox()
        banner_box.setTitle('Faction Banner')
        banner_box.setMaximumWidth(40 + banner_width)
        banner_vl = QVBoxLayout(banner_box)
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, banner_width, banner_width)
        for f in "ABCDEFGHIJKLMNOPQRST":
            resource = ":/Factions/Faction-" +f
            banner = QGraphicsSvgItem(resource)
            width = banner.boundingRect().width()
            banner.setScale(0.9 * banner_width / width)
            banner.setPos(0.05 * banner_width, 0.05 * banner_width)
            banner.setVisible(True)
            scene.addItem(banner)
            self.banners.append(banner)
        banner_view = QGraphicsView(scene)
        banner_vl.addWidget(banner_view)
        banner_vl.addWidget(self.selector)
        banner_hl = QHBoxLayout()
        banner_hl.addSpacing(40)
        banner_hl.addWidget(faction_box)
        banner_hl.addSpacing(60)
        banner_hl.addWidget(banner_box)
        banner_hl.addSpacing(40)
        self.surplus = QComboBox()
        surplus_box = QGroupBox()
        surplus_box.setTitle('Spent up to 50 leftover advantage points on ')
        surplus_box.setMinimumHeight(120)
        surplus_hl = QHBoxLayout(surplus_box)
        surplus_hl.addSpacing(10)
        surplus_hl.addWidget(self.surplus)
        surplus_hl.addSpacing(10)
        surplus_hl = QHBoxLayout()
        surplus_hl.addSpacing(40)
        surplus_hl.addWidget(surplus_box)
        surplus_hl.addSpacing(40)
        names_and_banner = QWidget(self)
        layout_vl = QVBoxLayout(names_and_banner)
        layout_vl.addSpacing(10)
        layout_vl.addLayout(names_gl)
        layout_vl.addSpacing(20)
        layout_vl.addLayout(banner_hl)
        layout_vl.addSpacing(20)
        layout_vl.addLayout(surplus_hl)
        layout_vl.addStretch()
        self.pages.addWidget(names_and_banner)
        self.surplus.addItem('Surface Minerals')
        self.surplus.addItem('Mineral Concentrations')
        self.surplus.addItem('Mines')
        self.surplus.addItem('Factories')
        self.surplus.addItem('Defenses')


    def switch_faction(self, buttonid):
        if buttonid < 6:
            self.next.setEnabled(True)
            name = self.factions.ai_faction[buttonid].species
            self.faction_singular.setPlaceholderText(name)
            self.faction_plural.setPlaceholderText(name + 's')
            self.default_name = name
            self.template = copy.deepcopy(self.factions.ai_faction[buttonid])
        elif buttonid < 7:
            self.randomize_faction()
        else:
            self.customize_faction()


    def randomize_faction(self):
        self.next.setEnabled(False)
        self.faction_singular.setPlaceholderText('Random')
        self.faction_plural.setPlaceholderText('Randoms')
        self.default_name = 'Random'


    def customize_faction(self):
        print('-- Customize --')


    def set_advantage_points(self, value):
        style = 'font-size: 24pt;font-weight: 800;padding: 0px;'
        if value < 0:
            self.advantage.setStyleSheet(style + 'color: red;')
            self.finish.setEnabled(False)
        else:
            self.advantage.setStyleSheet(style + 'color: black;')
            self.finish.setEnabled(True)
        self.advantage.setText(str(value))

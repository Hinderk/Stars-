
""" This module implements the dialog used to setup new game sessions """

import random
import json

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QKeySequence
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QComboBox
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton

from PyQt6.QtCore import pyqtSignal as QSignal

from faction import Faction
from aifactions import AIFactions
from defines import PlayerType as PT
from defines import AIMode as AI
from stylesheet import StyleSheet as ST



class NewGame(QWidget):

    """ The class implements the dialog used to setup new games """

    file_saved = QSignal(list)

    def __init__(self, people, rules):
        super().__init__()
        self.faction_selector = QComboBox()
        self.faction_setup = QPushButton()
        self.advanced_game = QPushButton()
        self.list_of_monikers = people.monikers
        self.solo_start = QPushButton()
        self.help = QPushButton()
        self.ruleset = rules
        self.map_size = []
        self.difficulty = []
        self.faction_name = []
        self.faction_data = []
        self._setup_wizard()
        self._create_layout()
        for ai in people.ai_faction:
            self.faction_selector.addItem(ai.singular)
            self.faction_data.append(ai)
            self.faction_name.append(ai.singular)
        self.faction_selector.addItem('Random')
        self.faction_name.append('Random')
        self.faction_data.append(Faction())


    def _create_layout(self):
        """ Specify the overall layout of the dialog """
        right_side = QWidget()
        right_vl = QVBoxLayout(right_side)
        right_vl.addWidget(self._create_faction_box())
        right_vl.addSpacing(20)
        right_vl.addWidget(self._create_game_box())
        right_vl.addStretch()
        right_vl.addLayout(self._create_button_layout())
        right_vl.addSpacing(15)
        left_side = QWidget()
        left_vl = QVBoxLayout(left_side)
        left_vl.setSpacing(0)
        left_vl.addWidget(self._create_mode_box())
        left_vl.addSpacing(20)
        left_vl.addWidget(self._create_size_box())
        left_vl.addStretch()
        layout_hl = QHBoxLayout(self)
        layout_hl.setSpacing(0)
        layout_hl.addWidget(left_side)
        layout_hl.addWidget(right_side)


    def _create_button_layout(self):
        """ Create a layout for a button bar below the other controls """
        button_size = QSize(160, 50)
        buttons_hl = QHBoxLayout()
        self.solo_start = QPushButton()
        self.solo_start.setText('&OK')
        self.solo_start.setToolTip(' Start a new game with default settings.')
        self.solo_start.setShortcut(QKeySequence('Ctrl+O'))
        self.solo_start.setFixedSize(button_size)
        self.solo_start.clicked.connect(self._start_game)
        buttons_hl.addWidget(self.solo_start)
        cancel = QPushButton()
        cancel.setText('&Cancel')
        cancel.setToolTip(' Close this dialog.')
        cancel.setShortcut(QKeySequence('Ctrl+C'))
        cancel.setFixedSize(button_size)
        cancel.clicked.connect(self.hide)
        buttons_hl.addStretch()
        buttons_hl.addWidget(cancel)
        self.help = QPushButton()
        self.help.setText('&Help')
        self.help.setToolTip(' Read the game manual.')
        self.help.setShortcut(QKeySequence('Ctrl+H'))
        self.help.setFixedSize(button_size)
        buttons_hl.addStretch()
        buttons_hl.addWidget(self.help)
        return buttons_hl


    def _setup_wizard(self):
        """ Define the window title, icon and the style for the wizard """
        self.setWindowTitle('New Game')
        self.setStyleSheet(ST.SIMPLESETUP.value)
        icon = QIcon()
        icon.addPixmap(QPixmap(':/Icons/Host'))
        self.setWindowIcon(icon)
        self.setFixedSize(800, 600)
        self.hide()


    def _create_faction_box(self):
        """ Implement a combo box to select predefined factions """
        box = QGroupBox()
        box.setTitle('Player Faction')
        faction_vl = QVBoxLayout(box)
        faction_vl.addWidget(self.faction_selector)
        self.faction_setup.setText('Customize &Faction')
        self.faction_setup.setShortcut(QKeySequence('Ctrl+F'))
        faction_vl.addWidget(self.faction_setup)
        return box


    def _create_game_box(self):
        """ Implement a button to switch to the advanced setup mode """
        box = QGroupBox()
        box.setTitle('Advanced Game')
        game_vl = QVBoxLayout(box)
        self.advanced_game.setText('&Advanced Game Configuration')
        self.advanced_game.setShortcut(QKeySequence('Ctrl+A'))
        explanation = QLabel('This button allows You to configure multi-player games '
                             'and customize advanced game options. You do not need to '
                             'press it to launch standard single player games.')
        explanation.setWordWrap(True)
        game_vl.addWidget(explanation)
        game_vl.addWidget(self.advanced_game)
        return box


    def _add_button(self, name, layout, buttonlist):
        """ Create a new button for the specified layout & append it to the list """
        button = QRadioButton(name)
        layout.addWidget(button)
        buttonlist.append(button)


    def _create_size_box(self):
        """ Implement a radio button to select the size of the galaxy """
        box = QGroupBox()
        box.setTitle('Universe Size')
        size_vl = QVBoxLayout(box)
        size_vl.setSpacing(0)
        self._add_button('Tiny', size_vl, self.map_size)
        self._add_button('Small', size_vl, self.map_size)
        self._add_button('Medium', size_vl, self.map_size)
        self._add_button('Large', size_vl, self.map_size)
        self._add_button('Huge', size_vl, self.map_size)
        return box


    def _create_mode_box(self):
        """ Implement radio buttons to modify the game's difficulty """
        box = QGroupBox()
        box.setTitle('Difficulty Level')
        mode_vl = QVBoxLayout(box)
        mode_vl.setSpacing(0)
        self._add_button('Easy', mode_vl, self.difficulty)
        self._add_button('Standard', mode_vl, self.difficulty)
        self._add_button('Harder', mode_vl, self.difficulty)
        self._add_button('Expert', mode_vl, self.difficulty)
        return box


    def configure_game(self):
        """ Open the new game wizard with default values """
        self.faction_selector.setCurrentIndex(0)
        self.map_size[1].setChecked(True)
        self.difficulty[1].setChecked(True)
        self.show()


    def add_custom_faction(self, newfaction):
        """ A custom faction has been created in the advanced game setup """
        if newfaction.singular in self.faction_name:
            i = self.faction_name.index(newfaction.singular)
            self.faction_data[i] = newfaction
        else:
            self.faction_selector.addItem(newfaction.singular)
            self.faction_data.append(newfaction)
            self.faction_name.append(newfaction.singular)
            i = self.faction_selector.count() - 1
        self.faction_selector.setCurrentIndex(i)


    def _get_number_of_factions(self):
        """ Return the number of AI controlled factions """
        difficulty = 0
        for mode in self.difficulty:
            if mode.isChecked():
                break
            difficulty += 1
        player = [[2, 2, 3, 3], [3, 3, 4, 4], [7, 7, 9, 9], [12, 12, 16, 16], [16, 16, 20, 20]]
        index = 0
        for size in self.map_size:
            if size.isChecked():
                break
            index += 1
        return player[index][difficulty]


    def _get_game_difficulty(self):
        """ Determine the difficulty level of the new game """
        ai_modes = [AI.AI0, AI.AI1, AI.AI2, AI.AI3]
        index  = 0
        for mode in self.difficulty:
            if mode.isChecked():
                return ai_modes[index].name
            index += 1
        return AI.AIR.name


    def _create_game_factions(self):
        """ Prepare a new game with predefined AI controlled factions """
        monikers = list(self.list_of_monikers)
        factions = list(AIFactions)
        pfaction = self.faction_data[self.faction_selector.currentIndex()]
        if pfaction.plural in monikers:
            monikers.remove(pfaction.plural)
        mode = self._get_game_difficulty()
        players = [['The ' + pfaction.plural, PT.HUP.name, ''] + pfaction.serialize()]
        n = self._get_number_of_factions()
        while n > 1:
            faction = random.choice(factions)
            name = random.choice(monikers)
            monikers.remove(name)
            p = ['The ' + name + 's', PT.AIP.name, mode] + faction.value
            p[5] = name
            p[6] = name + 's'
            n -= 1
            players.append(p)
        return players


    def _create_game_data(self):
        """ Configure the properties of the star map used for the game """
        names = [['Shooting Fish in a Barrel', 'Duck Hunt', 'Pressure Cooker', 'White Dwarf'],
                 ['A Walk in the Park', 'A barefoot Jaywalk', 'Roller Ball', 'Blade Runner'],
                 ['Sleepwalking in Paradise', 'A Rumble in the Jungle', 'Wall Street', 'D-Day'],
                 ['The Big Easy', 'Silent Running', 'Big League', 'War of the Worlds'],
                 ['Eternal Bliss', 'Jungle Safari', 'Long Road to Morning', 'Eternity in Hell']]
        gangs = [False, False, False, True]
        dist = [1, 1, 2, 2]
        d = 0
        s = 0
        for mode in self.difficulty:
            if mode.isChecked():
                break
            d += 1
        for size in self.map_size:
            if size.isChecked():
                break
            s += 1
        return [names[s][d], s, 1, dist[d], False, False, False, False, gangs[d], False, False]


    def _create_win_conditions(self):
        """ Specify the victory conditions for a preconfigured game scenario """
        d_day = [60, 22, 4, -1, 100, -1, -1, -1, 1, 70]
        eternal_bliss = [60, 22, 4, -1, 100, -1, -1, -1, 1, 110]
        big_easy = [60, 22, 4, -1, 100, -1, -1, -1, 1, 90]
        sleepwalking_in_paradise = [60, 22, 4, -1, 100, -1, -1, -1, 1, 70]
        walk_in_the_park = [60, 22, 4, -1, 100, -1, -1, -1, 1, 50]
        shooting_fish_in_a_barrel = [60, 22, 4, -1, 100, -1, -1, -1, 1, 30]
        eternity_in_a_hell = [60, 22, 4, -1, 100, -1, -1, -1, 1, 110]
        return d_day


    def _start_game(self):
        """ Launch a new game with predefined parameters """
        save_game = QFileDialog(self)
        save_game.setOption(save_game.Option.DontUseNativeDialog)
        save_game.setStyleSheet(ST.FILEBROWSER.value)
        save_game.setMinimumSize(1000, 750)
        save_game.setFileMode(save_game.FileMode.AnyFile)
        save_game.setViewMode(save_game.ViewMode.List)
        save_game.setAcceptMode(save_game.AcceptMode.AcceptSave)
        save_game.setNameFilters(['Game Files (*.xy)', 'All Files (*.*)'])
        save_game.setDefaultSuffix('xy')
        if save_game.exec():
            files = save_game.selectedFiles()
            try:
                with open(files[0], 'wt', encoding='utf-8') as f:
                    scenario = self._create_game_data()
                    scenario += self._create_game_factions()
                    scenario += self._create_win_conditions()
                    json.dump(scenario, f)
                    self.file_saved.emit(scenario)
            except OSError:
                self.error.setText('Failed to save game data!')
                self.error.exec()

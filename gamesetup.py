
""" This module implements the advanced game setup wizard """

import random
import json

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QHeaderView
from PyQt6.QtWidgets import QTableView, QMenu
from PyQt6.QtWidgets import QStackedLayout, QSpinBox
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton, QLineEdit

from PyQt6.QtCore import pyqtSignal as QSignal

from defines import PlayerType as PT
from defines import AIMode as AI
from guidesign import GuiDesign, GuiStyle
from faction import Faction
from victory import Victory
from playerdata import PlayerData




class GameSetup(QWidget):

    """ This class implements the graphical elements for the advanced game setup dialog """

    configure_faction = QSignal(bool, bool)

    ai_modes = [AI.AI0, AI.AI1, AI.AI2, AI.AI3, AI.AIR]

    def __init__(self, people, rules):
        super().__init__()
        self.setWindowTitle("Advanced New Game Wizard - Step 1 of 3")
        self.setStyleSheet(GuiDesign.get_style(GuiStyle.ADVANCEDSETUP_1))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Icons/Host"))
        self.setWindowIcon(icon)
        self.setFixedSize(1000, 750)
        self.hide()
        self.wizard = QWidget()
        self.pages = QStackedLayout(self.wizard)
        self.current_page = 0
        self.victory_condition = {}
        self.condition_counter = 4
        self.active_conditions = QSpinBox()
        self.game_feature = []
        self.map_size = []
        self.star_density = []
        self.player_distance = []
        self.factions = people
        self.rules = rules
        self.number_of_players = rules.get_number_of_players()
        self.model = PlayerData(people, self.number_of_players)
        self.players = QTableView()
        self.game_duration = QSpinBox()
        self.game_name = QLineEdit()
        self._setup_error_messages()
        self._setup_universe()
        self._setup_players()
        self._setup_victory_conditions()
        self._setup_menu(people)
        self._setup_buttons()


    def _setup_error_messages(self):
        """ Create a modal dialog to display error messages to the player """
        self.error = QMessageBox(self)
        self.error.setIcon(self.error.Icon.Warning)
        self.error.setWindowTitle('Advanced New Game Wizard')
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Icons/Stars"))
        self.error.setWindowIcon(icon)


    def _setup_buttons(self):
        """ Create the buttons to navigate through the pages of the wizard """
        button_size = QSize(140, 50)
        buttons_hl = QHBoxLayout()
        self.finish = QPushButton()
        self.finish.setText('Finish')
        self.finish.setToolTip(' Save the game settings.')
        self.finish.setFixedSize(button_size)
        self.finish.setShortcut(QKeySequence('Ctrl+F'))
        cancel = QPushButton()
        cancel.setText("Cancel")
        cancel.setToolTip(" Close this dialog.")
        cancel.setFixedSize(button_size)
        cancel.setShortcut(QKeySequence('Ctrl+C'))
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
        buttons_hl.addWidget(cancel)
        buttons_hl.addStretch()
        buttons_hl.addWidget(self.back)
        buttons_hl.addStretch()
        buttons_hl.addWidget(self.next)
        buttons_hl.addStretch()
        buttons_hl.addWidget(self.finish)
        buttons_hl.addSpacing(30)
        layout_vl = QVBoxLayout(self)
        layout_vl.addWidget(self.wizard)
        layout_vl.addLayout(buttons_hl)
        self.finish.clicked.connect(self._save_game_data)
        self.back.clicked.connect(self.revert)
        self.next.clicked.connect(self.proceed)
        cancel.clicked.connect(self.hide)


    def proceed(self):
        """ Go to the next page of the configuration wizard """
        if self.current_page < 2:
            self.current_page += 1
            step = 'Step ' + str(1 + self.current_page) + ' of 3'
            self.setWindowTitle('Advanced New Game Wizard - ' + step)
            self.pages.setCurrentIndex(self.current_page)
            self.back.setEnabled(True)
            self.next.setEnabled(self.current_page < 2)


    def revert(self):
        """ Return to the previous page of the configuration wizard """
        if 0 < self.current_page:
            self.current_page -= 1
            step = 'Step ' + str(1 + self.current_page) + ' of 3'
            self.setWindowTitle('Advanced New Game Wizard - ' + step)
            self.pages.setCurrentIndex(self.current_page)
            self.next.setEnabled(True)
            self.back.setEnabled(self.current_page > 0)


    def configure_game(self, map_size):
        """ Restore default settings before the configuration wizard is invoked """
        self.current_page = 0
        self.pages.setCurrentIndex(0)
        self.player_distance[1].setChecked(True)
        self.star_density[1].setChecked(True)
        index = 0
        for m in map_size:
            if m.isChecked():
                break
            index += 1
        self.map_size[index].setChecked(True)
        self.next.setEnabled(True)
        self.back.setEnabled(False)
        for rb in self.game_feature:
            rb.setChecked(False)
        self.game_name.setText('')
        self._restore_victory_conditions()
        self.model.reset_model(self.factions, self.number_of_players)
        self.show()


    def load_faction(self):
        """ Read & process a faction definition (*.f1) from disk """
        read_faction = QFileDialog(self)
        read_faction.setOption(read_faction.Option.DontUseNativeDialog)
        read_faction.setStyleSheet(GuiDesign.get_style(GuiStyle.FILEBROWSER))
        read_faction.setMinimumSize(1000, 750)
        read_faction.setFileMode(read_faction.FileMode.AnyFile)
        read_faction.setViewMode(read_faction.ViewMode.List)
        read_faction.setAcceptMode(read_faction.AcceptMode.AcceptOpen)
        read_faction.setNameFilters(['Game Files (*.f1)', 'All Files (*.*)'])
        read_faction.setDefaultSuffix('f1')
        if read_faction.exec():
            files = read_faction.selectedFiles()
            try:
                with open(files[0], 'rt', encoding='utf-8') as f:
                    fnew = Faction()
                    fnew.deserialize(json.load(f))
                    return fnew
            except (json.JSONDecodeError, UnicodeDecodeError):
                self.error.setText('Invalid Faction Specification!')
                self.error.exec()
            except OSError:
                self.error.setText('Failed to open file!')
                self.error.exec()
        return None


    def _collect_game_data_from_page_1(self):
        """ Collect the configuration data from the first page of the wizard """
        name = self.game_name.text()
        if not name:
            name = self.rules.get_default_game_name()
        data = [name]
        for rb in self.map_size:
            if rb.isChecked():
                data.append(self.map_size.index(rb))
                break
        for rb in self.star_density:
            if rb.isChecked():
                data.append(self.star_density.index(rb))
                break
        for rb in self.player_distance:
            if rb.isChecked():
                data.append(self.player_distance.index(rb))
                break
        for rb in self.game_feature:
            data.append(rb.isChecked())
        return data


    def _collect_player_data_from_page_2(self):
        """ Compile the faction data from the second page of the wizard """
        players = []
        for ptype, pmode, pfaction, pname in self.model.players.values():
            if pmode:
                if pmode == AI.AIR:
                    pmode = self.ai_modes[random.randint(0, 3)]
                p = [pname, ptype.name, pmode.name]
            else:
                p = [pname, ptype.name, '']
            players.append(p + pfaction.serialize())
        return players


    def _save_game_data(self):
        """ Save the faction specification to a file """
        save_game = QFileDialog(self)
        save_game.setOption(save_game.Option.DontUseNativeDialog)
        save_game.setStyleSheet(GuiDesign.get_style(GuiStyle.FILEBROWSER))
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
                    game_data = self._collect_game_data_from_page_1()
                    game_data += self._collect_player_data_from_page_2()
                    for radio, spinner in self.victory_condition.values():
                        if radio.isChecked():
                            game_data.append(spinner.value())
                        else:
                            game_data.append(-1)
                    game_data.append(self.active_conditions.value())
                    game_data.append(self.game_duration.value())
                    json.dump(game_data, f)
            except OSError:
                self.error.setText('Failed to save game data!')
                self.error.exec()


    def _setup_menu(self, people):
        """ Create the menu used to add new players to the game roster """
        self.select = QMenu()
        self.select.setStyleSheet(GuiDesign.get_style(GuiStyle.PLAYERMENU))
        submenu = self.select.addMenu('Predefined Faction  ')
        n = 1
        for ai in people.ai_faction:
            a = submenu.addAction(ai.species)
            a.setData((0, n, 0))
            n += 1
        a = submenu.addAction('Random')
        a.setData((0, 0, 0))
        submenu = self.select.addMenu('Custom Faction')
        a = submenu.addAction('New Faction')
        a.setData((1, 0, 0))
        a = submenu.addAction('Open File')
        a.setData((1, 1, 0))
        submenu.addSeparator()
        n = 0
        for pc in people.player:
            a = submenu.addAction(pc.name)
            a.setData((1, 2, n))
            n += 1
        self.select.addSeparator()
        submenu = self.select.addMenu('Computer Player')
        n = 1
        for ai in people.ai_faction:
            modemenu = submenu.addMenu(ai.name + '  ')
            m = 0
            for mode in AI:
                a = modemenu.addAction(mode.value)
                a.setData((2, n, m))
                m += 1
            n += 1
        modemenu = submenu.addMenu('Random')
        m = 0
        for mode in AI:
            a = modemenu.addAction(mode.value)
            a.setData((2, 0, m))
            m += 1
        self.select.addSeparator()
        submenu = self.select.addMenu('Expansion Slot')
        n = 1
        for ai in people.ai_faction:
            a = submenu.addAction(ai.species)
            a.setData((3, n, 0))
            n += 1
        a = submenu.addAction('Random')
        a.setData((3, 0, 0))
        self.select.addSeparator()
        a = self.select.addAction('Remove Player')
        a.setData((4, 0, 0))


    def _add_game_feature(self, layout, text, hotkey):
        """ Create a radio button to select a specific game feature """
        rb = QRadioButton(text)
        rb.setStyleSheet('font-size: 20pt;font-style: oblique;font-weight: 400;')
        rb.setShortcut(QKeySequence(hotkey))
        layout.addWidget(rb)
        self.game_feature.append(rb)


    def _create_universe_size_box(self):
        """ Create a group of buttons to select the size of the galaxy """
        size_box = QGroupBox(self)
        size_box.setTitle('Universe Size')
        tiny = QRadioButton('Tiny')
        small = QRadioButton('Small')
        medium = QRadioButton('Medium')
        large = QRadioButton('Large')
        huge = QRadioButton('Huge')
        self.map_size = [tiny, small, medium, large, huge]
        size_vl = QVBoxLayout(size_box)
        size_vl.setSpacing(0)
        size_vl.addWidget(tiny)
        size_vl.addWidget(small)
        size_vl.addWidget(medium)
        size_vl.addWidget(large)
        size_vl.addWidget(huge)
        small.setChecked(True)
        return size_box


    def _create_universe_density_box(self):
        """ Create a group of buttons to select the density of stars within the galaxy """
        density_box = QGroupBox(self)
        density_box.setTitle('Density')
        sparse = QRadioButton('Sparse')
        normal = QRadioButton('Normal')
        dense = QRadioButton('Dense')
        packed = QRadioButton('Packed')
        self.star_density = [sparse, normal, dense, packed]
        density_vl = QVBoxLayout(density_box)
        density_vl.setSpacing(0)
        density_vl.addWidget(sparse)
        density_vl.addWidget(normal)
        density_vl.addWidget(dense)
        density_vl.addWidget(packed)
        normal.setChecked(True)
        return density_box


    def _create_player_position_box(self):
        """ Create a group of buttons to select the initial distance between home worlds """
        player_box = QGroupBox()
        player_box.setTitle('Player Positions')
        player_box.setMinimumWidth(300)
        close = QRadioButton('Close')
        moderate = QRadioButton('Moderate')
        farther = QRadioButton('Farther')
        large = QRadioButton('Distant')
        self.player_distance = [close, moderate, farther, large]
        player_vl = QVBoxLayout(player_box)
        player_vl.setSpacing(0)
        player_vl.addWidget(close)
        player_vl.addWidget(moderate)
        player_vl.addWidget(farther)
        player_vl.addWidget(large)
        moderate.setChecked(True)
        return player_box


    def _setup_universe(self):
        """ Create the first page of the advanced game setup wizard """
        size_box = self._create_universe_size_box()
        density_box = self._create_universe_density_box()
        player_box = self._create_player_position_box()
        left_side = QWidget()
        left_side.setMinimumWidth(240)
        left_vl = QVBoxLayout(left_side)
        left_vl.setSpacing(0)
        left_vl.addWidget(size_box)
        left_vl.addSpacing(20)
        left_vl.addWidget(density_box)
        left_vl.addStretch()
        right_side = QWidget()
        right_vl = QVBoxLayout(right_side)
        right_vl.setSpacing(0)
        right_vl.addWidget(player_box)
        right_vl.addSpacing(20)
        self._add_game_feature(right_vl, ' &Beginner: Abundance of Minerals', 'Ctrl+B')
        self._add_game_feature(right_vl, ' &Slower Advances in Technology', 'Ctrl+S')
        self._add_game_feature(right_vl, ' Acclererated &Multi-player Game', 'Ctrl+M')
        self._add_game_feature(right_vl, ' No &Random Events', 'Ctrl+R')
        self._add_game_feature(right_vl, ' Computer Players form &Alliances', 'Ctrl+A')
        self._add_game_feature(right_vl, ' &Public Player Scores', 'Ctrl+P')
        self._add_game_feature(right_vl, ' &Galaxy features Star Clusters', 'Ctrl+G')
        right_vl.addStretch()
        layout_hl=QHBoxLayout()
        layout_hl.setSpacing(0)
        layout_hl.addWidget(left_side)
        layout_hl.addSpacing(20)
        layout_hl.addWidget(right_side)
        layout_hl.addStretch()
        self.game_name.setPlaceholderText('Silent Running')
        self.game_name.setMaxLength(56)
        self.game_name.setMinimumWidth(670)
        name_label=QLabel('Game Name:')
        name_label.setStyleSheet('font-size: 20pt;font-style: oblique;font-weight: 600;')
        game_hl=QHBoxLayout()
        game_hl.addStretch()
        game_hl.addWidget(name_label)
        game_hl.addSpacing(20)
        game_hl.addWidget(self.game_name)
        game_hl.addSpacing(20)
        game_world=QWidget()
        layout_vl=QVBoxLayout(game_world)
        layout_vl.addLayout(game_hl)
        layout_vl.addSpacing(10)
        layout_vl.addLayout(layout_hl)
        layout_vl.addStretch()
        self.pages.addWidget(game_world)


    def _setup_players(self):
        """ Create the layout for the player roster """
        self.players.setShowGrid(False)
        self.players.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.players.setModel(self.model)
        align = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        header_h = self.players.horizontalHeader()
        header_h.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        header_h.setStretchLastSection(True)
        header_h.resizeSection(0, 200)
        header_h.resizeSection(1, 200)
        header_h.setDefaultAlignment(align)
        header_v = self.players.verticalHeader()
        header_v.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        header_v.setDefaultSectionSize(48)
        header_v.setDefaultAlignment(align)
        layout_hl = QHBoxLayout()
        layout_hl.addSpacing(20)
        layout_hl.addWidget(self.players)
        layout_hl.addSpacing(20)
        player_setup = QWidget()
        player_setup.setStyleSheet(GuiDesign.get_style(GuiStyle.ADVANCEDSETUP_2))
        layout_vl = QVBoxLayout(player_setup)
        layout_vl.addLayout(layout_hl)
        layout_vl.addSpacing(10)
        self.pages.addWidget(player_setup)
        self.players.clicked.connect(self._select_player)


    def _select_player(self, select):
        """ Add a new player to the game roster """
        if select.column() < 2:
            here = self.cursor().pos()
            selected = self.select.exec(here)
            if selected:
                s_id, f_id, m_id = selected.data()
                self._update_game_roster(select.row(), s_id, f_id, m_id)


    def _update_game_roster(self, row, s_id, f_id, m_id):
        """ Add or remove a player from the game roster """
        def select_player_faction(f_id, m_id):
            if f_id == 2:
                return self.factions.get_faction(m_id)
            if f_id == 1:
                return self.load_faction()
            self.configure_faction.emit(False, True)
            return None
        def select_ai_faction(f_id, f_type, r_type=PT.RNG):
            if f_id > 0:
                return self.factions.get_ai_faction(f_id - 1), f_type
            return self.factions.random_faction(), r_type
        fnew = None
        p_type = PT.HUP
        p_mode = None
        if s_id == 0:
            fnew, p_type = select_ai_faction(f_id, PT.HUP)
        if s_id == 1:
            fnew = select_player_faction(f_id, m_id)
        if s_id == 2:
            fnew, p_type = select_ai_faction(f_id, PT.AIP)
            p_mode = self.ai_modes[m_id]
        if s_id == 3:
            fnew, p_type = select_ai_faction(f_id, PT.EXP, PT.REX)
        if s_id == 4:
            self.model.remove_player(row)
        elif fnew:
            self.model.add_player(row, p_type, p_mode, fnew)


    def _add_victory_condition(self, vlayout, vc):
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
        self.victory_condition[vc] = (radio, data)
        radio.toggled.connect(self._adjust_condition_count)


    def _adjust_condition_count(self, enabled):
        """ Update the upper limit on the number of victory conditions """
        if enabled:
            self.condition_counter += 1
        else:
            self.condition_counter -= 1
        self.active_conditions.setRange(0, self.condition_counter)


    def _setup_victory_conditions(self):
        """ Setup the page with the victory conditions for the game """
        title = QLabel('Victory is declared if some of these conditions are met:')
        victory_settings = QWidget()
        victory_settings.setStyleSheet(GuiDesign.get_style(GuiStyle.ADVANCEDSETUP_3))
        layout_vl = QVBoxLayout(victory_settings)
        layout_vl.setSpacing(0)
        layout_vl.addWidget(title)
        layout_vl.addSpacing(20)
        for vc in Victory:
            self._add_victory_condition(layout_vl, vc)
        layout_vl.addSpacing(40)
        label = QLabel('The following number of selected conditions must be met:')
        self.active_conditions.setRange(0, 4)
        self.active_conditions.setValue(1)
        self.active_conditions.setMinimumSize(QSize(60, 40))
        self.active_conditions.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.active_conditions.setStyleSheet('font-weight: 600;')
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.active_conditions)
        layout.addStretch()
        layout_vl.addLayout(layout)
        layout_vl.addSpacing(10)
        label = QLabel('These many years must pass before a winner is declared:')
        self.game_duration.setRange(30, 500)
        self.game_duration.setSingleStep(10)
        self.game_duration.setValue(50)
        self.game_duration.setMinimumSize(QSize(85, 40))
        self.game_duration.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.game_duration.setStyleSheet('font-weight: 600;')
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.game_duration)
        layout.addStretch()
        layout_vl.addLayout(layout)
        layout_vl.addStretch()
        self.pages.addWidget(victory_settings)


    def _restore_victory_conditions(self):
        """ Recover the default victory conditions for a game """
        for vc in Victory:
            radio, spinner = self.victory_condition[vc]
            spinner.setValue(vc.value[2])
            radio.setChecked(vc.value[7])
        self.condition_counter = 4
        self.active_conditions.setRange(0, 4)
        self.active_conditions.setValue(1)
        self.game_duration.setValue(50)


""" This module implements the graphical user interface of the game """

from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QStackedLayout, QSizePolicy
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QStatusBar, QGroupBox
from PyQt6.QtWidgets import QMainWindow, QPushButton

from guidesign import GuiDesign, GuiStyle
from defines import Stance
from menubar import Menu
from toolbar import ToolBar
from inspector import Inspector
from fleetdata import Fleetdata
from minedata import Minedata
from starmap import Starmap
from newgame import NewGame
from gamesetup import GameSetup
from newsreader import NewsReader
from factionwizard import FactionWizard



def _create_button(name):
    """ Helper function to create buttons in the title bar of the inspector """
    style = "padding: 0px 2px 0px 2px;border-width: 0px;background-color: transparent"
    icon = QIcon(name)
    button = QPushButton()
    button.setIcon(icon)
    button.setIconSize(QSize(30, 30))
    button.setStyleSheet(style)
    button.setVisible(False)
    return button


def _setup_mine_filter():
    """ Create a mine filter / show all mine fields """
    fields = {}
    fields[Stance.ALLIED] = True
    fields[Stance.FRIENDLY] = True
    fields[Stance.NEUTRAL] = True
    fields[Stance.HOSTILE] = True
    return fields



class Gui(QMainWindow):

    """ This class is responsible for rendering the user interface of the game """

    def __init__(self, people, rules):
        super().__init__()
        self.current_year = rules.first_year()
        self.selected_planet = None
        self.selected_fleet = None
        self.selected_fields = []
        self.selected_fleets = []
        self.mine_filter = _setup_mine_filter()
        self.number_of_fields = 0
        self.filtered_fields = 0
        self.enemy_fleet_index = 0
        self.neutral_fleet_index = 0
        self.fleet_index = 0
        self.mine_index = 0
        self.field_index = 0
        self.enemy_fleet_offset = 0
        self.neutral_fleet_offset = 0
        self.fleet_offset = 0
        self.mine_offset = 0
        self.allied_fleets = 0
        self.neutral_fleets = 0
        self.hostile_fleets = 0
        self.show_fleet_movements = False
        self.waypoint_mode = False
        self.action = {}
        self.buttons = ToolBar()
        self.item_info = QStackedLayout(self)
        self.planet_info = Inspector(people.my_faction())
        self.fleet_info = Fleetdata()
        self.mine_info = Minedata()
        self.info_box = QGroupBox()
        self.news_reader = NewsReader()
        self.map = Starmap(people, rules)
        self.selected_object = QLabel(self)
        self.previous_field = _create_button(":/Icons/Previous")
        self.next_field = _create_button(":/Icons/Next")
        self.show_alien_base = _create_button(":/Icons/Fortress")
        self.show_neutral_base = _create_button(":/Icons/Tradehub")
        self.show_star_base = _create_button(":/Icons/Starbase")
        self.select_next_enemy = _create_button(":/Icons/Enemies")
        self.select_next_neutral = _create_button(":/Icons/Neutrals")
        self.select_next_fleet = _create_button(":/Icons/Fleets")
        self.show_planet = _create_button(":/Icons/Planet")
        self.show_fields = _create_button(":/Icons/Mines")
        self.show_fleets = _create_button(":/Icons/Ships")
        self._setup_ui(people, rules)
        self._connect_signals_and_slots()


    def _connect_signals_and_slots(self):
        """ Connect the Qt signals with their corresponding slots """
        self.buttons.action_radar_view.toggled.connect(self.map.universe.show_scanner_ranges)
        self.buttons.action_planet_names.toggled.connect(self.map.universe.show_planet_names)
        self.buttons.action_concentration_view.toggled.connect(self._show_crust_diagrams)
        self.buttons.action_surface_mineral_view.toggled.connect(self._show_surface_diagrams)
        self.buttons.action_default_view.toggled.connect(self._show_default_view)
        self.buttons.action_population_view.toggled.connect(self._show_population_view)
        self.buttons.action_no_info_view.toggled.connect(self._show_minimal_view)
        self.buttons.action_percent_view.toggled.connect(self._show_percentage_view)
        self.buttons.action_foes.toggled.connect(self.map.universe.enable_foe_filter)
        self.buttons.action_friendlies.toggled.connect(self.map.universe.enable_friend_filter)
        self.buttons.action_ship_count.toggled.connect(self.map.universe.show_ship_count)
        self.buttons.action_waiting_fleets.toggled.connect(self.map.universe.filter_idle_fleets)
        self.buttons.action_path_overlay.toggled.connect(self._show_movements)
        self.buttons.action_add_waypoint.toggled.connect(self._add_waypoints)
        self.next_field.clicked.connect(self._show_next_mine_field)
        self.previous_field.clicked.connect(self._show_previous_mine_field)
        self.buttons.action_no_info_view.setChecked(True)
        self.buttons.radar_range.valueChanged.connect(self.map.universe.scale_radar_ranges)
        self.menu.change_zoom.connect(self.map.resize_starmap)
        self.buttons.mines.toggled.connect(self.map.universe.show_fields)
        self.buttons.show_mines.connect(self.map.universe.show_mines)
        self.map.universe.select_field.connect(self._inspect_mine_field)
        self.map.universe.select_fleet.connect(self._inspect_fleet)
        self.map.universe.select_planet.connect(self._inspect_planet)
        self.map.universe.update_planet.connect(self.update_planet_view)
        self.map.universe.update_filter.connect(self._update_fields)
        self.map.universe.update_route.connect(self.fleet_info.update_waypoint_info)
        self.show_planet.clicked.connect(self._inspect_planets)
        self.select_next_enemy.clicked.connect(self._inspect_hostile_fleet)
        self.select_next_neutral.clicked.connect(self._inspect_neutral_fleet)
        self.select_next_fleet.clicked.connect(self._inspect_allied_fleet)
        self.show_fields.clicked.connect(self._inspect_mines)
        self.show_fleets.clicked.connect(self._inspect_fleets)
        self.buttons.filter_enemy_fleets.connect(self.map.universe.filter_foes)
        self.buttons.filter_my_fleets.connect(self.map.universe.filter_fleets)
        self.menu.action_new_game.triggered.connect(self.new_game.configure_game)
        self.menu.action_wizard.triggered.connect(self.new_faction.configure_wizard)
        self.new_game.faction_setup.clicked.connect(self._configure_faction)
        self.new_game.advanced_game.clicked.connect(self._configure_game)
        self.game_setup.configure_faction.connect(self._configure_faction)
        self.new_faction.cancel.clicked.connect(self._abort_faction)
        self.map.universe.highlight_planet(self.map.universe.planets[-1])


    def _setup_ui(self, people, rules):
        """ Create the main layout of the user interface """
        self.setStyleSheet(GuiDesign.get_style(GuiStyle.GENERALGUI))
        sx, sy = GuiDesign.get_size()
        self.resize(sx, sy)
        self.setWindowTitle("My Stars!")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Icons/Stars"))
        self.setWindowIcon(icon)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setMinimumSize(sx, sy)
        self.new_game = NewGame(people, rules)
        self.new_game.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.game_setup = GameSetup(people, rules)
        self.game_setup.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.new_faction = FactionWizard(people, rules)
        self.new_faction.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._assemble_user_interface()
        self.menu = Menu(self)
        self.setMenuBar(self.menu)
        self.buttons.zoom.setMenu(self.menu.menu_zoom)
        self.setStatusBar(QStatusBar(self))


    def _assemble_user_interface(self):
        """ Layout the control panels on the left side & the star map """
        left_side = QWidget()
        left_side.setMinimumWidth(875)        # Minimal feasible value ...
        left_side.setMaximumWidth(875)
        layout_hl = QHBoxLayout(self.central_widget)
        layout_hl.setSpacing(0)
        layout_vl = QVBoxLayout(left_side)
        layout_vl.setSpacing(0)
        self.buttons.setAutoFillBackground(True)
        self.buttons.setMovable(False)
        self.buttons.setIconSize(QSize(40, 40))
        layout_vl.addWidget(self.buttons)
        policy = QSizePolicy()
        policy.setHorizontalPolicy(policy.Policy.MinimumExpanding)
        policy.setVerticalPolicy(policy.Policy.MinimumExpanding)
        self.info_box.setSizePolicy(policy)
        layout_vl.addWidget(self.info_box)
        layout_vl.addWidget(self.news_reader)
        info_box = QGroupBox()
        info_box.setMinimumHeight(420)
        info_box.setMaximumHeight(420)
        info_vl = QVBoxLayout(info_box)
        info_vl.setSpacing(0)
        info_vl.addWidget(self._setup_inspector_title())
        image = QSvgWidget(":/Graphics/Enigma")
        image.setMaximumSize(300, 300)
        enigma = QWidget()
        enigma_hl = QHBoxLayout(enigma)
        enigma_hl.addStretch()
        enigma_hl.addWidget(image)
        enigma_hl.addStretch()
        self.item_info.addWidget(self.planet_info)
        self.item_info.addWidget(self.fleet_info)
        self.item_info.addWidget(self.mine_info)
        self.item_info.addWidget(enigma)
        info_vl.addLayout(self.item_info)
        layout_vl.addWidget(info_box)
        layout_hl.addWidget(left_side)
        layout_hl.addWidget(self.map)


    def _setup_inspector_title(self):
        """ Create the visual elements of the inspector's title bar """
        title = QWidget()
        selected_object_hl = QHBoxLayout(title)
        selected_object_hl.setSpacing(0)
        selected_object_hl.addSpacing(250)
        self.selected_object.setAlignment(Qt.AlignmentFlag.AlignCenter)
        selected_object_hl.addWidget(self.selected_object)
        button_box = QWidget()
        button_box.setMaximumWidth(180)
        button_layout_hl = QHBoxLayout(button_box)
        button_layout_hl.setSpacing(0)
        button_layout_hl.addStretch()
        button_layout_hl.addWidget(self.previous_field)
        button_layout_hl.addWidget(self.next_field)
        button_layout_hl.addWidget(self.show_alien_base)
        button_layout_hl.addWidget(self.show_neutral_base)
        button_layout_hl.addWidget(self.show_star_base)
        button_layout_hl.addWidget(self.select_next_enemy)
        button_layout_hl.addWidget(self.select_next_neutral)
        button_layout_hl.addWidget(self.select_next_fleet)
        selected_object_hl.addWidget(button_box)
        switch_box = QWidget()
        switch_box.setMaximumWidth(70)
        switch_layout_hl = QHBoxLayout(switch_box)
        switch_layout_hl.setSpacing(0)
        switch_layout_hl.addStretch(0)
        switch_layout_hl.addWidget(self.show_planet)
        switch_layout_hl.addWidget(self.show_fields)
        switch_layout_hl.addWidget(self.show_fleets)
        selected_object_hl.addWidget(switch_box)
        title.setMinimumHeight(68)
        return title


    def display_starbase_icons(self, p=None):
        """ Display the proper button for the orbiting starbase """
        if p:
            if p.relation == Stance.ALLIED:
                self.show_neutral_base.setVisible(False)
                self.show_alien_base.setVisible(False)
                self.show_star_base.setVisible(p.space_station)
            elif p.relation == Stance.HOSTILE:
                self.show_neutral_base.setVisible(False)
                self.show_star_base.setVisible(False)
                self.show_alien_base.setVisible(p.space_station and p.ship_tracking)
            else:
                self.show_alien_base.setVisible(False)
                self.show_star_base.setVisible(False)
                self.show_neutral_base.setVisible(p.space_station and p.ship_tracking)
        else:
            self.show_neutral_base.setVisible(False)
            self.show_alien_base.setVisible(False)
            self.show_star_base.setVisible(False)


    def _display_fleet_icons(self):
        """ Display indicators for fleets in a planet's orbit """
        self.select_next_enemy.setVisible(self.hostile_fleets > 0)
        self.select_next_neutral.setVisible(self.neutral_fleets > 0)
        self.select_next_fleet.setVisible(self.allied_fleets > 0)


    def update_planet_view(self, p):
        """ Update the planetary data displayed in the inspector panel """
        if self.item_info.currentIndex() < 2:
            self.allied_fleets = p.total_friends
            if p.ship_tracking:
                self.hostile_fleets = p.total_foes
                self.neutral_fleets = p.total_others
            else:
                self.hostile_fleets = 0
                self.neutral_fleets = 0
            self._display_fleet_icons()
        if self.item_info.currentIndex() == 1:
            if self.enemy_fleet_offset > 0 and p.total_foes > 0:
                self.enemy_fleet_offset = 0
                self._inspect_hostile_fleet()
            elif self.neutral_fleet_offset > 0 and p.total_others > 0:
                self.neutral_fleet_offset = 0
                self._inspect_neutral_fleet()
            elif self.fleet_offset > 0 and p.total_friends > 0:
                self.fleet_offset = 0
                self._inspect_fleets()
            elif p.total_foes > 0:
                self.enemy_fleet_offset = 0
                self._inspect_hostile_fleet()
            elif p.total_others > 0:
                self.neutral_fleet_offset = 0
                self._inspect_neutral_fleet()
            elif p.total_friends > 0:
                self.fleet_offset = 0
                self._inspect_fleets()
            else:
                self._inspect_planet(p)


    def _inspect_planet(self, p):
        """ Show planet data in the inspector panel """
        self.selected_planet = p
        self.selected_fleets = p.fleets_in_orbit
        self.selected_fields = p.mine_fields
        self._apply_mine_filter()
        self.previous_field.setVisible(False)
        self.next_field.setVisible(False)
        self.show_planet.setVisible(False)
        self.show_fleets.setVisible(False)
        self.show_fields.setVisible(self.filtered_fields > 0)
        self.enemy_fleet_offset = 0
        self.neutral_fleet_offset = 0
        self.fleet_offset = 0
        self.mine_offset = 0
        if p.discovered:
            self.item_info.setCurrentIndex(0)
            self.planet_info.update_minerals(p)
            self.planet_info.update_biome(p)
            self.planet_info.update_text(self.current_year, p)
        else:
            self.item_info.setCurrentIndex(3)
        self.allied_fleets = p.total_friends
        if p.ship_tracking:
            self.hostile_fleets = p.total_foes
            self.neutral_fleets = p.total_others
        else:
            self.hostile_fleets = 0
            self.neutral_fleets = 0
        self.display_starbase_icons(p)
        self._display_fleet_icons()
        self.selected_object.setText(p.name)


    def _inspect_fleet(self, planet, index, f_list, m_list):
        """ Show fleet data in the inspector panel """
        self.enemy_fleet_offset = 0
        self.neutral_fleet_offset = 0
        self.fleet_offset = 0
        self.fleet_index = index % len(f_list)
        self.selected_fleets = f_list
        self.selected_planet = planet
        self.selected_fields = m_list
        self.allied_fleets = 0
        self.hostile_fleets = 0
        self.neutral_fleets = 0
        fleets = 0
        for f in f_list:
            if f.ship_counter > 0:
                if f.friend_or_foe == Stance.ALLIED:
                    self.allied_fleets += 1
                elif f.friend_or_foe == Stance.HOSTILE:
                    self.hostile_fleets += 1
                else:
                    self.neutral_fleets += 1
                fleets += 1
        self.next_field.setVisible(False)
        self.previous_field.setVisible(False)
        self.show_fleets.setVisible(False)
        if fleets > 0:
            self.display_starbase_icons(planet)
            self._apply_mine_filter()
            self.show_fields.setVisible(self.filtered_fields > 0)
            fof = f_list[self.fleet_index].friend_or_foe
            if fof == Stance.ALLIED:
                self._inspect_allied_fleet()
            elif fof == Stance.HOSTILE:
                self._inspect_hostile_fleet()
            else:
                self._inspect_neutral_fleet()
        elif planet:
            self._inspect_planet(planet)
        else:
            self.item_info.setCurrentIndex(3)
            self.show_fields.setVisible(False)
            self._display_fleet_icons()
            self.selected_object.setText("Deep Space")


    def _update_fields(self, new_filter):
        """ Filter mine field data in the inspector panel """
        self.mine_filter = new_filter
        self._apply_mine_filter()
        if self.item_info.currentIndex() < 2:
            self.show_fields.setVisible(self.filtered_fields > 0)
        elif self.item_info.currentIndex() < 3:
            if self.filtered_fields > 0:
                self._inspect_mines()
            elif self.selected_planet:
                self._inspect_planets()
            elif self.selected_fleets:
                self._inspect_fleets()
            else:
                self.item_info.setCurrentIndex(3)
                self.previous_field.setVisible(False)
                self.next_field.setVisible(False)
                self.show_fleets.setVisible(False)
                self.selected_object.setText("Deep Space")


    def _inspect_mine_field(self, planet, index, m_list, f_list):
        """ Show mine fields in the inspector panel """
        self.selected_fields = m_list
        self.mine_index = index
        self.selected_planet = planet
        self.selected_fleets = f_list
        self._inspect_mines()


    def _next_fleet(self, index, offset, fof):
        """ Skip to a new fleet in the inspector panel using the
            index of the current fleet and an arbitrary offset """
        if self.selected_planet:
            self.show_planet.setVisible(True)
            self.show_fields.setVisible(False)
        else:
            self.show_planet.setVisible(False)
        if self.selected_fleet:
            self.selected_fleet.colour_course(False)
            self.selected_fleet.show_course(self.show_fleet_movements)
        self._display_fleet_icons()
        self.item_info.setCurrentIndex(1)
        nmax = len(self.selected_fleets)
        n = (index + offset) % nmax
        while n < nmax:
            f = self.selected_fleets[n]
            if f.ship_counter > 0 and f.friend_or_foe in fof:
                self.selected_object.setText(f.name + ' #' + str(f.id))
                self.fleet_info.update_fleet_data(f)
                f.show_course(True)
                f.colour_course(True)
                self.selected_fleet = f
                self.map.universe.selected_fleet = f
                self.map.universe.fleet_index = n
                return n
            n += 1
        n = 0
        while n <= index:
            f = self.selected_fleets[n]
            if f.ship_counter > 0 and f.friend_or_foe in fof:
                self.selected_object.setText(f.name + ' #' + str(f.id))
                self.fleet_info.update_fleet_data(f)
                f.show_course(True)
                f.colour_course(True)
                self.map.universe.selected_fleet = f
                self.map.universe.fleet_index = n
                break
            n += 1
        return n


    def _next_minefield(self, i0, offset):
        """ Skip to a new mine field in the inspector panel using the
            index of the current mine field and an arbitrary offset """
        self.field_index += self.filtered_fields + offset
        self.field_index %= self.filtered_fields
        i = (i0 + self.number_of_fields + offset) % self.number_of_fields
        while i < self.number_of_fields:
            m = self.selected_fields[i]
            if self.mine_filter[m.fof]:
                self.mine_info.update_data(m, self.field_index + 1, self.filtered_fields)
                self.selected_object.setText(m.model.value + ' Mine Field #' + str(m.id))
                return i
            i += 1
        i = 0
        while i <= i0:
            m = self.selected_fields[i]
            if self.mine_filter[m.fof]:
                self.mine_info.update_data(m, self.field_index + 1, self.filtered_fields)
                self.selected_object.setText(m.model.value + ' Mine Field #' + str(m.id))
                break
            i += 1
        return i


    def _inspect_hostile_fleet(self):
        """ Show hostile fleets in the inspector panel """
        self.hostile_fleets -= 1
        self.enemy_fleet_index = self._next_fleet(self.enemy_fleet_index,
                                                  self.enemy_fleet_offset, [Stance.HOSTILE])
        self.hostile_fleets += 1
        self.enemy_fleet_offset = 1
        self.neutral_fleet_offset = 0
        self.fleet_offset = 0


    def _inspect_neutral_fleet(self):
        """ Show neutral fleets in the inspector panel """
        fof = [Stance.FRIENDLY, Stance.NEUTRAL]
        self.neutral_fleets -= 1
        self.neutral_fleet_index = self._next_fleet(self.neutral_fleet_index,
                                                    self.neutral_fleet_offset, fof)
        self.neutral_fleets += 1
        self.enemy_fleet_offset = 0
        self.neutral_fleet_offset = 1
        self.fleet_offset = 0


    def _inspect_allied_fleet(self):
        """ Show allied fleets in the inspector panel """
        self.allied_fleets -= 1
        self.fleet_index = self._next_fleet(self.fleet_index, self.fleet_offset, [Stance.ALLIED])
        self.allied_fleets += 1
        self.enemy_fleet_offset = 0
        self.neutral_fleet_offset = 0
        self.fleet_offset = 1


    def _inspect_planets(self):
        """ Switch to the planet view in the inspector panel """
        self._inspect_planet(self.selected_planet)


    def _inspect_fleets(self):
        """ Switch to the fleet view in the inspector panel """
        self.show_fleets.setVisible(False)
        self._inspect_fleet(self.selected_planet, self.fleet_index,
                            self.selected_fleets, self.selected_fields)


    def _inspect_mines(self):
        """ Switch to the mine field view in the inspector panel """
        self.enemy_fleet_offset = 0
        self.neutral_fleet_offset = 0
        self.fleet_offset = 0
        self.select_next_enemy.setVisible(False)
        self.select_next_neutral.setVisible(False)
        self.select_next_fleet.setVisible(False)
        self.show_neutral_base.setVisible(False)
        self.show_alien_base.setVisible(False)
        self.show_star_base.setVisible(False)
        if self.selected_planet:
            self.show_planet.setVisible(True)
            self.show_fleets.setVisible(False)
        elif self.selected_fleets:
            self.show_planet.setVisible(False)
            self.show_fleets.setVisible(True)
        else:
            self.show_planet.setVisible(False)
            self.show_fleets.setVisible(False)
        if self.selected_fleet:
            self.selected_fleet.colour_course(False)
            self.selected_fleet.show_course(self.show_fleet_movements)
        self.show_fields.setVisible(False)
        self._apply_mine_filter()
        self.next_field.setVisible(self.filtered_fields > 1)
        self.previous_field.setVisible(self.filtered_fields > 1)
        self.item_info.setCurrentIndex(2)
        self._next_minefield(self.mine_index, 0)


    def _apply_mine_filter(self):
        """ Apply new filter settings to the mine fields on the star map """
        self.filtered_fields = 0
        self.number_of_fields = 0
        if self.selected_fields:
            self.number_of_fields = len(self.selected_fields)
            for m in self.selected_fields:
                if self.mine_filter[m.fof]:
                    self.filtered_fields += 1


    def _show_next_mine_field(self):
        """ Cycle through mine fields in the standard direction """
        self.mine_index = self._next_minefield(self.mine_index, 1)


    def _show_previous_mine_field(self):
        """ Cycle through mine fields in the reversed direction """
        self.mine_index = self._next_minefield(self.mine_index, -1)


    def _show_crust_diagrams(self, event):
        """ Toggle a diagram of the planet's mineral wealth """
        if event:
            self.map.universe.show_crust_diagrams()
        else:
            self.map.universe.remove_diagrams()


    def _show_surface_diagrams(self, event):
        """ Toggle a diagram of the minerals available for transport of planet """
        if event:
            self.map.universe.show_surface_diagrams()
        else:
            self.map.universe.remove_diagrams()


    def _show_population_view(self, event):
        """ Enable the population view of the star map """
        if event:
            self.map.universe.show_population_view()


    def _show_default_view(self, event):
        """ Enable the default view of the star map """
        if event:
            self.map.universe.show_default_view()


    def _show_minimal_view(self, event):
        """ Enable the minimalistic view of the star map """
        if event:
            self.map.universe.show_minimal_view()


    def _show_percentage_view(self, event):
        """ Enable the planet value view of the star map """
        if event:
            self.map.universe.show_percentage_view()


    def _show_movements(self, event):
        """ Display or hide the flight paths of fleets on the star map """
        self.show_fleet_movements = event
        self.map.universe.show_movements(event)


    def _add_waypoints(self, event):
        """ Toggle a mode in which new waypoints can be added to existing
            flight paths by using the mouse pointer """
        self.waypoint_mode = event
        self.map.universe.set_waypoint_mode(event)


    def _configure_game(self):
        """ Switch to the advanced game configuration wizard """
        self.new_game.hide()
        self.game_setup.configure_game(self.new_game.map_size)


    def _configure_faction(self):
        """ Show the faction configuration wizard hiding all other dialogs
            and taking note from whence the wizard has been opened """
        advanced = self.game_setup.isVisible()
        simple = self.new_game.isVisible()
        self.game_setup.hide()
        self.new_game.hide()
        self.new_faction.configure_wizard(simple, advanced)


    def _abort_faction(self):
        """ Close the faction configuration dialog and return to any other
            dialog from whence the wizard has been called """
        self.new_faction.hide()
        self.game_setup.setVisible(self.new_faction.restart_game_wizard)
        self.new_game.setVisible(self.new_faction.restart_new_game)

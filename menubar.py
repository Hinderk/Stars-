
""" The menu bar of the user interface is defined in this module. """

from PyQt6.QtWidgets import QMenu
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QActionGroup
from PyQt6.QtCore import pyqtSignal as QSignal



class Menu(QMenuBar):

    """ This class implements the menu bar of the graphical user interface """

    change_zoom = QSignal(bool, int)


    def __init__(self, form):

        super().__init__(form)

        self.action_generate = QAction(self)
        self.action_generate.setText("Generate")
        self.action_generate.setToolTip("Generate a new turn ...")
        self.action_generate.setStatusTip("Advance the game time by one year ...")
        self.action_generate.setShortcut("F9")
        self.action_generate.setAutoRepeat(False)

        menu_turn = QMenu(self)
        menu_help = QMenu(self)
        menu_turn.addAction(self.action_generate)
        menu_turn.setTitle("Turn")
        menu_help.setTitle("Help")

        self._create_file_menu()
        self._create_view_menu()
        self.addAction(menu_turn.menuAction())
        self._create_commands_menu()
        self._create_report_menu()
        self.addAction(menu_help.menuAction())


    def _new_action(self, name, tip, hotkey=None):
        """ Create a non-repeating menu entry & action """
        action = QAction(self)
        action.setText(name)
        action.setStatusTip(tip)
        if hotkey:
            action.setShortcut(hotkey)
        action.setAutoRepeat(False)
        return action


    def _create_file_menu(self):
        """ Create a submenu for saving, loading or creating games """
        menu_file = QMenu(self)
        self.action_new_game = self._new_action('New', 'Start a new game ...', 'Ctrl+N')
        self.action_wizard = self._new_action(
            'Custom Faction Wizard ...', 'Launch the custom faction wizard ...')
        self.action_open_game = self._new_action(
            'Open', 'Open a set of game files ...', 'Ctrl+O')
        self.action_close_game = self._new_action('Close', 'Close the current game ...')
        self.action_save_game = self._new_action(
            'Save', 'Save the current turn to a set of game files ...', 'Ctrl+S')
        self.action_export_map = self._new_action(
            'Export Map', 'Print the current star map to a file ...')
        self.action_save_game_as = self._new_action(
            'Save Game as ...', 'Save the current game under a new name ...')
        self.action_exit = self._new_action(
            'Exit', 'Leave the current turn behind & close the game ...', 'Ctrl+X')
        self.action_exit.setToolTip("Exit the current game ...")
        self.action_save_submit = self._new_action(
            'Save and Submit', 'Save Game & submit Your turn ...', 'Ctrl+A')
        menu_file.addAction(self.action_new_game)
        menu_file.addAction(self.action_wizard)
        menu_file.addAction(self.action_open_game)
        menu_file.addAction(self.action_close_game)
        menu_file.addAction(self.action_save_game_as)
        menu_file.addAction(self.action_save_game)
        menu_file.addAction(self.action_save_submit)
        menu_file.addSeparator()
        menu_file.addAction(self.action_export_map)
        menu_file.addSeparator()
        menu_file.addAction(self.action_exit)
        menu_file.setTitle("File")
        self.addAction(menu_file.menuAction())


    def _create_view_menu(self):
        """ Create a submenu for displaying game & faction parameters """
        menu_view = QMenu(self)
        menu_toolbar = QMenu(menu_view)
        menu_layout = QMenu(menu_view)
        self.menu_zoom = QMenu(menu_view)
        self.action_game_parameters = QAction(self)
        self.action_game_parameters.setText("Game Parameters ...")
        self.action_game_parameters.setAutoRepeat(False)
        self.action_toolbar_on = QAction(self)
        self.action_toolbar_on.setText("On")
        self.action_toolbar_on.setToolTip("Show the toolbar ...")
        self.action_toolbar_on.setStatusTip("Show the toolbar ...")
        self.action_toolbar_on.setCheckable(True)
        self.action_toolbar_on.setChecked(True)
        self.action_toolbar_off = QAction(self)
        self.action_toolbar_off.setText("Off")
        self.action_toolbar_off.setToolTip("Hide the toolbar ...")
        self.action_toolbar_off.setStatusTip("Hide the toolbar ...")
        self.action_toolbar_off.setCheckable(True)
        menu_toolbar.setTitle("Toolbar")
        menu_toolbar.setStatusTip("Modify the tool bar of the game ...")
        menu_toolbar.setStyleSheet("QMenu::item{padding: 5px 20px 5px 0px}")
        menu_toolbar.addAction(self.action_toolbar_on)
        menu_toolbar.addAction(self.action_toolbar_off)
        toolbar_actions = QActionGroup(self)
        toolbar_actions.addAction(self.action_toolbar_on)
        toolbar_actions.addAction(self.action_toolbar_off)
        self.action_default = QAction(self)
        self.action_default.setText("Default")
        self.action_default.setCheckable(True)
        self.action_default.setChecked(True)
        self.action_faction = QAction(self)
        self.action_faction.setText("Faction ...")
        self.action_faction.setShortcut("F8")
        self.action_faction.setAutoRepeat(False)
        self.define_zoom_level(self.menu_zoom, [25, 50, 75, 100, 125, 150, 200, 400])
        self.menu_zoom.setStyleSheet("QMenu::item { padding: 5px 30px 5px 0px }")
        self.menu_zoom.setTitle("Zoom")
        menu_layout.addAction(self.action_default)
        menu_layout.setTitle("Layout")
        menu_layout.setStyleSheet("QMenu::item { padding: 5px 30px 5px 0px }")
        menu_view.addAction(menu_toolbar.menuAction())
        menu_view.addAction(self.menu_zoom.menuAction())
        menu_view.addAction(menu_layout.menuAction())
        menu_view.addSeparator()
        menu_view.addAction(self.action_faction)
        menu_view.addAction(self.action_game_parameters)
        menu_view.setTitle("View")
        self.addAction(menu_view.menuAction())


    def _create_commands_menu(self):
        """ Create a submenu for research, diplomacy, ship design & battle tactics """
        menu_commands = QMenu(self)
        self.action_ship_design = QAction(self)
        self.action_ship_design.setText("Ship Design ...")
        self.action_ship_design.setShortcut("F4")
        self.action_battle_plans = QAction(self)
        self.action_battle_plans.setText("Battle Plans ...")
        self.action_battle_plans.setShortcut("F6")
        self.action_player_relations = QAction(self)
        self.action_player_relations.setText("Player Relations ...")
        self.action_player_relations.setShortcut("F7")
        self.action_player_relations.setIconVisibleInMenu(False)
        self.action_research = QAction(self)
        self.action_research.setText("Research ...")
        self.action_research.setShortcut("F5")
        self.action_change_password = QAction(self)
        self.action_change_password.setText("Change Password ...")
        menu_commands.addAction(self.action_ship_design)
        menu_commands.addAction(self.action_research)
        menu_commands.addAction(self.action_battle_plans)
        menu_commands.addAction(self.action_player_relations)
        menu_commands.addSeparator()
        menu_commands.addAction(self.action_change_password)
        menu_commands.setTitle("Commands")
        self.addAction(menu_commands.menuAction())


    def _create_report_menu(self):
        """ Create a submenu to track of items & events in the game world """
        menu_report = QMenu(self)
        menu_dump_text_file = QMenu(menu_report)
        self.action_planets = QAction(self)
        self.action_planets.setShortcut("F3")
        self.action_planets.setAutoRepeat(False)
        self.action_planets.setIconVisibleInMenu(False)
        self.action_planets.setText("Planets ...")
        self.action_fleets = QAction(self)
        self.action_fleets.setAutoRepeat(False)
        self.action_fleets.setIconVisibleInMenu(False)
        self.action_fleets.setText("Fleets ...")
        self.action_fleets.setShortcut("F3")
        self.action_other_fleets = QAction(self)
        self.action_other_fleets.setShortcut("F3")
        self.action_other_fleets.setAutoRepeat(False)
        self.action_other_fleets.setIconVisibleInMenu(False)
        self.action_other_fleets.setText("Others\' Fleets ...")
        self.action_battles = QAction(self)
        self.action_battles.setShortcut("F3")
        self.action_battles.setAutoRepeat(False)
        self.action_battles.setIconVisibleInMenu(False)
        self.action_battles.setText("Battles ...")
        self.action_score = QAction(self)
        self.action_score.setShortcut("F10")
        self.action_score.setAutoRepeat(False)
        self.action_score.setIconVisibleInMenu(False)
        self.action_score.setText("Score ...")
        menu_dump_text_file.setTitle("Dump to Text File")
        self.action_planet_information = QAction(self)
        self.action_planet_information.setText("Planet Information")
        menu_dump_text_file.addAction(self.action_planet_information)
        self.action_fleet_information = QAction(self)
        self.action_fleet_information.setText("Fleet Information")
        menu_dump_text_file.addAction(self.action_fleet_information)
        self.action_universe_definition = QAction(self)
        self.action_universe_definition.setText("Universe Definition")
        menu_dump_text_file.addAction(self.action_universe_definition)
        menu_report.addAction(self.action_planets)
        menu_report.addAction(self.action_fleets)
        menu_report.addAction(self.action_other_fleets)
        menu_report.addAction(self.action_battles)
        menu_report.addSeparator()
        menu_report.addAction(self.action_score)
        menu_report.addSeparator()
        menu_report.addAction(menu_dump_text_file.menuAction())
        menu_report.setTitle("Report")
        self.addAction(menu_report.menuAction())


    def define_zoom_level(self, menu, level_set):
        """ Create the submenu containing the available zoom levels """
        zoom_actions = QActionGroup(menu)
        for level in level_set:
            new_action = QAction()
            new_action.setData(level)
            menu.addAction(new_action)
            new_action.setCheckable( True )
            label = str(level) + '%'
            new_action.setText(label)
            new_action.setToolTip('Set magnification level: ' + label)
            new_action.setStatusTip('Set magnification level: ' + label)
            zoom_actions.addAction(new_action)
            new_action.setChecked(level == 100)
            new_action.toggled.connect(self.resize_starmap)


    def resize_starmap(self, event):
        """ Change the zoom level of the star map """
        self.change_zoom.emit(event, self.sender().data())


""" The menu bar of the user interface is defined in this module. """

from PyQt6.QtWidgets import QMenu
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QActionGroup
from PyQt6.QtCore import pyqtSignal as QSignal



def _new_menu(top, name, tip):
    menu = QMenu(top)
    action = menu.menuAction()
    action.setStatusTip(tip)
    menu.setTitle(name)
    return menu



class Menu(QMenuBar):

    """ This class implements the menu bar of the graphical user interface """

    change_zoom = QSignal(bool, int)


    def __init__(self, form):

        super().__init__(form)

        self.action_generate = self._new_action(
            'Generate', 'Advance the game time by one year ...', 'F9')

        menu_turn = _new_menu(self, 'Turn', 'Generate a new turn ...')
        menu_turn.addAction(self.action_generate)
        menu_help = _new_menu(self, 'Help', 'Instructions & information ...')

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
        action.setIconVisibleInMenu(False)
        return action


    def _create_file_menu(self):
        """ Create a submenu for saving, loading or creating games """
        menu_file = _new_menu(
            self, 'File', 'Create new games, save games in progress, '
            'open saved games & submit Your turns ...')
        self.action_new_game = self._new_action('New', 'Start a new game ...', 'Ctrl+N')
        self.action_wizard = self._new_action(
            'Custom Faction Wizard ...', 'Launch the custom faction wizard ...')
        self.action_open_game = self._new_action(
            'Open', 'Open a set of game files ...', 'Ctrl+O')
        self.action_close_game = self._new_action('Close', 'Close the current game ...')
        self.action_save_game = self._new_action(
            'Save', 'Save the current turn to a set of game files ...', 'Ctrl+S')
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
        menu_file.addAction(self.action_exit)
        self.addAction(menu_file.menuAction())


    def _create_view_menu(self):
        """ Create a submenu for displaying game & faction parameters """
        menu_view = _new_menu(
            self, 'View', 'Review game & faction parameters, print the star map ...')
        self.action_export_map = self._new_action(
            'Export Map', 'Print the current star map to a file ...')
        self.action_game_parameters = self._new_action(
            'Game Parameters ...', 'Show victory conditions & other game settings ...')
        self.action_faction = self._new_action(
            'Faction ...', 'Show the traits & perks of Your faction ...', 'F8')
        self.menu_zoom = QMenu(menu_view)
        self.define_zoom_level(self.menu_zoom, [25, 50, 75, 100, 125, 150, 200, 400])
        self.menu_zoom.setStyleSheet('QMenu::item { padding: 5px 30px 5px 0px }')
        self.menu_zoom.setTitle('Zoom')
        zoom = self.menu_zoom.menuAction()
        zoom.setStatusTip('Specify a magnification level for the star map ...')
        menu_view.addAction(self.action_export_map)
        menu_view.addAction(self.action_faction)
        menu_view.addAction(self.action_game_parameters)
        menu_view.addSeparator()
        menu_view.addAction(zoom)
        self.addAction(menu_view.menuAction())


    def _create_commands_menu(self):
        """ Create a submenu for research, diplomacy, ship design & battle tactics """
        menu_commands = _new_menu(
            self, 'Commands',
            'Allocate resources, engage in diplomacy & elaborate battle tactics ...')
        self.action_ship_design = self._new_action(
            'Ship Design ...', 'Create new blueprints for Your space ships ...', 'F4')
        self.action_research = self._new_action(
            'Research ...', 'Allocate resources to Your R&D programs ...','F5')
        self.action_battle_plans = self._new_action(
            'Battle Plans ...', 'Define the rules of engagement for Your fleets ...', 'F6')
        self.action_player_relations = self._new_action(
            'Player Relations ...', 'Declare war or sue for peace ...', 'F7')
        self.action_change_password = self._new_action(
            'Change Password ...', 'Protect Your game files with a password ...')
        menu_commands.addAction(self.action_ship_design)
        menu_commands.addAction(self.action_research)
        menu_commands.addAction(self.action_battle_plans)
        menu_commands.addAction(self.action_player_relations)
        menu_commands.addSeparator()
        menu_commands.addAction(self.action_change_password)
        self.addAction(menu_commands.menuAction())


    def _create_report_menu(self):
        """ Create a submenu to track of items & events in the game world """
        self.action_planets = self._new_action(
            'Planets ...', 'Collect all currently available planetary data ...', 'F3')
        self.action_fleets = self._new_action(
            'Fleets ...', 'Show information about Your latest fleet movements ...', 'F3')
        self.action_other_fleets = self._new_action(
            'Others\' Fleets ...',
            'Show information about the latest hostile fleet movements ...', 'F3')
        self.action_battles = self._new_action(
            'Battles ...', 'Collect statistics on the latest fleet battles ...', 'F3')
        self.action_score = self._new_action(
            'Score ...',
            'Evaluate the players\' progress towards meeting the victory conditions ...',
            'F10')
        self.action_planet_information = self._new_action(
            'Planet Information',
            'Export a list of all planetary data gathered by the player ...')
        self.action_fleet_information = self._new_action(
            'Fleet Information',
            'Export a list of all fleets within the player\'s scanner range ...')
        self.action_universe_definition = self._new_action(
            'Universe Definition', 'Export a list of all star systems in the galaxy ...')
        menu_report = _new_menu(self, 'Report', 'Inquire into the state of the galaxy ...')
        menu_dump_text_file = _new_menu(
            menu_report, 'Dump to Text File', 'Export game data in the CSV format ...')
        menu_dump_text_file.addAction(self.action_planet_information)
        menu_dump_text_file.addAction(self.action_fleet_information)
        menu_dump_text_file.addAction(self.action_universe_definition)
        menu_report.addAction(self.action_planets)
        menu_report.addAction(self.action_fleets)
        menu_report.addAction(self.action_other_fleets)
        menu_report.addAction(self.action_battles)
        menu_report.addSeparator()
        menu_report.addAction(self.action_score)
        menu_report.addSeparator()
        menu_report.addAction(menu_dump_text_file.menuAction())
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

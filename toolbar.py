
""" This module implements the tool bar used to control the presentation of the star map """

from PyQt6.QtWidgets import QMenu, QToolButton
from PyQt6.QtWidgets import QToolBar, QSpinBox
from PyQt6.QtGui import QActionGroup
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
from PyQt6.QtCore import pyqtSignal as QSignal

from defines import Stance, ShipClass


_instant = QToolButton.ToolButtonPopupMode.InstantPopup
_delayed = QToolButton.ToolButtonPopupMode.DelayedPopup



class ToolBar(QToolBar):

    """ This class implements the tool bar for the star map """

    show_mines = QSignal(bool, Stance)
    filter_my_fleets = QSignal(bool, dict)
    filter_enemy_fleets = QSignal(bool, dict)


    def __init__(self):

        super().__init__()

        self.design_names = []
        self.my_designs = {}
        self.alien_designs = {}
        self.mine_filter = {}
        self.mine_action = {}
        self.my_filter = {}
        self.foe_filter = {}

        self.action_default_view = self._new_action(
            ':/Toolbar/Default',
            'Indicate the strength of fleets in planetary orbits ...')
        self.action_percent_view = self._new_action(
            ':/Toolbar/Percent', 'Indicate planet values by colours & size ...')
        self.action_population_view = self._new_action(
            ':/Toolbar/People', 'Display the size of planetary settlements ...')
        self.action_surface_mineral_view = self._new_action(
            ':/Toolbar/Surface',
            'Indicate mineral stores on the planets\' surface ...')
        self.action_concentration_view = self._new_action(
            ':/Toolbar/Minerals',
            'Indicate mineral concentrations within the planets\' crust ...')
        self.action_no_info_view = self._new_action(
            ':/Toolbar/Cancel', 'Hide all player related information ...')
        self.action_add_waypoint = self._new_action(
            ':/Toolbar/Waypoint', 'Add way points to the flight path ...')
        self.action_waiting_fleets = self._new_action(
            ':/Toolbar/Waiting', 'Show fleets without any task to complete ...')
        self.action_ship_count = self._new_action(
            ':/Toolbar/Orbiting',
            'Show the strength of all fleets within scanner range ...')
        self.action_path_overlay = self._new_action(
            ':/Toolbar/Paths',
            'Show the flight paths of all fleets within scanner range ...')
        self.action_planet_names = self._new_action(
            ':/Toolbar/Names', 'Show planet names ...')
        self.action_radar_view = self._new_action(
            ':/Toolbar/Scanner', 'Show scanner coverage on the star map ...')

        self.mines = self._new_button(
            ':/Toolbar/Mine', 'Show mine fields ...')
        self._define_mine_menu(self.mines)
        self.action_friendlies = self._new_button(
            ':/Toolbar/Friendlies',
            'Apply a filter to hide certain friendly fleets on the star map ...',
            True)
        self._define_my_design_menu(self.action_friendlies)
        self.action_foes = self._new_button(
            ':/Toolbar/Foes',
            'Apply a filter to hide certain hostile fleets on the star map ...',
            True)
        self._define_enemy_design_menu(self.action_foes)
        self.zoom = self._new_button(
            ':/Toolbar/Zoomlevel',
            'Specify the level of magnification for the star map ...', True)

        self.radar_range = QSpinBox()
        self.radar_range.setSuffix('%')
        self.radar_range.setRange(10, 100)
        self.radar_range.setValue(100)
        self.radar_range.setSingleStep(10)
        self.radar_range.setMinimumSize(QSize(100, 40))
        self.radar_range.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.view_mode = QActionGroup(self)
        self._assemble_toolbar()


    def _assemble_toolbar(self):
        """ Compose the tool bar from its individual elements """
        self.view_mode.addAction(self.action_default_view)
        self.view_mode.addAction(self.action_surface_mineral_view)
        self.view_mode.addAction(self.action_concentration_view)
        self.view_mode.addAction(self.action_percent_view)
        self.view_mode.addAction(self.action_population_view)
        self.view_mode.addAction(self.action_no_info_view)
        self.addAction(self.action_default_view)
        self.addAction(self.action_surface_mineral_view)
        self.addAction(self.action_concentration_view)
        self.addAction(self.action_percent_view)
        self.addAction(self.action_population_view)
        self.addAction(self.action_no_info_view)
        self.addAction(self.action_add_waypoint)
        self.addAction(self.action_radar_view)
        self.addWidget(self.radar_range)
        self.addWidget(self.mines)
        self.addAction(self.action_path_overlay)
        self.addAction(self.action_planet_names)
        self.addAction(self.action_ship_count)
        self.addAction(self.action_waiting_fleets)
        self.addWidget(self.action_friendlies)
        self.addWidget(self.action_foes)
        self.addWidget(self.zoom)


    def _new_action(self, iconfile, tip):
        """ Create a new action """
        action = QAction(self)
        action.setCheckable(True)
        action.setIcon(QIcon(iconfile))
        action.setAutoRepeat(False)
        action.setStatusTip(tip)
        return action


    def _new_button(self, iconfile, tip, instant=False):
        """ Create a new button """
        button = QToolButton(self)
        if instant:
            button.setPopupMode(_instant)
            button.setCheckable(False)
        else:
            button.setCheckable(True)
        button.setIcon(QIcon(iconfile))
        button.setAutoRepeat(False)
        button.setStatusTip(tip)
        return button


    def _add_new_design(self, menu, name):
        """ Create a new menu entry for the design filter """
        action = QAction()
        action.setText(name)
        action.setData(name)
        action.setCheckable(True)
        action.setChecked(True)
        action.toggled.connect(self.show_my_fleets)
        menu.addAction(action)
        self.my_filter[name] = action


    def update_my_designs(self, design_data):
        """ Update the filter settings for ship designs created by the player """
        menu = self.action_friendlies.menu()
        for design in self.design_names:
            menu.removeAction(self.my_filter[design])
        self.my_filter = {}
        design_data.sort()
        new_designs = {}
        for name in design_data:
            if name in self.design_names:
                new_designs[name] = self.my_designs[name]
            else:
                new_designs[name] = True
            self._add_new_design(menu, name)
        self.my_designs = new_designs
        self.design_names = design_data


    def _define_my_design_menu(self, design_menu):
        """ Create the menu with the filter settings for the player's ship designs """
        menu = QMenu(self)
        menu.setStyleSheet("QMenu::item{padding: 5px 40px 5px 0px}")
        self.all_my_designs = menu.addAction('   All Designs')
        self.all_my_designs.setCheckable(False)
        self.all_my_designs.triggered.connect(self.show_all_my_designs)
        self.invert_my_designs = menu.addAction('   Invert Filter')
        self.invert_my_designs.setCheckable(False)
        self.invert_my_designs.triggered.connect(self.invert_my_display)
        self.hide_my_designs = menu.addAction('   No Designs')
        self.hide_my_designs.setCheckable(False)
        self.hide_my_designs.triggered.connect(self.hide_all_my_designs)
        menu.addSeparator()
        design_menu.setMenu(menu)


    def _add_enemy_design(self, menu, design):
        """ Create a new entry in the enemy design filter menu """
        action = QAction()
        action.setData(design.name)
        action.setText(design.value)
        action.setCheckable(True)
        action.setChecked(True)
        action.toggled.connect(self.show_enemy_fleets)
        menu.addAction(action)
        self.foe_filter[design] = action
        self.alien_designs[design.name] = True


    def _define_enemy_design_menu(self, design_menu):
        """ Create the menu with the filter settings for enemy ship designs """
        menu = QMenu(self)
        menu.setStyleSheet("QMenu::item{padding: 5px 40px 5px 0px}")
        self.all_enemy_designs = menu.addAction('   All Designs')
        self.all_enemy_designs.setCheckable(False)
        self.all_enemy_designs.triggered.connect(self.show_all_enemy_designs)
        self.invert_enemy_designs = menu.addAction('   Invert Filter')
        self.invert_enemy_designs.setCheckable(False)
        self.invert_enemy_designs.triggered.connect(self.invert_enemy_display)
        self.hide_enemy_designs = menu.addAction('   No Designs')
        self.hide_enemy_designs.setCheckable(False)
        self.hide_enemy_designs.triggered.connect(self.hide_all_enemy_designs)
        menu.addSeparator()
        self.foe_filter = {}
        for design in ShipClass:
            self._add_enemy_design(menu, design)
        design_menu.setMenu(menu)


    def _add_mine_action(self, menu, data, label, tick=True):
        """ Create a new entry in the mine filter menu """
        action = QAction()
        action.setData(data)
        action.setText(label)
        action.setCheckable(tick)
        action.setChecked(True)
        self.mine_action[data] = action
        if tick:
            action.toggled.connect(self.show_minefields)
            self.mine_filter[data] = True
        else:
            action.triggered.connect(self.change_mine_display)
        menu.addAction(action)


    def _define_mine_menu(self, mines):
        """ Create the menu with the filter settings for mine fields """
        menu = QMenu(self)
        menu.setStyleSheet("QMenu::item{padding: 5px 40px 5px 0px}")
        self._add_mine_action(menu, Stance.ACCEPT, '   All Mine Fields', False)
        self._add_mine_action(menu, Stance.IGNORE, '   No Mine Fields', False)
        menu.addSeparator()
        self._add_mine_action(menu, Stance.ALLIED, 'Mine Fields of Yours')
        self._add_mine_action(menu, Stance.FRIENDLY, 'Mine Fields of Friends')
        self._add_mine_action(menu, Stance.NEUTRAL, 'Mine Fields of Neutrals')
        self._add_mine_action(menu, Stance.HOSTILE, 'Mine Fields of Enemies')
        mines.setMenu(menu)


    def change_mine_display(self, _):
        """ Show or hide mine fields on the star map """
        show = self.sender().data() == Stance.ACCEPT
        if not show:
            self.mines.setChecked(False)
        for action in self.mine_action.values():
            action.setChecked(show)


    def show_minefields(self, event):
        """ Apply new filter settings for mine fields to the star maps """
        fof = self.sender().data()
        self.mine_filter[fof] = event
        show = False
        for b in self.mine_filter.values():
            show = show or b
        if show:
            self.mines.setCheckable(True)
            self.mines.setChecked(True)
            self.mines.setPopupMode(_delayed)
        else:
            self.mines.setChecked(False)
            self.mines.setCheckable(False)
            self.mines.setPopupMode(_instant)
        self.show_mines.emit(event, fof)


    def show_enemy_fleets(self, event):
        """ Apply any changes to the filter settings for hostile fleets """
        sc = self.sender().data()
        self.alien_designs[sc] = event
        disabled = True
        for b in self.alien_designs.values():
            disabled = disabled and b
        if disabled:
            self.action_foes.setChecked(False)
            self.action_foes.setCheckable(False)
            self.action_foes.setPopupMode(_instant)
        else:
            self.action_foes.setCheckable(True)
            self.action_foes.setChecked(True)
            self.action_foes.setPopupMode(_delayed)
        self.filter_enemy_fleets.emit(not disabled, self.alien_designs)


    def show_my_fleets(self, event):
        """ Apply any changes to the player's filter settings """
        sc = self.sender().data()
        self.my_designs[sc] = event
        disabled = True
        for b in self.my_designs.values():
            disabled = disabled and b
        if disabled:
            self.action_friendlies.setChecked(False)
            self.action_friendlies.setCheckable(False)
            self.action_friendlies.setPopupMode(_instant)
        else:
            self.action_friendlies.setCheckable(True)
            self.action_friendlies.setChecked(True)
            self.action_friendlies.setPopupMode(_delayed)
        self.filter_my_fleets.emit(not disabled, self.my_designs)


    def show_all_my_designs(self):
        """ Enable all player designs in the fleet filter """
        for design in self.design_names:
            self.my_filter[design].setChecked(True)


    def invert_my_display(self):
        """ Invert the filter settings for all player designs """
        for design in self.design_names:
            show = self.my_filter[design].isChecked()
            self.my_filter[design].setChecked(not show)


    def hide_all_my_designs(self):
        """ Disable all player designs in the fleet filter """
        for design in self.design_names:
            self.my_filter[design].setChecked(False)


    def show_all_enemy_designs(self):
        """ Enable all enemy designs in the fleet filter """
        for design in ShipClass:
            self.foe_filter[design].setChecked(True)


    def invert_enemy_display(self):
        """ Invert the filter settings for all enemy designs """
        for design in ShipClass:
            show = self.foe_filter[design].isChecked()
            self.foe_filter[design].setChecked(not show)


    def hide_all_enemy_designs(self):
        """ Disable all enemy designs in the fleet filter """
        for design in ShipClass:
            self.foe_filter[design].setChecked(False)

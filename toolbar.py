
from PyQt6.QtWidgets import QMenu, QToolButton
from PyQt6.QtWidgets import QToolBar, QSpinBox
from PyQt6.QtGui import QActionGroup
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
from PyQt6.QtCore import pyqtSignal as QSignal

from defines import Stance, ShipClass


instant = QToolButton.ToolButtonPopupMode.InstantPopup
delayed = QToolButton.ToolButtonPopupMode.DelayedPopup



class ToolBar(QToolBar):

    show_mines = QSignal(bool, Stance)
    filter_my_fleets = QSignal(bool, dict)
    filter_enemy_fleets = QSignal(bool, dict)


    def __init__(self):

        super(self.__class__, self).__init__()

        self.design_names = []
        self.my_designs = {}
        self.alien_designs = {}
        for sc in ShipClass:
            self.alien_designs[sc.name] = True
        self.mine_filter = dict()
        self.mine_filter[Stance.ALLIED] = True
        self.mine_filter[Stance.FRIENDLY] = True
        self.mine_filter[Stance.NEUTRAL] = True
        self.mine_filter[Stance.HOSTILE] = True

        icon = QIcon(":/Toolbar/Mine")
        self.mines = QToolButton(self)
        self.mines.setIcon(icon)
        self.mines.setCheckable(True)
        self.mines.setAutoRepeat(False)
        self.mines.setToolTip('Show mine fields ...')
        self.mines.setStatusTip('Show mine fields ...')
        self.define_mine_menu(self.mines)

        icon = QIcon(":/Toolbar/Default")
        self.action_default_view = QAction(self)
        self.action_default_view.setCheckable(True)
        self.action_default_view.setIcon(icon)
        self.action_default_view.setAutoRepeat(False)
        self.action_default_view.setToolTip("Normal View")
        self.action_default_view.setStatusTip("Normal View")

        icon = QIcon(":/Toolbar/Percent")
        self.action_percent_view = QAction(self)
        self.action_percent_view.setCheckable(True)
        self.action_percent_view.setIcon(icon)
        self.action_percent_view.setAutoRepeat(False)
        self.action_percent_view.setToolTip("Planet Value View")
        self.action_percent_view.setStatusTip("Planet Value View")

        icon = QIcon(":/Toolbar/People")
        self.action_population_view = QAction(self)
        self.action_population_view.setCheckable(True)
        self.action_population_view.setIcon(icon)
        self.action_population_view.setAutoRepeat(False)
        self.action_population_view.setToolTip("Population View")
        self.action_population_view.setStatusTip("Population View")

        icon = QIcon(":/Toolbar/Surface")
        self.action_surface_mineral_view = QAction(self)
        self.action_surface_mineral_view.setCheckable(True)
        self.action_surface_mineral_view.setIcon(icon)
        self.action_surface_mineral_view.setAutoRepeat(False)
        self.action_surface_mineral_view.setToolTip("Surface Mineral View")
        self.action_surface_mineral_view.setStatusTip("Surface Mineral View")

        icon = QIcon(":/Toolbar/Minerals")
        self.action_concentration_view = QAction(self)
        self.action_concentration_view.setCheckable(True)
        self.action_concentration_view.setIcon(icon)
        self.action_concentration_view.setAutoRepeat(False)
        self.action_concentration_view.setToolTip("Mineral Concentration View")
        self.action_concentration_view.setStatusTip("Mineral Concentration View")

        icon = QIcon(":/Toolbar/Cancel")
        self.action_no_info_view = QAction(self)
        self.action_no_info_view.setCheckable(True)
        self.action_no_info_view.setIcon(icon)
        self.action_no_info_view.setAutoRepeat(False)
        self.action_no_info_view.setToolTip("No Player Info View")
        self.action_no_info_view.setStatusTip("Remove information about players ...")

        icon = QIcon(":/Toolbar/Waypoint")
        self.action_add_waypoint = QAction(self)
        self.action_add_waypoint.setCheckable(True)
        self.action_add_waypoint.setIcon(icon)
        self.action_add_waypoint.setAutoRepeat(False)
        self.action_add_waypoint.setStatusTip("Add way points to the flight path ...")
        self.action_add_waypoint.setToolTip("Add way points ...")

        icon = QIcon(":/Toolbar/Waiting")
        self.action_waiting_fleets = QAction(self)
        self.action_waiting_fleets.setCheckable(True)
        self.action_waiting_fleets.setIcon(icon)
        self.action_waiting_fleets.setAutoRepeat(False)
        self.action_waiting_fleets.setToolTip("Show idle fleets only ...")
        self.action_waiting_fleets.setStatusTip("Show fleets without any task to complete ...")

        icon = QIcon(":/Toolbar/Orbiting")
        self.action_ship_count = QAction(self)
        self.action_ship_count.setCheckable(True)
        self.action_ship_count.setIcon(icon)
        self.action_ship_count.setAutoRepeat(False)
        self.action_ship_count.setToolTip("Show fleet strengths ...")
        self.action_ship_count.setStatusTip("Show the strength of all fleets within scanner range ...")

        icon = QIcon(":/Toolbar/Friendlies")
        self.action_friendlies = QToolButton(self)
        self.action_friendlies.setCheckable(False)
        self.action_friendlies.setPopupMode(instant)
        self.action_friendlies.setIcon(icon)
        self.action_friendlies.setToolTip("Show friendly fleets ...")
        self.action_friendlies.setStatusTip("Show only friendly fleets on the star map ...")
        self.action_friendlies.setAutoRepeat(False)
        self.define_my_design_menu(self.action_friendlies)

        icon = QIcon(":/Toolbar/Foes")
        self.action_foes = QToolButton(self)
        self.action_foes.setCheckable(False)
        self.action_foes.setPopupMode(instant)
        self.action_foes.setIcon(icon)
        self.action_foes.setToolTip("Show enemy fleets ...")
        self.action_foes.setStatusTip("Show only enemy fleets on the star map ...")
        self.action_foes.setAutoRepeat(False)
        self.define_enemy_design_menu(self.action_foes)

        icon = QIcon(":/Toolbar/Zoomlevel")
        self.zoom = QToolButton(self)
        self.zoom.setPopupMode(instant)
        self.zoom.setIcon(icon)
        self.zoom.setAutoRepeat(False)
        self.zoom.setToolTip("Define the level of magnification ...")
        self.zoom.setStatusTip("Define the level of magnification ...")

        icon = QIcon(":/Toolbar/Paths")
        self.action_path_overlay = QAction(self)
        self.action_path_overlay.setCheckable(True)
        self.action_path_overlay.setIcon(icon)
        self.action_path_overlay.setAutoRepeat(False)
        self.action_path_overlay.setToolTip("Show fleet paths")
        self.action_path_overlay.setStatusTip("Show the flight paths of all fleets within scanner range ...")

        icon = QIcon(":/Toolbar/Names")
        self.action_planet_names = QAction(self)
        self.action_planet_names.setCheckable(True)
        self.action_planet_names.setIcon(icon)
        self.action_planet_names.setAutoRepeat(False)
        self.action_planet_names.setToolTip("Show planet names ...")
        self.action_planet_names.setStatusTip("Show planet names ...")

        self.radar_range = QSpinBox()
        self.radar_range.setSuffix('%')
        self.radar_range.setRange(10, 100)
        self.radar_range.setValue(100)
        self.radar_range.setSingleStep(10)
        self.radar_range.setMinimumSize(QSize(100, 40))
        self.radar_range.setAlignment(Qt.AlignmentFlag.AlignRight)

        icon = QIcon(":/Toolbar/Scanner")
        self.action_radar_view = QAction(self)
        self.action_radar_view.setCheckable(True)
        self.action_radar_view.setIcon(icon)
        self.action_radar_view.setAutoRepeat(False)
        self.action_radar_view.setToolTip("Scanner coverage overlay ...")
        self.action_radar_view.setStatusTip("Show scanner coverage on the star map ...")

        self.view_mode = QActionGroup(self)
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


    def update_my_designs(self, design_data):

        class MyAction(QAction):

            def __init__(self, name):
                super(self.__class__, self).__init__()
                self.ship_design = name

        @staticmethod
        def add_action(menu, action, label):
            action.setText(label)
            action.setCheckable(True)
            action.setChecked(True)
            action.toggled.connect(self.show_my_fleets)
            menu.addAction(action)

        menu = self.action_friendlies.menu()
        for design in self.design_names:
            menu.removeAction(self.my_filter[design])
        self.my_filter.clear()
        design_data.sort()
        new_designs = dict()
        for name in design_data:
            if name in self.design_names:
                new_designs[name] = self.my_designs[name]
            else:
                new_designs[name] = True
            new_action = MyAction(name)
            add_action(menu, new_action, name)
            self.my_filter[name] = new_action
        self.my_designs = new_designs
        self.design_names = design_data


    def define_my_design_menu(self, design_menu):
        self.design_names = []
        self.my_designs = dict()
        self.my_filter = dict()
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


    def define_enemy_design_menu(self, design_menu):

        class EnemyAction(QAction):

            def __init__(self, design):
                super(self.__class__, self).__init__()
                self.ship_design = design.name

        @staticmethod
        def add_action(menu, action, label):
            action.setText(label)
            action.setCheckable(True)
            action.setChecked(True)
            action.toggled.connect(self.show_enemy_fleets)
            menu.addAction(action)

        self.foe_filter = dict()
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
        for design in ShipClass:
            action = EnemyAction(design)
            add_action(menu, action, design.value)
            self.foe_filter[design] = action
        design_menu.setMenu(menu)


    def define_mine_menu(self, mines):

        class MineAction(QAction):

            def __init__(self, stance):
                super(self.__class__, self).__init__()
                self.mine_view = stance

        @staticmethod
        def add_action(menu, action, label, tick=True):
            action.setText(label)
            action.setCheckable(tick)
            action.setChecked(True)
            if tick:
                action.toggled.connect(self.show_minefields)
            else:
                action.triggered.connect(self.change_mine_display)
            menu.addAction(action)

        menu = QMenu(self)
        menu.setStyleSheet("QMenu::item{padding: 5px 40px 5px 0px}")
        self.all_mines = MineAction(Stance.ACCEPT)
        self.no_mines = MineAction(Stance.IGNORE)
        self.allied_mines = MineAction(Stance.ALLIED)
        self.friendly_mines = MineAction(Stance.FRIENDLY)
        self.neutral_mines = MineAction(Stance.NEUTRAL)
        self.hostile_mines = MineAction(Stance.HOSTILE)
        add_action(menu, self.all_mines, '   All Mine Fields', False)
        add_action(menu, self.no_mines, '   No Mine Fields', False)
        menu.addSeparator()
        add_action(menu, self.allied_mines, 'Mine Fields of Yours')
        add_action(menu, self.friendly_mines, 'Mine Fields of Friends')
        add_action(menu, self.neutral_mines, 'Mine Fields of Neutrals')
        add_action(menu, self.hostile_mines, 'Mine Fields of Enemies')
        mines.setMenu(menu)


    def change_mine_display(self, event):
        show = (self.sender().mine_view == Stance.ACCEPT)
        if not show:
            self.mines.setChecked(False)
        self.allied_mines.setChecked(show)
        self.friendly_mines.setChecked(show)
        self.neutral_mines.setChecked(show)
        self.hostile_mines.setChecked(show)


    def show_minefields(self, event):
        fof = self.sender().mine_view
        self.mine_filter[fof] = event
        show = False
        for b in self.mine_filter.values():
            show = show or b
        if show:
            self.mines.setCheckable(True)
            self.mines.setChecked(True)
            self.mines.setPopupMode(delayed)
        else:
            self.mines.setChecked(False)
            self.mines.setCheckable(False)
            self.mines.setPopupMode(instant)
        self.show_mines.emit(event, fof)


    def show_enemy_fleets(self, event):
        sc = self.sender().ship_design
        self.alien_designs[sc] = event
        disabled = True
        for b in self.alien_designs.values():
            disabled = disabled and b
        if disabled:
            self.action_foes.setChecked(False)
            self.action_foes.setCheckable(False)
            self.action_foes.setPopupMode(instant)
        else:
            self.action_foes.setCheckable(True)
            self.action_foes.setChecked(True)
            self.action_foes.setPopupMode(delayed)
        self.filter_enemy_fleets.emit(not disabled, self.alien_designs)


    def show_my_fleets(self, event):
        sc = self.sender().ship_design
        self.my_designs[sc] = event
        disabled = True
        for b in self.my_designs.values():
            disabled = disabled and b
        if disabled:
            self.action_friendlies.setChecked(False)
            self.action_friendlies.setCheckable(False)
            self.action_friendlies.setPopupMode(instant)
        else:
            self.action_friendlies.setCheckable(True)
            self.action_friendlies.setChecked(True)
            self.action_friendlies.setPopupMode(delayed)
        self.filter_my_fleets.emit(not disabled, self.my_designs)


    def show_all_my_designs(self):
        for design in self.design_names:
            self.my_filter[design].setChecked(True)


    def invert_my_display(self):
        for design in self.design_names:
            show = self.my_filter[design].isChecked()
            self.my_filter[design].setChecked(not show)


    def hide_all_my_designs(self):
        for design in self.design_names:
            self.my_filter[design].setChecked(False)


    def show_all_enemy_designs(self):
        for design in ShipClass:
            self.foe_filter[design].setChecked(True)


    def invert_enemy_display(self):
        for design in ShipClass:
            show = self.foe_filter[design].isChecked()
            self.foe_filter[design].setChecked(not show)


    def hide_all_enemy_designs(self):
        for design in ShipClass:
            self.foe_filter[design].setChecked(False)
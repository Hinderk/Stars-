
""" This module implements the custom faction wizard """

import copy
import json

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QMessageBox, QSpinBox
from PyQt6.QtWidgets import QFileDialog, QGridLayout
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QScrollBar
from PyQt6.QtWidgets import QButtonGroup
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtWidgets import QComboBox, QCheckBox
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton, QLineEdit
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from biomeslider import BiomeSlider
from faction import Faction
from industry import Industry
from defines import Research
from stylesheet import StyleSheet as ST
from perks import Perks as TS
from traits import Traits as TR



_FACTION_TRAITS = [TR.HE, TR.ST, TR.WM, TR.CA, TR.IS,
                   TR.SD, TR.PP, TR.IT, TR.AR, TR.JT]
_FACTION_PERKS = [TS.IFE, TS.TTF, TS.ARM, TS.ISB, TS.GRE, TS.URE, TS.MAL,
                  TS.NRS, TS.CHE, TS.BRM, TS.NAS, TS.LSP, TS.BET, TS.RSH]

_INFO_MESSAGE = ('These lesser traits may bestow a boon onto a faction or '
                 'prove detrimental. There is no need to choose any of '
                 'them. Multiple selections are possible. However, '
                 'unbalanced choices may affect the advantage score in a '
                 'disproportionate manner.')



class FactionWizard(QWidget):

    """ This class provides all the graphical elements of the wizard """

    class Selector(QRadioButton):

        """ This nested class is used to modify the behaviour of the radio
            buttons employed to select the lesser traits of a faction. """

        def __init__(self, box, label, text, n):
            super().__init__(text)
            self.index = n
            self.box = box
            self.info = label

        # The following methods are event handlers for the radio buttons.
        # Hence, their naming follows Qt coding conventions ...

        # pylint: disable=invalid-name

        def enterEvent(self, _):
            """ Display a short description of the perk """
            perk = _FACTION_PERKS[self.index]
            self.box.setTitle(perk.value[0] + ' ')
            self.info.setText(str(perk.value[1]))

        def leaveEvent(self, _):
            """ Remove any descriptions and box headings """
            self.box.setTitle('Secondary Traits ')
            self.info.setText(_INFO_MESSAGE)

        # pylint: enable=invalid-name


    class BiomeButton(QPushButton):

        """ This nested class is used to encode a biome parameter
            and the requested mode of interaction with its slider """

        # pylint: disable=too-few-public-methods

        def __init__(self, n, mode):
            super().__init__()
            self.n = n
            self.mode = mode

        # pylint: enable=too-few-public-methods


    def __init__(self, people, rules):
        super().__init__()
        self.setWindowTitle("Custom Faction Wizard - Step 1 of 6")
        self.setStyleSheet(ST.FACTIONSETUP_1.value)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Icons/Host"))
        self.setWindowIcon(icon)
        self.setFixedSize(1000, 750)
        self.hide()
        self.banners = []
        self.wizard = QWidget(self)
        self.pages = QStackedLayout(self.wizard)
        self.surplus = QComboBox()
        self.settings = QButtonGroup()
        self.traits = QButtonGroup()
        self.trait_info = QLabel()
        self.features = QButtonGroup()
        self.selector = QScrollBar(Qt.Orientation.Horizontal)
        self.faction_singular = QLineEdit()
        self.faction_plural = QLineEdit()
        self.default_name = 'Humanoid'
        self.research_level = QCheckBox()
        self.industry_settings = {}
        self.research_costs = {}
        self.biome_slider = []
        self.max_growth_rate = 15
        self.restart_game_wizard = False
        self.restart_new_game = False
        self.factions = people
        self.selected_banner = 0
        self.template = None
        self.current_page = 0
        self._setup_error_messages()
        self._setup_buttons_and_score()
        self._setup_names_and_banner()
        self._setup_primary_traits()
        self._setup_secondary_traits()
        self._setup_biome_tolerances()
        self._setup_mining_and_resources()
        self._setup_research_costs()

        self.adv_score = 80                 # TODO: Remove test rigging
        self.compute_advantage_points()     # TODO: Remove me?


    def _setup_error_messages(self):
        """ Create a modal dialog to display warnings to the player """
        self.error = QMessageBox(self)
        self.error.setIcon(self.error.Icon.Warning)
        self.error.setWindowTitle('Custom Faction Wizard')
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Icons/Stars"))
        self.error.setWindowIcon(icon)


    def _create_button(self, label, tooltip, shortcut):
        """ Create a button with the specified label, tooltip & shortcut """
        button = QPushButton(label, self)
        button.setToolTip(' ' + tooltip)
        button.setFixedSize(QSize(140, 50))
        button.setShortcut(QKeySequence('Ctrl+' + shortcut))
        return button


    def _setup_buttons_and_score(self):
        """ Implement graphical elements of the wizard present on all of its pages """
        buttons_hl = QHBoxLayout()
        self.finish = self._create_button('Finish', ' Save the game settings.', 'F')
        self.cancel = self._create_button('Cancel', 'Close this dialog.', 'C')
        self.help = self._create_button('Help', 'Read the game manual.', 'H')
        self.next = self._create_button('Next', 'Proceed to the next page.', 'N')
        self.back = self._create_button('Back', 'Return to the previous page.', 'B')
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
        advantage_points.addSpacing(40)
        layout_vl = QVBoxLayout(self)
        layout_vl.addSpacing(10)
        layout_vl.addLayout(advantage_points)
        layout_vl.addSpacing(10)
        layout_vl.addWidget(self.wizard)
        layout_vl.addLayout(buttons_hl)
        self.finish.clicked.connect(self._save_faction_data)
        self.back.clicked.connect(self._revert)
        self.next.clicked.connect(self._proceed)


    def _proceed(self):
        """ Go to the next page of the custom faction wizard """
        if self.current_page < 5:
            self.current_page += 1
            step = 'Step ' + str(1 + self.current_page) + ' of 6'
            self.setWindowTitle('Custom Faction Wizard - ' + step)
            self.pages.setCurrentIndex(self.current_page)
            self.back.setEnabled(True)
            self.next.setEnabled(self.current_page < 5)


    def _revert(self):
        """ Return to the previous page of the custom faction wizard """
        if 0 < self.current_page:
            self.current_page -= 1
            step = 'Step ' + str(1 + self.current_page) + ' of 6'
            self.setWindowTitle('Custom Faction Wizard - ' + step)
            self.pages.setCurrentIndex(self.current_page)
            self.next.setEnabled(True)
            self.back.setEnabled(self.current_page > 0)


    def _save_faction_data(self):
        """ Store the faction specification in a file """
        save_faction = QFileDialog(self)
        save_faction.setOption(save_faction.Option.DontUseNativeDialog)
        save_faction.setStyleSheet(ST.FILEBROWSER.value)
        save_faction.setMinimumSize(1000, 750)
        save_faction.setFileMode(save_faction.FileMode.AnyFile)
        save_faction.setViewMode(save_faction.ViewMode.List)
        save_faction.setAcceptMode(save_faction.AcceptMode.AcceptSave)
        save_faction.setNameFilters(['Game Files (*.f1)', 'All Files (*.*)'])
        save_faction.setDefaultSuffix('f1')
        if save_faction.exec():
            files = save_faction.selectedFiles()
            try:
                with open(files[0], 'wt', encoding='utf-8') as f:
                    faction_data = ['Content']  # TODO: Lift this content from the wizard
                    json.dump(faction_data, f)
                    if self.restart_new_game:          # FIX ME
                        nf = Faction()
                        nf.deserialize(faction_data)
                    if self.restart_game_wizard:
                        pass
            except OSError:
                self.error.setText('Failed to save faction data!')
                self.error.exec()


    def configure_wizard(self, simple=False, advanced=False):
        """ Initialise the configuration wizard & store the invocation method """
        self.restart_new_game = simple
        self.restart_game_wizard = advanced
        self.current_page = 1
        self._revert()
        self.settings.button(0).setChecked(True)
        self.banners[self.selected_banner].setVisible(False)
        self.selected_banner = 0
        self.banners[0].setVisible(True)
        self.selector.setValue(0)
        self.faction_singular.setText('')
        self.faction_plural.setText('')
        self.surplus.setCurrentIndex(0)
        self.traits.button(9).setChecked(True)
        self._switch_primary_trait(9)
        self._switch_faction(0)
        self._restore_industry_modifier()
        for r in Research:
            self.research_costs[r].button(2).setChecked(True)
        self.research_level.setChecked(False)
        self.show()


    def _configure_surplus_usage(self):
        """ Create a combo box with various choices how to spend any
            leftover advantage points """
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
        self.surplus.addItem('Surface Minerals')
        self.surplus.addItem('Mineral Concentrations')
        self.surplus.addItem('Mines')
        self.surplus.addItem('Factories')
        self.surplus.addItem('Defenses')
        return surplus_hl


    def _create_banner_box(self):
        """ Create the graphical elements for the banner selector """
        self.selector.setMinimum(0)
        self.selector.setMaximum(19)
        banner_width = 180
        banner_box = QGroupBox()
        banner_box.setTitle('Faction Banner')
        banner_box.setMaximumWidth(40 + banner_width)
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, banner_width, banner_width)
        for f in "ABCDEFGHIJKLMNOPQRST":
            resource = ":/Factions/Faction-" +f
            banner = QGraphicsSvgItem(resource)
            width = banner.boundingRect().width()
            banner.setScale(0.9 * banner_width / width)
            banner.setPos(0.05 * banner_width, 0.05 * banner_width)
            banner.setVisible(False)
            scene.addItem(banner)
            self.banners.append(banner)
        banner_vl = QVBoxLayout(banner_box)
        banner_vl.addWidget(QGraphicsView(scene))
        banner_vl.addWidget(self.selector)
        return banner_box


    def _create_faction_box(self):
        """ Create the graphical elements for the faction selector """
        faction_box = QGroupBox()
        faction_box.setTitle('Predefined Factions')
        factions_gl = QGridLayout(faction_box)
        spacer = QLabel()
        spacer.setMaximumWidth(80)
        factions_gl.addWidget(spacer, 0, 0)
        n = 0
        for sp in self.factions.ai_faction:
            rb = QRadioButton(sp.species)
            factions_gl.addWidget(rb, n % 4, 1 + n // 4)
            self.settings.addButton(rb, n)
            n += 1
        rb = QRadioButton('Random')
        factions_gl.addWidget(rb, 2, 2)
        self.settings.addButton(rb, 6)
        rb = QRadioButton('Custom')
        factions_gl.addWidget(rb, 3, 2)
        self.settings.addButton(rb, 7)
        return faction_box


    def _setup_names_and_banner(self):
        """ Create the first page of the configuration wizard """
        alignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight
        names_gl = QGridLayout()
        spacer = QLabel()
        spacer.setMaximumWidth(35)
        label = QLabel('Faction Name (singular):')
        label.setAlignment(alignment)
        self.faction_singular.setMaximumWidth(600)
        self.faction_plural.setMaximumWidth(600)
        self.faction_singular.setPlaceholderText(self.default_name)
        self.faction_plural.setPlaceholderText(self.default_name + 's')
        names_gl.addWidget(spacer, 0, 2)
        names_gl.addWidget(label, 0, 0)
        names_gl.addWidget(self.faction_singular, 0, 1)
        label = QLabel('Faction Name (plural):')
        label.setAlignment(alignment)
        names_gl.addWidget(label, 1, 0)
        names_gl.addWidget(self.faction_plural, 1, 1)
        banner_hl = QHBoxLayout()
        banner_hl.addSpacing(40)
        banner_hl.addWidget(self._create_faction_box())
        banner_hl.addSpacing(60)
        banner_hl.addWidget(self._create_banner_box())
        banner_hl.addSpacing(40)
        names_and_banner = QWidget(self)
        layout_vl = QVBoxLayout(names_and_banner)
        layout_vl.addSpacing(10)
        layout_vl.addLayout(names_gl)
        layout_vl.addSpacing(20)
        layout_vl.addLayout(banner_hl)
        layout_vl.addSpacing(20)
        layout_vl.addLayout(self._configure_surplus_usage())
        layout_vl.addStretch()
        self.pages.addWidget(names_and_banner)
        self.settings.idClicked.connect(self._switch_faction)
        self.selector.valueChanged.connect(self._switch_faction_banner)


    def _setup_primary_traits(self):
        """ Create the second page of the configuration wizard """
        self.trait_info.setWordWrap(True)
        traits_box = QGroupBox(self)
        traits_box.setMaximumHeight(280)
        traits_box.setTitle('Essential Traits of the Faction ')
        traits_gl = QGridLayout(traits_box)
        n = -1
        for t in TR:
            if n >= 0:
                rb = QRadioButton(t.value[0])
                traits_gl.addWidget(rb, n % 5, 1 + n // 5)
                self.traits.addButton(rb, n)
            n += 1
        spacer = QLabel()
        spacer.setMaximumSize(80, 5)
        traits_gl.addWidget(spacer, 5, 0)
        rb.setChecked(True)
        traits_hl = QHBoxLayout()
        traits_hl.addSpacing(40)
        traits_hl.addWidget(traits_box)
        traits_hl.addSpacing(40)
        descriptions = QGroupBox(self)
        text_vl = QVBoxLayout(descriptions)
        text_vl.addWidget(self.trait_info)
        text_vl.addStretch()
        descriptions.setTitle('Description of the Traits ')
        description_hl = QHBoxLayout()
        description_hl.addSpacing(40)
        description_hl.addWidget(descriptions)
        description_hl.addSpacing(40)
        primary_traits = QWidget(self)
        layout_vl = QVBoxLayout(primary_traits)
        layout_vl.addSpacing(10)
        layout_vl.addLayout(traits_hl)
        layout_vl.addSpacing(20)
        layout_vl.addLayout(description_hl)
        layout_vl.addSpacing(20)
        self.pages.addWidget(primary_traits)
        self.traits.idClicked.connect(self._switch_primary_trait)


    def _setup_secondary_traits(self):
        """ Create the third page of the configuration wizard """
        self.features.setExclusive(False)
        info = QLabel()
        info.setWordWrap(True)
        info.setText(_INFO_MESSAGE)
        info_box = QGroupBox(self)
        info_box.setTitle('Secondary Traits ')
        traits_box = QGroupBox(self)
        traits_box.setMaximumHeight(380)
        traits_box.setTitle('Secondary Traits of the Faction ')
        traits_gl = QGridLayout(traits_box)
        n = 0
        for t in TS:
            rb = self.Selector(info_box, info, t.value[0], n)
            traits_gl.addWidget(rb, n % 7, 1 + n // 7)
            self.features.addButton(rb, n)
            n += 1
        spacer = QLabel()
        spacer.setMaximumSize(80, 5)
        traits_gl.addWidget(spacer, 8, 0)
        traits_hl = QHBoxLayout()
        traits_hl.addSpacing(40)
        traits_hl.addWidget(traits_box)
        traits_hl.addSpacing(40)
        text_vl = QVBoxLayout(info_box)
        text_vl.addWidget(info)
        text_vl.addStretch()
        description_hl = QHBoxLayout()
        description_hl.addSpacing(40)
        description_hl.addWidget(info_box)
        description_hl.addSpacing(40)
        secondary_traits = QWidget(self)
        layout_vl = QVBoxLayout(secondary_traits)
        layout_vl.addSpacing(10)
        layout_vl.addLayout(traits_hl)
        layout_vl.addSpacing(20)
        layout_vl.addLayout(description_hl)
        layout_vl.addSpacing(20)
        self.pages.addWidget(secondary_traits)
        self.features.idClicked.connect(self._select_secondary_trait)


    def _setup_biome_tolerances(self):
        """ Create the fourth page of the configuration wizard """
        biome_settings = QWidget()
        biome_settings.setStyleSheet(ST.FACTIONSETUP_3.value)
        layout_vl = QVBoxLayout(biome_settings)
        for i in 0, 1, 2:
            self._create_biome_slider(layout_vl, i)
        layout_vl.addSpacing(10)
        self._add_growth_modifier(layout_vl)
        layout_vl.addSpacing(10)
        self.pages.addWidget(biome_settings)


    def _add_growth_modifier(self, layout):
        """ Create a spin box to adjust the growth rate of the colonies """
        data = QSpinBox()
        data.setSuffix('%')
        data.setRange(1, 20)
        data.setValue(15)
        data.setMinimumSize(QSize(95, 40))
        data.setAlignment(Qt.AlignmentFlag.AlignLeft)
        data.setWrapping(False)
        data.lineEdit().setEnabled(False)
        data.valueChanged.connect(self._adjust_growth_rate)
        label = QLabel('Maximum colony growth rate per year:')
        hlayout = QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addWidget(data)
        hlayout.addStretch()
        layout.addLayout(hlayout)


    def _adjust_growth_rate(self, newrate):
        """ Store new growth rate & recompute spent advantage points """
        self.max_growth_rate = newrate
        self.compute_advantage_points()


    def _create_biome_slider(self, layout, n):
        """ Create a graphical element to adjust biome tolerances """
        title = ['Gravity', 'Temperature', 'Radiation']
        slider = BiomeSlider(n)
        slider.update_advantage_score.connect(self.compute_advantage_points)
        self.biome_slider.append(slider)
        frame = QGroupBox(title[n])
        layout_vl = QVBoxLayout(frame)
        view = QGraphicsView(slider)
        view.setMouseTracking(False)
        layout_vl.addWidget(view)
        self._create_biome_controls(layout_vl, n)
        layout.addWidget(frame)


    def _create_biome_controls(self, layout, n):
        """ Create the buttom bar to adjust tolerance settings """
        parameter = ['Gravity', 'Temperature', 'Radiation']
        control = QWidget()
        control.setFixedWidth(720)
        control_hl = QHBoxLayout(control)
        control_hl.setSpacing(10)
        control_hl.addWidget(self._create_biome_button(n, 0))
        control_hl.addWidget(self._create_biome_button(n, 2))
        control_hl.addWidget(self._create_biome_button(n, 3))
        control_hl.addSpacing(25)
        immune = QCheckBox('  Immune to ' + parameter[n])
        immune.setStyleSheet('padding: 0px')
        immune.checkStateChanged.connect(self.biome_slider[n].update_immunity)
        control_hl.addWidget(immune)
        control_hl.addStretch()
        control_hl.addWidget(self._create_biome_button(n, 1))
        controls = QHBoxLayout()
        controls.addWidget(control)
        layout.addLayout(controls)


    def _process_biome_button(self):
        """ Adjust the biome tolerances currently in use """
        lower_shift_value = [-0.01, 0.01, 0.01, -0.01]
        upper_shift_value = [-0.01, 0.01, -0.01, 0.01]
        button = self.sender()
        slider = self.biome_slider[button.n]
        smin = lower_shift_value[button.mode]
        smax = upper_shift_value[button.mode]
        slider.adjust_biome_limits(smin, smax)


    def _create_biome_button(self, n, m):
        """ Create a button of the specified icon """
        name = ['Left', 'Right', 'Shrink', 'Expand']
        width = [40, 40, 80, 80]
        button = self.BiomeButton(n, m)
        image = QIcon(':/Icons/' + name[m])
        button.setIcon(image)
        button.setIconSize(QSize(width[m] - 10, 30))
        button.setFixedSize(QSize(width[m], 40))
        button.setStyleSheet('padding: 0px;')
        button.clicked.connect(self._process_biome_button)
        return button


    def _setup_mining_and_resources(self):
        """ Create the fifth page of the configuration wizard """
        industry_settings = QWidget()
        industry_settings.setStyleSheet(ST.FACTIONSETUP_2.value)
        layout_vl = QVBoxLayout(industry_settings)
        layout_vl.addSpacing(20)
        for imod in Industry:
            self._add_industry_modifier(layout_vl, imod)
        layout_vl.addStretch()
        self.pages.addWidget(industry_settings)


    def _setup_research_costs(self):
        """ Create the sixth page of the configuration wizard """
        research_costs = QWidget()
        research_costs.setStyleSheet(ST.FACTIONSETUP_2.value)
        layout = QGridLayout()
        layout.setSpacing(20)
        layout_vl = QVBoxLayout(research_costs)
        layout_vl.addLayout(layout)
        n = 0
        for fe in Research:
            self._add_research_box(fe, layout, n // 2, n % 2)
            n += 1
        self.research_level.setText('  All extra expensive research starts at technology level 4.')
        layout_vl.addStretch()
        layout_vl.addWidget(self.research_level)
        self.pages.addWidget(research_costs)


    def _add_research_box(self, area, layout, xpos, ypos):
        """ Create a group box with settings for a particular field of research """
        box = QGroupBox(area.value + ' Research')
        buttons = QButtonGroup()
        self.research_costs[area] = buttons
        layout_vl = QVBoxLayout(box)
        radio = QRadioButton('Costs 75% extra')
        buttons.addButton(radio, 1)
        layout_vl.addWidget(radio)
        radio = QRadioButton('Costs standard amount')
        radio.setChecked(True)
        buttons.addButton(radio, 2)
        layout_vl.addWidget(radio)
        radio = QRadioButton('Costs 50% less')
        buttons.addButton(radio, 3)
        layout_vl.addWidget(radio)
        layout.addWidget(box, xpos, ypos)


    def _add_industry_modifier(self, vlayout, imod):
        """ Create one line with production related game settings to tweak """
        msg, suffix, default, low, high, step, width = imod.value
        data = QSpinBox()
        data.setSuffix(suffix)
        data.setRange(low, high)
        data.setValue(default)
        data.setSingleStep(step)
        data.setMinimumSize(QSize(width, 40))
        data.setAlignment(Qt.AlignmentFlag.AlignLeft)
        if default < 1:
            data.setWrapping(True)
            data.lineEdit().setEnabled(False)
        label = QLabel(msg)
        hlayout = QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addWidget(data)
        hlayout.addStretch()
        vlayout.addSpacing(10)
        vlayout.addLayout(hlayout)
        self.industry_settings[imod] = data


    def _restore_industry_modifier(self):
        """ Recover the default industry settings for a game """
        for imod in Industry:
            spinner = self.industry_settings[imod]
            spinner.setValue(imod.value[2])


    def _switch_faction(self, buttonid):
        """ Switch to another predefined faction """
        if buttonid < 6:
            self.next.setEnabled(True)
            faction = self.factions.ai_faction[buttonid]
            self.faction_singular.setPlaceholderText(faction.species)
            self.faction_plural.setPlaceholderText(faction.species + 's')
            self.default_name = faction.species
            self.template = copy.deepcopy(faction)
        elif buttonid < 7:
            self._randomize_faction()
        else:
            self._customize_faction()


    def _switch_primary_trait(self, buttonid):
        """ Switch to another primary trait of the faction """
        trait = _FACTION_TRAITS[buttonid]
        self.trait_info.setText(trait.value[1])
        self.compute_advantage_points()


    def _select_secondary_trait(self, buttonid):
        """ Check the selected perk & recompute advantage points """
        if buttonid == 2:
            self.features.button(9).setChecked(False)
        elif buttonid == 9:
            self.features.button(2).setChecked(False)
        self.compute_advantage_points()


    def _switch_faction_banner(self, value):
        """ The scroll bar has been moved to change the faction banner """
        self.banners[self.selected_banner].setVisible(False)
        self.selected_banner = value
        self.banners[value].setVisible(True)


    def _randomize_faction(self):
        """ Select a faction with randomized traits """
        self.next.setEnabled(False)
        self.faction_singular.setPlaceholderText('Random')
        self.faction_plural.setPlaceholderText('Randoms')
        self.default_name = 'Random'


    def _customize_faction(self):
        """ Create a cutomized faction """
        print('-- Customize --')


    def compute_advantage_points(self):
        """ Render the current advantage point count & prevent
            the player from saving the configuration data, if
            the number of advantage points has dropped below 0 """
        style = 'font-size: 24pt;font-weight: 800;padding: 0px;'

        value = self.adv_score - 10   # TODO: Perform the actual computation ...
        self.adv_score = value

        if value < 0:
            self.advantage.setStyleSheet(style + 'color: red;')
            self.finish.setEnabled(False)
        else:
            self.advantage.setStyleSheet(style + 'color: black;')
            self.finish.setEnabled(True)
        self.advantage.setText(str(value))

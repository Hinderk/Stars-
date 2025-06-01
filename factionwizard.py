
""" This module implements the custom faction wizard """

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
from PyQt6.QtWidgets import QComboBox  # , QSpinBox
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton, QLineEdit
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from faction import Faction
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

        #  pylint: disable=invalid-name

        def enterEvent(self, _):
            """ Display a short description of the perk """
            perk = _FACTION_PERKS[self.index]
            self.box.setTitle(perk.value[0] + ' ')
            self.info.setText(str(perk.value[1]))


        def leaveEvent(self, _):
            """ Remove any descriptions and box headings """
            self.box.setTitle('Secondary Traits ')
            self.info.setText(_INFO_MESSAGE)

        #  pylint: enable=invalid-name


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
        self.set_advantage_points(0)  # TODO: Remove me


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
        save_faction.setStyleSheet(ST.FILEBROWSER)
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
#        self.traits.button(9).setChecked(True)
#        self._switch_primary_trait(9)
        self._switch_faction(0)
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
# TODO: Compute advantage points!


    def _show_secondary_trait(self, buttonid):
        """ Show the description of the selected secondary trait """
        trait = _FACTION_TRAITS[buttonid]
        self.feature_info.setText(trait.value[1])
        print(buttonid)
# TODO: Compute advantage points!



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


    def set_advantage_points(self, value):
        """ Render the current advantage point count & prevent
            the player from saving the configuration data, if
            the number of advantage points has dropped below 0 """
        style = 'font-size: 24pt;font-weight: 800;padding: 0px;'
        if value < 0:
            self.advantage.setStyleSheet(style + 'color: red;')
            self.finish.setEnabled(False)
        else:
            self.advantage.setStyleSheet(style + 'color: black;')
            self.finish.setEnabled(True)
        self.advantage.setText(str(value))

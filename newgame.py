
""" This module implements the dialog used to setup new game sessions """

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QKeySequence
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QComboBox
from PyQt6.QtWidgets import QRadioButton, QLabel
from PyQt6.QtWidgets import QPushButton

from stylesheet import StyleSheet as ST



class NewGame(QWidget):

    """ The class implements the dialog used to setup new games """

    def __init__(self, people, _):
        super().__init__()
        self.setWindowTitle('New Game')
        self.setStyleSheet(ST.SIMPLESETUP.value)
        icon = QIcon()
        icon.addPixmap(QPixmap(':/Icons/Host'))
        self.setWindowIcon(icon)
        self.setFixedSize(800, 600)
        self.hide()

        left_side = QWidget()
        right_side = QWidget()
        faction_box = QGroupBox()
        faction_box.setTitle('Player Faction')
        faction_vl = QVBoxLayout(faction_box)
        self.faction_selector = QComboBox()
        faction_vl.addWidget(self.faction_selector)
        self.faction_setup = QPushButton()
        self.faction_setup.setText('Customize &Faction')
        self.faction_setup.setShortcut(QKeySequence('Ctrl+F'))
        faction_vl.addWidget(self.faction_setup)

        game_box = QGroupBox()
        game_box.setTitle('Advanced Game')
        game_vl = QVBoxLayout(game_box)
        self.advanced_game = QPushButton()
        self.advanced_game.setText('&Advanced Game Configuration')
        self.advanced_game.setShortcut(QKeySequence('Ctrl+A'))
        explanation = QLabel('This button allows You to configure multi-player games '
                             'and customize advanced game options. You do not need to '
                             'press it to launch standard single player games.')
        explanation.setWordWrap(True)
        game_vl.addWidget(explanation)
        game_vl.addWidget(self.advanced_game)

        button_size = QSize(160, 50)
        buttons_hl = QHBoxLayout()
        self.solo_start = QPushButton()
        self.solo_start.setText('&OK')
        self.solo_start.setToolTip(' Start a new game with default settings.')
        self.solo_start.setShortcut(QKeySequence('Ctrl+O'))
        self.solo_start.setFixedSize(button_size)
        buttons_hl.addWidget(self.solo_start)
        cancel = QPushButton()
        cancel.setText('&Cancel')
        cancel.setToolTip(' Close this dialog.')
        cancel.setShortcut(QKeySequence('Ctrl+C'))
        cancel.setFixedSize(button_size)
        buttons_hl.addStretch()
        buttons_hl.addWidget(cancel)
        self.help = QPushButton()
        self.help.setText('&Help')
        self.help.setToolTip(' Read the game manual.')
        self.help.setShortcut(QKeySequence('Ctrl+H'))
        self.help.setFixedSize(button_size)
        buttons_hl.addStretch()
        buttons_hl.addWidget(self.help)

        right_vl = QVBoxLayout(right_side)
        right_vl.addWidget(faction_box)
        right_vl.addSpacing(20)
        right_vl.addWidget(game_box)
        right_vl.addStretch()
        right_vl.addLayout(buttons_hl)
        right_vl.addSpacing(15)

        size_box = QGroupBox()
        size_box.setTitle('Universe Size')
        tiny = QRadioButton('Tiny')
        small = QRadioButton('Small')
        medium = QRadioButton('Medium')
        large = QRadioButton('Large')
        huge = QRadioButton('Huge')
        size_vl = QVBoxLayout(size_box)
        size_vl.setSpacing(0)
        size_vl.addWidget(tiny)
        size_vl.addWidget(small)
        size_vl.addWidget(medium)
        size_vl.addWidget(large)
        size_vl.addWidget(huge)
        small.setChecked(True)
        self.map_size = [tiny, small, medium, large, huge]

        mode_box = QGroupBox()
        mode_box.setTitle('Difficulty Level')
        easy = QRadioButton('Easy')
        standard = QRadioButton('Standard')
        harder = QRadioButton('Harder')
        expert = QRadioButton('Expert')
        mode_vl = QVBoxLayout(mode_box)
        mode_vl.setSpacing(0)
        mode_vl.addWidget(easy)
        mode_vl.addWidget(standard)
        mode_vl.addWidget(harder)
        mode_vl.addWidget(expert)
        standard.setChecked(True)
        self.difficulty = [easy, standard, harder, expert]

        left_vl = QVBoxLayout(left_side)
        left_vl.setSpacing(0)
        left_vl.addWidget(mode_box)
        left_vl.addSpacing(20)
        left_vl.addWidget(size_box)
        left_vl.addStretch()

        layout_hl = QHBoxLayout(self)
        layout_hl.setSpacing(0)
        layout_hl.addWidget(left_side)
        layout_hl.addWidget(right_side)

        for ai in people.ai_faction:
            self.faction_selector.addItem(ai.species)
        self.faction_selector.addItem('Random')

        cancel.clicked.connect(self.hide)


    def configure_game(self):
        """ Open the new game wizard with default values """
        self.faction_selector.setCurrentIndex(0)
        self.map_size[1].setChecked(True)
        self.difficulty[1].setChecked(True)
        self.show()

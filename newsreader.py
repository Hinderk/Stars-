
""" This module implements the news reader panel on the left side of the GUI """

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QPushButton, QToolButton
from PyQt6.QtWidgets import QGroupBox, QCheckBox
from PyQt6.QtWidgets import QPlainTextEdit

# from guidesign import GuiDesign, GuiStyle



class NewsReader(QGroupBox):

    """ This class is responsible for logging the latest game events """

    def __init__(self):
        super().__init__()
        self.current_game_year = QLabel(self)
        self.current_message = QPlainTextEdit(self)
        self.previous_message = QPushButton(self)
        self.next_message = QPushButton(self)
        self.follow_message = QPushButton(self)
        self.filter_message = QCheckBox(self)
        self._setup_news_reader()



    def _apply_message_filter(self, state):
        """ Either engage or disengage the message filter """
        print('Message filter: ' + str(state) + ' ...')



    def _create_message_filter(self):
        """ Create the message filter button in the title of the news reader """
        icon = QIcon()
        show = QPixmap(":/Icons/ShowNews")
        no_show = QPixmap(":/Icons/NoNews")
        icon.addPixmap(no_show, QIcon.Mode.Normal, QIcon.State.Off)
        icon.addPixmap(show, QIcon.Mode.Normal, QIcon.State.On)
        message_filter = QToolButton(self)
        message_filter.setCheckable(True)
        message_filter.setIcon(icon)
        message_filter.setAutoRepeat(False)
        message_filter.setToolTip("Show the likes of the current message ...")
        message_filter.setStatusTip("Show the likes of the current message ...")
        message_filter.setIconSize(QSize(30, 30))
        message_filter.toggled.connect(self._apply_message_filter)
        return message_filter


    def _setup_news_reader(self):
        """ Create the news reader panel & its controls """
        self.filter_message.setToolTip("Show the likes of the current message ...")
        self.filter_message.setStatusTip("Show the likes of the current message ...")
        self.filter_message.setChecked(True)
        self.current_game_year.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_game_year.setToolTip("Current Age of the Galaxy ...")
        self.current_game_year.setText("Year 2400 - Message: 1 of 9999")  # TODO: Create alongside messages - To be removed here!
        filter_hl = QHBoxLayout()
        filter_hl.addWidget(self.filter_message)
        filter_hl.addStretch()
        filter_hl.addWidget(self.current_game_year)
        filter_hl.addStretch()
        filter_hl.addWidget(self._create_message_filter())
        self.current_message.setReadOnly(True)
        self.current_message.setPlainText('This is a very important message ...')  # TODO: Delete this ...
        self.previous_message.setText("Prev")
        self.previous_message.setToolTip("Read previous message ...")
        self.previous_message.setStatusTip("Read the previous message ...")
        self.follow_message.setText("Goto")
        self.follow_message.setToolTip("Follow up on current message ...")
        self.follow_message.setStatusTip("Follow up on the current message ...")
        self.next_message.setText("Next")
        self.next_message.setToolTip("Read next message ...")
        self.next_message.setStatusTip("Read the next message ...")
        news_buttons_vl = QVBoxLayout()
        news_buttons_vl.addStretch()
        news_buttons_vl.addWidget(self.previous_message)
        news_buttons_vl.addWidget(self.follow_message)
        news_buttons_vl.addWidget(self.next_message)
        news_buttons_vl.addStretch()
        news_hl = QHBoxLayout()
        news_hl.setSpacing(5)
        news_hl.addWidget(self.current_message)
        news_hl.addLayout(news_buttons_vl)
        news_vl = QVBoxLayout(self)
        news_vl.addLayout(filter_hl)
        news_vl.addLayout(news_hl)
        news_vl.addSpacing(5)
        self.setMaximumHeight(190)

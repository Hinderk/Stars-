
from enum import Enum



class GuiStyle(Enum):
    GeneralGui = 0
    StarMap = 1
    SimpleSetup = 2
    AdvancedSetup_1 = 3
    AdvancedSetup_2 = 4
    AdvancedSetup_3 = 5
    PlayerMenu = 6
    FileBrowser = 7
    FactionSetup_1 = 8


class GuiDesign:

    Style_0 = """

             QCheckBox {
                 spacing: 0px;
             }

             QCheckBox::indicator {
                 width: 30px;
                 height: 30px;
             }

             QPlainTextEdit {
                 padding: 5px 10px 5px 10px;
                 border: 1px solid rgb(120,120,120);
                 border-radius: 6px;
                 font-size: 16pt;
                 font-weight: 400;
                 background-color: white;
             }

             QLabel {
                 padding: 5px 10px 5px 10px;
                 font-size: 18pt;
                 font-weight: 600;
                 background-color: transparent;
             }

             QPushButton {
                 padding: 5px 10px 5px 10px;
                 font-size: 16pt;
                 font-weight: 400;
                 border: 1.5px solid rgb(120,120,120);
                 border-radius: 6px;
                 background-color: white;
             }

             QStatusBar {
                 background: rgb(243,243,243);
                 color: black;
                 font-style: italic;
                 font-size: 16pt;
                 font-weight: 600;
             }

             QSpinBox {
                 font-size: 24px;
                 font-style: italic;
                 font-weight: 600;
             }

             QSpinBox::down-button {
                 width: 20
             }

             QSpinBox::up-button {
                 width: 20
             }

             QMenuBar {
                 background-color: rgb(255,255,255);
                 color: rgb(0,0,0);
                 font-size: 18px;
             }

             QMenuBar::item {
                 background-color: rgb(255,255,255);
                 color: rgb(0,0,0);
             }

             QMenuBar::item::selected {
                 background-color: rgb(240,240,240);
                 color: rgb(0,0,0);
             }

             QMenu::item {
                 background-color: rgb(255,255,255);
                 color: rgb(0,0,0);
                 font-size: 18px;
                 padding: 5px 25px 5px 15px;
             }

             QMenu::indicator:unchecked {
                 width: 30px;
             }

             QMenu::indicator:checked {
                 width: 20px;
                 padding: 0px 0px 0px 10px;
             }

             QMenu::separator {
                 width: 1.0px;
                 height: 1.0px;
                 background-color: rgb(0,0,0);
             }

             QMenu::item::selected {
                 background-color: rgb(240,240,240);
                 color: rgb(0,0,0);
                 font-size: 18px;
             }

         """

    Style_1 = """

             QMenu {
                 border: 1.5px solid rgb(200,200,200) ;
                 border-radius: 0px
             }

             QMenu::item {
                 background-color: rgb(0,0,0);
                 color: rgb(240,240,240);
                 font-size: 18px;
                 padding: 6px 12px 6px 12px;
             }

             QMenu::separator {
                 width: 1.0px;
                 height: 1.0px;
                 background-color: rgb(200,200,200);
             }

             QMenu::item::selected {
                 background-color: rgb(200,200,200);
                 color: rgb(0,0,0);
                 font-size: 18px;
             }

         """

    Style_2 = """

             QLineEdit {
                 padding: 5px 10px 10px 10px;
                 font-size: 18pt;
                 font-style: oblique;
                 font-weight: 400;
                 border: 1.5px solid rgb(120,120,120);
                 border-radius: 6px;
                 background-color: white;
             }

             QPushButton {
                 padding: 5px 10px 10px 10px;
                 font-size: 16pt;
                 font-style: oblique;
                 font-weight: 400;
                 border: 1.5px solid rgb(120,120,120);
                 border-radius: 6px;
             }

             QPushButton:enabled {
                 background-color: white;
             }

             QPushButton:disabled {
                 background-color: #f3f3f3;
                 color: #c8c8c8;
                 border: 1.5px solid #c8c8c8;
             }

             QPushButton:hover:!pressed {
                 background-color:#5f94bc;
             }

             QPushButton:pressed {
                 background-color: #4f84ac;
             }

             QLabel {
                 padding: 0px 10px 10px 10px;
                 font-size: 16pt;
                 font-style: oblique;
                 font-weight: 400;
                 background-color: transparent;
             }

             QRadioButton {
                 padding: 5px 10px 5px 10px;
                 font-size: 16pt;
                 font-style: oblique;
                 font-weight: 400;
             }

             QGroupBox {
                 background: rgb(243,243,243);
                 color: black;
                 font-style: oblique;
                 font-size: 20pt;
                 font-weight: 400;
             }

             QComboBox {
                 padding: 5px 0px 10px 20px;
                 font-size: 22px;
                 font-style: oblique;
                 font-weight: 400;
                 border: 1.5px solid rgb(120,120,120);
                 border-radius: 6px;
                 background-color: white;
             }

             QComboBox::drop-down {
                 subcontrol-origin: padding;
                 subcontrol-position: top right;
                 width: 25px;
                 border-left-width: 1px;
                 border-left-color: darkgray;
                 border-left-style: solid;
                 border-top-right-radius: 6px;
                 border-bottom-right-radius: 6px;
             }

             QComboBox::down-arrow {
                 image: url(:/Icons/Select);
                 width: 20px;
                 height: 20px;
             }

         """

    Style_3 = """

             QWidget {
                 background-color: #f3f3f3;
             }

             QTableView {
                 padding: 20px 20px 20px 20px;
                 font-weight: 400;
                 font-size: 16pt;
                 font-style: oblique;
                 border-radius: 6px;
                 border: 1.5px solid #787878;
                 outline: none;
             }

             QTableView::item {
                 padding: 0px 10px 0px 10px;
                 background-color: white;
                 border-bottom: 1px solid #a0a0a0;
                 border-right: 1px solid #a0a0a0;
             }

             QTableView::item:selected {
                 background-color: #5f94bc;
                 selection-color: white;
             }

             QHeaderView::section {
                 padding: 4px 10px 4px 10px;
                 border-style: none;
                 background-color: #f3f3f3;
                 font-weight: 600;
                 font-size: 16pt;
                 font-style: oblique;
                 border-bottom: 1px solid #a0a0a0;
                 border-right: 1px solid #a0a0a0;
             }

             QHeaderView::section:horizontal {
                 border-top: 1px solid #a0a0a0;
             }

             QHeaderView::section:vertical {
                 border-left: 1px solid #a0a0a0;
             }

             QTableCornerButton::section {
                 border: 1px solid #a0a0a0;
                 background-color: #f3f3f3;
             }

             QLineEdit {
                 padding: 0px;
                 border: none;
                 font-size: 16pt;
                 font-style: oblique;
                 font-weight: 600;
                 color: black;
                 background-color: white;
             }

         """

    Style_4 = """

             QMenu {
                 border: 1px solid #787878;
                 padding: 5px;
                 border-radius: 6px
             }

             QMenu::item {
                 background-color: #f3f3f3;
                 color: black;
                 font-size: 16pt;
                 font-style: oblique;
                 font-weight: 400;
                 padding: 6px 12px 6px 12px;
             }

             QMenu::separator {
                 width: 1.0px;
                 height: 1.0px;
                 background-color: black;
             }

             QMenu::item::selected {
                 background-color: #5f94bc;
                 color: white;
                 font-size: 16pt;
                 font-style: oblique;
                 font-weight: 600;
             }

         """

    Style_5 = """

             QLabel {
                 font-size: 20pt;
                 font-style: oblique;
                 font-weight: 600;
                 padding: 6px 0px 6px 0px;
             }

             QRadioButton {
                 font-size: 20pt;
                 font-style: oblique;
                 font-weight: 400;
                 padding: 6px 0px 6px 32px;
             }

             QSpinBox {
                 font-size: 20pt;
                 font-style: oblique;
                 font-weight: 400;
                 background-color: #f3f3f3;
             }

             QSpinBox::down-button {
                 width: 20
             }

             QSpinBox::up-button {
                 width: 20
             }

         """

    Style_6 = """

             QLineEdit {
                 padding: 5px 10px 10px 10px;
                 font-size: 18pt;
                 font-weight: 500;
             }

             QPushButton {
                 padding: 5px 10px 10px 10px;
                 font-size: 18pt;
                 font-style: oblique;
                 font-weight: 500;
             }

             QLabel {
                 padding: 5px 10px 10px 10px;
                 font-weight: 500;
                 font-size: 18pt;
                 font-style: oblique;
             }

             QComboBox {
                 padding: 5px 0px 10px 20px;
                 font-size: 20px;
                 font-style: oblique;
                 font-weight: 600;
             }

             QTreeView {
                 font-size: 18px;
                 font-style: oblique;
                 font-weight: 400;
             }

             QTreeView::item:selected:active {
                 background: #4f84ac;
             }

             QTreeView::item:hover {
                 background: #5f94bc;
             }

             QHeaderView::section {
                 font-size: 16px;
                 font-style: oblique;
                 font-weight: 600;
                 padding: 6px 0px 0px 20px;
             }

             QTreeView::header {
                 font-size: 18px;
                 font-style: oblique;
                 font-weight: 400;
             }

             QListView {
                 font-size: 18px;
                 font-style: oblique;
                 font-weight: 400;
             }

             QListView::item:selected:active {
                 background: #4f84ac;
             }

             QListView::item:hover {
                 background: #5f94bc;
             }

         """

    def getStyle(role, select=0):
        if role == GuiStyle.GeneralGui:
            return GuiDesign.Style_0
        elif role == GuiStyle.StarMap:
            return GuiDesign.Style_1
        elif role == GuiStyle.SimpleSetup:
            return GuiDesign.Style_2
        elif role == GuiStyle.AdvancedSetup_1:
            return GuiDesign.Style_2
        elif role == GuiStyle.AdvancedSetup_2:
            return GuiDesign.Style_3
        elif role == GuiStyle.PlayerMenu:
            return GuiDesign.Style_4
        elif role == GuiStyle.AdvancedSetup_3:
            return GuiDesign.Style_5
        elif role == GuiStyle.FileBrowser:
            return GuiDesign.Style_6
        elif role == GuiStyle.FactionSetup_1:
            return GuiDesign.Style_2  # FIX ME !!


    def getSize():
        return [2400, 1350]

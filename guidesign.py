

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


    def getGuiStyle(select=0):
        return GuiDesign.Style_0


    def getMapStyle(select=0):
        return GuiDesign.Style_1


    def getSize():
        return [2400, 1350]

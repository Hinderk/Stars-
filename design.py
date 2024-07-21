

class Design:

    Style_0 = """

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

             QMenu::separator {
                 width: 1.5px;
                 height: 1.5px;
                 background-color: #000;
             }

             QMenu::item::selected {
                 background-color: rgb(240,240,240);
                 color: rgb(0,0,0);
                 font-size: 18px;
             }

         """

    def __init__(self):
        self.MenuFontSize = 16
        self.GuiDesign = (self.Style_0, self.Style_0)

    def getStyle(self, select=1):
        return self.GuiDesign[select]

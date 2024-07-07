

class Design:

    Style_0 = """
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
     
             QMenu {
                 background-color: rgb(255,255,255);
                 color: rgb(0,0,0);
             }
     
             QMenu::item::selected {
                 background-color: rgb(240,240,240);
                 color: rgb(0,0,0);
             }
         """

    def __init__(self):
        self.MenuFontSize = 16
        self.GuiDesign = (self.Style_0, self.Style_0)

    def getStyle(self, select=1):
        return self.GuiDesign[select]
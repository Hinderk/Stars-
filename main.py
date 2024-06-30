
import sys
import stars_ui

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPen, QBrush, QColor, QPolygon
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene

from gui import Gui
from planet import Planet
from ruleset import Ruleset
from spaceinfo import SpaceInfo
from toolbar import ToolBar
from inspector import Inspector



class Design:
    MenuFontSize = 16


class Stars(QMainWindow, stars_ui.Ui_GUI):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This has been defined in 'stars_ui.py'



def main():
    app = QApplication(sys.argv)

    form = Stars()                 # Create the main user interface

#    SInfo = SpaceInfo( form )
#    PInfo = ToolBar(form)

#    SInfo.UpdateFriendlyDesigns( [ 'A', 'B', 'C' ] )


    Rules = Ruleset()
    Terra = Planet(Rules)

    PlanetInfo = Inspector(Terra)

    form.Inspector.setScene(PlanetInfo)
    Terra.Available.Ironium = 45000
    Terra.Available.Boranium = 2500
    Terra.Available.Germanium = 15000
    PlanetInfo.Update(Terra)

# PlanetInfo.sText[2].setVisible(False)

    form.show()                         # Show the form
    app.exec()                          # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
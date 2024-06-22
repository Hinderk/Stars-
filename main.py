
import sys
import stars_ui

from PyQt5 import QtWidgets, QtCore

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

from gui import Gui
from planet import Planet
from ruleset import Ruleset
from spaceinfo import SpaceInfo
from toolbar import ToolBar



class Design:
    MenuFontSize = 16


class Stars(QtWidgets.QMainWindow, stars_ui.Ui_GUI):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This has been defined in 'stars_ui.py'



def main():
    app = QtWidgets.QApplication(sys.argv)
    
# form = Gui(Design())                      # Define the main user interface
    
    form = Stars()

#    SInfo = SpaceInfo( form )
#    PInfo = ToolBar(form)

#    SInfo.UpdateFriendlyDesigns( [ 'A', 'B', 'C' ] )


    scene = QtWidgets.QGraphicsScene()
    scene.addText( 'Hallo Hinderk' )

##    form.Universe.setScene( scene )

    Rules = Ruleset()
    Terra = Planet( Rules )    


    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
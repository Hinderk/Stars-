
from PyQt4 import QtGui 
from planet import Planet
from ruleset import Ruleset

import sys
import os
import stars



class Stars(QtGui.QMainWindow, stars.Ui_GUI):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This has been defined in the file 'stars.py'


def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = Stars()                      # Define the form 'Stars'
    
    MyBox = QtGui.QSpinBox() 

    scene = QtGui.QGraphicsScene()
    scene.addText( 'Hallo Hinderk' )

    form.Universe.setScene( scene )
    form.PlanetInfo.addWidget( MyBox )


    Rules = Ruleset()
    Terra = Planet( Rules )    


    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function



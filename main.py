
from PyQt4 import QtGui, QtCore 
from planet import Planet
from ruleset import Ruleset
from spaceinfo import SpaceInfo

import sys
import os
import stars



class Stars(QtGui.QMainWindow, stars.Ui_GUI):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This has been defined in the file 'stars.py'


def main():
    app = QtGui.QApplication( sys.argv )   # A new instance of QApplication
    form = Stars()                         # Define the form 'Stars'
    
    Info = SpaceInfo( form )


    Info.UpdateFriendlyDesigns( [ 'A', 'B', 'C' ] )


    RadarRange = QtGui.QSpinBox()
    RadarRange.setSuffix( '%' )
    RadarRange.setRange( 10, 100 )
    RadarRange.setValue( 100 )
    RadarRange.setSingleStep( 10 )
    RadarRange.setAlignment( QtCore.Qt.AlignRight )
    form.PlanetInfo.addWidget( RadarRange )



    scene = QtGui.QGraphicsScene()
    scene.addText( 'Hallo Hinderk' )

    form.Universe.setScene( scene )

    


    Rules = Ruleset()
    Terra = Planet( Rules )    


    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function



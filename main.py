
import sys
# import stars_ui
import stars_rc

from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu

from gui import Gui
from planet import Planet
from ruleset import Ruleset
from inspector import Inspector
from design import Design



# class Stars(QMainWindow, stars_ui.Ui_GUI):
#
#    def __init__(self):
#        super(self.__class__, self).__init__()
#        self.setStyleSheet(Design().getStyle())
#        self.setupUi(self)  # This has been defined in 'stars_ui.py'



def main():
    app = QApplication(sys.argv)

# form = Stars()                 # Create the main user interface
    form = Gui()                 # Create the main user interface

#    SInfo.UpdateFriendlyDesigns(['A', 'B', 'C'])

#    FoeFilter = QMenu(form)
#    form.actionFoes.setMenu(FoeFilter)
#    FoeFilter.addAction('All Designs')
#    FoeFilter.addAction('Invert Filter')
#    FoeFilter.addAction('No Designs')
#    FoeFilter.addSeparator()

    Rules = Ruleset()
    Terra = Planet(Rules)

    PlanetInfo = Inspector(Terra)

    form.Inspector.setScene(PlanetInfo)
    Terra.Mined.Ironium = 45000
    Terra.Mined.Boranium = 2500
    Terra.Mined.Germanium = 15000
    PlanetInfo.Update(Terra)

# PlanetInfo.sText[2].setVisible(False)

    form.show()                         # Show the form
    app.exec()                          # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
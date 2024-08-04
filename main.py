
import sys
# import stars_ui
import stars_rc

from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu

from gui import Gui
from planet import Planet
from ruleset import Ruleset
from inspector import Inspector
from race import Race



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

    form.Buttons.UpdateFriendlyDesigns(['A - This is a very long name ...', 'B', 'C'])

    Rules = Ruleset()
    Terra = Planet(Rules)
    People = Race()

    PlanetInfo = Inspector(Terra, People)

    form.Inspector.setScene(PlanetInfo)
    Terra.Mined.Ironium = 45000
    Terra.Mined.Boranium = 2500
    Terra.Mined.Germanium = 15000
    Terra.Crust.Boranium = 55.0
    PlanetInfo.UpdateMinerals(Terra)

    Terra.Gravity = 1 / 8
    Terra.Temperature = -120.6
    Terra.Radioactivity = 80.75

    PlanetInfo.UpdateBiome(Terra)

# PlanetInfo.sText[2].setVisible(False)

    form.show()                         # Show the form
    app.exec()                          # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

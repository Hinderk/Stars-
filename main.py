
import sys
import stars_rc

from PyQt6.QtWidgets import QApplication

from gui import Gui
from planet import Planet
from ruleset import Ruleset
from race import Race



def main():
    app = QApplication(sys.argv)

    Rules = Ruleset()
    Terra = Planet(Rules)
    People = Race()

    form = Gui(People)                 # Create the main user interface

    form.Buttons.UpdateFriendlyDesigns(['A - This is a very long name ...', 'B', 'C'])

    Terra.Mined.Ironium = 45000
    Terra.Mined.Boranium = 2500
    Terra.Mined.Germanium = 15000
    Terra.Crust.Boranium = 55.0
    form.PlanetInfo.UpdateMinerals(Terra)

    Terra.Gravity = 1 / 8
    Terra.Temperature = -120.6
    Terra.Radioactivity = 80.75

    form.PlanetInfo.UpdateBiome(Terra)

    form.ChangeInspectorTitle("Proxima Centauri", True, True)
#    form.ChangeInspectorTitle("Tau Ceti", False, True)


    form.show()                         # Show the form
    app.exec()                          # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

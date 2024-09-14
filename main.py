
import sys
import stars_rc

from PyQt6.QtWidgets import QApplication

from gui import Gui
from planet import Planet
from ruleset import Ruleset
from race import Race
from fleet import Fleet
from ship import Ship



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

    Terra.TemperatureRate = 15.0
    Terra.GravityRate = 1 / 40
    Terra.RadioactivityRate = -7.0

    form.PlanetInfo.UpdateBiome(Terra)
    
    ship = Ship()
    ship.TotalWeight = 25
    ship.CargoSpace = 200
    ship.Settlers = 60
    ship.Boranium = 10
    ship.Germanium = 30
    ship.Ironium = 20
    ship.Fuel = 130
    ship.TotalFuel = 150
    ship.Name = "Explorer"
    ship.Type = "Scout"

    fleet = Fleet(ship)
    form.FleetInfo.UpdateCargo(fleet)

#    form.ChangeInspectorTitle("Proxima Centauri", True, True, True, True)
    form.ChangeInspectorTitle("Tau Ceti", True, False, True)

    form.ItemInfo.setCurrentIndex(1)

    form.Universe.planets[2].AddFriends(2020)
    form.Universe.planets[2].AddFriends(-2000)
    form.Universe.planets[2].AddOthers(2)
    form.Universe.planets[2].AddOthers(23)
    form.Universe.planets[2].AddFoes(-2000)
    form.Universe.planets[2].AddFoes(8)
    form.Universe.planets[2].AddFoes(18)

    form.Universe.planets[0].BuildStarbase()


    form.show()                         # Show the form
    app.exec()                          # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

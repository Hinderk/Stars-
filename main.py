
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

    Terra.Discovered = True
    Terra.Name = 'Tau Ceti'

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

    form.InspectPlanet(Terra)

    form.Map.Universe.planets[2].UpdateFriends(2020)
    form.Map.Universe.planets[2].UpdateFriends(-2000)
    form.Map.Universe.planets[2].UpdateOthers(2)
    form.Map.Universe.planets[2].UpdateOthers(23)
    form.Map.Universe.planets[2].UpdateFoes(-2000)
    form.Map.Universe.planets[2].UpdateFoes(8)
    form.Map.Universe.planets[2].UpdateFoes(18)

    form.Map.Universe.planets[0].BuildStarbase()
    form.Map.Universe.planets[0].Friendly = True
    form.Map.Universe.planets[0].Colonists = 24000

    form.Map.Universe.planets[5].Surface.Ironium = 20.0
    form.Map.Universe.planets[5].Surface.Boranium = 130.0
    form.Map.Universe.planets[5].Surface.Germanium = 100.0
    form.Map.Universe.planets[5].Crust.Ironium = 70.0
    form.Map.Universe.planets[5].Crust.Boranium = 30.0
    form.Map.Universe.planets[5].Crust.Germanium = 90.0
    form.Map.Universe.planets[5].Explore(2400)
    form.Map.Universe.planets[5].Colonists = 4000

#    form.Map.Universe.ShowCrustDiagram(form.Map.Universe.planets[5])
    form.Map.Universe.ShowSurfaceDiagram(form.Map.Universe.planets[5])

    form.Map.Universe.ComputeTurn()

    for p in form.Map.Universe.planets:
        p.ShowNormalView()


    form.show()                         # Show the form
    app.exec()                          # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

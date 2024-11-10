
import sys
import stars_rc

from PyQt6.QtWidgets import QApplication

from gui import Gui
from faction import Faction
from defines import Stance
from planet import Planet
from ruleset import Ruleset
from race import Race
from fleet import Fleet
from ship import Ship
from system import System
from system import SystemType as ST
from scanner import Model
from minefield import Minefield
from minefield import Model as M



def main():
    app = QApplication(sys.argv)

    Rules = Ruleset()
    People = Race()

    form = Gui(People, Rules)            # Create the main user interface

    form.Buttons.UpdateFriendlyDesigns(['A - This is a very long name ...', 'B', 'C'])

    Terra = Planet(Rules)
    Terra.Surface.Ironium = 45000
    Terra.Surface.Boranium = 2500
    Terra.Surface.Germanium = 15000
    Terra.Crust.Boranium = 55.0

    Terra.Gravity = 1 / 8
    Terra.Temperature = -120.6
    Terra.Radioactivity = 80.75

    Terra.TemperatureRate = 15.0
    Terra.GravityRate = 1 / 40
    Terra.RadioactivityRate = -7.0

    Terra.Explore(2390)

    Terra.Name = 'Tau Ceti'

    s = System()
    s.itemCount = 1
    s.itemType = Model.Rhino
    s.domain = ST.SCANNER

    ship = Ship()
    ship.EmptyWeight = 25
    ship.TotalWeight = 120
    ship.CargoSpace = 200
    ship.System.append(s)
    ship.Settlers = 60
    ship.Boranium = 10
    ship.Germanium = 30
    ship.Ironium = 20
    ship.Cloaking = 700
    ship.Fuel = 130
    ship.TotalFuel = 150
    ship.Name = "Explorer"
    ship.Type = "Scout"

    fleet_0 = Fleet(ship, 4)
    fleet_1 = Fleet(ship, 2)
    fleet_2 = Fleet(ship, 0)

    ship.Name = "Hauler"
    ship.Type = "Freighter"

    fleet_3 = Fleet(ship, 1)
    fleet_4 = Fleet(ship, 3)
    fleet_5 = Fleet(ship, 9)

    form.InspectPlanet(Terra)

    p = form.Map.Universe.planets[2]

    form.Map.Universe.RegisterFleet(fleet_0, p)
    form.Map.Universe.RegisterFleet(fleet_1, p)
    form.Map.Universe.RegisterFleet(fleet_2, p)
    form.Map.Universe.RegisterFleet(fleet_3, p)
    form.Map.Universe.RegisterFleet(fleet_4, p)
    form.Map.Universe.RegisterFleet(fleet_5, p)

    form.Map.Universe.planets[0].BuildStarbase()
    form.Map.Universe.planets[0].Relation = Stance.neutral
    form.Map.Universe.planets[0].Colonists = 24000

    form.Map.Universe.planets[5].Surface.Ironium = 20.0
    form.Map.Universe.planets[5].Surface.Boranium = 130.0
    form.Map.Universe.planets[5].Surface.Germanium = 100.0
    form.Map.Universe.planets[5].Crust.Ironium = 70.0
    form.Map.Universe.planets[5].Crust.Boranium = 30.0
    form.Map.Universe.planets[5].Crust.Germanium = 90.0
    form.Map.Universe.planets[5].Explore(2400)
    form.Map.Universe.planets[5].Colonists = 400000
    form.Map.Universe.planets[5].Relation = Stance.allied

    x = -30
    y = -30

    M0 = Minefield(form.Map.Universe, p.x, p.y, 2500, M.Normal, 0)
    M0.Detected = True
    form.Map.Universe.minefields.append(M0)
    M0 = Minefield(form.Map.Universe, p.x, p.y, 25000, M.SpeedTrap, 11)
    M0.Detected = True
    form.Map.Universe.minefields.append(M0)

    form.Map.Universe.minefields.append(Minefield(form.Map.Universe, x, y, 400, M.Normal, 4))
    form.Map.Universe.minefields.append(Minefield(form.Map.Universe, x, y, 1400, M.SpeedTrap, 4))
    form.Map.Universe.minefields.append(Minefield(form.Map.Universe, x + 10, y + 50, 2500, M.Normal, 0))
    form.Map.Universe.minefields.append(Minefield(form.Map.Universe, x + 50, y - 10, 16000, M.Normal, -1))

    form.Map.Universe.ComputeTurn()

    for p in form.Map.Universe.planets:
        p.BuildStarbase()
        p.Explore(2390)
        p.UpdatePlanetView()


    form.show()                         # Show the form
    app.exec()                          # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

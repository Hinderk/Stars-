
import sys
import stars_rc

from PyQt6.QtWidgets import QApplication

from gui import Gui
from hull import Hull
from design import Design
from defines import Stance
# from planet import Planet
from ruleset import Ruleset
from people import People
from fleet import Fleet
from ship import Ship
from system import System
from system import SystemType as ST
from scanner import Model
# from waypoint import Waypoint
from minefield import Minefield
from minefield import Model as M



def main():
    app = QApplication(sys.argv)

    rules = Ruleset()
    people = People()

    form = Gui(people, rules)            # Create the main user interface

    form.Buttons.UpdateMyDesigns(['Scout Mk 1', 'Small Freighter Mk 1', 'C'])

    s = System()
    s.itemCount = 1
    s.itemType = Model.Rhino
    s.domain = ST.SCANNER

    ship = Ship(Design(0, Hull.SCT))
    ship.EmptyWeight = 25
    ship.TotalWeight = 120
    ship.CargoSpace = 200
    ship.Design.System.append(s)
    ship.Settlers = 60
    ship.Boranium = 10
    ship.Germanium = 30
    ship.Ironium = 20
    ship.Cloaking = 700
    ship.Fuel = 130
    ship.TotalFuel = 150
    ship.MineLaying = 0
    ship.MineSweeping = 1
    ship.Name = "Explorer"

    fleet_0 = Fleet([ship], 4, people)
    fleet_1 = Fleet([ship], 2, people)
    fleet_2 = Fleet([ship], 0, people)

    freighter = Ship(Design(0, Hull.SFR))
    freighter.EmptyWeight = 20
    freighter.TotalWeight = 100
    freighter.CargoSpace = 500
    freighter.Settlers = 100
    freighter.Boranium = 20
    freighter.Germanium = 10
    freighter.Ironium = 30
    freighter.Cloaking = 0
    freighter.Fuel = 300
    freighter.TotalFuel = 1000
    freighter.MineLaying = 10
    freighter.MineSweeping = 0
    freighter.Name = "Hauler"

    fleet_3 = Fleet([ship, ship, ship], 1, people)
    fleet_4 = Fleet([ship], 3, people)
    fleet_5 = Fleet([ship], 9, people)
    fleet_6 = Fleet([freighter, freighter], 0, people)
    fleet_7 = Fleet([freighter, freighter, freighter], 9, people)
    fleet_8 = Fleet([ship, ship, ship, ship], 9, people)

    fleet_3.Idle = False
    fleet_7.Idle = False
    fleet_8.WarpSpeed = 10

    p = form.Map.Universe.planets[2]

    form.Map.Universe.RegisterFleet(fleet_0, p)
    form.Map.Universe.RegisterFleet(fleet_1, p)
    form.Map.Universe.RegisterFleet(fleet_2, p)
    form.Map.Universe.RegisterFleet(fleet_3, p)
    form.Map.Universe.RegisterFleet(fleet_4, p)
    form.Map.Universe.RegisterFleet(fleet_5, p)

    form.Map.Universe.RegisterFleet(fleet_6, 40, -50)
    form.Map.Universe.addWaypoint(fleet_6, 240, 420)
    form.Map.Universe.addWaypoint(fleet_6, 120, 550)
    form.Map.Universe.addWaypoint(fleet_6, 480, 500)
    form.Map.Universe.addWaypoint(fleet_6, 550, 300)

    form.Map.Universe.RegisterFleet(fleet_7, 40, -50)
    form.Map.Universe.addWaypoint(fleet_7, -20, 500)
    form.Map.Universe.addWaypoint(fleet_7, 180, 350)
    form.Map.Universe.addWaypoint(fleet_7, 280, 600)
    form.Map.Universe.addWaypoint(fleet_7, 500, 400)

    form.Map.Universe.RegisterFleet(fleet_8, 140, -150)
    form.Map.Universe.addWaypoint(fleet_8, -120, 600)
    form.Map.Universe.addWaypoint(fleet_8, 280, 450)
    form.Map.Universe.addWaypoint(fleet_8, 280, 600)
    form.Map.Universe.addWaypoint(fleet_8, 600, 600)
    form.Map.Universe.addWaypoint(fleet_8, 500, 550)
    form.Map.Universe.addWaypoint(fleet_8, 140, -150)
    form.Map.Universe.addWaypoint(fleet_8, -120, 600)

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

    M0 = Minefield(form.Map.Universe, p.x, p.y, 2500, M.Normal, 0, people)
    M0.Detected = True
    form.Map.Universe.minefields.append(M0)
    M0 = Minefield(form.Map.Universe, p.x, p.y, 25000, M.SpeedTrap, 11, people)
    M0.Detected = True
    form.Map.Universe.minefields.append(M0)

    form.Map.Universe.minefields.append(Minefield(form.Map.Universe, x, y, 400, M.Normal, 4, people))
    form.Map.Universe.minefields.append(Minefield(form.Map.Universe, x, y, 1400, M.SpeedTrap, 4, people))
    form.Map.Universe.minefields.append(Minefield(form.Map.Universe, x + 10, y + 50, 25000, M.Normal, 0, people))
    form.Map.Universe.minefields.append(Minefield(form.Map.Universe, x + 50, y - 10, 64000, M.Normal, -1, people))

    fleet_7.WarpSpeed = 10
    fleet_8.RepeatTasks(True)
    form.Map.Universe.ComputeTurn()

    for p in form.Map.Universe.planets:
        p.BuildStarbase()
        p.Explore(2390)
        p.UpdatePlanetView()


    form.show()                         # Show the form
    app.exec()                          # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

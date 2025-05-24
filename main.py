
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

    form.buttons.update_my_designs(['Scout Mk 1', 'Small Freighter Mk 1', 'C'])

    s = System()
    s.item_count = 1
    s.item_type = Model.RHINO
    s.domain = ST.SCANNER

    ship = Ship(Design(0, Hull.SCT))
    ship.empty_weight = 25
    ship.total_weight = 120
    ship.cargo_space = 200
    ship.design.system.append(s)
    ship.settlers = 60
    ship.boranium = 10
    ship.germanium = 30
    ship.ironium = 20
    ship.cloaking = 700
    ship.fuel = 130
    ship.total_fuel = 150
    ship.mine_laying = 0
    ship.mine_sweeping = 1
    ship.name = "Explorer"

    fleet_0 = Fleet([ship], 4, people)
    fleet_1 = Fleet([ship], 2, people)
    fleet_2 = Fleet([ship], 0, people)

    freighter = Ship(Design(0, Hull.SFR))
    freighter.empty_weight = 20
    freighter.total_weight = 100
    freighter.cargo_space = 500
    freighter.settlers = 100
    freighter.boranium = 20
    freighter.germanium = 10
    freighter.ironium = 30
    freighter.cloaking = 0
    freighter.fuel = 300
    freighter.total_fuel = 1000
    freighter.mine_laying = 10
    freighter.mine_sweeping = 0
    freighter.name = "Hauler"

    fleet_3 = Fleet([ship, ship, ship], 1, people)
    fleet_4 = Fleet([ship], 3, people)
    fleet_5 = Fleet([ship], 9, people)
    fleet_6 = Fleet([freighter, freighter], 0, people)
    fleet_7 = Fleet([freighter, ship, freighter], 9, people)
    fleet_8 = Fleet([ship, ship, freighter, freighter], 9, people)

    fleet_3.idle = False
    fleet_7.idle = False
    fleet_8.warp_speed = 10

    p = form.map.universe.planets[2]

    form.map.universe.register_fleet(fleet_0, p)
    form.map.universe.register_fleet(fleet_1, p)
    form.map.universe.register_fleet(fleet_2, p)
    form.map.universe.register_fleet(fleet_3, p)
    form.map.universe.register_fleet(fleet_4, p)
    form.map.universe.register_fleet(fleet_5, p)

    form.map.universe.register_fleet(fleet_6, 40, -50)
    fleet_6.add_waypoint(240, 420)
    fleet_6.add_waypoint(120, 550)
    fleet_6.add_waypoint(480, 500)
    fleet_6.add_waypoint(550, 300)

    form.map.universe.register_fleet(fleet_7, 40, -50)
    fleet_7.add_waypoint(-20, 500)
    fleet_7.add_waypoint(180, 350)
    fleet_7.add_waypoint(280, 600)
    fleet_7.add_waypoint(500, 400)

    form.map.universe.register_fleet(fleet_8, 140, -150)
    fleet_8.add_waypoint(-120, 600)
    fleet_8.add_waypoint(280, 450)
    fleet_8.add_waypoint(280, 600)
    fleet_8.add_waypoint(600, 600)
    fleet_8.add_waypoint(500, 550)
    fleet_8.add_waypoint(140, -150)
    fleet_8.add_waypoint(-120, 600)

    form.map.universe.planets[0].build_starbase()
    form.map.universe.planets[0].relation = Stance.NEUTRAL
    form.map.universe.planets[0].colonists = 24000

    form.map.universe.planets[5].surface.ironium = 20.0
    form.map.universe.planets[5].surface.boranium = 130.0
    form.map.universe.planets[5].surface.germanium = 100.0
    form.map.universe.planets[5].crust.ironium = 70.0
    form.map.universe.planets[5].crust.boranium = 30.0
    form.map.universe.planets[5].crust.germanium = 90.0
    form.map.universe.planets[5].explore(2400)
    form.map.universe.planets[5].colonists = 400000
    form.map.universe.planets[5].relation = Stance.ALLIED

    x = -30
    y = -30

    m0 = Minefield(form.map.universe, M.NORMAL, 0)
    m0.move_field(p.x, p.y)
    m0.update_stance(Stance.ALLIED)
    m0.resize_field(2500)
    m0.detected = True
    form.map.universe.minefields.append(m0)
    m0 = Minefield(form.map.universe, M.SPEED_TRAP, 11)
    m0.move_field(p.x, p.y)
    m0.update_stance(Stance.HOSTILE)
    m0.resize_field(25000)
    m0.detected = True
    form.map.universe.minefields.append(m0)

    m0 = Minefield(form.map.universe, M.NORMAL, 4)
    m0.move_field(x, y)
    m0.update_stance(Stance.NEUTRAL)
    m0.resize_field(400)
    form.map.universe.minefields.append(m0)

    m0 = Minefield(form.map.universe, M.SPEED_TRAP, 4)
    m0.move_field(x, y)
    m0.update_stance(Stance.NEUTRAL)
    m0.resize_field(1400)
    form.map.universe.minefields.append(m0)

    m0 = Minefield(form.map.universe, M.NORMAL, 0)
    m0.move_field(x + 10, y + 50)
    m0.update_stance(Stance.ALLIED)
    m0.resize_field(25000)
    form.map.universe.minefields.append(m0)

    m0 = Minefield(form.map.universe, M.NORMAL, -1)
    m0.move_field(x + 50, y - 10)
    m0.update_stance(Stance.FRIENDLY)
    m0.resize_field(64000)
    form.map.universe.minefields.append(m0)

    fleet_7.warp_speed = 2
    fleet_8.repeat_tasks(True)
    form.map.universe.compute_turn()

    for p in form.map.universe.planets:
        p.build_starbase()
        p.explore(2390)
        p.update_planet_view(2395)


    form.show()                         # Show the form
    app.exec()                          # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

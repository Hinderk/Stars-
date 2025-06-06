
""" This module implements the solar systems of the Stars universe """

import copy
import math

from minerals import Minerals
from planetdata import PlanetData
from defines import Stance
from diagram import Diagram


# This class represents the solar systems of the Stars universe each of
# which is represented by just one of its planets and named after its sun.

class Planet:

    """ This class represents the solar systems of the Stars universe each of
        which is represented by just one of its planets and named after its sun. """

    def __init__(self, rules, home_world=False):    # TODO: remove the home_world flag

        self.name = rules._find_name()                     # The name of the solar system
        self.x = 0                                         # The coordinates of the solar system
        self.y = 0                                         # on the star map [ly]
        self.faction = None                                # The planet is uninhabited by default.

        self.radioactivity = rules.random(0, 100, 50)      # These parameters may be modified via
        self.gravity = 64.0 ** rules.random(-0.5, 0.5, 0)  # terraforming technologies and influence
        self.temperature = rules.random(-200, 200, 0)      # population density & growth

        self.radioactivity_rate = 0.0                      # TODO: Create a viable terraforming
        self.gravity_rate = 0.0                            # model to compute these rates.
        self.temperature_rate = 0.0

        self.delta_radioactivity = 1e8                     # These values depend on the faction the
        self.delta_gravity = 1e8                           # player is controlling himself. They
        self.delta_temperature = 1e8                       # require an initial setup. Unit: [%]
        self.center_radioactivity = 0.5                    # The values used by default correspond
        self.center_gravity = 0.0                          # to a species that is completely immune
        self.center_temperature = 0.0                      # to adverse environmental factors.

        self.orbit = None                                  # The following class members will be
        self.starbase = None                               # used to render planets on the star
        self.neutral = None                                # map in different ways depending on
        self.foes = None                                   # player choices & the game state ...
        self.friends = None
        self.attackers = None
        self.center = None
        self.core = None
        self.body = None
        self.ships = None
        self.others = None
        self.flag = None
        self.population = None

        self.scanner = None
        self.diagram = Diagram()

        self.orbit_visible = False
        self.starbase_visible = False
        self.foes_visible = False
        self.friends_visible = False
        self.others_visible = False
        self.core_visible = False
        self.body_visible = False
        self.flag_visible = False

        self.fleets_in_orbit = []
        self.mine_fields = []

        self.total_friends = 0
        self.idle_friends = 0
        self.total_foes = 0
        self.total_others = 0
        self.total_orbit = 0
        self.colonists = 0

        self.show_idle_only = False
        self.strength_visible = False

        self.space_station = False

        # TODO: Compute these class members in a dedicated 'colonize' procedure ...

        self.discovered = home_world                     # Obviously, the home world is settled
        self.ship_tracking = home_world                  # from the first turn of the game ...
        self.home_world = home_world

        self.crust = Minerals(rules)                     # Create a random amount of minerals
        self.explored = PlanetData()                     # inside the planet's crust and - for
        if home_world:                                   # the home world - on its surface
            self.surface = Minerals(rules, 0.1)
            self.relation = Stance.ALLIED
            self.explore(rules.first_year())             # Start with the first game year ...
        else:
            self.surface = Minerals()
            self.relation = Stance.NEUTRAL


    def explore(self, year):
        """ Record the current state of the planet for future reports """
        self.explored.radioactivity = self.radioactivity
        self.explored.gravity = self.gravity
        self.explored.temperature = self.temperature
        self.explored.radioactivity_rate = self.radioactivity_rate
        self.explored.gravity_rate = self.gravity_rate
        self.explored.temperature_rate = self.temperature_rate
        self.explored.colonists = self.colonists
        self.explored.relation = self.relation
        self.explored.space_station = self.space_station
        self.explored.crust = copy.deepcopy(self.crust)
        self.explored.surface = copy.deepcopy(self.surface)
        self.last_visit = year
        self.discovered = True


    def value(self):
        """ Compute a planet value based on the habitability of its biome """
        gravity = math.log(self.gravity) / math.log(64.0)
        delta_r = abs(self.radioactivity / 100.0 - self.center_radioactivity)
        delta_g = abs(gravity - self.center_gravity)
        delta_t = abs(self.temperature / 400.0 - self.center_temperature)
        res = (max(min(self.delta_radioactivity - delta_r, 0.0), -0.15)
               + max(min(self.delta_gravity - delta_g, 0.0), -0.15)
               + max(min(self.delta_temperature - delta_t, 0.0), -0.15))
        if res < 0.0:
            return res
        q_r = delta_r / self.delta_radioactivity
        q_g = delta_g / self.delta_gravity
        q_t = delta_t / self.delta_temperature
        q = ((1 - q_r) * (1 - q_r) + (1 - q_g) * (1 - q_g) + (1 - q_t) * (1 - q_t)) / 3
        res = (1.5 - max(q_r, 0.5)) * (1.5 - max(q_g, 0.5)) * (1.5 - max(q_t, 0.5))
        return res * math.sqrt(q)


    def update_ship_tracking(self, year):
        """ Check if a planet has been explored by nearby allied ships,
            an orbiting space station or colonists on its surface """
        if self.relation == Stance.ALLIED:
            if self.space_station or self.colonists > 0:
                self.ship_tracking = True
        if self.total_friends > 0:
            for f in self.fleets_in_orbit:
                if f.friend_or_foe == Stance.ALLIED:
                    self.ship_tracking = True
                    break
        if self.ship_tracking:
            self.explore(year)


    def enter_orbit(self, fleet):
        """ Update the planet's data if a fleet enters it's orbit """
        if fleet.ship_counter > 0:
            if fleet.friend_or_foe == Stance.ALLIED:
                self.update_friends(fleet.ship_counter)
            elif fleet.friend_or_foe == Stance.HOSTILE:
                self.update_foes(fleet.ship_counter)
            else:
                self.update_others(fleet.ship_counter)
        fleet.orbiting = self


    def clear_orbit(self):
        """ Remove all fleets from a planet's orbit """
        self.total_friends = 0
        self.total_foes = 0
        self.total_others = 0
        self.friends_visible = False
        self.foes_visible = False
        self.others_visible = False


    def update_friends(self, count=0):
        """ Update a planet's state if allied fleets have entered its orbit """
        self.total_friends += count
        self.total_orbit += count
        if self.total_orbit < 1:
            self.total_orbit = 0
        if self.total_friends > 0:
            self.friends_visible = True
            self.orbit_visible = True
            w0 = self.ships.boundingRect().width()
            x0 = self.ships.x()
            self.ships.setText(str(self.total_friends))
            w = self.ships.boundingRect().width()
            self.ships.setX(x0 - w + w0)
        else:
            self.total_friends = 0
            self.friends_visible = False


    def update_foes(self, count=0):
        """ Update a planet's state if hostile fleets have entered its orbit """
        self.total_foes += count
        self.total_orbit += count
        if self.total_orbit < 1:
            self.total_orbit = 0
        if self.total_foes > 0:
            self.foes_visible |= self.ship_tracking
            w0 = self.attackers.boundingRect().width()
            x0 = self.attackers.x()
            self.attackers.setText(str(self.total_foes))
            w = self.attackers.boundingRect().width()
            self.attackers.setX(x0 - w + w0)
        else:
            self.total_foes = 0
            self.foes_visible = False


    def update_others(self, count=0):
        """ Update a planet's state if neutral fleets have entered its orbit """
        self.total_others += count
        self.total_orbit += count
        if self.total_orbit < 1:
            self.total_orbit = 0
        if self.total_others > 0:
            self.others_visible |= self.ship_tracking
            self.others.setText(str(self.total_others))
        else:
            self.total_others = 0
            self.others_visible = False


    def build_starbase(self):
        """ Update the planet's state to reflect the construction of a starbase """
        if not self.space_station:
            self.total_orbit += 1
            self.space_station = True


    def destroy_starbase(self):
        """ Update the planet's state to reflect the destruction of its starbase """
        if self.space_station:
            self.total_orbit -= 1
            self.space_station = False
        if self.total_orbit < 1:
            self.total_orbit = 0
            self.orbit_visible = False
        self.starbase_visible = False


    def update_planet_view(self, year):
        """ Update the planet's state to reflect changes in the composition
            of the orbiting objects such as starbases or fleets """
        self.update_ship_tracking(year)
        self.update_foes()
        self.update_others()
        self.update_friends()
        if self.space_station:
            self.starbase_visible = self.ship_tracking
        if self.total_orbit < 1:
            self.orbit_visible = False
        else:
            self.orbit_visible |= self.ship_tracking
        self.core_visible = self.ship_tracking or self.discovered
        if self.colonists > 0:
            self.body_visible = self.relation == Stance.ALLIED
            self.flag_visible = self.core_visible
        else:
            self.flag_visible = False


    def show_default_view(self, show_numbers):
        """ Present the planet's default view either with or without fleet strength numbers """
        self.center.setVisible(True)
        self.core.setVisible(self.core_visible)
        self.body.setVisible(False)
        self.orbit.setVisible(self.orbit_visible)
        self.starbase.setVisible(self.starbase_visible)
        self.neutral.setVisible(self.others_visible)
        self.foes.setVisible(self.foes_visible)
        self.friends.setVisible(self.friends_visible)
        self.ships.setVisible(self.friends_visible and show_numbers)
        self.attackers.setVisible(self.foes_visible and show_numbers)
        self.others.setVisible(self.others_visible and show_numbers)
        self.population.setVisible(False)
        self.flag.setVisible(False)


    def show_minimal_view(self):
        """ Present a minimalistic view of the planet """
        self.center.setVisible(True)
        self.core.setVisible(False)
        self.body.setVisible(False)
        self.orbit.setVisible(False)
        self.starbase.setVisible(False)
        self.neutral.setVisible(False)
        self.foes.setVisible(False)
        self.friends.setVisible(False)
        self.ships.setVisible(False)
        self.attackers.setVisible(False)
        self.others.setVisible(False)
        self.population.setVisible(False)
        self.flag.setVisible(False)


    def show_percentage_view(self):
        """ Present a view indicating the planet's value / habitability """
        self.center.setVisible(False)
        self.core.setVisible(False)
        self.body.setVisible(self.core_visible)
        self.orbit.setVisible(False)
        self.starbase.setVisible(False)
        self.neutral.setVisible(False)
        self.foes.setVisible(False)
        self.friends.setVisible(False)
        self.ships.setVisible(False)
        self.attackers.setVisible(False)
        self.others.setVisible(False)
        self.population.setVisible(False)
        self.flag.setVisible(self.flag_visible)


    def show_population_view(self):
        """ Present a view indicating the size of the planet's population """
        self.center.setVisible(not self.body_visible)
        self.core.setVisible(False)
        self.body.setVisible(self.body_visible)
        self.orbit.setVisible(False)
        self.starbase.setVisible(False)
        self.neutral.setVisible(False)
        self.foes.setVisible(False)
        self.friends.setVisible(False)
        self.ships.setVisible(False)
        self.attackers.setVisible(False)
        self.others.setVisible(False)
        self.population.setVisible(self.body_visible)
        self.flag.setVisible(False)

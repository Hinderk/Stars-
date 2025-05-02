
""" This file implements the handling of fleets of starships """

import math

from PyQt6.QtGui import QPen

from universe import Universe
from design import Design
from defines import Stance, Task
from perks import Perks
from colours import Pen, Brush
from system import SystemType
from guiprop import GuiProps as GP

import ruleset


def get_delta(dx, dy):

    """ Scale the ships's velocity to indicate warp 10 """

    length = math.sqrt(dx * dx + dy * dy)
    if length > 0:
        scale = GP.xscale * 100.0 / length   # Warp 10
        return scale * dx, scale * dy
    return 0, 0



class Fleet:

    """ This class manages hetereogeneous collection of ships """

    counter = {}

    def __init__(self, ships, f_id, people):
        faction = people.get_faction(f_id)
        self.xc = 0
        self.yc = 0
        self.ship_list = []
        self.ship_counter = 0
        self.warp_speed = 0
        self.heading = 0.0
        self.first_waypoint = None
        self.active_waypoint = []
        self.last_waypoint = None
        self.next_waypoint = None
        self.mine_fields = []
        self.repeat_schedule = False
        self.idle = True
        self.task = Task.IDLE
        self.discovered = True           # TODO: Depends on scanners!
        self.orbiting = None
        self.total_weight = 0
        self.total_fuel = 0
        self.fuel = 0
        self.germanium = 0
        self.boranium = 0
        self.ironium = 0
        self.settlers = 0
        self.cargo_space = 0
        self.mine_laying = 0
        self.mine_sweeping = 0
        self.max_range = 0
        self.pen_range = 0
        self.steal_cargo = faction.cargo_robber
        self.name = None
        self.index = None
        self.picture = None
        self.friend_or_foe = people.get_stance(ruleset.F_ID0, f_id)  # TODO: just a test
        self.ship_counter = len(ships)
        for s in ships:
            self.add_ship(s)
        self.banner_index = faction.banner_index
        self.scanner = None
        self.moving_fleet = None
        self.resting_fleet = None
        self.ship_count = None
        self.course = None
        self.cloaking_factor = self.compute_cloaking()
        self.set_fleet_name_and_index()
        if self.name in Fleet.counter:
            Fleet.counter[self.name] += 1
        else:
            Fleet.counter[self.name] = 1
        self.id = Fleet.counter[self.name]


    def add_ship(self, ship):
        """ Add a new ship to the fleet & update fleet properties """
        self.ship_list.append(ship)
        self.total_weight += ship.total_weight
        self.total_fuel += ship.total_fuel
        self.fuel += ship.fuel
        self.germanium += ship.germanium
        self.boranium += ship.boranium
        self.ironium += ship.ironium
        self.settlers += ship.settlers
        self.cargo_space += ship.cargo_space
        self.mine_laying += ship.mine_laying
        self.mine_sweeping += ship.mine_sweeping
#        self.update_scanner_data(ship)   # TODO: Update this information when advancing game time


    def update_scanner_data(self, ship):
        """ Recalculate scanner & penetration ranges, check for pickpocket scanners """
        maxrange = 0
        penrange = 0
        for s in ship.design.system:
            if s.domain == SystemType.SCANNER:
                mr = s.item_type.value[0]
                pr = s.item_type.value[1]
                if s.item_type.value[15] == Perks.ROB:
                    self.steal_cargo = True
                maxrange += s.item_count * mr * mr * mr * mr
                penrange += s.item_count * pr * pr * pr * pr
        if maxrange > 0:
            maxrange = math.sqrt(math.sqrt(maxrange))
            self.max_range = max(maxrange, self.max_range)
        if penrange > 0:
            penrange = math.sqrt(math.sqrt(penrange))
            self.pen_range = max(penrange, self.pen_range)


    def compute_cloaking(self):
        """ Compute cloaking effectiveness of the entire fleet """
        total = 0
        cloak = 0
        for s in self.ship_list:
            if s.cloaking > 0:
                cloak += s.cloaking * s.empty_weight
            total += s.total_weight
        return ruleset.cloaking_ratio(cloak, total)


    def set_fleet_name_and_index(self):
        """ Select a fleet's name & icon based on the highest battle rating """
        designs = [s.design.index for s in self.ship_list]
        val = -1
        for d in set(designs):
            n = designs.count(d)
            sd = Design.get_design(d)
            r = sd.compute_battle_rating()
            if val < n * r:
                self.picture = sd.get_picture_index()
                self.name = sd.get_design_name()
                val = n * r


    def apply_foe_filter(self, select):
        """ Update the ship counter of hostile fleets to account for new filter settings """
        self.ship_counter = 0
        for s in self.ship_list:
            if select[s.design.hull.value[2].name]:
                self.ship_counter += 1


    def apply_my_filter(self, idle, select):
        """ Update the fleet's ship counter to account for new filter settings """
        self.ship_counter = 0
        if self.idle or not idle:
            for s in self.ship_list:
                if select[s.design.name]:
                    self.ship_counter += 1


    def get_colours(self, selected=False):
        """ Retrieve pens & brushes for fleets on the star map """
        if selected:
            if self.friend_or_foe == Stance.ALLIED:
                return (QPen(Pen.blue_h), Brush.blue)
            if self.friend_or_foe == Stance.HOSTILE:
                return (QPen(Pen.red_l), Brush.red_d)
            return (QPen(Pen.green), Brush.green)
        if self.friend_or_foe == Stance.ALLIED:
            return (QPen(Pen.blue_l), Brush.blue)
        if self.friend_or_foe == Stance.HOSTILE:
            return (QPen(Pen.red), Brush.red_d)
        return (QPen(Pen.green), Brush.green)


    def update_ship_count(self):
        """ Show the fleet's current ship count on the star map """
        self.ship_count.setText(str(self.ship_counter))
        h = self.ship_count.boundingRect().height() - 2
        xs = GP.xscale * self.xc
        ys = GP.xscale * self.yc
        if abs(self.heading) > 0.5 * math.pi:
            xs += GP.f_radius + GP.f_dist
        else:
            w = self.ship_count.boundingRect().width()
            xs -= GP.f_radius + GP.f_dist + w
        self.ship_count.setPos(xs, ys - h / 2)


    def show_course(self, show):
        """ Display the flight path of a fleet on the star map """
        if self.course:
            self.course.setVisible(show)


    def colour_course(self, selected=False):
        """ Colour the flight path of a fleet on the star map """
        pen, brush = self.get_colours(selected)
        z = 1
        if selected:
            z = 2
        if self.moving_fleet:
            self.moving_fleet.setPen(pen)
            self.moving_fleet.setBrush(brush)
            self.moving_fleet.setZValue(z)
        self.resting_fleet.setPen(pen)
        self.resting_fleet.setBrush(brush)
        if self.course:
            pen.setWidthF(Universe.current_path_width)
            self.course.setPen(pen)
            self.course.setZValue(z)
        self.resting_fleet.setZValue(z)


    def update_course(self, wp, planets):
        """ Insert a planet into the flight path instead of a waypoint if both a very close """
        wp.planet = None
        for p in planets:
            d = (p.x - wp.xo) * (p.x - wp.xo) + (p.y - wp.yo) * (p.y - wp.yo)
            if d < GP.p_snap:
                wp.xo = p.x
                wp.yo = p.y
                wp.planet = p
                return


    def clear_waypoints(self):
        """ Erase the entire flight path """
        wp = self.first_waypoint
        while wp:
            wo = wp
            wp = wp.next
            del wo
        self.first_waypoint = None
        self.next_waypoint = None
        self.last_waypoint = None


    def repeat_tasks(self, repeat):
        """ Check flight paths for closed loops to support task repetition """
        state = False
        wp = self.first_waypoint
        while wp:
            if wp.next and wp.at(self.last_waypoint):
                state = repeat
            wp.retain = state      # TODO: Does this flag really do the trick?
            wp = wp.next
        self.repeat_schedule = state
        return state


    def update_schedule(self):
        """ Update the check for closed loops after waypoints have been modified """
        return self.repeat_tasks(self.repeat_schedule) # TODO: 'retain' flags have not been cleared!


    def delete_waypoint(self, n0):
        """ Remove the waypoint with index n0 from the flight path """
        wp = None
        wo = self.first_waypoint
        wn = wo.next
        n = 1
        while wn and n < n0:
            n += 1
            wp = wo
            wo = wn
            wn = wn.next
        if wp:
            wp.next = wn
        else:
            self.first_waypoint = wn
        if wn:
            wn.previous = wp
        else:
            self.last_waypoint = wp
        if wo == self.next_waypoint:
            self.next_waypoint = wn
        del wo
        return self.find_next_waypoint()


    def find_next_waypoint(self):  # FIX ME!!  -- Check for planets?
        """ Update the first & the next waypoint of the flight path """
        wn = self.next_waypoint
        if wn and self.xc == wn.xo and self.yc == wn.yo:
            self.warp_speed = wn.warp
            self.task = wn.task
            self.next_waypoint = wn.next
        wp = self.first_waypoint
        if wp and wp is not self.next_waypoint:
            if not wp.retain:
                wo = wp
                wp = wp.next
                del wo
        if wp:
            wp.previous = None
        else:
            self.last_waypoint = None
        self.first_waypoint = wp
        return self.next_waypoint

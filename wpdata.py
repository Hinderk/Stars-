
""" This module implements an inspector panel for fleet waypoints """

from PyQt6.QtCore import QRectF

import brush as BRUSH
import pen as PEN
from dataviewer import DataViewer

import guiprop as GP



class WPData(DataViewer):

    """ This class is used to display information about fleet waypoints """

    def __init__(self):
        super().__init__()
        self.freight = []
        self._add_static_text()
        self._add_info_text()
        self._init_cargo()
        self.add_logos()


    def _add_static_text(self):
        """ Add the static text elements to the inspector panel for fleets """
        ship_count = self.scene.addSimpleText("Ship count:", GP.INFO_FONT)
        xpos = self.x_offset
        ypos = 0
        ship_count.moveBy(xpos, ypos)
        fuel_load = self.scene.addSimpleText("Fuel:", GP.INFO_FONT)
        ypos += self.y_delta + 5
        fuel_load.moveBy(xpos, ypos)
        cargo = self.scene.addSimpleText("Cargo:", GP.INFO_FONT)
        ypos += self.y_delta
        cargo.moveBy(xpos, ypos)
        fleet_mass = self.scene.addSimpleText("Fleet Mass:", GP.INFO_FONT)
        ypos += self.y_delta + 5
        fleet_mass.moveBy(xpos, ypos)
        waypoint = self.scene.addSimpleText("Next Waypoint:", GP.INFO_FONT)
        ypos += self.y_delta
        waypoint.moveBy(xpos, ypos)
        task = self.scene.addSimpleText("Waypoint Task:", GP.INFO_FONT)
        ypos += self.y_delta
        task.moveBy(xpos, ypos)
        speed = self.scene.addSimpleText("Warp Speed:", GP.INFO_FONT)
        ypos += self.y_delta
        speed.moveBy(xpos, ypos)
        self.sweeps = self.scene.addSimpleText("", GP.INFO_FONT)
        ypos += self.y_delta
        self.sweeps.moveBy(xpos, ypos)


    def _add_info_text(self):
        """ Create the variable text elements of the inspector panel """
        self.ship_count = self.scene.addSimpleText('', GP.INFO_FONT)
        xpos = self.x_offset + self.data_offset
        ypos = 0
        self.ship_count.moveBy(xpos, ypos)
        ypos += 2 * self.y_delta + 10
        self.mass = self.scene.addSimpleText('', GP.INFO_FONT)
        ypos += self.y_delta
        self.mass.moveBy(xpos, ypos)
        self.waypoint = self.scene.addSimpleText('', GP.INFO_FONT)
        ypos += self.y_delta
        self.waypoint.moveBy(xpos, ypos)
        self.task = self.scene.addSimpleText('', GP.INFO_FONT)
        ypos += self.y_delta
        self.task.moveBy(xpos, ypos)
        self.speed = self.scene.addSimpleText('', GP.INFO_FONT)
        ypos += self.y_delta
        self.speed.moveBy(xpos, ypos)


    def _init_cargo(self):
        """ Create the bar diagrams for cargo loadout & fuel reserves """
        brush = [BRUSH.WHITE, BRUSH.YELLOW, BRUSH.GREEN, BRUSH.BLUE_F, BRUSH.RED]
        xp = self.x_offset + self.x_text
        yp = self.y_delta + 5
        box = QRectF(xp, yp, self.x_width, self.y_size)
        self.scene.addRect(box, PEN.BLACK_2, BRUSH.GREY)
        box = QRectF(xp, yp, self.x_width / 2, self.y_size)
        self.fuel = self.scene.addRect(box, PEN.BLACK_2, brush[4])
        self.fuel_weight = self.scene.addSimpleText("", GP.CARGO_FONT)
        yp += self.y_delta + 2
        box = QRectF(xp, yp, self.x_width, self.y_size)
        self.scene.addRect(box, PEN.BLACK_2, BRUSH.GREY)
        for n in (0, 1, 2, 3):
            box = QRectF(xp, yp, self.x_width, self.y_size)
            self.freight.append(self.scene.addRect(box, PEN.BLACK_2, brush[n]))
        self.cargo = self.scene.addSimpleText("", GP.CARGO_FONT)


    def _compute_cargo_fractions(self, fleet):
        """ Prepare against drawing a bar diagram for the fleet's cargo """
        fractions = []
        fractions.append(fleet.ironium / fleet.cargo_space)
        fractions.append(fleet.boranium / fleet.cargo_space)
        fractions.append(fleet.germanium / fleet.cargo_space)
        fractions.append(fleet.settlers / fleet.cargo_space)
        for n in (1, 2, 3):
            fractions[n] += fractions[n - 1]
        return fractions


    def update_fleet_data(self, fleet):
        """ Update the inspector panel for fleets """
        self.update_fleet_banner(fleet)
        fraction = self._compute_cargo_fractions(fleet)
        xp = self.x_offset + self.x_text
        yp = self.y_delta + 5
        self.fuel.setRect(xp, yp, self.x_width * fleet.fuel / fleet.total_fuel, self.y_size)
        self.fuel_weight.setText(str(fleet.fuel) + " of " + str(fleet.total_fuel) + "mg")
        x = self.x_width - self.fuel_weight.boundingRect().width()
        self.fuel_weight.setPos(xp + x / 2, yp + 2)
        total = fleet.germanium + fleet.boranium + fleet.ironium + fleet.settlers
        self.mass.setText(str(total + fleet.total_weight))
        text = " of " + str(fleet.cargo_space) + "kT"
        yp += self.y_delta + 2
        for n in (0, 1, 2, 3):
            self.freight[3 - n].setRect(xp, yp, self.x_width * fraction[n], self.y_size)
        self.cargo.setText(str(total) + text)
        x = self.x_width - self.cargo.boundingRect().width()
        self.cargo.setPos(xp + x / 2, yp + 2)
        if fleet.mine_sweeping > 0:
            text = 'This fleet can destroy up to ' + str(fleet.mine_sweeping)
            self.sweeps.setText(text + ' mines per year.')
        else:
            self.sweeps.setText('')
        if fleet.next_waypoint:
            if fleet.next_waypoint.planet:
                self.waypoint.setText(fleet.next_waypoint.planet.name)
            else:
                x = str(fleet.next_waypoint.xo)
                y = str(fleet.next_waypoint.yo)
                self.waypoint.setText('(' + x + ',' + y + ')')
            self.task.setText(fleet.next_waypoint.task.value)
        else:
            self.waypoint.setText('None')
        if fleet.warp_speed > 0:
            self.speed.setText(str(fleet.warp_speed))
        else:
            self.speed.setText('Stopped')
            self.task.setText(fleet.task.value)
        self.ship_count.setText(str(len(fleet.ship_list)))


    def update_flight_path(self, fleet):
        """ Update the fleet inspector panel if flight path has changed """
        wp = fleet.next_waypoint
        if wp:
            if wp.planet:
                self.waypoint.setText(wp.planet.name)
            else:
                self.waypoint.setText('(' + str(wp.xo) + ',' + str(wp.yo) + ')')
        if fleet.warp_speed > 0:
            self.speed.setText(str(fleet.warp_speed))
        else:
            self.speed.setText('Stopped')


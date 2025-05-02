
""" This module implements the data viewer for fleets of star ships """

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from guiprop import GuiProps as GP
from colours import Brush, Pen
from defines import Stance



class Fleetdata(QGraphicsView):

    """ This class is used to display information about fleets of star ships """

    x_offset = 150
    y_offset = 110
    y_delta = 35
    y_size = 27
    x_width = 550
    x_text = 100
    icon_width = 120
    data_offset = 180
    flag_offset = 20
    top_offset = 10


    def __init__(self):
        super().__init__()
        self.freight = []
        self.hull_logo = {}
        self.scene = QGraphicsScene(self)
        self.backdrop = None
        self._add_static_text()
        self._add_info_text()
        self._init_cargo()
        self._add_logos()
        self.setScene(self.scene)
        self.setMaximumHeight(325)
        self.fleet_picture = 0
        self.current_banner = 0


    def _add_static_text(self):
        """ Add the static text elements to the inspector panel for fleets """
        ship_count = self.scene.addSimpleText("Ship count:", GP.info_font)
        xpos = self.x_offset
        ypos = 0
        ship_count.moveBy(xpos, ypos)
        fuel_load = self.scene.addSimpleText("Fuel:", GP.info_font)
        ypos += self.y_delta + 5
        fuel_load.moveBy(xpos, ypos)
        cargo = self.scene.addSimpleText("Cargo:", GP.info_font)
        ypos += self.y_delta
        cargo.moveBy(xpos, ypos)
        fleet_mass = self.scene.addSimpleText("Fleet Mass:", GP.info_font)
        ypos += self.y_delta + 5
        fleet_mass.moveBy(xpos, ypos)
        waypoint = self.scene.addSimpleText("Next Waypoint:", GP.info_font)
        ypos += self.y_delta
        waypoint.moveBy(xpos, ypos)
        task = self.scene.addSimpleText("Waypoint Task:", GP.info_font)
        ypos += self.y_delta
        task.moveBy(xpos, ypos)
        speed = self.scene.addSimpleText("Warp Speed:", GP.info_font)
        ypos += self.y_delta
        speed.moveBy(xpos, ypos)
#    self.Mines = self.Scene.addSimpleText("", GP.infoFont)
#    ypos += self.yDelta
#    self.Mines.moveBy(xpos, ypos)
        self.sweeps = self.scene.addSimpleText("", GP.info_font)
        ypos += self.y_delta
        self.sweeps.moveBy(xpos, ypos)


    def _add_info_text(self):
        """ Create the variable text elements of the inspector panel """
        self.ship_count = self.scene.addSimpleText('', GP.info_font)
        xpos = self.x_offset + self.data_offset
        ypos = 0
        self.ship_count.moveBy(xpos, ypos)
        ypos += 2 * self.y_delta + 10
        self.mass = self.scene.addSimpleText('', GP.info_font)
        ypos += self.y_delta
        self.mass.moveBy(xpos, ypos)
        self.waypoint = self.scene.addSimpleText('', GP.info_font)
        ypos += self.y_delta
        self.waypoint.moveBy(xpos, ypos)
        self.task = self.scene.addSimpleText('', GP.info_font)
        ypos += self.y_delta
        self.task.moveBy(xpos, ypos)
        self.speed = self.scene.addSimpleText('', GP.info_font)
        ypos += self.y_delta
        self.speed.moveBy(xpos, ypos)


    def _init_cargo(self):
        """ Create the bar diagrams for cargo loadout & fuel reserves """
        brush = [Brush.white, Brush.yellow, Brush.green, Brush.blue_f, Brush.red]
        xp = self.x_offset + self.x_text
        yp = self.y_delta + 5
        box = QRectF(xp, yp, self.x_width, self.y_size)
        self.scene.addRect(box, Pen.black_2, Brush.grey)
        box = QRectF(xp, yp, self.x_width / 2, self.y_size)
        self.fuel = self.scene.addRect(box, Pen.black_2, brush[4])
        self.fuel_weight = self.scene.addSimpleText("", GP.cargo_font)
        yp += self.y_delta + 2
        box = QRectF(xp, yp, self.x_width, self.y_size)
        self.scene.addRect(box, Pen.black_2, Brush.grey)
        for n in (0, 1, 2, 3):
            box = QRectF(xp, yp, self.x_width, self.y_size)
            self.freight.append(self.scene.addRect(box, Pen.black_2, brush[n]))
        self.cargo = self.scene.addSimpleText("", GP.cargo_font)


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


    def _update_fleet_banner(self, fleet):
        """ Display the proper faction banner & fleet symbol """
        if fleet.friend_or_foe == Stance.ALLIED:
            self.backdrop.setBrush(Brush.blue_p)
        elif fleet.friend_or_foe == Stance.FRIENDLY:
            self.backdrop.setBrush(Brush.green_p)
        elif fleet.friend_or_foe == Stance.NEUTRAL:
            self.backdrop.setBrush(Brush.yellow_p)
        else:
            self.backdrop.setBrush(Brush.red_p)
        self.faction_banner[self.current_banner].setVisible(False)
        self.hull_logo[self.fleet_picture].setVisible(False)
        self.current_banner = fleet.banner_index
        self.fleet_picture = fleet.picture
        self.faction_banner[self.current_banner].setVisible(True)
        self.hull_logo[self.fleet_picture].setVisible(True)


    def update_fleet_data(self, fleet):
        """ Update the inspector panel for fleets """
        self._update_fleet_banner(fleet)
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
#    if fleet.MineLaying > 0:
#      text = 'This fleet can lay up to ' + str(fleet.MineLaying)
#      self.Mines.setText(text + ' mines per year.')
#    else:
#      self.Mines.setText('')
        if fleet.mine_sweeping > 0:
            text = 'This fleet can destroy up to ' + str(fleet.mine_sweeping)
            self.sweeps.setText(text + ' mines per year.')
        else:
            self.sweeps.setText('')
        if fleet.next_waypoint:
            if fleet.next_waypoint.planet:
                self.waypoint.setText(fleet.next_waypoint.planet.Name)
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


    def update_waypoint_info(self, speed, wp):
        """ Update the fleet inspector panel if a waypoint has changed """
        if wp:
            if wp.planet:
                self.waypoint.setText(wp.planet.Name)
            else:
                self.waypoint.setText('(' + str(wp.xo) + ',' + str(wp.yo) + ')')
        if speed > 0:
            self.speed.setText(str(speed))
        else:
            self.speed.setText('Stopped')


    def _add_logos(self):
        """ Prepare the various ship icons for the fleet inspector panel """
        self.hull_logo = []
        yp = self.top_offset
        rectangle = QRectF(1, yp + 1, self.icon_width - 2, self.icon_width - 2)
        self.backdrop = self.scene.addRect(rectangle)
        for e1 in "abcdefghi":
            for e2 in "123456":
                resource = "Design/Images/Graphics/ship-" + e1 + e2 + ".svg"
                image = QGraphicsSvgItem(resource)
                width = image.boundingRect().width()
                if width > 0:
                    image.setScale(self.icon_width / width)
                    image.setPos(0, yp)
                    image.setVisible(False)
                    self.scene.addItem(image)
                    self.hull_logo.append(image)
        yp += self.flag_offset + self.icon_width
        self.faction_banner = []
        for faction in "ABCDEFGHIJKLMNOPQRST":
            resource = ":/Factions/Faction-" + faction
            banner = QGraphicsSvgItem(resource)
            width = banner.boundingRect().width()
            banner.setScale(0.5 * self.icon_width / width)
            banner.setPos(0.25 * self.icon_width, yp)
            banner.setVisible(False)
            self.scene.addItem(banner)
            self.faction_banner.append(banner)
        self.scene.addRect(QRectF(800, 315, 5, 5), Pen.noshow)

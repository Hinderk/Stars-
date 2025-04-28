
""" This module implements the user interactions with the star map """

import math

from PyQt6.QtGui import QPolygonF, QPen
from PyQt6.QtGui import QTransform
from PyQt6.QtGui import QPainterPath
from PyQt6.QtCore import QPointF, QLineF, QRectF, Qt
from PyQt6.QtWidgets import QMenu
from PyQt6.QtWidgets import QGraphicsScene

from PyQt6.QtCore import pyqtSignal as QSignal

from guidesign import GuiDesign, GuiStyle
from scanner import Scanner
from ruleset import Ruleset
from planet import Planet
from colours import Pen
from colours import Brush
from defines import Stance, Task
from waypoint import Waypoint
from guiprop import GuiProps as GP


_arrow = QPolygonF()
_arrow.append( QPointF(GP.h_vector - GP.dh_vector, 0))
_arrow.append( QPointF(-GP.dh_vector, -GP.w_vector))
_arrow.append(QPointF(0, 0))
_arrow.append(QPointF(-GP.dh_vector, GP.w_vector))

_flag = QPolygonF()
_flag.append( QPointF(0, 0))
_flag.append(QPointF(0, - GP.flag_height - GP.flag_width))
_flag.append(QPointF(GP.flag_width + GP.flag_stem, -GP.flag_height - GP.flag_width))
_flag.append(QPointF(GP.flag_width + GP.flag_stem, -GP.flag_height))
_flag.append(QPointF(GP.flag_stem, -GP.flag_height))
_flag.append(QPointF(GP.flag_stem, 0))


def _setup_mine_filter():
    """ Create a mine filter / show all mine fields """
    fields = {}
    fields[Stance.allied] = True
    fields[Stance.friendly] = True
    fields[Stance.neutral] = True
    fields[Stance.hostile] = True
    return fields


class Universe(QGraphicsScene):

    """ This class is responsible for rendering the star map """

    select_planet = QSignal(Planet)
    update_planet = QSignal(Planet)
    update_filter = QSignal(dict)
    update_route = QSignal(int, object)
    select_fleet = QSignal(object, int, list, list)
    select_field = QSignal(object, int, list, list)

    current_path_width = GP.fp_width[100]

    def __init__(self, rules):
        super().__init__()

        self.planets = []
        self.fleets = []
        self.minefields = []
        self.debris = []

        self.selected_planet = None
        self.selected_fleet = None
        self.selected_waypoint = None
        self.waypoint_index = 0
        self.waypoint_offset = 0
        self.fleet_index = 0
        self.fleet_offset = 0
        self.selected_fleets = []
        self.default_view = False
        self.show_fleet_strength = False
        self.show_idle_fleets_only = False
        self.show_fleet_movements = False
        self.foe_filter_enabled = False
        self.friend_filter_enabled = False
        self.active_foe_filter = None
        self.active_friend_filter = None
        self.fields_visible = False
        self.movement_approved = False
        self.waypoint_selected = False
        self.names_visible = False

        self.show_field = _setup_mine_filter()
        self.population_ceiling = Ruleset.get_population_ceiling()

        self.pointer = None
        self.select = None
        self.wpselect = None

        self._create_indicator()
        self._create_planets(rules)
        self._colonize_planets()

        self.setBackgroundBrush(Brush.black)


    def _colonize_planets(self):
        """ Populate the planets with NPC factions """


    def focusOutEvent(self, _):
        """ Event handler: Prevent waypoint relocation if the game looses focus """
        self.movement_approved = False


    def keyPressEvent(self, key_press):
        """ Event handler: Process mouse interactions with the star map """
        key = key_press.key()
        if key == Qt.Key.Key_Shift:
            self.movement_approved = True
        elif key == Qt.Key.Key_Delete:
            if self.waypoint_selected:
                wp = self.selected_fleet.DeleteWaypoint(self.selected_waypoint[1])
                if wp:
                    dx = wp.xo - self.selected_fleet.xc
                    dy = wp.yo - self.selected_fleet.yc
                    self.selected_fleet.Heading = math.atan2(dy, dx)
                    self.selected_fleet.UpdateSchedule()
                else:
                    self.selected_fleet.warp_speed = 0
                    self.removeItem(self.selected_fleet.MovingFleet)
                    self.selected_fleet.MovingFleet = None
                self.plot_course(self.selected_fleet)
                self.selected_fleet.colour_course(True)
                self.waypoint_selected = False
                self.wpselect.setVisible(False)



    def keyReleaseEvent(self, key_press):
        key = key_press.key()
        if key == Qt.Key.Key_Shift:
            self.movement_approved = False


    def contextMenuEvent(self, mouse_click):
        select = QMenu()
        select.setStyleSheet(GuiDesign.get_style(GuiStyle.STARMAP))
        n = 0
        if self.context[0]:
            p = self.context[0]
            a = select.addAction(p.Name)
            a.setData((0, 0))
            n = 1
            if p.fleets_in_orbit:
                select.addSeparator()
                n = 0
                for f in p.fleets_in_orbit:
                    a = select.addAction(f.name + ' #' + str(f.id))
                    a.setData((1, n))
                    n += 1
            if p.mine_fields:
                select.addSeparator()
                n = 0
                for m in p.mine_fields:
                    a = select.addAction(m.model.value + ' Mine Field #' + str(m.id))
                    a.setData((2, n))
                    n += 1
        elif self.context[2]:
            for f in self.context[2]:
                a = select.addAction(f.name + ' #' + str(f.id))
                a.setData((3, n))
                n += 1
            fields = self.context[2][0].MineFields
            if fields:
                select.addSeparator()
                n = 0
                for m in fields:
                    a = select.addAction(m.model.value + ' Mine Field #' + str(m.id))
                    a.setData((4, n))
                    n += 1
        elif self.context[1]:
            for m in self.context[1]:
                a = select.addAction(m.model.value + ' Mine Field #' + str(m.id))
                a.setData((5, n))
                n += 1
        if self.context[3]:
            if n > 0:
                select.addSeparator()
            n = 0
            for w in self.context[3]:
                name = w[0].Name + ' #' + str(w[0].id)
                a = select.addAction(name + ' - WP ' + str(w[2]))
                a.setData((6, n))
                n += 1
        selected = select.exec(mouse_click.screenPos())
        if selected:
            itemtype, item = selected.data()
            if itemtype == 0:
                self.highlight_planet(self.context[0])
            elif itemtype == 1:
                p = self.context[0]
                self.highlight_planet(p)
                self.select_fleet.emit(p, item, p.fleets_in_orbit, p.mine_fields)
            elif itemtype == 2:
                p = self.context[0]
                self.highlight_planet(p)
                self.select_field.emit(p, item, p.mine_fields, [])
            elif itemtype == 3:
                self.highlight_fleet(item)
            elif itemtype == 4:
                self.fleet_offset = 0
                self.highlight_fleet()
                self.select_field.emit(None, item, fields, self.context[2])
            elif itemtype == 5:
                self.highlight_minefield(item)
            elif itemtype == 6:
                self.highlight_waypoint(item)


    def mouseReleaseEvent(self, _):
        """ Event handler: Cancel waypoint selection by releasing the mouse """
        self.waypoint_selected = False


    def mousePressEvent(self, mouse_click):
        p0 = mouse_click.scenePos()
        self.waypoint_selected = False
        xo = round(0.5 + p0.x() / GP.xscale)
        yo = round(0.5 + p0.y() / GP.xscale)
        self.context = self.identify_context(xo, yo)
        if mouse_click.buttons() == Qt.MouseButton.LeftButton:
            if self.context[1]:
                self.waypoint_offset = 0
                self.fleet_offset = 0
                self.highlight_minefield(0)
            elif self.context[0]:
                self.waypoint_offset = 0
                self.fleet_offset = 0
                self.highlight_planet(self.context[0])
            elif self.context[2]:
                self.waypoint_offset = 0
                self.highlight_fleet()
            elif self.context[3]:
                self.highlight_waypoint()


    def mouseMoveEvent(self, event):
        if self.waypoint_selected and self.movement_approved:
            w0 = self.selected_waypoint[0]
            f0 = self.selected_fleet
            p0 = event.scenePos()
            w0.xo = round(0.5 + p0.x() / GP.xscale)
            w0.yo = round(0.5 + p0.y() / GP.xscale)
            f0.update_course(w0, self.planets)
            p0 = QPointF(GP.xscale * w0.xo, GP.xscale * w0.yo)
            if f0.next_waypoint == w0:
                f0.Heading = math.atan2(w0.yo - f0.yc, w0.xo - f0.xc)
                f0.update_ship_count()
                self.update_route.emit(f0.warp_speed, w0)
            else:
                self.update_route.emit(f0.warp_speed, None)
            self.plot_course(f0)
            f0.colour_course(True)
            self.wpselect.setPos(p0)


    def identify_context(self, xo, yo):
        dist = 1e20
        po = None
        for p in self.planets:
            d = (p.x - xo) * (p.x - xo) + (p.y - yo) * (p.y - yo)
            if d < dist:
                po = p
                dist = d
        f_list = []
        w_list = []
        for f in self.fleets:
            if f.discovered and f.ship_counter > 0 and not f.orbiting:
                d = (f.xc - xo) * (f.xc - xo) + (f.yc - yo) * (f.yc - yo)
                if d < dist:
                    dist = d
                    f_list = [f]
                    w_list = []
                    po = None
                elif d == dist:
                    f_list.append(f)
                if f.friend_or_foe == Stance.allied:
                    if self.show_fleet_movements or f == self.selected_fleet:
                        n = 0
                        selectable = False
                        wp = f.first_waypoint
                        while wp:
                            n += 1
                            if wp == f.next_waypoint:
                                selectable = True
                            if selectable or wp.retain:
                                d = (wp.xo - xo) * (wp.xo - xo) + (wp.yo - yo) * (wp.yo - yo)
                                if d < dist:
                                    po = None
                                    w_list = [(f, wp, n)]
                                    f_list = []
                                    f.active_waypoint = [wp]
                                    dist = d
                                elif d == dist:
                                    f.active_waypoint.append(wp)
                                    w_list.append((f, wp, n))
                            wp = wp.next
        m_list = []
        for m in self.minefields:
            if m.detected:
                if self.fields_visible:
                    d = (m.x - xo) * (m.x - xo) + (m.y - yo) * (m.y - yo)
                    if d < dist:
                        m_list = [m]
                        w_list = []
                        f_list = []
                        po = None
                        dist = d
                    elif d == dist:
                        m_list.append(m)
        return po, m_list, f_list, w_list, xo, yo


    def _create_indicator(self):
        """ Create the object designator for the starmap """
        triangle = QPolygonF()
        triangle.append(QPointF(0, 0))
        triangle.append(QPointF(GP.pointer_size / 2, GP.pointer_size * math.sqrt(3.0) / 2))
        triangle.append(QPointF(-GP.pointer_size / 2, GP.pointer_size * math.sqrt(3.0) / 2))
        self.pointer = self.addPolygon(triangle, Pen.white_08, Brush.yellow)
        self.pointer.setZValue(8)
        w = GP.fp_radius
        self.select = self.addEllipse(-w, -w, w + w, w + w, Pen.white_08, Brush.yellow)
        self.select.setZValue(-2)
        w = GP.wp_radius
        pen = QPen(Pen.yellow)
        pen.setWidthF(GP.wp_width)
        self.wpselect = self.addEllipse(-w, -w, w + w, w + w, pen)
        self.wpselect.setZValue(-2)


    def highlight_planet(self, p):
        self.select.setVisible(False)
        self.wpselect.setVisible(False)
        if self.selected_planet:
            self.selected_planet.label.setPen(Pen.white_l)
            self.selected_planet.label.setBrush(Brush.white_l)
        if self.selected_fleet:
            self.selected_fleet.colour_course(False)
            self.selected_fleet.show_course(self.show_fleet_movements)
        self.selected_waypoint = None
        self.selected_fleet = None
        self.selected_fleets = []
        if self.names_visible:
            p.label.setPen(Pen.white)
            p.label.setBrush(Brush.white)
            self.pointer.setVisible(False)
        else:
            xp = GP.xscale * p.x
            yp = GP.xscale * p.y + GP.p_radius + GP.dy_pointer
            self.pointer.setPos(xp, yp)
            self.pointer.setVisible(True)
        self.selected_planet = p
        self.select_planet.emit(p)


    def highlight_fleet(self, index=-1):
        self.wpselect.setVisible(False)
        self.pointer.setVisible(False)
        if self.selected_planet:
            self.selected_planet.label.setPen(Pen.white_l)
            self.selected_planet.label.setBrush(Brush.white_l)
        self.selected_planet = None
        self.selected_waypoint = None
        if index < 0:
            index = (self.fleet_index + self.fleet_offset) % len(self.context[2])
        f0 = self.context[2][index]
        self.select.setPos(GP.xscale * f0.xc, GP.xscale * f0.yc)
        self.select.setVisible(True)
        self.selected_fleet = f0
        self.fleet_index = index
        self.fleet_offset = 1
        self.selected_fleets = self.context[2]
        self.select_fleet.emit(None, index, self.context[2], f0.mine_fields)


    def highlight_minefield(self, index):
        self.select.setVisible(False)
        if self.selected_planet:
            self.selected_planet.label.setPen(Pen.white_l)
            self.selected_planet.label.setBrush(Brush.white_l)
        self.selected_waypoint = None
        self.selected_fleet = None
        self.selected_fleets = []
        self.selected_planet = None
        xp = GP.xscale * self.context[1][0].x
        yp = GP.xscale * self.context[1][0].y + GP.dy_pointer
        self.pointer.setPos(xp, yp)
        self.pointer.setVisible(True)
        self.select_field.emit(None, index, self.context[1], [])


    def highlight_waypoint(self, index=-1):
        self.pointer.setVisible(False)
        if self.selected_planet:
            self.selected_planet.label.setPen(Pen.white_l)
            self.selected_planet.label.setBrush(Brush.white_l)
        self.selected_planet = None
        if self.movement_approved:
            index = self.waypoint_index
        elif index < 0:
            index = (self.waypoint_index + self.waypoint_offset) % len(self.context[3])
        f0, w0, n0 = self.context[3][index]
        self.wpselect.setPos(GP.xscale * w0.xo, GP.xscale * w0.yo)
        self.select.setPos(GP.xscale * f0.xc, GP.xscale * f0.yc)
        self.wpselect.setVisible(True)
        self.select.setVisible(True)
        self.selected_waypoint = (w0, n0)
        self.selected_fleet = f0
        self.waypoint_index = index
        self.fleet_index = index
        self.waypoint_offset = 1
        self.selected_fleets = [w[0] for w in self.context[3]]
        self.waypoint_selected = True
        self.select_fleet.emit(None, index, self.selected_fleets, [])


    def segment_path(self, path, xa, ya, xb, yb):
        dx = GP.xscale * (xb - xa)
        dy = GP.xscale * (yb - ya)
        d2 = float(dx * dx + dy * dy)
        if d2 > 0.0:
            sval = [(0.0, -1), (1.0, 1)]
            r2 = GP.fleet_halo * GP.fleet_halo / d2
            for f in self.fleets:
                if f.discovered and f.ship_counter > 0 and not f.orbiting:
                    fx = GP.xscale * (xa - f.xc)
                    fy = GP.xscale * (ya - f.yc)
                    p = (fx * dx + fy * dy) / d2
                    q2 = (fx * fx + fy * fy) / d2
                    s2 = r2 + p * p - q2
                    if s2 > 0.0:
                        s = math.sqrt(s2)
                        sm = -s - p
                        sp = s - p
                        if 0.0 < sp or sm < 1.0:
                            sval.append((sm, 1))
                            sval.append((sp, -1))
            sval.sort(key=lambda p: p[0])
            s = 1
            x = GP.xscale * xa
            y = GP.xscale * ya
            for (so, ds) in sval:
                s += ds
                if s < 1:
                    path.moveTo(x + so * dx, y + so * dy)
                elif s < 2 and ds > 0:
                    path.lineTo(x + so * dx, y + so * dy)


    def show_mines(self, switch, fof):
        """ Display or hide all mine fields of certain factions """
        self.show_field[fof] = switch
        if self.fields_visible:
            self.show_fields(True)
            self.update_filter.emit(self.show_field)


    def show_fields(self, show):
        """ Enable or disable the display of mine fields """
        if show:
            for field in self.minefields:
                switch = self.show_field[field.fof] and field.detected
                field.area.setVisible(switch)
                field.center.setVisible(switch)
        else:
            for field in self.minefields:
                field.area.setVisible(False)
                field.center.setVisible(False)
        self.fields_visible = show


    def show_movements(self, show):
        """ Enable or disable the display of flight paths """
        for f in self.fleets:
            if f.ship_counter > 0 and f.discovered and not f.orbiting:
                f.show_course(show)
        if self.selected_fleet:
            self.selected_fleet.show_course(self.selected_fleet.ship_counter > 0)
        self.show_fleet_movements = show


    def show_scanner_ranges(self, switch):
        """ Enable or disable the display of scanner ranges """
        for p in self.planets:
            if p.scanner:
                p.scanner.show_ranges(switch)
        for f in self.fleets:
            if f.scanner:
                f.scanner.show_ranges(switch)


    def show_planet_names(self, switch):
        """ Enable or disable the display of planet names / the indicator """
        self.names_visible = switch
        if self.selected_planet:
            if switch:
                self.selected_planet.label.setPen(Pen.white)
                self.selected_planet.label.setBrush(Brush.white)
                self.pointer.setVisible(False)
            else:
                xp = GP.xscale * self.selected_planet.x
                yp = GP.xscale * self.selected_planet.y + GP.p_radius + GP.dy_pointer
                self.pointer.setPos(xp, yp)
                self.pointer.setVisible(True)
        for p in self.planets:
            p.label.setVisible(switch)


    def show_crust_diagrams(self):
        """ Display a diagram indicating the size of mineral deposits """
        for p in self.planets:
            p.show_default_view(self.show_fleet_strength)
            p.diagram.show_crust_diagram(p)
        self.update()
        self.default_view = True


    def show_surface_diagrams(self):
        """ Display a diagram indicating the amount of surface minerals """
        for p in self.planets:
            p.show_default_view(self.show_fleet_strength)
            p.diagram.show_surface_diagram(p)
        self.update()
        self.default_view = True


    def remove_diagrams(self):
        """ Hide any diagrams indicating the mineral wealth of a planet """
        for p in self.planets:
            p.diagram.show(False)
        self.update()


    def show_default_view(self):
        """ Restore the default view of the star map """
        for p in self.planets:
            p.show_default_view(self.show_fleet_strength)
        self.update()
        self.default_view = True


    def show_minimal_view(self):
        """ Display a minimalistic view of the star map """
        for p in self.planets:
            p.show_minimal_view()
        self.update()
        self.default_view = False


    def show_population_view(self):
        for p in self.planets:
            p.show_population_view()
            if p.body_visible:
                q = math.sqrt(p.colonists / self.population_ceiling)
                if q > 1.0:
                    q = 1.0
                rnew = GP.p_radius * (1 + q) / 2 + q * GP.d_radius
                x = GP.xscale * p.x - rnew
                y = GP.xscale * p.y - rnew
                w = 2 * rnew
                p.body.setRect(QRectF(x, y, w, w))
                p.body.setPen(Pen.brown)
                p.body.setBrush(Brush.brown)
                p.population.setText(str(p.colonists))
        self.update()
        self.default_view = False


    def scale_radar_ranges(self, factor):
        f = factor / 100.0
        for p in self.planets:
            if p.scanner:
                p.scanner.scale_ranges(f)
        for fleet in self.fleets:
            if fleet.scanner:
                fleet.scanner.scale_ranges(f)
        self.update()


    def show_percentage_view(self):
        for p in self.planets:
            p.show_percentage_view()
            if p.core_visible:
                q = p.value()
                if q < 0.33:
                    p.body.setPen(Pen.red)
                    p.body.setBrush(Brush.red)
                    q = 3 * q
                elif q < 0.66:
                    p.body.setPen(Pen.yellow)
                    p.body.setBrush(Brush.yellow)
                    q = 3 * (q - 0.33)
                else:
                    p.body.setPen(Pen.green)
                    p.body.setBrush(Brush.green)
                    q = 3 * (q - 0.66)
                rnew = GP.p_radius * (1 + q) / 2 + q * GP.d_radius
                x = GP.xscale * p.x - rnew
                y = GP.xscale * p.y - rnew
                w = 2 * rnew
                p.body.setRect(QRectF(x, y, w, w))
            if p.flag_visible:
                if p.relation == Stance.allied:
                    p.flag.setPen(Pen.blue_l)
                    p.flag.setBrush(Brush.blue)
                elif p.relation == Stance.friendly:
                    p.flag.setPen(Pen.green_d)
                    p.flag.setBrush(Brush.green)
                elif p.relation == Stance.neutral:
                    p.flag.setPen(Pen.yellow_d)
                    p.flag.setBrush(Brush.yellow)
                else:
                    p.flag.setPen(Pen.red_l)
                    p.flag.setBrush(Brush.red)
        self.update()
        self.default_view = False


    def _create_planets(self, rules):
        """ Populate the star map with randomly placed solar systems / planets """
        x = []
        y = []
        n = Ruleset.planet_count()
        while n > 0:
            n -= 1
            p = self.create_planet(rules, n < 1)
            x.append(p.x)
            y.append(p.y)
            self.planets.append(p)
        xmin = GP.xscale * min(x) - GP.map_frame
        xmax = GP.xscale * max(x) + GP.map_frame
        ymin = GP.xscale * min(y) - GP.map_frame
        ymax = GP.xscale * max(y) + GP.map_frame
        self.setSceneRect(xmin, ymin, xmax - xmin, ymax - ymin)
        model = rules.first_scanner()
        if model:
            p.scanner = self._create_scanner(p.x, p.y, model.value[0], model.value[1])


    def _create_scanner(self, xo, yo, rmax, rpen=0):
        """ Create the visual elements indicating the scanning range of a fleet or planet """
        s = Scanner(xo, yo, rmax, rpen)
        x = GP.xscale * xo
        y = GP.xscale * yo
        if rmax > 0:
            r = rmax * GP.xscale
            box = QRectF(x - r, y - r, r + r, r + r)
            s.detection = self.addEllipse(box, Pen.red_s, Brush.red_s)
            s.detection.setZValue(-10)
            s.detection.setVisible(False)
        if rpen > 0:
            r = rpen * GP.xscale
            box = QRectF(x - r, y - r, r + r, r + r)
            s.penetration = self.addEllipse(box, Pen.yellow_s, Brush.yellow_s)
            s.penetration.setZValue(-8)
            s.penetration.setVisible(False)
        return s


    def _remove_scanner(self, fleet):
        """ Remove a fleet scanner from the star map """
        if fleet.scanner:
            if fleet.scanner.detection:
                self.removeItem(fleet.scanner.detection)
            if fleet.scanner.penetration:
                self.removeItem(fleet.penetration)
            del fleet.scanner
            fleet.scanner = None


    def register_fleet(self, fleet, p, y=None):
        w = GP.f_radius + GP.f_radius
        fleet.resting_fleet = self.addEllipse(-GP.f_radius, -GP.f_radius, w, w)
        fleet.resting_fleet.setVisible(False)
        if y:
            xo = p
            yo = y
        else:
            xo = p.x
            yo = p.y
        if fleet.friend_or_foe == Stance.allied and fleet.max_range > 0:
            fleet.scanner = self._create_scanner(xo, yo, fleet.max_range, fleet.pen_range)
        fleet.ship_count = self.create_orbit_label(0, 0)
        fleet.xc = xo
        fleet.yc = yo
        self.fleets.append(fleet)


    def _unregister_fleet(self, fleet):
        """ Remove a fleet & all its visual elements from the star map """
        self.removeItem(fleet.ShipCount)
        self.removeItem(fleet.RestingFleet)
        if fleet.MovingFleet:
            self.removeItem(fleet.MovingFleet)
        if fleet.Course:
            self.removeItem(fleet.Course)
        if fleet.Orbiting:
            fleet.Orbiting.fleets_in_orbit.remove(fleet)
        self._remove_scanner(fleet)
        self.fleets.remove(fleet)
        fleet.ClearWaypoints()


    def set_waypoint_mode(self, event):
        self.waypoint_mode = event


    def add_waypoint(self, fleet, x, y, index=0):   # FIX ME!
        wa = Waypoint(x, y)
        if fleet.first_waypoint:
            w0 = fleet.active_waypoint[index]
            wa.warp = w0.warp
            if w0.next:
                wa.task = Task.MOVE
                w1 = w0.next
                w1.previous = wa
                wa.next = w1
                if w1 == fleet.next_waypoint:
                    fleet.next_waypoint = wa
            else:
                fleet.last_waypoint = wa
            w0.next = wa
            wa.previous = w0
        else:
            fleet.first_waypoint = wa
            fleet.last_waypoint = wa
            fleet.next_waypoint = wa
        fleet.active_waypoint = [wa]


    def create_orbit_label(self, x, y):
        label = self.addSimpleText("", GP.map_font)
        label.setPen(Pen.white_l)
        label.setBrush(Brush.white_l)
        label.setPos(x, y)
        label.setVisible(False)
        label.setZValue(4)
        return label


    def create_diagram(self, diagram, x, y, w):
        line = QLineF(0, -GP.scale_length, 0, 0)
        line.translate(x + w / 2 - GP.scale_length / 2, y - GP.dy_label)
        diagram.v_axis = self.addLine(line, Pen.white_08)
        d = GP.scale_length / 13
        box = QRectF(d, 0, 3 * d, -GP.scale_length)
        diagram.blue_box = self.addRect(box, Pen.blue, Brush.blue)
        diagram.blue_box.setPos(x + w / 2 - GP.scale_length / 2, y - GP.dy_label)
        box = QRectF(5 * d, 0, 3 * d, -GP.scale_length)
        diagram.green_box = self.addRect(box, Pen.green, Brush.green)
        diagram.green_box.setPos(x + w / 2 - GP.scale_length / 2, y - GP.dy_label)
        box = QRectF(9 * d, 0, 3 * d, -GP.scale_length)
        diagram.yellow_box = self.addRect(box, Pen.yellow, Brush.yellow)
        diagram.yellow_box.setPos(x + w / 2 - GP.scale_length / 2, y - GP.dy_label)
        line = QLineF(GP.scale_length, 0, 0, 0)
        line.translate(x + w / 2 - GP.scale_length / 2, y - GP.dy_label)
        diagram.h_axis = self.addLine(line, Pen.white_08)
        diagram.scale_length = GP.scale_length
        diagram.show(False)


    def create_planet(self, rules, homeworld):
        """ Render a planet onto the star map but keep it invisible """
        p = Planet(rules, homeworld)
        [p.x, p.y] = rules.find_position()
        w = GP.p_radius
        xo = p.x * GP.xscale - w
        yo = p.y * GP.xscale - w
        x = xo + w / 2
        y = yo + w / 2
        p.center = self.addEllipse(x, y, w, w, Pen.white, Brush.white)
        w += GP.p_radius
        p.core = self.addEllipse(xo, yo, w, w, Pen.brown, Brush.brown)
        p.core.setVisible(False)
        x = xo - GP.d_radius
        y = yo - GP.d_radius
        w += 2 * GP.d_radius
        c = 2 * GP.o_radius
        w0 = w / math.sqrt(8.0) + 0.5
        xm = x + w / 2 - w0 - GP.o_radius
        xp = x + w / 2 + w0 - GP.o_radius
        ym = y + w / 2 - w0 - GP.o_radius
        yp = y + w / 2 + w0 - GP.o_radius
        p.body = self.addEllipse(x, y, w, w)
        p.orbit = self.addEllipse(x, y, w, w, Pen.white_2)
        p.orbit.setVisible(False)
        p.starbase = self.addEllipse(xp, ym, c, c, Pen.yellow, Brush.yellow)
        p.neutral = self.addEllipse(xp, yp, c, c, Pen.neutral, Brush.neutral)
        p.friends = self.addEllipse(xm, yp, c, c, Pen.blue, Brush.blue)
        p.foes = self.addEllipse(xm, ym, c, c, Pen.red, Brush.red)
        p.starbase.setVisible(False)
        p.neutral.setVisible(False)
        p.foes.setVisible(False)
        p.friends.setVisible(False)
        p.label = self.addSimpleText(p.name, GP.map_font)
        p.label.setPen(Pen.white_l)
        p.label.setBrush(Brush.white_l)
        p.label.setVisible(False)
        w0 = p.label.boundingRect().width()
        p.label.setPos(x - w0 / 2 + w / 2, y + w + GP.dy_label)
        p.ships = self.create_orbit_label(x - c / 2, y + w - GP.fontsize)
        p.attackers = self.create_orbit_label(x - c / 2, y - GP.fontsize / 2)
        p.others = self.create_orbit_label(x + w + c / 2, y + w - GP.fontsize)
        p.population = self.create_orbit_label(x + w + c / 2, y - GP.fontsize / 2)
        p.flag = self.addPolygon(_flag)
        p.flag.setPos(x + w / 2 - GP.flag_stem / 2, y + w / 2)
        p.flag.setVisible(False)
        self.create_diagram(p.diagram, x, y, w)
        return p


    def show_ship_count(self, event):
        if self.default_view:
            for p in self.planets:
                p.show_default_view(event)
        for f in self.fleets:
            if f.discovered and not f.orbiting:
                f.ship_count.setVisible(event and f.ship_counter > 0)
        self.update()
        self.show_fleet_strength = event


    def apply_fleet_filter(self):
        for f in self.fleets:
            if f.discovered and not f.orbiting:
                if f.ship_counter > 0:
                    if f.warp_speed > 0:
                        f.moving_fleet.setVisible(True)
                    else:
                        f.resting_fleet.setVisible(True)
                    f.ship_count.setVisible(self.show_fleet_strength)
                    f.show_course(self.show_fleet_movements)
                else:
                    if f.warp_speed > 0:
                        f.moving_fleet.setVisible(False)
                    f.ship_count.setVisible(False)
                    f.show_course(False)
                    f.resting_fleet.setVisible(False)
        if self.selected_fleets:
            if self.selected_fleet.ship_counter == 0:
                self.fleet_index += 1
                self.selected_fleet.colour_course(False)
            total = 0
            for f in self.selected_fleets:
                total += f.ship_counter
            if total > 0:
                if self.selected_waypoint:
                    self.wpselect.setVisible(True)
                self.select.setVisible(True)
            else:
                self.wpselect.setVisible(False)
                self.select.setVisible(False)
            self.select_fleet.emit(self.selected_planet, self.fleet_index, self.selected_fleets, self.selected_fleet.mine_fields)


    def filter_foes(self, enabled, select):
        self.foe_filter_enabled = enabled
        if select:
            self.active_foe_filter = select
        if self.show_idle_fleets_only:
            for f in self.fleets:
                if f.friend_or_foe != Stance.allied:
                    f.ship_counter = 0
        elif enabled:
            for f in self.fleets:
                if f.friend_or_foe != Stance.allied:
                    f.apply_foe_filter(select)
                    f.update_ship_count()
        else:
            for f in self.fleets:
                if f.friend_or_foe != Stance.allied:
                    f.ship_counter = len(f.ship_list)
                    f.update_ship_count()
        for p in self.planets:
            total_others = 0
            total_foes = 0
            for f in p.fleets_in_orbit:
                if f.friend_or_foe == Stance.hostile:
                    total_foes += f.ship_counter
                elif f.friend_or_foe != Stance.allied:
                    total_others += f.ship_counter
            p.update_foes(total_foes - p.total_foes)
            p.update_others(total_others - p.total_others)
            if self.default_view:
                p.show_default_view(self.show_fleet_strength)
        self.apply_fleet_filter()
        if self.selected_planet:
            self.update_planet.emit(self.selected_planet)
        self.update()


    def filter_fleets(self, enabled, select):
        self.friend_filter_enabled = enabled
        if select:
            self.active_friend_filter = select
        if enabled:
            for f in self.fleets:
                if f.friend_or_foe == Stance.allied:
                    f.apply_my_filter(self.show_idle_fleets_only, select)
                    f.update_ship_count()
        elif self.show_idle_fleets_only:
            for f in self.fleets:
                if f.friend_or_foe == Stance.allied:
                    if f.idle:
                        f.ship_counter = len(f.ship_list)
                        f.update_ship_count()
                    else:
                        f.ship_counter = 0
        else:
            for f in self.fleets:
                if f.friend_or_foe == Stance.allied:
                    f.ship_counter = len(f.ship_list)
                    f.update_ship_count()
        for p in self.planets:
            total_friends = 0
            for f in p.fleets_in_orbit:
                if f.friend_or_foe == Stance.allied:
                    total_friends += f.ship_counter
            p.update_friends(total_friends - p.total_friends)
            if self.default_view:
                p.show_default_view(self.show_fleet_strength)
        self.apply_fleet_filter()
        if self.selected_planet:
            self.update_planet.emit(self.selected_planet)
        self.update()


    def enable_foe_filter(self, event):
        if event and self.active_foe_filter:
            self.filter_foes(True, self.active_foe_filter)
        else:
            self.filter_foes(False, None)


    def enable_friend_filter(self, event):
        if event and self.active_friend_filter:
            self.filter_fleets(True, self.active_friend_filter)
        else:
            self.filter_fleets(False, None)


    def filter_idle_fleets(self, event):
        self.show_idle_fleets_only = event
        self.filter_foes(self.foe_filter_enabled, self.active_foe_filter)
        self.filter_fleets(self.friend_filter_enabled, self.active_friend_filter)


    def resize_flight_paths(self, width):
        for f in self.fleets:
            if f.course:
                pen = f.course.pen()
                pen.setWidthF(width)
                f.course.setPen(pen)
        Universe.current_path_width = width


    def plot_course(self, f):
        x0 = GP.xscale * f.xc
        y0 = GP.xscale * f.yc
        if f.course:
            self.removeItem(f.course)
        if f.warp_speed > 0:
            if f.moving_fleet:
                self.removeItem(f.moving_fleet)
            q0 = QTransform()
            q0.translate(x0, y0)
            q0.rotateRadians(f.heading)
            f.moving_fleet = self.addPolygon(q0.map(_arrow))
        else:
            f.resting_fleet.setPos(x0, y0)
            f.resting_fleet.setVisible(True)
        f.course = None
        if f.friend_or_foe == Stance.allied:
            path = QPainterPath()
            render = False
            a = f.first_waypoint
            while a:
                if a == f.next_waypoint:
                    render = True
                    self.segment_path(path, f.xc, f.yc, a.xo, a.yo)
                if (render or a.retain) and a.next:
                    self.segment_path(path, a.xo, a.yo, a.next.xo, a.next.yo)
                a = a.next
            if f.next_waypoint:
                f.course = self.addPath(path)
        elif f.warp_speed > 0:
            path = QPainterPath()
            length = f.warp_speed * f.warp_speed * GP.time_horizon
            dx = length * math.cos(f.heading)
            dy = length * math.sin(f.heading)
            self.segment_path(path, f.xc, f.yc, f.xc + dx, f.yc + dy)
            f.course = self.addPath(path)


    def compute_turn(self):
        for p in self.planets:
            p.clear_orbit()
            p.fleets_in_orbit = []
        for f in self.fleets:
            f.orbiting = None
            for p in self.planets:
                if p.x == f.xc and p.y == f.yc:
                    p.enter_orbit(f)
                    p.fleets_in_orbit.append(f)
                    break
        for f in self.fleets:
            if f.moving_fleet:
                self.removeItem(f.moving_fleet)
                f.moving_fleet = None
            if f.course:
                self.removeItem(f.course)
                f.course = None
            f.resting_fleet.setVisible(False)
            f.ship_count.setVisible(False)
            if f.ship_counter > 0 and f.discovered and not f.orbiting:
                f.heading = math.pi
                if f.next_waypoint:
                    x1 = f.next_waypoint.xo
                    y1 = f.next_waypoint.yo
                    f.heading = math.atan2(y1 - f.yc, x1 - f.xc)
                self.plot_course(f)
                f.colour_course()
                f.update_ship_count()
                f.ship_count.setVisible(self.show_fleet_strength)
                f.show_course(self.show_fleet_movements)
        for p in self.planets:
            p.update_ship_tracking()
            p.mine_fields = []
            for m in self.minefields:
                d = (m.x - p.x) * (m.x - p.x) + (m.y - p.y) * (m.y - p.y)
                if d < m.mines:
                    p.mine_fields.append(m)
        for f in self.fleets:
            f.mine_fields = []
            for m in self.minefields:
                d = (f.xc - m.x) * (f.xc - m.x) + (f.yc - m.y) * (f.yc - m.y)
                if d < m.mines:
                    f.mine_fields.append(m)
        self.update()

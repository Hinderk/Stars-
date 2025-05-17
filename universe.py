
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
from planet import Planet
from colours import Pen, Brush
from defines import Stance, Task

import guiprop as GP




_arrow = QPolygonF()
_arrow.append(QPointF(GP.H_VECTOR - GP.DH_VECTOR, 0))
_arrow.append( QPointF(-GP.DH_VECTOR, -GP.W_VECTOR))
_arrow.append(QPointF(0, 0))
_arrow.append(QPointF(-GP.DH_VECTOR, GP.W_VECTOR))

_flag = QPolygonF()
_flag.append( QPointF(0, 0))
_flag.append(QPointF(0, - GP.FLAG_HEIGHT - GP.FLAG_WIDTH))
_flag.append(QPointF(GP.FLAG_WIDTH + GP.FLAG_STEM, -GP.FLAG_HEIGHT - GP.FLAG_WIDTH))
_flag.append(QPointF(GP.FLAG_WIDTH + GP.FLAG_STEM, -GP.FLAG_HEIGHT))
_flag.append(QPointF(GP.FLAG_STEM, -GP.FLAG_HEIGHT))
_flag.append(QPointF(GP.FLAG_STEM, 0))


def _setup_mine_filter():
    """ Create a mine filter / show all mine fields """
    fields = {}
    fields[Stance.ALLIED] = True
    fields[Stance.FRIENDLY] = True
    fields[Stance.NEUTRAL] = True
    fields[Stance.HOSTILE] = True
    return fields



class Universe(QGraphicsScene):

    """ This class is responsible for rendering the star map """

    select_planet = QSignal(Planet)
    update_planet = QSignal(Planet)
    update_filter = QSignal(dict)
    update_route = QSignal(object)
    select_fleet = QSignal(object, int, list, list)
    select_field = QSignal(object, int, list, list)

    current_path_width = GP.FP_WIDTH[100]

    def __init__(self, people, rules):
        super().__init__()

        self.planets = []
        self.fleets = []
        self.minefields = []
        self.debris = []
        self.xo = 0
        self.yo = 0

        self.selected_planet = None
        self.selected_fleet = None
        self.selected_waypoint = None
        self.context = None
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
        self.waypoint_mode = False

        self.show_field = _setup_mine_filter()
        self.population_ceiling = rules.get_population_ceiling(people.my_faction())
        self.year = rules.first_year()

        self.pointer = None
        self.select = None
        self.wpselect = None

        self._create_indicator()
        self._create_planets(people, rules)
        self._colonize_planets(people, rules)

        self.setBackgroundBrush(Brush.black)



# The following methods are overloaded event handlers whence their names must follow Qt
# coding conventions. Until further notice, camel case will be used ...

# pylint: disable=invalid-name


    def focusOutEvent(self, _):
        """ Event handler: Prevent waypoint relocation if the game looses focus """
        self.movement_approved = False


    def keyReleaseEvent(self, key_press):
        """ Prevent waypoint movement if the shift key is released """
        key = key_press.key()
        if key == Qt.Key.Key_Shift:
            self.movement_approved = False


    def contextMenuEvent(self, mouse_click):
        """ Create a context menu for the selected object on the star map """
        select = QMenu()
        select.setStyleSheet(GuiDesign.get_style(GuiStyle.STARMAP))
        n = 0
        if self.context[0]:
            p = self.context[0]
            a = select.addAction(p.name)
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
            fields = self.context[2][0].mine_fields
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
                name = w[0].name + ' #' + str(w[0].id)
                a = select.addAction(name + ' - WP ' + str(w[2]))
                a.setData((6, n))
                n += 1
        self._process_context_menu(select.exec(mouse_click.screenPos()))


    def mouseReleaseEvent(self, _):
        """ Event handler: Cancel waypoint movement by releasing the mouse """
#        self.movement_approved = False


    def mousePressEvent(self, mouse_click):
        """ Event handler: Select items on the star map closest to the mouse pointer """
        p0 = mouse_click.scenePos()
        self.waypoint_selected = False
        self.xo = round(0.5 + p0.x() / GP.XSCALE)
        self.yo = round(0.5 + p0.y() / GP.XSCALE)
        self.context = self._identify_context(self.xo, self.yo)
        if mouse_click.buttons() == Qt.MouseButton.LeftButton:
            if self.context[1]:
                self.waypoint_offset = 0
                self.fleet_offset = 0
                self._highlight_minefield(0)
            elif self.context[0]:
                self.waypoint_offset = 0
                self.fleet_offset = 0
                self.highlight_planet(self.context[0])
            elif self.context[2]:
                self.waypoint_offset = 0
                self._highlight_fleet()
            elif self.context[3]:
                self._highlight_waypoint()


    def mouseMoveEvent(self, event):
        """ Event handler: Move the selected waypoint around on the star map """
        p0 = event.scenePos()
        self.xo = round(0.5 + p0.x() / GP.XSCALE)
        self.yo = round(0.5 + p0.y() / GP.XSCALE)
        if self.waypoint_selected and self.movement_approved:
            w0 = self.selected_waypoint[0]
            f0 = self.selected_fleet
            w0.xo = self.xo
            w0.yo = self.yo
            f0.update_course(w0, self.planets)
            if f0.next_waypoint == w0:
                f0.Heading = math.atan2(w0.yo - f0.yc, w0.xo - f0.xc)
                f0.update_ship_count()
                self.update_route.emit(f0)
            self.plot_course(f0)
            f0.colour_course(True)
            self.wpselect.setPos(QPointF(GP.XSCALE * w0.xo, GP.XSCALE * w0.yo))



# pylint: enable=invalid-name


    def process_key_event(self, key, xo, yo):
        """ Event handler: Process keyboard interactions with the star map """
        if key == Qt.Key.Key_Shift:
            self.movement_approved = True
        elif key == Qt.Key.Key_Delete:
            if self.waypoint_selected:
                wp = self.selected_fleet.delete_waypoint(self.selected_waypoint[1])
                if wp:
                    dx = wp.xo - self.selected_fleet.xc
                    dy = wp.yo - self.selected_fleet.yc
                    self.selected_fleet.heading = math.atan2(dy, dx)
                    self.selected_fleet.update_schedule()
                else:
                    self.selected_fleet.warp_speed = 0
                    self.removeItem(self.selected_fleet.moving_fleet)
                    self.selected_fleet.moving_fleet = None
                    self.selected_fleet.task = Task.IDLE
                    self.selected_fleet.heading = math.pi
                self.selected_fleet.active_waypoint = []
                self.selected_fleet.update_ship_count()
                self.plot_course(self.selected_fleet)
                self.selected_fleet.colour_course(True)
                self.waypoint_selected = False
                self.wpselect.setVisible(False)
                self.update_route.emit(self.selected_fleet)
        elif key == Qt.Key.Key_Insert:
            if self.selected_fleet and self.selected_fleet.friend_or_foe == Stance.ALLIED:
                w0 = self.selected_fleet.add_waypoint(xo, yo)
                self.selected_fleet.update_course(w0, self.planets)
                self.selected_fleet.update_schedule()
                if self.selected_fleet.next_waypoint == w0:
                    dx = w0.xo - self.selected_fleet.xc
                    dy = w0.yo - self.selected_fleet.yc
                    self.selected_fleet.heading = math.atan2(dy, dx)
                    self.selected_fleet.update_ship_count()
                self.plot_course(self.selected_fleet)
                self.selected_fleet.colour_course(True)
                self.update_route.emit(self.selected_fleet)
#                self.context = self._identify_context(w0.xo, w0.yo)
#                self._highlight_waypoint()


    def _process_context_menu(self, selected):
        """ Process the context menu & select the proper item """
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
                self._highlight_fleet(item)
            elif itemtype == 4:
                self.fleet_offset = 0
                self._highlight_fleet()
                fields = self.context[2][0].mine_fields
                self.select_field.emit(None, item, fields, self.context[2])
            elif itemtype == 5:
                self._highlight_minefield(item)
            elif itemtype == 6:
                self._highlight_waypoint(item)


    def _identify_context(self, xo, yo):
        """ Find the objects closest to the specified coordinates """
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
            f.active_waypoint = []
            if f.discovered and f.ship_counter > 0:
                d = (f.xc - xo) * (f.xc - xo) + (f.yc - yo) * (f.yc - yo)
                if d < dist:
                    dist = d
                    f_list = [f]
                    w_list = []
                    po = None
                elif d == dist:
                    f_list.append(f)
                if f.friend_or_foe == Stance.ALLIED:
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
        return po, m_list, f_list, w_list # , xo, yo


    def _create_indicator(self):
        """ Create the object designator for the starmap """
        triangle = QPolygonF()
        triangle.append(QPointF(0, 0))
        triangle.append(QPointF(GP.POINTER_SIZE / 2, GP.POINTER_SIZE * math.sqrt(3.0) / 2))
        triangle.append(QPointF(-GP.POINTER_SIZE / 2, GP.POINTER_SIZE * math.sqrt(3.0) / 2))
        self.pointer = self.addPolygon(triangle, Pen.white_08, Brush.yellow)
        self.pointer.setZValue(8)
        w = GP.FP_RADIUS
        self.select = self.addEllipse(-w, -w, w + w, w + w, Pen.white_08, Brush.yellow)
        self.select.setZValue(-2)
        w = GP.WP_RADIUS
        pen = QPen(Pen.yellow)
        pen.setWidthF(GP.WP_WIDTH)
        self.wpselect = self.addEllipse(-w, -w, w + w, w + w, pen)
        self.wpselect.setZValue(-2)


    def highlight_planet(self, p):
        """ Select & highlight a planet on the star map """
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
            xp = GP.XSCALE * p.x
            yp = GP.XSCALE * p.y + GP.P_RADIUS + GP.DY_POINTER
            self.pointer.setPos(xp, yp)
            self.pointer.setVisible(True)
        self.selected_planet = p
        self.select_planet.emit(p)


    def _highlight_fleet(self, index=-1):
        """ Select & highlight the indexed fleet on the star map """
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
        self.select.setPos(GP.XSCALE * f0.xc, GP.XSCALE * f0.yc)
        self.select.setVisible(True)
        self.selected_fleet = f0
        self.fleet_index = index
        self.fleet_offset = 1
        self.selected_fleets = self.context[2]
        self.select_fleet.emit(None, index, self.context[2], f0.mine_fields)


    def _highlight_minefield(self, index):
        """ Select & highlight the indexed mine field on the star map """
        self.select.setVisible(False)
        if self.selected_planet:
            self.selected_planet.label.setPen(Pen.white_l)
            self.selected_planet.label.setBrush(Brush.white_l)
        self.selected_waypoint = None
        self.selected_fleet = None
        self.selected_fleets = []
        self.selected_planet = None
        xp = GP.XSCALE * self.context[1][0].x
        yp = GP.XSCALE * self.context[1][0].y + GP.DY_POINTER
        self.pointer.setPos(xp, yp)
        self.pointer.setVisible(True)
        self.select_field.emit(None, index, self.context[1], [])


    def _highlight_waypoint(self, index=-1):
        """ Select & highlight the indexed waypoint on the star map """
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
        self.wpselect.setPos(GP.XSCALE * w0.xo, GP.XSCALE * w0.yo)
        self.select.setPos(GP.XSCALE * f0.xc, GP.XSCALE * f0.yc)
        self.wpselect.setVisible(True)
        self.select.setVisible(not f0.orbiting)
        self.selected_waypoint = (w0, n0)
        self.selected_fleet = f0
        self.waypoint_index = index
        self.fleet_index = index
        self.waypoint_offset = 1
        self.selected_fleets = [w[0] for w in self.context[3]]
        self.waypoint_selected = True
        self.select_fleet.emit(None, index, self.selected_fleets, [])  # TODO: Chheck the handler! - New signal required?


    def _segment_path(self, path, xa, ya, xb, yb):
        """ Interrupt the flight path to create a halo effect around nearby fleets """
        dx = GP.XSCALE * (xb - xa)
        dy = GP.XSCALE * (yb - ya)
        d2 = float(dx * dx + dy * dy)
        if d2 > 0.0:
            r2 = GP.FLEET_HALO * GP.FLEET_HALO / d2
            sval = [(0.0, -1), (1.0, 1)]

            def process_object(xo, yo):
                """ Find intersections of halos & flight paths """
                fx = GP.XSCALE * (xa - xo)
                fy = GP.XSCALE * (ya - yo)
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

            def draw_segment():
                """ Sort intervals to locate visible segments """
                sval.sort(key=lambda p: p[0])
                s = 1
                x = GP.XSCALE * xa
                y = GP.XSCALE * ya
                for (so, ds) in sval:
                    s += ds
                    if s < 1:
                        path.moveTo(x + so * dx, y + so * dy)
                    elif s < 2 and ds > 0:
                        path.lineTo(x + so * dx, y + so * dy)

            for p in self.planets:
                process_object(p.x, p.y)
            for f in self.fleets:
                if f.discovered and f.ship_counter > 0:
                    process_object(f.xc, f.yc)
            draw_segment()


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
            if f.ship_counter > 0 and f.discovered:
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
                xp = GP.XSCALE * self.selected_planet.x
                yp = GP.XSCALE * self.selected_planet.y + GP.P_RADIUS + GP.DY_POINTER
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
        """ Indicate the size of each planet's population in relative terms """
        for p in self.planets:
            p.show_population_view()
            if p.body_visible:
                q = min(1.0, math.sqrt(p.colonists / self.population_ceiling))
                rnew = GP.P_RADIUS * (1 + q) / 2 + q * GP.D_RADIUS
                x = GP.XSCALE * p.x - rnew
                y = GP.XSCALE * p.y - rnew
                w = 2 * rnew
                p.body.setRect(QRectF(x, y, w, w))
                p.body.setPen(Pen.brown)
                p.body.setBrush(Brush.brown)
                p.population.setText(str(p.colonists))
        self.update()
        self.default_view = False


    def scale_radar_ranges(self, factor):
        """ Show effective scanner detection ranges to account for cloaking """
        f = factor / 100.0
        for p in self.planets:
            if p.scanner:
                p.scanner.scale_ranges(f)
        for fleet in self.fleets:
            if fleet.scanner:
                fleet.scanner.scale_ranges(f)
        self.update()


    def show_percentage_view(self):
        """ Indicate panet values by color & size coding the star systems """
        for p in self.planets:
            p.show_percentage_view()
            if p.core_visible:
                q = max(0.0, p.value())
                if q < 0.33:
                    p.body.setPen(Pen.red)
                    p.body.setBrush(Brush.red)
                    q = 3 * q
                elif q < 0.66:
                    p.body.setPen(Pen.yellow)
                    p.body.setBrush(Brush.yellow)
                    q = 3 * q - 1.0
                else:
                    p.body.setPen(Pen.green)
                    p.body.setBrush(Brush.green)
                    q = 3 * q - 2.0
                rnew = GP.P_RADIUS * (1 + q) / 2 + q * GP.D_RADIUS
                x = GP.XSCALE * p.x - rnew
                y = GP.XSCALE * p.y - rnew
                w = 2 * rnew
                p.body.setRect(QRectF(x, y, w, w))
            if p.flag_visible:
                if p.relation == Stance.ALLIED:
                    p.flag.setPen(Pen.blue_l)
                    p.flag.setBrush(Brush.blue)
                elif p.relation == Stance.FRIENDLY:
                    p.flag.setPen(Pen.green_d)
                    p.flag.setBrush(Brush.green)
                elif p.relation == Stance.NEUTRAL:
                    p.flag.setPen(Pen.yellow_d)
                    p.flag.setBrush(Brush.yellow)
                else:
                    p.flag.setPen(Pen.red_l)
                    p.flag.setBrush(Brush.red)
        self.update()
        self.default_view = False


    def _colonize_planets(self, people, rules):
        """ Populate the planets with NPC factions """
        f0 = people.my_faction()
        delta_r = (f0.max_radioactivity - f0.min_radioactivity) / 200.0
        opt_r = (f0.max_radioactivity + f0.min_radioactivity) / 200.0
        delta_g = (math.log2(f0.max_gravity) - math.log2(f0.min_gravity)) / 12.0
        opt_g = (math.log2(f0.max_gravity) + math.log2(f0.min_gravity)) / 12.0
        delta_t = (f0.max_temperatur - f0.min_temperatur) / 800.0
        opt_t = (f0.max_temperatur + f0.min_temperatur) / 800.0
        if f0.ignore_radioactivity:
            delta_r = 1e8
        if f0.ignore_gravity:
            delta_g = 1e8
        if f0.ignore_temperature:
            delta_t = 1e8
        for p in self.planets:
            if p.home_world:
                p.radioactivity = opt_r * 100.0
                p.gravity = 64.0 ** opt_g
                p.temperature = opt_t * 400.0
            p.center_radioactivity = opt_r
            p.delta_radioactivity = delta_r
            p.center_gravity = opt_g
            p.delta_gravity = delta_g
            p.center_temperature = opt_t
            p.delta_temperature = delta_t


    def _create_planets(self, people, rules):
        """ Populate the star map with randomly placed solar systems / planets """
        x = []
        y = []
        n = rules.planet_count()
        while n > 0:
            n -= 1
            p = self.create_planet(rules, n < 1)
            x.append(p.x)
            y.append(p.y)
            self.planets.append(p)
        xmin = GP.XSCALE * min(x) - GP.MAP_FRAME
        xmax = GP.XSCALE * max(x) + GP.MAP_FRAME
        ymin = GP.XSCALE * min(y) - GP.MAP_FRAME
        ymax = GP.XSCALE * max(y) + GP.MAP_FRAME
        self.setSceneRect(xmin, ymin, xmax - xmin, ymax - ymin)
        model = rules.first_scanner(people.my_faction())
        if model:
            p.scanner = self._create_scanner(p.x, p.y, model.value[0], model.value[1])


    def _create_scanner(self, xo, yo, rmax, rpen=0):
        """ Create the visual elements indicating the scanning range of a fleet or planet """
        s = Scanner(xo, yo, rmax, rpen)
        x = GP.XSCALE * xo
        y = GP.XSCALE * yo
        if rmax > 0:
            r = rmax * GP.XSCALE
            box = QRectF(x - r, y - r, r + r, r + r)
            s.detection = self.addEllipse(box, Pen.red_s, Brush.red_s)
            s.detection.setZValue(-10)
            s.detection.setVisible(False)
        if rpen > 0:
            r = rpen * GP.XSCALE
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
        """ Create the visual elements for a new fleet on the star map """
        w = GP.F_RADIUS + GP.F_RADIUS
        fleet.resting_fleet = self.addEllipse(-GP.F_RADIUS, -GP.F_RADIUS, w, w)
        fleet.resting_fleet.setVisible(False)
        if y:
            xo = p
            yo = y
        else:
            xo = p.x
            yo = p.y
        if fleet.friend_or_foe == Stance.ALLIED and fleet.max_range > 0:
            fleet.scanner = self._create_scanner(xo, yo, fleet.max_range, fleet.pen_range)
        fleet.ship_count = self._create_orbit_label(0, 0)
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
        """ Enable or disable the waypoint insertion mode """
        self.waypoint_mode = event


    def _create_orbit_label(self, x, y):
        """ Create labels for fleet strengths and population sizes """
        label = self.addSimpleText("", GP.MAP_FONT)
        label.setPen(Pen.white_l)
        label.setBrush(Brush.white_l)
        label.setPos(x, y)
        label.setVisible(False)
        label.setZValue(4)
        return label


    def _create_diagram(self, diagram, x, y, w):
        """ Prepare the box diagrams used to indicate the amount of mineral resources
            which can be found on the surface of a planet and inside its crust """
        line = QLineF(0, -GP.SCALE_LENGTH, 0, 0)
        line.translate(x + w / 2 - GP.SCALE_LENGTH / 2, y - GP.DY_LABEL)
        diagram.v_axis = self.addLine(line, Pen.white_08)
        d = GP.SCALE_LENGTH / 13
        box = QRectF(d, 0, 3 * d, -GP.SCALE_LENGTH)
        diagram.blue_box = self.addRect(box, Pen.blue, Brush.blue)
        diagram.blue_box.setPos(x + w / 2 - GP.SCALE_LENGTH / 2, y - GP.DY_LABEL)
        box = QRectF(5 * d, 0, 3 * d, -GP.SCALE_LENGTH)
        diagram.green_box = self.addRect(box, Pen.green, Brush.green)
        diagram.green_box.setPos(x + w / 2 - GP.SCALE_LENGTH / 2, y - GP.DY_LABEL)
        box = QRectF(9 * d, 0, 3 * d, -GP.SCALE_LENGTH)
        diagram.yellow_box = self.addRect(box, Pen.yellow, Brush.yellow)
        diagram.yellow_box.setPos(x + w / 2 - GP.SCALE_LENGTH / 2, y - GP.DY_LABEL)
        line = QLineF(GP.SCALE_LENGTH, 0, 0, 0)
        line.translate(x + w / 2 - GP.SCALE_LENGTH / 2, y - GP.DY_LABEL)
        diagram.h_axis = self.addLine(line, Pen.white_08)
        diagram.scale_length = GP.SCALE_LENGTH   # TODO: Remove this! GP.SCALE_LENGTH can be used in diagram.py directly ...
        diagram.show(False)


    def create_planet(self, rules, homeworld):
        """ Render a planet onto the star map but keep it invisible """
        p = Planet(rules, homeworld)
        [p.x, p.y] = rules.find_position()
        w = GP.P_RADIUS
        xo = p.x * GP.XSCALE - w
        yo = p.y * GP.XSCALE - w
        x = xo + w / 2
        y = yo + w / 2
        p.center = self.addEllipse(x, y, w, w, Pen.white, Brush.white)
        w += GP.P_RADIUS
        p.core = self.addEllipse(xo, yo, w, w, Pen.brown, Brush.brown)
        p.core.setVisible(False)
        x = xo - GP.D_RADIUS
        y = yo - GP.D_RADIUS
        w += 2 * GP.D_RADIUS
        c = 2 * GP.O_RADIUS
        w0 = w / math.sqrt(8.0) + 0.5
        xm = x + w / 2 - w0 - GP.O_RADIUS
        xp = x + w / 2 + w0 - GP.O_RADIUS
        ym = y + w / 2 - w0 - GP.O_RADIUS
        yp = y + w / 2 + w0 - GP.O_RADIUS
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
        p.label = self.addSimpleText(p.name, GP.MAP_FONT)
        p.label.setPen(Pen.white_l)
        p.label.setBrush(Brush.white_l)
        p.label.setVisible(False)
        w0 = p.label.boundingRect().width()
        p.label.setPos(x - w0 / 2 + w / 2, y + w + GP.DY_LABEL)
        p.ships = self._create_orbit_label(x - c / 2, y + w - GP.FONTSIZE)
        p.attackers = self._create_orbit_label(x - c / 2, y - GP.FONTSIZE / 2)
        p.others = self._create_orbit_label(x + w + c / 2, y + w - GP.FONTSIZE)
        p.population = self._create_orbit_label(x + w + c / 2, y - GP.FONTSIZE / 2)
        p.flag = self.addPolygon(_flag)
        p.flag.setPos(x + w / 2 - GP.FLAG_STEM / 2, y + w / 2)
        p.flag.setVisible(False)
        self._create_diagram(p.diagram, x, y, w)
        return p


    def show_ship_count(self, event):
        """ Display the number of ships in detected fleets outside orbit """
        if self.default_view:
            for p in self.planets:
                p.show_default_view(event)
        for f in self.fleets:
            if f.discovered and not f.orbiting:
                f.ship_count.setVisible(event and f.ship_counter > 0)
        self.update()
        self.show_fleet_strength = event


    def apply_fleet_filter(self):
        """ Update ship counts based on the current filter settings """
        for f in self.fleets:
            if f.discovered and not f.orbiting:
                show_count = self.show_fleet_strength and f.ship_counter > 0
                if f.warp_speed > 0:
                    f.moving_fleet.setVisible(f.ship_counter > 0)
                else:
                    f.resting_fleet.setVisible(f.ship_counter > 0)
                f.ship_count.setVisible(show_count and not f.orbiting)
                f.show_course(self.show_fleet_movements and f.ship_counter > 0)
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
            self.select_fleet.emit(self.selected_planet, self.fleet_index,
                                   self.selected_fleets, self.selected_fleet.mine_fields)


    def filter_foes(self, enabled, select):
        """ Apply the current ship filter settings to enemy fleets """
        self.foe_filter_enabled = enabled
        if select:
            self.active_foe_filter = select
        if self.show_idle_fleets_only:
            for f in self.fleets:
                if f.friend_or_foe != Stance.ALLIED:
                    f.ship_counter = 0
        elif enabled:
            for f in self.fleets:
                if f.friend_or_foe != Stance.ALLIED:
                    f.apply_foe_filter(select)
                    f.update_ship_count()
        else:
            for f in self.fleets:
                if f.friend_or_foe != Stance.ALLIED:
                    f.ship_counter = len(f.ship_list)
                    f.update_ship_count()
        for p in self.planets:
            total_others = 0
            total_foes = 0
            for f in p.fleets_in_orbit:
                if f.friend_or_foe == Stance.HOSTILE:
                    total_foes += f.ship_counter
                elif f.friend_or_foe != Stance.ALLIED:
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
        """ Apply the current ship filter settings to allied fleets """
        self.friend_filter_enabled = enabled
        if select:
            self.active_friend_filter = select
        if enabled:
            for f in self.fleets:
                if f.friend_or_foe == Stance.ALLIED:
                    f.apply_my_filter(self.show_idle_fleets_only, select)
                    f.update_ship_count()
        elif self.show_idle_fleets_only:
            for f in self.fleets:
                if f.friend_or_foe == Stance.ALLIED:
                    if f.idle:
                        f.ship_counter = len(f.ship_list)
                        f.update_ship_count()
                    else:
                        f.ship_counter = 0
        else:
            for f in self.fleets:
                if f.friend_or_foe == Stance.ALLIED:
                    f.ship_counter = len(f.ship_list)
                    f.update_ship_count()
        for p in self.planets:
            total_friends = 0
            for f in p.fleets_in_orbit:
                if f.friend_or_foe == Stance.ALLIED:
                    total_friends += f.ship_counter
            p.update_friends(total_friends - p.total_friends)
            if self.default_view:
                p.show_default_view(self.show_fleet_strength)
        self.apply_fleet_filter()
        if self.selected_planet:
            self.update_planet.emit(self.selected_planet)
        self.update()


    def enable_foe_filter(self, event):
        """ Engage or disengage the filter for hostile fleets """
        if event and self.active_foe_filter:
            self.filter_foes(True, self.active_foe_filter)
        else:
            self.filter_foes(False, None)


    def enable_friend_filter(self, event):
        """ Engage or disengage the filter for friendly fleets """
        if event and self.active_friend_filter:
            self.filter_fleets(True, self.active_friend_filter)
        else:
            self.filter_fleets(False, None)


    def filter_idle_fleets(self, event):
        """ Apply a ship filter to show only idle fleets on the star map """
        self.show_idle_fleets_only = event
        self.filter_foes(self.foe_filter_enabled, self.active_foe_filter)
        self.filter_fleets(self.friend_filter_enabled, self.active_friend_filter)


    def resize_flight_paths(self, width):
        """ Adjust the thickness of the flight paths """
        for f in self.fleets:
            if f.course:
                pen = f.course.pen()
                pen.setWidthF(width)
                f.course.setPen(pen)
        Universe.current_path_width = width


    def plot_course(self, f):
        """ Render the flight path of the specified fleet """
        x0 = GP.XSCALE * f.xc
        y0 = GP.XSCALE * f.yc
        if f.course:
            self.removeItem(f.course)
        if f.warp_speed > 0 and not f.orbiting:
            if f.moving_fleet:
                self.removeItem(f.moving_fleet)
            q0 = QTransform()
            q0.translate(x0, y0)
            q0.rotateRadians(f.heading)
            f.moving_fleet = self.addPolygon(q0.map(_arrow))
        else:
            f.resting_fleet.setPos(x0, y0)
            f.resting_fleet.setVisible(not f.orbiting)
        f.course = None
        if f.friend_or_foe == Stance.ALLIED:
            path = QPainterPath()
            render = False
            a = f.first_waypoint
            while a:
                if a == f.next_waypoint:
                    render = True
                    self._segment_path(path, f.xc, f.yc, a.xo, a.yo)
                if (render or a.retain) and a.next:
                    self._segment_path(path, a.xo, a.yo, a.next.xo, a.next.yo)
                a = a.next
            if f.next_waypoint:
                f.course = self.addPath(path)
        elif f.warp_speed > 0:
            path = QPainterPath()
            length = max(50, f.warp_speed * f.warp_speed * GP.TIME_HORIZON)
            dx = length * math.cos(f.heading)
            dy = length * math.sin(f.heading)
            self._segment_path(path, f.xc, f.yc, f.xc + dx, f.yc + dy)
            f.course = self.addPath(path)


    def compute_turn(self):
        """ Update the star map to reflect the new game turn """
        self.year += 1
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
            if f.ship_counter > 0 and f.discovered:
                f.heading = math.pi
                if f.next_waypoint:
                    x1 = f.next_waypoint.xo
                    y1 = f.next_waypoint.yo
                    f.heading = math.atan2(y1 - f.yc, x1 - f.xc)
                self.plot_course(f)
                f.colour_course()
                f.update_ship_count()
                f.ship_count.setVisible(self.show_fleet_strength and not f.orbiting)
                f.show_course(self.show_fleet_movements)
        for p in self.planets:
            p.update_ship_tracking(self.year)
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

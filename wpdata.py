
""" This module implements an inspector panel for fleet waypoints """

from dataviewer import DataViewer

import guiprop as GP



class WPData(DataViewer):

    """ This class is used to display information about fleet waypoints """

    def __init__(self):
        super().__init__()
        self.freight = []
        self._add_static_text()
        self._add_info_text()
        self.add_logos()


    def _add_static_text(self):
        """ Add the static text to the inspector panel for waypoints """
        wp_location = self.scene.addSimpleText("Waypoint location:", GP.INFO_FONT)
        xpos = self.x_offset
        ypos = 0
        wp_location.moveBy(xpos, ypos)
        travel_distance = self.scene.addSimpleText("Travel distance [ly]:", GP.INFO_FONT)
        ypos += 2 * self.y_delta
        travel_distance.moveBy(xpos, ypos)
        travel_time = self.scene.addSimpleText("Travel Time [y]:", GP.INFO_FONT)
        ypos += self.y_delta
        travel_time.moveBy(xpos, ypos)
        wp_task = self.scene.addSimpleText("Waypoint Task:", GP.INFO_FONT)
        ypos += 2 * self.y_delta
        wp_task.moveBy(xpos, ypos)
        wp_speed = self.scene.addSimpleText("Warp Speed:", GP.INFO_FONT)
        ypos += self.y_delta
        wp_speed.moveBy(xpos, ypos)


    def _add_info_text(self):
        """ Create the variable text elements of the inspector panel """
        self.wp_location = self.scene.addSimpleText('', GP.INFO_FONT)
        xpos = self.x_offset + 1.25 * self.data_offset
        ypos = 0
        self.wp_location.moveBy(xpos, ypos)
        self.wp_distance = self.scene.addSimpleText('', GP.INFO_FONT)
        ypos += 2 * self.y_delta
        self.wp_distance.moveBy(xpos, ypos)
        self.travel_time = self.scene.addSimpleText('', GP.INFO_FONT)
        ypos += self.y_delta
        self.travel_time.moveBy(xpos, ypos)
        self.wp_task = self.scene.addSimpleText('', GP.INFO_FONT)
        ypos += 2 * self.y_delta
        self.wp_task.moveBy(xpos, ypos)
        self.wp_speed = self.scene.addSimpleText('', GP.INFO_FONT)
        ypos += self.y_delta
        self.wp_speed.moveBy(xpos, ypos)


    def update_waypoint_data(self, f0, w0):
        """ Update the inspector panel for waypoints """
        self.update_fleet_banner(f0)
        self.wp_task.setText(w0.task.value)
        if w0.warp > 0:
            self.wp_speed.setText(str(w0.warp))
        else:
            self.wp_speed.setText('Stopped')
        self.update_flight_path(f0, w0)


    def update_flight_path(self, f0, w0):
        """ Update the inspector panel if the waypoint has moved """
        if w0.planet:
            self.wp_location.setText(w0.planet.name)
        else:
            self.wp_location.setText('(' + str(w0.xo) + ',' + str(w0.yo) + ')')
        time, dist = f0.compute_time_and_distance(w0)
        if time < 0:
            self.travel_time.setText('\u221E')
        else:
            self.travel_time.setText(str(time))
        self.wp_distance.setText(str(round(dist, 1)))

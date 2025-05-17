
""" This module implements an inspector panel for mine fields """

import math

from dataviewer import DataViewer
import guiprop as GP



class Minedata(DataViewer):

    """ This class implements the data viewer for mine fields """

    def __init__(self):
        super().__init__()
        self._add_static_text()
        self._add_info_text()
        self.add_logos(False)
        self.current_faction = 0


    def _add_static_text(self):
        """ Add the static text elements to the inspector panel """
        location = self.scene.addSimpleText("Location:", GP.INFO_FONT)
        xpos = self.x_offset
        ypos = 0
        location.moveBy(xpos, ypos)
        field_type = self.scene.addSimpleText("Field Type:", GP.INFO_FONT)
        ypos += self.y_delta
        field_type.moveBy(xpos, ypos)
        field_radius = self.scene.addSimpleText("Field Radius:", GP.INFO_FONT)
        ypos += self.y_delta
        field_radius.moveBy(xpos, ypos)
        mine_count = self.scene.addSimpleText("Live Mines:", GP.INFO_FONT)
        ypos += self.y_delta
        mine_count.moveBy(xpos, ypos)
        decay_rate = self.scene.addSimpleText("Decay Rate:", GP.INFO_FONT)
        ypos += self.y_delta
        decay_rate.moveBy(xpos, ypos)
        self.index_label = self.scene.addSimpleText("Field:", GP.INFO_FONT)
        ypos += 2 * self.y_delta
        self.index_label.moveBy(xpos, ypos)


    def _add_info_text(self):
        """ Create the variable text elements of the inspector panel """
        self.location = self.scene.addSimpleText("", GP.INFO_FONT)
        xpos = self.x_offset + self.data_offset
        ypos = 0
        self.location.moveBy(xpos, ypos)
        self.field_type = self.scene.addSimpleText("", GP.INFO_FONT)
        ypos += self.y_delta
        self.field_type.moveBy(xpos, ypos)
        self.field_radius = self.scene.addSimpleText("", GP.INFO_FONT)
        ypos += self.y_delta
        self.field_radius.moveBy(xpos, ypos)
        self.mine_count = self.scene.addSimpleText("", GP.INFO_FONT)
        ypos += self.y_delta
        self.mine_count.moveBy(xpos, ypos)
        self.decay_rate = self.scene.addSimpleText("", GP.INFO_FONT)
        ypos += self.y_delta
        self.decay_rate.moveBy(xpos, ypos)
        self.field_index = self.scene.addSimpleText("", GP.INFO_FONT)
        ypos += 2 * self.y_delta
        self.field_index.moveBy(xpos, ypos)


    def update_data(self, field, index, maxindex):
        """ Update the information about the selected mine field """
        self.faction_banner[self.current_faction].setVisible(False)
        self.current_faction = field.faction
        self.faction_banner[field.faction].setVisible(True)
        text = '(' + str(field.x) + ',' + str(field.y) + ')'
        self.location.setText(text)
        self.field_type.setText(field.model.value)
        radius = round(10 * math.sqrt(field.mines) + 0.5) / 10
        self.field_radius.setText(str(radius))
        self.mine_count.setText(str(field.mines))
        rate = round(field.mines * field.rate_of_decay + 0.5)
        self.decay_rate.setText(str(rate) + ' / year')
        if maxindex > 1:
            self.field_index.setText(str(index) + ' of ' + str(maxindex))
            self.field_index.setVisible(True)
            self.index_label.setVisible(True)
        else:
            self.index_label.setVisible(False)
            self.field_index.setVisible(False)
        self.update_mines_backdrop(field.fof)

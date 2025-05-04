
import math

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from colours import Brush, Pen
from minefield import Minefield
from defines import Stance

import guiprop as GP



class Minedata(QGraphicsView):

    x_offset = 150
    y_offset = 110
    y_delta = 35
    y_size = 27
    x_width = 550
    x_text = 100
    icon_width = 120
    data_offset = 150
    flag_offset = 20
    top_offset = 10


    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.add_static_text()
        self.add_info_text()
        self.add_logos()
        self.setScene(self.scene)
        self.setMaximumHeight(325)
        self.current_faction = 0


    def add_static_text(self):
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


    def add_info_text(self):
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


    def update_data(self, field: Minefield, index, maxindex):
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
        if field.fof == Stance.ALLIED:
            self.backdrop.setBrush(Brush.blue_p)
        elif field.fof == Stance.FRIENDLY:
            self.backdrop.setBrush(Brush.yellow_p)
        else:
            self.backdrop.setBrush(Brush.red_p)


    def add_logos(self):
        yp = self.top_offset
        rectangle = QRectF(1, yp + 1, self.icon_width - 2, self.icon_width - 2)
        self.backdrop = self.scene.addRect(rectangle)
        image = QGraphicsSvgItem(":/Graphics/Mines")
        width = image.boundingRect().width()
        image.setScale(self.icon_width / width)
        image.setPos(0, yp)
        self.scene.addItem(image)
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

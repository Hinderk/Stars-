
""" This module implements a base class for inspector widgets """

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

import brush as Brush
import pen as Pen
from defines import Stance



class DataViewer(QGraphicsView):

    """ This class is used to display information about space objects """

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
        self.faction_banner = []
        self.hull_logo = []
        self.scene = QGraphicsScene(self)
        self.backdrop = None
        self.setScene(self.scene)
        self.setMaximumHeight(325)
        self.fleet_picture = 0
        self.current_banner = 0


    def update_fleet_backdrop(self, friend_or_foe):
        """ Display the proper backdrop color for fleets """
        if friend_or_foe == Stance.ALLIED:
            self.backdrop.setBrush(Brush.BLUE_P)
        elif friend_or_foe == Stance.FRIENDLY:
            self.backdrop.setBrush(Brush.GREEN_P)
        elif friend_or_foe == Stance.NEUTRAL:
            self.backdrop.setBrush(Brush.YELLOW_P)
        else:
            self.backdrop.setBrush(Brush.RED_P)


    def update_mines_backdrop(self, friend_or_foe):
        """ Display the proper backdrop color for mine fields """
        if friend_or_foe == Stance.ALLIED:
            self.backdrop.setBrush(Brush.BLUE_P)
        elif friend_or_foe == Stance.FRIENDLY:
            self.backdrop.setBrush(Brush.YELLOW_P)
        else:
            self.backdrop.setBrush(Brush.RED_P)


    def update_fleet_banner(self, fleet):
        """ Display the proper faction banner & fleet symbol """
        if self.hull_logo:
            self.faction_banner[self.current_banner].setVisible(False)
            self.hull_logo[self.fleet_picture].setVisible(False)
            self.current_banner = fleet.banner_index
            self.fleet_picture = fleet.picture
            self.faction_banner[self.current_banner].setVisible(True)
            self.hull_logo[self.fleet_picture].setVisible(True)
        self.update_fleet_backdrop(fleet.friend_or_foe)


    def add_logos(self, load_ship_icons=True):
        """ Prepare the various icons for the inspector panel """
        yp = self.top_offset
        rectangle = QRectF(1, yp + 1, self.icon_width - 2, self.icon_width - 2)
        self.backdrop = self.scene.addRect(rectangle)
        if load_ship_icons:
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
        else:
            image = QGraphicsSvgItem(":/Graphics/Mines")
            width = image.boundingRect().width()
            image.setScale(self.icon_width / width)
            image.setPos(0, yp)
            self.scene.addItem(image)
        yp += self.flag_offset + self.icon_width
        for faction in "ABCDEFGHIJKLMNOPQRST":
            resource = ":/Factions/Faction-" + faction
            banner = QGraphicsSvgItem(resource)
            width = banner.boundingRect().width()
            banner.setScale(0.5 * self.icon_width / width)
            banner.setPos(0.25 * self.icon_width, yp)
            banner.setVisible(False)
            self.scene.addItem(banner)
            self.faction_banner.append(banner)
        self.scene.addRect(QRectF(800, 315, 5, 5), Pen.NOSHOW)

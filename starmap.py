
""" This module implements graphics view for the star map """

from PyQt6.QtGui import QPainter, QCursor
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QSizePolicy

from universe import Universe

import guiprop as GP



class Starmap(QGraphicsView):

    """ This class implements the QGraphicsView for the star map """

    def __init__(self, parent, people, rules):
        super().__init__(parent)
        self.universe = Universe(people, rules)
        self.setScene(self.universe)
        self.setMouseTracking(True)
#    self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.current_scaling = 100
        pol = QSizePolicy()
        pol.setHorizontalPolicy(pol.Policy.MinimumExpanding)
        pol.setVerticalPolicy(pol.Policy.MinimumExpanding)
        self.setSizePolicy(pol)
        self.setResizeAnchor(self.ViewportAnchor.AnchorViewCenter)


    def resize_starmap(self, event, level):
        """ This event handler is used to switch between zoom levels """
        if event:
            if level == 100:
                self.resetTransform()
            else:
                ratio = (1.0 * level) / self.current_scaling
                self.scale(ratio, ratio)
            self.universe.resize_flight_paths(GP.FP_WIDTH[level])
            self.current_scaling = level


    def process_key_event(self, key):
        """ This method maps the mouse cursor into the star map before
            keyboard events are forwarded to the proper event handler """
        if self.underMouse():
            p0 = self.mapToScene(self.mapFromGlobal(QCursor.pos()))
            xo = round(p0.x() / GP.XSCALE)
            yo = round(p0.y() / GP.XSCALE)
            self.universe.process_key_event(key, xo, yo)

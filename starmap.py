
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QSizePolicy

from universe import Universe
from guiprop import GuiProps as GP



class Starmap(QGraphicsView):

    def __init__(self, rules):

        super(self.__class__, self).__init__()

        self.universe = Universe(rules)
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
        if event:
            if level == 100:
                self.resetTransform()
            else:
                ratio = (1.0 * level) / self.current_scaling
                self.scale(ratio, ratio)
            self.universe.resize_flight_paths(GP.fp_width[level])
            self.current_scaling = level

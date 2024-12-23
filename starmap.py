
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QSizePolicy

from universe import Universe
from guiprop import GuiProps as GP



class Starmap(QGraphicsView):

  def __init__(self, rules):

    super(self.__class__, self).__init__()

    self.Universe = Universe(rules)
    self.setScene(self.Universe)
    self.CurrentScaling = 100
    pol = QSizePolicy()
    pol.setHorizontalPolicy(pol.Policy.MinimumExpanding)
    pol.setVerticalPolicy(pol.Policy.MinimumExpanding)
    self.setSizePolicy(pol)
    self.setResizeAnchor(self.ViewportAnchor.AnchorViewCenter)


  def ResizeStarmap(self, event, level):
    if event:
      if level == 100:
        self.resetTransform()
        self.Universe.ResizeFlightPaths(GP.fp_width)
      else:
        ratio = (1.0 * level) / self.CurrentScaling
        self.scale(ratio, ratio)
        self.Universe.ResizeFlightPaths(100.0 * GP.fp_width / level)
      self.CurrentScaling = level

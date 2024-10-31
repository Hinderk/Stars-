
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QSizePolicy

from universe import Universe



class Starmap(QGraphicsView):

  def __init__(self, rules):

    super(self.__class__, self).__init__()

    self.Universe = Universe(rules)
    self.setScene(self.Universe)
    pol = QSizePolicy()
    pol.setHorizontalPolicy(pol.Policy.MinimumExpanding)
    pol.setVerticalPolicy(pol.Policy.MinimumExpanding)
    self.setSizePolicy(pol)
    self.setResizeAnchor(self.ViewportAnchor.AnchorViewCenter)


  def ResizeStarmap(self, event, level):
    if event:
      if level == 100:
        self.resetTransform()
      else:
        ratio = level / self.CurrentScaling / 100.0
        self.scale(ratio, ratio)
    else:
      self.CurrentScaling = level / 100.0

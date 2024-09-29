
from PyQt6.QtWidgets import QGraphicsView
from PyQt6 import QtWidgets

from universe import Universe



class Starmap(QGraphicsView):

  def __init__(self, rules):
    super(self.__class__, self).__init__()

    self.Universe = Universe(rules)
    self.setScene(self.Universe)
    policy = QtWidgets.QSizePolicy()
    policy.setHorizontalPolicy(policy.Policy.MinimumExpanding)
    policy.setVerticalPolicy(policy.Policy.MinimumExpanding)
    self.setSizePolicy(policy)

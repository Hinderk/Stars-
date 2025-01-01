
class Diagram:


  def __init__(self):

    self.BlueBox = None
    self.GreenBox = None
    self.YellowBox = None
    self.VAxis = None
    self.HAxis = None
    self.ScaleLength = 0


  def Show(self, switch):

    self.BlueBox.setVisible(switch)
    self.GreenBox.setVisible(switch)
    self.YellowBox.setVisible(switch)
    self.VAxis.setVisible(switch)
    self.HAxis.setVisible(switch)


  def ShowCrustDiagram(self, planet):
    minerals = planet.Explored.Crust.Ironium + planet.Explored.Crust.Boranium + planet.Explored.Crust.Germanium
    if planet.Discovered and minerals > 0:
      box = self.BlueBox.rect()
      box.setBottom(-self.ScaleLength * planet.Explored.Crust.Ironium / 100.0)
      self.BlueBox.setRect(box)
      box = self.GreenBox.rect()
      box.setBottom(-self.ScaleLength * planet.Explored.Crust.Boranium / 100.0)
      self.GreenBox.setRect(box)
      box = self.YellowBox.rect()
      box.setBottom(-self.ScaleLength * planet.Explored.Crust.Germanium / 100.0)
      self.YellowBox.setRect(box)
      self.Show(True)
    else:
      self.Show(False)


  def ShowSurfaceDiagram(self, planet):
    minerals = planet.Explored.Surface.Ironium + planet.Explored.Surface.Boranium + planet.Explored.Surface.Germanium
    if planet.Discovered and minerals > 0:
      if planet.Explored.Surface.Ironium < 120:
        val = planet.Explored.Surface.Ironium / 100.0
      else:
        val = 1.2
      box = self.BlueBox.rect()
      box.setBottom(-self.ScaleLength * val)
      self.BlueBox.setRect(box)
      if planet.Explored.Surface.Boranium < 120:
        val = planet.Explored.Surface.Boranium / 100.0
      else:
        val = 1.2
      box = self.GreenBox.rect()
      box.setBottom(-self.ScaleLength * val)
      self.GreenBox.setRect(box)
      if planet.Explored.Surface.Germanium < 120:
        val = planet.Explored.Surface.Germanium / 100.0
      else:
        val = 1.2
      box = self.YellowBox.rect()
      box.setBottom(-self.ScaleLength * val)
      self.YellowBox.setRect(box)
      self.Show(True)
    else:
      self.Show(False)

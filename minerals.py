

class Minerals:

  def __init__(self, Rules=None, Scale=1.0):
    if Rules:
      MinVal = Scale * Rules.GetMinResources()
      MaxVal = Scale * Rules.GetMaxResources()
      OptVal = Scale * Rules.GetResources()
      self.Ironium = Rules.Random(MinVal, MaxVal, OptVal)
      self.Boranium = Rules.Random(MinVal, MaxVal, OptVal)
      self.Germanium = Rules.Random(MinVal, MaxVal, OptVal)
    else:
      self.Ironium = 0      # Three types of resources are Mined. These
      self.Boranium = 0     # stand in for minerals, energy and food.
      self.Germanium = 0
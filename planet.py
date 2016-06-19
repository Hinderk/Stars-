
class Minerals:
  
  Ironium = 0        # Three types of resources are available. These 
  Boronium = 0       # stand in for minerals, energy and food.
  Hydronium = 0

  def __init__( self, Rules ) :
    MinVal = Rules.GetMinResources() 
    OptVal = Rules.GetResources()
    self.Ironium = Rules.Random( MinVal, 100.0, OptVal )
    self.Boronium = Rules.Random( MinVal, 100.0, OptVal )
    self.Hydronium = Rules.Random( MinVal, 100.0, OptVal )


# This class represents the solar systems of the Stars universe each of
# which is represented by just one of its planets and named after its sun.

class Planet:

  def __init__(self, Rules) :

    self.Name = Rules.FindName()      # The name of the solar system

    self.Radioactivity = Rules.Random( 0, 100, 0 )     # These parameters may be modified via
    self.Gravity = Rules.Random( 0.1, 8, 1 )           # terraforming technologies and influence
    self.Temperature = Rules.Random( -200, 200, 0 )    # population density & growth

    self.Initial = Minerals( Rules )
    self.Current = self.Initial
    self.Surface = self.Initial
    self.Surface.Ironium *= Rules.Random( 0, 1, 0.5 )


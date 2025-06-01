
""" This module defines mineral stores either in the crust or on a planet's surface """

class Minerals:

    """ This class implements mineral deposits & surface stores """

    def __init__(self, rules=None, scale=1.0):
        if rules:
            min_val = scale * rules.get_min_resources()
            max_val = scale * rules.get_max_resources()
            opt_val = scale * rules.get_resources()
            self.ironium = rules.random(min_val, max_val, opt_val)
            self.boranium = rules.random(min_val, max_val, opt_val)
            self.germanium = rules.random(min_val, max_val, opt_val)
        else:
            self.ironium = 0      # Three types of resources are Mined. These
            self.boranium = 0     # stand in for minerals, energy and food.
            self.germanium = 0

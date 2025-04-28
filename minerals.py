

class Minerals:

    def __init__(self, rules=None, scale=1.0):
        if rules:
            min_val = scale * rules.get_min_resources()
            max_val = scale * rules.get_max_resources()
            opt_val = scale * rules.get_resources()
            self.ironium = rules.Random(min_val, max_val, opt_val)
            self.boranium = rules.Random(min_val, max_val, opt_val)
            self.germanium = rules.Random(min_val, max_val, opt_val)
        else:
            self.ironium = 0      # Three types of resources are Mined. These
            self.boranium = 0     # stand in for minerals, energy and food.
            self.germanium = 0

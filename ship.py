
""" This module implements the generic properties of space ships """


class Ship:

    """ Class definition of for a single space ship """

    def __init__(self, design):
        self.name = ""
        self.design = design
        self.total_weight = 0
        self.empty_weight = 0
        self.total_fuel = 0
        self.warp_speed = 0
        self.mine_laying = 0
        self.mine_sweeping = 0
        self.cloaking = 0
        self.fuel = 0
        self.settlers = 0
        self.ironium = 0
        self.boranium = 0
        self.germanium = 0
        self.cargo_space = 0

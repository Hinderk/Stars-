
""" This module implements a class to handle faction specific properties """

import math

from traits import Traits
from perks import Perks
from defines import Research



class Faction:

    """ This class implements the properties of a player faction """

    def __init__(self):
        self.f_id = -1
        self.ptype = None
        self.aimode = None
        self.banner_index = 0
        self.species = ''
        self.name = ''
        self.singular = 'Human'
        self.plural = 'Humans'
        self.max_colony_growth_rate = 15
        self.min_radiation = 15
        self.max_radiation = 85
        self.min_gravity = 15
        self.max_gravity = 85
        self.min_temperatur = 15
        self.max_temperatur = 85
        self.ignore_temperature = False
        self.ignore_gravity = False
        self.ignore_radiation = False
        self.primary_trait = Traits.NO
        self.secondary_traits = []
        self.colonist_productivity = 1000
        self.factory_productivity = 10
        self.factory_labor_limit = 10
        self.factory_resource_cost = 10
        self.factory_material_cost = 10
        self.mine_productivity = 10
        self.mine_resource_cost = 10
        self.mine_labor_limit = 10
        self.research_speed = {}
        for r in Research:
            self.research_speed[r.name] = 1.0
        self.boost_level = 3
        self.research_boost = False
        self.surplus_usage = 0
        self.randomize_parameters = False


    def serialize(self):
        """ Serialize the contents of the class for storage purposes """
        result = [self.banner_index, self.surplus_usage]
        result += [self.species, self.name, self.singular, self.plural]
        result += [self.max_colony_growth_rate]
        result += [self.min_gravity, self.max_gravity]
        result += [self.ignore_gravity]
        result += [self.min_temperatur, self.max_temperatur]
        result += [self.ignore_temperature]
        result += [self.min_radiation, self.max_radiation]
        result += [self.ignore_radiation]
        result += [self.primary_trait.name]
        name_list = []
        for tr in self.secondary_traits:
            name_list.append(tr.name)
        result += [name_list]
        result += [self.colonist_productivity]
        result += [self.factory_productivity]
        result += [self.factory_labor_limit]
        result += [self.factory_resource_cost]
        result += [self.factory_material_cost]
        result += [self.mine_productivity]
        result += [self.mine_resource_cost]
        result += [self.mine_labor_limit]
        result += [self.research_speed, self.boost_level, self.research_boost]
        result += [self.randomize_parameters]
        return result


    def deserialize(self, data):
        """ Initialise the class from a json string read from a file """
        self.banner_index = data[0]
        self.surplus_usage = data[1]
        self.species = data[2]
        self.name = data[3]
        self.singular = data[4]
        self.plural = data[5]
        self.max_colony_growth_rate = data[6]
        self.min_gravity = data[7]
        self.max_gravity = data[8]
        self.ignore_gravity = data[9]
        self.min_temperatur = data[10]
        self.max_temperatur = data[11]
        self.ignore_temperature = data[12]
        self.min_radiation = data[13]
        self.max_radiation = data[14]
        self.ignore_radiation = data[15]
        self.primary_trait = Traits[data[16]]
        self.secondary_traits = []
        for name in data[17]:
            self.secondary_traits.append(Perks[name])
        self.colonist_productivity = data[18]
        self.factory_productivity = data[19]
        self.factory_labor_limit = data[20]
        self.factory_resource_cost = data[21]
        self.factory_material_cost = data[22]
        self.mine_productivity = data[23]
        self.mine_resource_cost = data[24]
        self.mine_labor_limit = data[25]
        self.research_speed = data[26]
        self.boost_level = data[27]
        self.research_boost = data[28]
        self.randomize_parameters = data[29]


    def get_biome_limits(self, biome):
        """ Return the biome tolerances currently in effect """
        if biome < 1:
            minval = math.pow(2, 0.06 * (self.min_gravity - 50))
            maxval = math.pow(2, 0.06 * (self.max_gravity - 50))
        elif biome < 2:
            minval = 4 * self.min_temperatur - 200
            maxval = 4 * self.max_temperatur - 200
        else:
            minval = self.min_radiation
            maxval = self.max_radiation
        return minval, maxval

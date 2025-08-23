
""" This module implements a class to handle faction specific properties """

from traits import Traits
from perks import Perks
from defines import Research



class Faction:

    """ This class implements the properties of a player faction """

    def __init__(self, faction_id=0):
        self.f_id = faction_id
        self.banner_index = 0
        self.species = ''
        self.name = 'Humans'
        self.singular = 'Human'
        self.max_colony_growth_rate = 15
        self.min_radiation = 20
        self.max_radiation = 70
        self.min_gravity = 0.2
        self.max_gravity = 2.5
        self.min_temperatur = -40.0
        self.max_temperatur = 50.0
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
        self.mine_resource_cost = 5
        self.mine_labor_limit = 5
        self.research_speed = {}
        for r in Research:
            self.research_speed[r.name] = 1.0
        self.research_boost = False
        self.surplus_usage = 0


    def serialize(self):
        """ Serialize the contents of the class for storage purposes """
        result = [self.f_id, self.banner_index, self.surplus_usage]
        result += [self.species, self.name, self.singular]
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
        result += [self.research_speed, self.research_boost]
        return result


    def deserialize(self, data):
        """ Initialise the class from a json string read from a file """
        self.f_id = data[0]
        self.banner_index = data[1]
        self.surplus_usage = data[2]
        self.species = data[3]
        self.name = data[4]
        self.singular = data[5]
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
        self.research_boost = data[27]

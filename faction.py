
""" This module implements a class to handle faction specific properties """

from defines import PlayerType


class Faction:

    """ This class implements the properties of a player faction """

    def __init__(self, faction_id=0):
        self.f_id = faction_id
        self.banner_index = 0
        self.species = 'Homo Sapiens'
        self.name = 'Humans'
        self.mode = PlayerType.HUP
        self.min_radioactivity = 20
        self.max_radioactivity = 70
        self.min_gravity = 0.2
        self.max_gravity = 2.5
        self.min_temperatur = -40.0
        self.max_temperatur = 50.0
        self.ignore_temperature = False
        self.ignore_gravity = False
        self.ignore_radioactivity = False
        self.cargo_robber = False


    def serialize(self):
        """ Serialize the contents of the class for storage purposes """
        result = [self.f_id, self.species, self.name, self.mode.name]
        result += [self.min_radioactivity, self.max_radioactivity]
        result += [self.min_gravity, self.max_gravity]
        result += [self.min_temperatur, self.max_temperatur]
        result += [self.ignore_radioactivity]
        result += [self.ignore_gravity]
        result += [self.ignore_temperature]
        return result + [self.cargo_robber, self.banner_index]


    def deserialize(self, data):
        """ Initialise the class from a json string read from a file """
        self.f_id = data[0]
        self.species = data[1]
        self.name = data[2]
        self.mode = PlayerType[data[3]]
        self.min_radioactivity = data[4]
        self.max_radioactivity = data[5]
        self.min_gravity = data[6]
        self.max_gravity = data[7]
        self.min_temperatur = data[8]
        self.max_temperatur = data[9]
        self.ignore_radioactivity = data[10]
        self.ignore_gravity = data[11]
        self.ignore_temperature = data[12]
        self.cargo_robber = data[13]
        self.banner_index = data[14]

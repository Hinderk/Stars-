
import random

from defines import Stance
from faction import Faction



class People:

    species = ['Humanoid', 'Rabbitoid', 'Insectoid', 'Nucletoid', 'Silicanoid', 'Antetheral']
    names = ['Robotoids', 'Turindrones', 'Automitrons', 'Rototills', 'Cybertrons', 'Macinti']
    ai_faction = []

    max_ai = 0
    for name in names:
        fi = Faction(max_ai)
        fi.name = names[max_ai]
        fi.species = species[max_ai]
        max_ai += 1
        ai_faction.append(fi)

        
    def __init__(self):
        self.player_id = 0
        self.player_count = 1
        self.player = [Faction()]


    def get_stance(self, f_ida, f_idb):  # TODO: For testing purposes only ...
        if f_ida == f_idb:
            return Stance.allied
        elif f_idb < 4:
            return Stance.friendly
        elif f_idb < 8:
            return Stance.neutral
        else:
            return Stance.hostile


    def my_faction(self):
        return self.player[self.player_id]


    def get_faction(self, f_id):
        return self.player[f_id % self.player_count]


    def get_ai_faction(self, f_id):
        return People.ai_faction[f_id % People.max_ai]


    def random_faction(self):
        return People.ai_faction[random.randint(0, People.max_ai - 1)]



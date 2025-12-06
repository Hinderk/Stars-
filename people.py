
""" This module is used to define the roster of players joining a game """

import random

from aifactions import AIFactions

from defines import Stance
from faction import Faction


def _create_faction_list(list_of_factions):
    """ Create a list of faction objects from their textual representations """
    for ai in AIFactions:
        fi = Faction()
        fi.deserialize(ai.value)
        list_of_factions.append(fi)


class People:

    """ This class implements the roster of human & AI players """

    monikers = [ 'Americon', 'Automitron', 'Berserker', 'Bulushi', 'Cleaver', 'Crusher',
                 'Cybertron', 'Eagle', 'Europ', 'Felite', 'Ferret', 'Golem', 'Hawk',
                 'Hicardi', 'Hooveron', 'Hulon', 'Indion', 'Kurkonian', 'Loraxoid',
                 'Macinti', 'Mensoid', 'Nairnians', 'Nees', 'Nulons', 'Omicron', 'Picardi',
                 'Robotoid', 'Rototile', 'Rush\'n', 'Tritizoid', 'Turindrone', 'Ubert',
                 'Ultron', 'Valadian', 'Zilon' ]

    ai_faction = []

    _create_faction_list(ai_faction)

    max_ai = len(ai_faction)


    def __init__(self):
        self.player_id = 0
        self.player_count = 1
        self.player = [Faction()]


    def get_stance(self, f_ida, f_idb):  # TODO: For testing purposes only ...
        """ Return the stance of two factions towards each other """
        if f_ida == f_idb:
            return Stance.ALLIED
        if f_idb < 4:
            return Stance.FRIENDLY
        if f_idb < 8:
            return Stance.NEUTRAL
        return Stance.HOSTILE


    def my_faction(self):
        """ Return the faction of the game master """
        return self.player[self.player_id]


    def get_faction(self, f_id):
        """ Return a specific player operated game faction """
        return self.player[f_id % self.player_count]


    def add_faction(self, faction):
        """ Add a new game faction to the player list """
        self.player.append(faction)
        self.player_count += 1
        return self.player_count - 1


    def get_ai_faction(self, f_id):
        """ Return a specific AI controlled game faction """
        return People.ai_faction[f_id % People.max_ai]


    def random_ai_faction(self):
        """ Choose an AI controlled game faction at random """
        return People.ai_faction[random.randint(0, People.max_ai - 1)]

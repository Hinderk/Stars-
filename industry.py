
""" This module defines industry & growth related traits of a game faction """

from enum import Enum


class Industry(Enum):
    """ Contraints on industrial development & growth for a given species """
    RGC = ['Number of colonists required to generate 1 resource each year:',
           '', 1000, 700, 2500, 100, 105]
    RGF = ['Number of resources produced by 10 factories each year:', '', 10, 5, 15, 1, 75]
    FRB = ['Resources required to build a factory:', '', 10, 5, 25, 1, 75]
    FCO = ['Number of factories every 10000 colonists can operate:', '', 10, 5, 25, 1, 75]
    FGC = ['Factories cost 1T Germanium less to build:', '', 0, 0, 1, 1, 85]
    YMP = ['Yearly mineral production of every 10 mines:', 'kT', 10, 5, 25, 1, 105]
    MRB = ['Resources required to build a mine:', '', 5, 2, 15, 1, 80]
    MCO = ['Number of mines every 10000 colonists can operate:', '', 10, 5, 25, 1, 75]

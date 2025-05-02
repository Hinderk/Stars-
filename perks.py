
""" This module defines the various lesser traits a faction can exhibit. """

from enum import Enum


class Perks(Enum):
    """ List of perks factions may enjoy or endure """
    IFE = ['Improved Fuel Efficiency', 1]
    TTF = ['Total Terraforming', 2]
    ARM = ['Advanced Remote Mining', 3]
    ISB = ['Improved Starbases', 4]
    GRE = ['Generalized Research', 5]
    URE = ['Ultimate Recycling', 6]
    MAL = ['Mineral Alchemy', 7]
    NRS = ['No Ramscoop Engines', 8]
    CHE = ['Cheap Engines', 9]
    BRM = ['Only Basic Remote Mining', 10]
    NAS = ['No Advanced Scanners', 11]
    LSP = ['Low starting population', 12]
    BET = ['Bleeding edge technology', 13]
    RSH = ['Regenerating shields', 14]

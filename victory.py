
""" The victory conditions for a game are defined in this module """

from enum import Enum


class Victory(Enum):
    """ Victory conditions for a game, their defaults & their constraints """
    PP = ['Percentage of all planets owned:', '%', 60, 20, 100, 5, 105, True]
    TF = ['Development threshold to be reached:', None, 22, 8, 26, 1, 70, True]
    NF = ['Number of fields in which to reach this threshold:', None, 4, 2, 6, 1, 55, True]
    PS = ['The following player score is exceeded:', None, 11000, 1000, 20000, 1000, 115, False]
    ES = ['The second best player score is surpassed by:', '%', 100, 20, 300, 10, 105, True]
    PC = ['Production capacity to be reached:', 'k', 100, 10, 500, 10, 95, False]
    CS = ['Capital ships to be operated:', None, 100, 10, 300, 10, 85, False]
    HS = ['Highest score attained after these many years:', None, 100, 30, 900, 10, 85, False]

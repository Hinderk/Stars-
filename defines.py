
from enum import Enum


class MapView(Enum):
    DEFAULT = 0
    SURFACE = 1
    CRUST = 2
    POPULATION = 3
    NETWORTH = 4
    MINIMAL = 5


class Stance(Enum):
    allied = 0
    friendly = 1
    neutral = 2
    hostile = 3


class Traits(Enum):
    NO = 0           # No special traits
    HE = 1           # Hyper expansion
    SD = 2           # Space demolition
    ST = 3           # Super stealthy
    PP = 4           # Packet physics
    WM = 5           # War monger
    IT = 6           # Interstellar traveller
    CA = 7           # Claim adjuster
    AR = 8           # Alternate reality
    IS = 9           # Inner strength
    JT = 10          # Jack of all trades
    

class Perks(Enum):
    NONE = 0         # No specific perks
    IFE = 1          # Improved fuel efficiency
    NRSE = 2         # No ramscoop engines
    TTF = 3          # Total terraforming
    CHE = 4          # Cheap engines
    ARM = 5          # Advanced remote mining
    OBRM = 6         # Only basis remote mining
    ISB = 7          # Improved starbases
    NAS = 8          # No advanced scanners
    GRE = 9          # Generalized research
    LSP = 10         # Low starting population
    URE = 11         # Ultimate Recycling
    BET = 12         # Bleeding edge technology
    MAL = 13         # Mineral alchemy
    RSH = 14         # Regenerating shields
    ROB = 15         # Steal freight
    HIDE = 16        # Improve ship cloaking

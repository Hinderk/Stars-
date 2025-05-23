
from enum import Enum



class MapView(Enum):
    DEFAULT = 0
    SURFACE = 1
    CRUST = 2
    POPULATION = 3
    NETWORTH = 4
    MINIMAL = 5


class Stance(Enum):
    none = 0
    allied = 1
    friendly = 2
    neutral = 4
    hostile = 8
    accept = 15


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


class ShipClass(Enum):
    COL = "Colony Ship"
    FRT = "Freighter"
    SCT = "Scout"
    WAR = "Warship"
    UTL = "Utility Vessel"
    MLY = "Mine Layer"
    BMB = "Bomber"
    MIN = "Mining Rig"
    FLT = "Fuel Transport"


class Task(Enum):
    IDLE = 'None'
    MOVE = 'Travel'
    HAUL = 'Transport'
    MINE = 'Mining'


class PlayerType(Enum):
    AIP = 'AI Antagonist'
    EXP = 'Expansion Slot'
    HUP = 'Human Player'
    RNG = 'Random Player'


class AIMode(Enum):
    AI0 = 'Easy'
    AI1 = 'Standard'
    AI2 = 'Tough'
    AI3 = 'Expert'
    AIR = 'Random'
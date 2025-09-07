
""" This module is used to specify AI controlled game factions """

from enum import Enum



class AIFactions(Enum):
    """ Lists of perks & properties used to instantiate 'Faction' objects """
    JT = [0, 0, "Robotoids", "Humanoid", "", "", 15,
           15, 85, False, 15, 85, False, 15, 85, False,
           "JT", [],
           1000, 10, 10, 10, 10, 10, 5, 10,
           {"ENE": 1.0, "CON": 1.0, "WEP": 1.0, "ELE": 1.0, "PRO": 1.0, "BIO": 1.0},
           4, False, False]
    IT = [0, 4, "Turindrones", "Rabbitoid", "", "", 20,
           7, 55, False, 35, 81, False, 13, 53, False,
           "IT", ["IFE", "TTF", "CHE", "NAS"],
           1000, 10, 17, 9, 9, 10, 9, 10,
           {"ENE": 1.75, "CON": 1.0, "WEP": 1.75, "ELE": 1.0, "PRO": 0.5, "BIO": 0.5},
           3, False, False]
    WM = [0, 1, "Automitrons", "Insectoid", "", "", 10,
           40, 60, True, 0, 100, False, 70, 100, False,
           "WM", ["ISB", "CHE", "RSH"],
           1000, 10, 10, 10, 10, 9, 10, 6,
           {"ENE": 0.5, "CON": 0.5, "WEP": 0.5, "ELE": 1.0, "PRO": 0.5, "BIO": 1.75},
           3, False, False]
    ST = [0, 3, "Rototills", "Nucletoid", "", "", 10,
           40, 60, True, 12, 88, False, 0, 100, False,
           "ST", ["ARM", "ISB"],
           900, 10, 10, 10, 10, 10, 15, 5,
           {"ENE": 1.75, "CON": 1.75, "WEP": 1.75, "ELE": 1.75, "PRO": 1.75, "BIO": 1.75},
           3, True, False]
    HE = [0, 3, "Cybertrons", "Silicanoid", "", "", 6,
           40, 60, True, 40, 60, True, 40, 60, True,
           "HE", ["IFE", "URE", "BRM", "BET"],
           800, 12, 15, 12, 10, 10, 9, 10,
           {"ENE": 1.0, "CON": 0.5, "WEP": 1.0, "ELE": 1.0, "PRO": 0.5, "BIO": 1.75},
           3, False, False]
    SD = [0, 0, "Macinti", "Antetheral", "", "", 7,
           0, 36, False, 0, 100, False, 70, 100, False,
           "SD", ["ARM", "MAL", "NRS", "CHE", "NAS"],
           700, 11, 18, 10, 10, 10, 10, 10,
           {"ENE": 0.5, "CON": 0.5, "WEP": 1.75, "ELE": 0.5, "PRO": 0.5, "BIO": 0.5},
           3, False, False]

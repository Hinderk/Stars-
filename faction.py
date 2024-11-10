
from defines import Stance
from defines import Traits as T
from defines import Perks as P


class Faction:


    def Stance(fIDA, fIDB):  # TODO: For testing purposes only ...
        if fIDA == fIDB:
            return Stance.allied
        elif fIDB < 4:
            return Stance.friendly
        elif fIDB < 8:
            return Stance.neutral
        else:
            return Stance.hostile


    def __init__(self):
        self.FactionLogo = None

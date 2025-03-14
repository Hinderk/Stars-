
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


    def CargoRobber(fID):    # TODO: For testing purposes only ...
        return 5 < fID


    def __init__(self, FactionID=0):
        self.fID = FactionID
        self.FactionLogo = None
        self.Name = 'Homo Sapiens'
        self.Species = 'Humans'
        self.MinRadioactivity = 20
        self.MaxRadioactivity = 70
        self.MinGravity = 0.2
        self.MaxGravity = 2.5
        self.MinTemperatur = -40.0
        self.MaxTemperatur = 50.0

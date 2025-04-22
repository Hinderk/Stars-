
import random

from defines import Stance
from faction import Faction



class People:

    Species = ['Humanoid', 'Rabbitoid', 'Insectoid', 'Nucletoid', 'Silicanoid', 'Antetheral']
    Names = ['Robotoids', 'Turindrones', 'Automitrons', 'Rototills', 'Cybertrons', 'Macinti']
    AIFaction = []

    MaxAI = 0
    for name in Names:
        fi = Faction(MaxAI)
        fi.Name = Names[MaxAI]
        fi.Species = Species[MaxAI]
        MaxAI += 1
        AIFaction.append(fi)

        
    def __init__(self):
        self.PlayerID = 0
        self.PlayerCount = 1
        self.Player = [Faction()]


    def getStance(self, fIDA, fIDB):  # TODO: For testing purposes only ...
        if fIDA == fIDB:
            return Stance.allied
        elif fIDB < 4:
            return Stance.friendly
        elif fIDB < 8:
            return Stance.neutral
        else:
            return Stance.hostile


    def myFaction(self):
        return self.Player[self.PlayerID]


    def getFaction(self, fID):
        return self.Player[fID % self.PlayerCount]


    def getAIFaction(self, fID):
        return People.AIFaction[fID % People.MaxAI]


    def randomFaction(self):
        return People.AIFaction[random.randint(0, People.MaxAI - 1)]



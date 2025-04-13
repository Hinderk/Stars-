
import random

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
        self.PlayerFaction = [Faction()]


    def myFaction(self):
        return self.PlayerFaction[self.PlayerID]


    def getFaction(self, fID):
        return self.PlayerFaction[fID % self.PlayerCount]


    def getAIFaction(self, fID):
        return People.AIFaction[fID % People.MaxAI]


    def randomFaction(self):
        return People.AIFaction[random.randint(0, People.MaxAI - 1)]



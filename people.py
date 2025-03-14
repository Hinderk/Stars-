
from faction import Faction


class People:

    Species = ['Humanoid', 'Rabbitoid', 'Insectoid', 'Nucletoid', 'Silicanoid', 'Antetheral']
    Names = ['Robotoids', 'Turindrones', 'Automitrons', 'Rototills', 'Cybertrons', 'Macinti']
    AIFaction = []
    PlayerFaction = [Faction()]

    MaxAI = 0
    for name in Names:
        fi = Faction(MaxAI)
        fi.Name = Names[MaxAI]
        fi.Species = Species[MaxAI]
        MaxAI += 1
        AIFaction.append(fi)


    def __init__(self):
        self.PlayerID = 0


    def myFaction(self):
        return People.PlayerFaction[self.PlayerID]


    def getAIFaction(self, fID):
        return People.AIFaction[fID % People.MaxAI]


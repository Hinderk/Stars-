
from defines import PlayerType


class Faction:

    def __init__(self, FactionID=0):
        self.fID = FactionID
        self.BannerIndex = 0
        self.Species = 'Homo Sapiens'
        self.Name = 'Humans'
        self.Type = PlayerType.HUP
        self.MinRadioactivity = 20
        self.MaxRadioactivity = 70
        self.MinGravity = 0.2
        self.MaxGravity = 2.5
        self.MinTemperatur = -40.0
        self.MaxTemperatur = 50.0
        self.CargoRobber = False


    def serialize(self):
        result = [self.fID, self.Species, self.Name, self.Type.name]
        result += [self.MinRadioactivity, self.MaxRadioactivity]
        result += [self.MinGravity, self.MaxGravity]
        result += [self.MinTemperatur, self.MaxTemperatur]
        return result + [self.CargoRobber, self.BannerIndex]


    def deserialize(self, data):
        self.fID = data[0]
        self.Species = data[1]
        self.Name = data[2]
        self.Type = PlayerType[data[3]]
        self.MinRadioactivity = data[4]
        self.MaxRadioactivity = data[5]
        self.MinGravity = data[6]
        self.MaxGravity = data[7]
        self.MinTemperatur = data[8]
        self.MaxTemperatur = data[9]
        self.CargoRobber = data[10]
        self.BannerIndex = data[11]

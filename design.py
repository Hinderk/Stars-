
from hull import Hull


class Design:

    HullDesign = dict()
    DesignCounter = dict()
    LatestIndex = 0

    def getDesign(index):
        return Design.HullDesign.get(index)

    # fID : foe identifier ...

    def __init__(self, fID, hull):
        self.fID = fID
        self.Index = (fID, self.LatestIndex)
        self.Hull = hull
        self.System = []
        name = hull.value[1]
        if (name,fID) in self.DesignCounter:
            nr = self.DesignCounter[(name, fID)]
            self.Name = name + ' Mk ' + str(nr)
            self.DesignCounter[(name, fID)] = nr + 1
        else:
            self.Name = name + ' Mk 1'
            self.DesignCounter[(name, fID)] = 1
        self.PictureIndex = hull.value[0]
        self.LatestIndex += 1
        Design.HullDesign[self.Index] = self


    def getDesignName(self):
        return self.Hull.value[1]

    def getPictureIndex(self):
        return self.PictureIndex

    def ComputeBattleRating(self):
        return 1


from PyQt6.QtCore import QRectF

from enum import Enum
from guiprop import GuiProps
from defines import Perks as P
from defines import Traits as T




class Model(Enum):
    Bat = [0, 0, 2, True, 0, 0, 0, 0, 0, 0, T.NO, 1, 0, 1, 1, P.NONE]
    Rhino = [50, 0, 5, True, 0, 0, 0, 0, 1, 0, T.NO, 3, 0, 2, 3, P.NONE]
    Viewer50 = [50, 0, -1, False, 0, 0, 0, 0, 0, 0, T.NO, 10, 10, 70, 100, P.NONE]
    Viewer90 = [90, 0, -1, False, 0, 0, 0, 0, 1, 0, T.NO, 10, 10, 70, 100, P.NONE]
    Scoper150 = [150, 0, -1, False, 0, 0, 0, 0, 3, 0, T.NO, 10, 10, 70, 100, P.NONE]
    Mole = [100, 0, 2, True, 0, 0, 0, 0, 4, 0, T.NO, 2, 0, 2, 9, P.NONE]
    PickPocket = [80, 0, 15, True, 4, 0, 0, 0, 4, 4, T.ST, 8, 10, 6, 35, P.ROB]
    Possum = [150, 0, 3, True, 0, 0, 0, 0, 5, 0, T.NO, 3, 0, 3, 18, P.NONE]
    Chameleon = [160, 45, 6, True, 3, 0, 0, 0, 6, 0, T.ST, 4, 6, 4, 25, P.HIDE]
    Scoper220 = [220, 0, -1, False, 0, 0, 0, 0, 6, 0, T.NO, 10, 10, 70, 100, P.NONE]
    DNA = [125, 0, 2, True, 0, 0, 3, 0, 0, 6, T.NO, 1, 1, 1, 5, P.NONE]
    Ferret = [185, 50, 2, True, 3, 0, 0, 0, 7, 2, T.NO, 2, 0, 8, 36, P.NAS]
    Gazelle = [225, 0, 5, True, 4, 0, 0, 0, 8, 0, T.NO, 4, 0, 5, 24, P.NONE]
    Scoper280 = [280, 0, -1, False, 0, 0, 0, 0, 8, 0, T.NO, 10, 10, 70, 100, P.NONE]
    Dolphin = [220, 100, 4, True, 5, 0, 0, 0, 10, 4, T.NO, 5, 5, 10, 40, P.NAS]
    Snooper320X = [320, 160, -1, False, 3, 0, 0, 0, 10, 3, T.AR, 10, 10, 70, 100, P.NONE]
    RNA = [230, 0, 2, True, 0, 0, 5, 0, 0, 10, T.NO, 1, 1, 2, 20, P.NONE]
    Cheetah = [275, 0, 4, True, 5, 0, 0, 0, 11, 0, T.NO, 3, 1, 13, 50, P.NONE]
    Snooper400X = [400, 200, -1, False, 4, 0, 0, 0, 13, 6, T.AR, 10, 10, 70, 100, P.NONE]
    EagleEye = [335, 0, 3, True, 6, 0, 0, 0, 14, 0, T.NO, 3, 2, 21, 64, P.NONE]
    RobberBaron = [220, 120, 20, True, 10, 0, 0, 0, 24, 10, T.ST, 10, 10, 10, 90, P.ROB]
    Elephant = [300, 200, 6, True, 6, 0, 0, 0, 16, 7, T.NO, 8, 5, 14, 70, P.NAS]
    Snooper500X = [500, 250, -1, False, 5, 0, 0, 0, 16, 7, T.AR, 10, 10, 70, 100, P.NONE]
    Snooper620X = [620, 310, -1, False, 7, 0, 0, 0, 23, 9, T.AR, 10, 10, 70, 100, P.NONE]
    Peerless = [500, 0, 4, True, 7, 0, 0, 0, 24, 0, T.NO, 3, 2, 30, 90, P.NONE]




class Scanner:


    def __init__(self, x, y, rmax, rp=0):
        self.maxrange = rmax
        self.penrange = rp
        self.xo = x
        self.yo = y
        self.detection = None
        self.penetration = None


    def ShowRanges(self, toggle):
        if self.penetration:
            self.penetration.setVisible(toggle)
        if self.detection:
            self.detection.setVisible(toggle)


    def ScaleRanges(self, factor):
        x = GuiProps.Xscale * self.xo
        y = GuiProps.Xscale * self.yo
        if self.detection:
            r = factor * self.maxrange * GuiProps.Xscale
            box = QRectF(x - r, y - r, r + r, r + r)
            self.detection.setRect(box)
        if self.penetration:
            r = factor * self.penrange * GuiProps.Xscale
            box = QRectF(x - r, y - r, r + r, r + r)
            self.penetration.setRect(box)

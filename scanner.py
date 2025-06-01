
""" This module implements scanners both on ships and on planets """

from enum import Enum

from PyQt6.QtCore import QRectF

from defines import Feature as F
from traits import Traits as T

import guiprop as GP




class Model(Enum):
    """ Definition of the various scanner models in the game """
    BAT = [0, 0, 2, True, 0, 0, 0, 0, 0, 0, T.NO, 1, 0, 1, 1, F.NONE]
    RHINO = [50, 0, 5, True, 0, 0, 0, 0, 1, 0, T.NO, 3, 0, 2, 3, F.NONE]
    VIEWER50 = [50, 0, -1, False, 0, 0, 0, 0, 0, 0, T.NO, 10, 10, 70, 100, F.NONE]
    VIEWER90 = [90, 0, -1, False, 0, 0, 0, 0, 1, 0, T.NO, 10, 10, 70, 100, F.NONE]
    SCOPER150 = [150, 0, -1, False, 0, 0, 0, 0, 3, 0, T.NO, 10, 10, 70, 100, F.NONE]
    MOLE = [100, 0, 2, True, 0, 0, 0, 0, 4, 0, T.NO, 2, 0, 2, 9, F.NONE]
    PICKPOCKET = [80, 0, 15, True, 4, 0, 0, 0, 4, 4, T.ST, 8, 10, 6, 35, F.CROB]
    POSSUM = [150, 0, 3, True, 0, 0, 0, 0, 5, 0, T.NO, 3, 0, 3, 18, F.NONE]
    CHAMELEON = [160, 45, 6, True, 3, 0, 0, 0, 6, 0, T.ST, 4, 6, 4, 25, F.HIDE]
    SCOPER220 = [220, 0, -1, False, 0, 0, 0, 0, 6, 0, T.NO, 10, 10, 70, 100, F.NONE]
    DNA = [125, 0, 2, True, 0, 0, 3, 0, 0, 6, T.NO, 1, 1, 1, 5, F.NONE]
    FERRET = [185, 50, 2, True, 3, 0, 0, 0, 7, 2, T.NO, 2, 0, 8, 36, F.OSSC]
    GAZELLE = [225, 0, 5, True, 4, 0, 0, 0, 8, 0, T.NO, 4, 0, 5, 24, F.NONE]
    SCOPER280 = [280, 0, -1, False, 0, 0, 0, 0, 8, 0, T.NO, 10, 10, 70, 100, F.NONE]
    DOLPHIN = [220, 100, 4, True, 5, 0, 0, 0, 10, 4, T.NO, 5, 5, 10, 40, F.OSSC]
    SNOOPER320X = [320, 160, -1, False, 3, 0, 0, 0, 10, 3, T.AR, 10, 10, 70, 100, F.NONE]
    RNA = [230, 0, 2, True, 0, 0, 5, 0, 0, 10, T.NO, 1, 1, 2, 20, F.NONE]
    CHEETAH = [275, 0, 4, True, 5, 0, 0, 0, 11, 0, T.NO, 3, 1, 13, 50, F.NONE]
    SNOOPER400X = [400, 200, -1, False, 4, 0, 0, 0, 13, 6, T.AR, 10, 10, 70, 100, F.NONE]
    EAGLEEYE = [335, 0, 3, True, 6, 0, 0, 0, 14, 0, T.NO, 3, 2, 21, 64, F.NONE]
    ROBBERBARON = [220, 120, 20, True, 10, 0, 0, 0, 24, 10, T.ST, 10, 10, 10, 90, F.CROB]
    ELEPHANT = [300, 200, 6, True, 6, 0, 0, 0, 16, 7, T.NO, 8, 5, 14, 70, F.OSSC]
    SNOOPER500X = [500, 250, -1, False, 5, 0, 0, 0, 16, 7, T.AR, 10, 10, 70, 100, F.NONE]
    SNOOPER620X = [620, 310, -1, False, 7, 0, 0, 0, 23, 9, T.AR, 10, 10, 70, 100, F.NONE]
    PEERLESS = [500, 0, 4, True, 7, 0, 0, 0, 24, 0, T.NO, 3, 2, 30, 90, F.NONE]



class Scanner:

    """ This class contains the actual scanner implementation """

    def __init__(self, x, y, rmax, rp=0):
        self.maxrange = rmax
        self.penrange = rp
        self.xo = x
        self.yo = y
        self.detection = None
        self.penetration = None


    def show_ranges(self, toggle):
        """ Show respectively hide the range indicators on the star map """
        if self.penetration:
            self.penetration.setVisible(toggle)
        if self.detection:
            self.detection.setVisible(toggle)


    def scale_ranges(self, factor):
        """ Scale the range indicators when zooming into or out of the map """
        x = GP.XSCALE * self.xo
        y = GP.XSCALE * self.yo
        if self.detection:
            r = factor * self.maxrange * GP.XSCALE
            box = QRectF(x - r, y - r, r + r, r + r)
            self.detection.setRect(box)
        if self.penetration:
            r = factor * self.penrange * GP.XSCALE
            box = QRectF(x - r, y - r, r + r, r + r)
            self.penetration.setRect(box)

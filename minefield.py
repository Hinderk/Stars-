
""" This module implements the game mechanics for mine fields """

import math

from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPolygonF

import pen as PEN
import brush as BRUSH
from defines import Model, Stance

import guiprop as GP
import ruleset



_caret = QPolygonF()
_caret.append(QPointF(0, - GP.CENTER_SIZE))
_caret.append(QPointF(GP.CENTER_SIZE, 0))
_caret.append(QPointF(0, GP.CENTER_SIZE))
_caret.append(QPointF(-GP.CENTER_SIZE, 0))


class Minefield:

    """ This class is used to render mine fields in the star map """

    counter = {}
    for m in Model:
        counter[m] = 0

    def __init__(self, scene, model, f_id):

        Minefield.counter[model] += 1

        self.id = Minefield.counter[model]
        self.fleets_en_route = []
        self.total_friends = 0
        self.total_foes = 0
        self.total_others = 0
        self.detected = True # False    -- FIXME: Test feature
        self.ship_tracking = False
        self.fof = Stance.NEUTRAL
        self.faction = f_id
        self.xc = 0
        self.yc = 0
        self.mines = 0
        self.model = model
        self.rate_of_decay = ruleset.minefield_decay(f_id)
        self.countdown = 0

        self.area = scene.addEllipse(QRectF(0, 0, 10, 10))
        self.center = scene.addPolygon(_caret)
        self.center.setZValue(4)
        self.area.setVisible(False)
        self.center.setVisible(False)


    def move_field(self, x, y):
        """ Place the mine field on the star map """
        self.xc = x
        self.yc = y
        xs = x * GP.XSCALE
        ys = y * GP.XSCALE
        r = math.sqrt(self.mines) * GP.XSCALE
        self.center.setPos(xs, ys)
        self.area.setRect(QRectF(xs - r, ys - r, r + r, r + r))


    def resize_field(self, m):
        """ Update the number of mines in the field """
        self.mines = m
        x = self.xc * GP.XSCALE
        y = self.yc * GP.XSCALE
        r = math.sqrt(m) * GP.XSCALE
        self.area.setRect(QRectF(x - r, y - r, r + r, r + r))


    def update_stance(self, fof):
        """ Update the colours if a faction changes allegiances """
        self.fof = fof
        if fof == Stance.ALLIED:
            self.area.setPen(PEN.BLUE_M)
            self.area.setBrush(BRUSH.BLUE_M)
            self.area.setZValue(-6)
            self.center.setPen(PEN.BLUE_L)
            self.center.setBrush(BRUSH.BLUE)
        elif fof == Stance.FRIENDLY:
            self.area.setPen(PEN.YELLOW_M)
            self.area.setBrush(BRUSH.YELLOW_M)
            self.area.setZValue(-5)
            self.center.setPen(PEN.NOSHOW)
            self.center.setBrush(BRUSH.YELLOW)
        else:
            self.area.setPen(PEN.RED_M)
            self.area.setBrush(BRUSH.RED_M)
            self.area.setZValue(-4)
            self.center.setPen(PEN.NOSHOW)
            self.center.setBrush(BRUSH.RED)


import math
from enum import Enum

from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPolygonF

from colours import Pen, Brush
from defines import Stance
from guiprop import GuiProps

import ruleset


class Model(Enum):
    Normal = 'Standard'
    Heavy = 'Heavy'
    SpeedTrap = 'Speed Trap'



class Minefield:

    caret = QPolygonF()
    caret << QPointF(0, - GuiProps.center_size)
    caret << QPointF(GuiProps.center_size, 0)
    caret << QPointF(0, GuiProps.center_size)
    caret << QPointF(-GuiProps.center_size, 0)

    counter = {}
    for m in Model:
        counter[m] = 0

    def __init__(self, scene, x, y, m, model, f_id, people):

        r = math.sqrt(m) * GuiProps.xscale
        Minefield.counter[model] += 1

        self.id = Minefield.counter[model]
        self.fleets_en_route = []
        self.total_friends = 0
        self.total_foes = 0
        self.total_others = 0
        self.detected = True # False    -- FIXME: Test feature
        self.ship_tracking = False
        self.fof = people.get_stance(ruleset.F_ID0, f_id)
        self.faction = f_id
        self.x = x
        self.y = y
        self.mines = m
        self.model = model
        self.rate_of_decay = ruleset.minefield_decay(f_id)
        self.countdown = 0

        x *= GuiProps.xscale
        y *= GuiProps.xscale
        box = QRectF(x - r, y - r, r + r, r + r)
        if self.fof == Stance.ALLIED:
            self.area = scene.addEllipse(box, Pen.blue_m, Brush.blue_m)
            self.area.setZValue(-6)
            self.center = scene.addPolygon(self.caret, Pen.blue_l, Brush.blue)
        elif self.fof == Stance.FRIENDLY:
            self.area = scene.addEllipse(box, Pen.yellow_m, Brush.yellow_m)
            self.area.setZValue(-5)
            self.center = scene.addPolygon(self.caret, Pen.noshow, Brush.yellow)
        else:
            self.area = scene.addEllipse(box, Pen.red_m, Brush.red_m)
            self.area.setZValue(-4)
            self.center = scene.addPolygon(self.caret, Pen.noshow, Brush.red)
        self.center.setZValue(4)
        self.center.setPos(x, y)
        self.area.setVisible(False)
        self.center.setVisible(False)

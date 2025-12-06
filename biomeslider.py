
""" This module implements the sliders used to define biome tolerances """

import math

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsScene

from PyQt6.QtCore import pyqtSignal as QSignal

import pen as PEN
import brush as BRUSH




class BiomeSlider(QGraphicsScene):

    """ Create a special scene to facilitate mouse interactions
        with the sliders representing the biome tolerances """

    update_advantage_score = QSignal()

    def __init__(self, n):
        super().__init__()
        pen = [PEN.BLUE, PEN.RED_I, PEN.GREEN_I]
        brush = [BRUSH.BLUE, BRUSH.RED_I, BRUSH.GREEN_I]
        font = QFont('Segoe', pointSize=16, weight=400)
        self.addRect(QRectF(0, 0, 700, 40), PEN.BLACK, BRUSH.BLACK)
        self.addRect(QRectF(-85, 0, 5, 5), PEN.NOSHOW)
        self.addRect(QRectF(780, 0, 5, 5), PEN.NOSHOW)
        self.slider = self.addRect(QRectF(280, 4, 140, 32), pen[n], brush[n])
        self.mintext = self.addSimpleText('', font)
        self.maxtext = self.addSimpleText('', font)
        self.maxtext.setPos(720, 7)
        self.immune = False
        self.x0 = 50
        self.xpos = 50
        self.xmin = 40
        self.xmax = 60
        self.biome = n
        self.selected = False
        self.update_biome_limits()

# pylint: disable=invalid-name

    def mousePressEvent(self, mouse_click):
        """ Event handler: Pick the biome slider with the mouse """
        p0 = mouse_click.scenePos()
        xval = p0.x() / 7.0
        if self.xmin < xval < self.xmax:
            self.selected = True
            self.x0 = xval
            self.xpos = self.xmin
        else:
            self.selected = False

    def mouseMoveEvent(self, event):
        """ Event handler: Move the biome slider left & right """
        p0 = event.scenePos()
        if self.selected:
            delta = p0.x() / 7.0 - self.x0 + 1000.5
            move = int(delta + self.xpos - self.xmin) - 1000
            self.adjust_biome_limits(move, move)

# pylint: enable=invalid-name

    def get_biome_data(self):
        """ Return the raw biome data """
        return self.xmin, self.xmax


    def get_biome_limits(self):
        """ Return the biome tolerances currently in effect """
        if self.biome < 1:
            minval = math.pow(2, 0.06 * (self.xmin - 50))
            maxval = math.pow(2, 0.06 * (self.xmax - 50))
        elif self.biome < 2:
            minval = 4 * self.xmin - 200
            maxval = 4 * self.xmax - 200
        else:
            minval = self.xmin
            maxval = self.xmax
        return minval, maxval


    def update_biome_limits(self):
        """ Update the biome tolerances currently in effect """
        if self.immune:
            mintext = 'N/A'
            maxtext = 'N/A'
            self.slider.setVisible(False)
        else:
            length = [2, 0, 0]
            unit = ['g', '\u00B0C', 'mR']
            self.slider.setVisible(True)
            self.slider.setRect(7 * self.xmin, 4, 6.99 * (self.xmax - self.xmin), 32)
            minval, maxval = self.get_biome_limits()
            mintext = f'{minval:.{length[self.biome]}f}' + unit[self.biome]
            maxtext = f'{maxval:.{length[self.biome]}f}' + unit[self.biome]
        self.mintext.setText(mintext)
        xpos = -self.mintext.boundingRect().width()
        self.mintext.setPos(xpos - 20, 7)
        self.maxtext.setText(maxtext)
        self.update_advantage_score.emit()


    def adjust_biome_limits(self, smin, smax):
        """ Adjust the biome tolerances currently in use """
        if self.immune:
            return
        minval = self.xmin + smin
        maxval = self.xmax + smax
        if maxval - minval < 20:
            midval = (minval + maxval) // 2
            minval = midval - 10
            maxval = midval + 10
        if minval < 0:
            maxval -= minval
            minval = 0
        if 100 < maxval:
            minval -= maxval - 100
            maxval = 100
        minval = max(0, minval)
        self.xmin = minval
        self.xmax = maxval
        self.update_biome_limits()


    def update_immunity(self, state):
        """ Toggle biome immunity for a specific parameter """
        if state == Qt.CheckState.Checked:
            self.immune = True
        else:
            self.immune = False
        self.update_biome_limits()


    def set_biome_limits(self, xlo, xhi):
        """ Specify the biome tolerance settings """
        self.xmin = xlo
        self.xmax = xhi
        self.update_biome_limits()

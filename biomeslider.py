
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
        self.x0 = 0.5
        self.xpos = 0.5
        self.xmin = 0.4
        self.xmax = 0.6
        self.biome = n
        self.selected = False
        self.update_biome_limits()

# pylint: disable=invalid-name

    def mousePressEvent(self, mouse_click):
        """ Event handler: Pick the biome slider with the mouse """
        p0 = mouse_click.scenePos()
        xval = p0.x() / 700.0
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
            delta = p0.x() / 700.0 - self.x0
            delta += self.xpos - self.xmin
            self.adjust_biome_limits(delta, delta)

# pylint: enable=invalid-name

    def get_biome_limits(self):
        """ Return the biome tolerances currently in effect """
        if self.biome < 1:
            minval = math.pow(2, 6 * (self.xmin - 0.5))
            maxval = math.pow(2, 6 * (self.xmax - 0.5))
        elif self.biome < 2:
            minval = 400 * self.xmin - 200
            maxval = 400 * self.xmax - 200
        else:
            minval = 100 * self.xmin
            maxval = 100 * self.xmax
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
            self.slider.setRect(700 * self.xmin, 4, 699 * (self.xmax - self.xmin), 32)
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
        if maxval - minval < 0.2:
            midval = 0.5 * (minval + maxval)
            minval = midval - 0.1
            maxval = midval + 0.1
        if minval < 0:
            maxval -= minval
            minval = 0
        if 1 < maxval:
            minval -= maxval - 1
            maxval = 1
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


    def reset(self):
        """ Restore the default biome tolerance settings """
        self.xmin = 0.4
        self.xmax = 0.6
        self.update_biome_limits()

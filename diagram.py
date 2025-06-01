
""" This module implements the box diagrams for a planets's mineral deposits """

from PyQt6.QtCore import QRectF, QLineF

import pen as PEN
import brush as BRUSH
import guiprop as GP



class Diagram:

    """ This class renders crust & surface mineral diagrams onto the star map """

    def __init__(self):

        self.blue_box = None
        self.green_box = None
        self.yellow_box = None
        self.v_axis = None
        self.h_axis = None


    def create(self, scene, x, y, w):
        """ Prepare the box diagrams used to indicate the amount of mineral resources
            which can be found on the surface of a planet and inside its crust """
        line = QLineF(0, -GP.SCALE_LENGTH, 0, 0)
        line.translate(x + w / 2 - GP.SCALE_LENGTH / 2, y - GP.DY_LABEL)
        self.v_axis = scene.addLine(line, PEN.WHITE_08)
        d = GP.SCALE_LENGTH / 13
        box = QRectF(d, 0, 3 * d, -GP.SCALE_LENGTH)
        self.blue_box = scene.addRect(box, PEN.BLUE, BRUSH.BLUE)
        self.blue_box.setPos(x + w / 2 - GP.SCALE_LENGTH / 2, y - GP.DY_LABEL)
        box = QRectF(5 * d, 0, 3 * d, -GP.SCALE_LENGTH)
        self.green_box = scene.addRect(box, PEN.GREEN, BRUSH.GREEN)
        self.green_box.setPos(x + w / 2 - GP.SCALE_LENGTH / 2, y - GP.DY_LABEL)
        box = QRectF(9 * d, 0, 3 * d, -GP.SCALE_LENGTH)
        self.yellow_box = scene.addRect(box, PEN.YELLOW, BRUSH.YELLOW)
        self.yellow_box.setPos(x + w / 2 - GP.SCALE_LENGTH / 2, y - GP.DY_LABEL)
        line = QLineF(GP.SCALE_LENGTH, 0, 0, 0)
        line.translate(x + w / 2 - GP.SCALE_LENGTH / 2, y - GP.DY_LABEL)
        self.h_axis = scene.addLine(line, PEN.WHITE_08)
        self.show(False)


    def show(self, switch):
        """ Display or hide the boxes & axes of the diagram """
        self.blue_box.setVisible(switch)
        self.green_box.setVisible(switch)
        self.yellow_box.setVisible(switch)
        self.v_axis.setVisible(switch)
        self.h_axis.setVisible(switch)


    def show_crust_diagram(self, planet):
        """ Prepare the data for a crust diagram & display the diagram """
        minerals = ( planet.explored.crust.ironium +
                     planet.explored.crust.boranium +
                     planet.explored.crust.germanium )
        if planet.discovered and minerals > 0:
            box = self.blue_box.rect()
            box.setBottom(-GP.SCALE_LENGTH * planet.explored.crust.ironium / 100.0)
            self.blue_box.setRect(box)
            box = self.green_box.rect()
            box.setBottom(-GP.SCALE_LENGTH * planet.explored.crust.boranium / 100.0)
            self.green_box.setRect(box)
            box = self.yellow_box.rect()
            box.setBottom(-GP.SCALE_LENGTH * planet.explored.crust.germanium / 100.0)
            self.yellow_box.setRect(box)
            self.show(True)
        else:
            self.show(False)


    def show_surface_diagram(self, planet):
        """ Prepare the data for a surface diagram & display the diagram """
        minerals = ( planet.explored.surface.ironium +
                     planet.explored.surface.boranium +
                     planet.explored.surface.germanium )
        if planet.discovered and minerals > 0:
            if planet.explored.surface.ironium < 120:
                val = planet.explored.surface.ironium / 100.0
            else:
                val = 1.2
            box = self.blue_box.rect()
            box.setBottom(-GP.SCALE_LENGTH * val)
            self.blue_box.setRect(box)
            if planet.explored.surface.boranium < 120:
                val = planet.explored.surface.boranium / 100.0
            else:
                val = 1.2
            box = self.green_box.rect()
            box.setBottom(-GP.SCALE_LENGTH * val)
            self.green_box.setRect(box)
            if planet.explored.surface.germanium < 120:
                val = planet.explored.surface.germanium / 100.0
            else:
                val = 1.2
            box = self.yellow_box.rect()
            box.setBottom(-GP.SCALE_LENGTH * val)
            self.yellow_box.setRect(box)
            self.show(True)
        else:
            self.show(False)

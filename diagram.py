
""" This module implements the box diagrams for a planets's mineral deposits """

class Diagram:

    """ This class renders crust & surface mineral diagrams onto the star map """

    def __init__(self):

        self.blue_box = None
        self.green_box = None
        self.yellow_box = None
        self.v_axis = None
        self.h_axis = None
        self.scale_length = 0


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
            box.setBottom(-self.scale_length * planet.explored.crust.ironium / 100.0)
            self.blue_box.setRect(box)
            box = self.green_box.rect()
            box.setBottom(-self.scale_length * planet.explored.crust.boranium / 100.0)
            self.green_box.setRect(box)
            box = self.yellow_box.rect()
            box.setBottom(-self.scale_length * planet.explored.crust.germanium / 100.0)
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
            box.setBottom(-self.scale_length * val)
            self.blue_box.setRect(box)
            if planet.explored.surface.boranium < 120:
                val = planet.explored.surface.boranium / 100.0
            else:
                val = 1.2
            box = self.green_box.rect()
            box.setBottom(-self.scale_length * val)
            self.green_box.setRect(box)
            if planet.explored.surface.germanium < 120:
                val = planet.explored.surface.germanium / 100.0
            else:
                val = 1.2
            box = self.yellow_box.rect()
            box.setBottom(-self.scale_length * val)
            self.yellow_box.setRect(box)
            self.show(True)
        else:
            self.show(False)

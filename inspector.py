
""" This module implements the inspector panel """

import math

from PyQt6.QtCore import QRectF, QPointF, QLineF
from PyQt6.QtGui import QPolygonF, QFont
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene

from colours import Pen, Brush


def _setup_colors():
    """ Compile the colour scheme for the inspector panel """
    pen = [Pen.blue_i, Pen.red_i, Pen.green_i,
           Pen.blue_i, Pen.green_i, Pen.yellow_i,
           Pen.blue, Pen.red, Pen.green,
           Pen.blue, Pen.green, Pen.yellow,
           Pen.blue_25, Pen.red_25, Pen.green_25]
    brush = [Brush.blue_i, Brush.red_i, Brush.green_i,
             Brush.blue_i, Brush.green_i, Brush.yellow_i,
             Brush.blue, Brush.red, Brush.green,
             Brush.blue, Brush.green, Brush.yellow]
    return pen, brush



class Inspector(QGraphicsView):

    """ This class is responsible for rendering the contents of the inspector panel """

    font = QFont('Segoe', pointSize=16, weight=400)

    x_info = 110
    y_info = 60
    x_minerals = 110
    y_minerals = 180
    x_width = 610
    y_width = 100
    x_offset = 40
    text_offset = 1
    left_offset = 15
    bottom_offset = 5
    right_offset = 10
    top_offset = 5


    def __init__(self, faction):
        super().__init__()

        self.m_conc = []
        self.s_conc = []
        self.s_text = []
        self.biome = []
        self.rates = []

        self.pen = []
        self.brush = []

        self.scene = QGraphicsScene(self)
        self.report_age = self.scene.addSimpleText('', Inspector.font)
        self.planet_value = self.scene.addSimpleText('', Inspector.font)
        self.gravity = self.scene.addSimpleText('', Inspector.font)
        self.population = self.scene.addSimpleText('', Inspector.font)
        self.temperature = self.scene.addSimpleText('', Inspector.font)
        self.radiation = self.scene.addSimpleText('', Inspector.font)

        self.add_static_text()
        self.paint_backdrop(faction)
        self.init_biome()
        self.init_minerals()
        self.setScene(self.scene)
        self.setMaximumHeight(325)



    def add_and_move_text_elements(self, label, text, n):
        """ Create & position text labels on the inspector panel """
        measurement = self.scene.addSimpleText(text, self.font)
        width = measurement.boundingRect().width() + self.left_offset
        height = self.y_width - 3 * measurement.boundingRect().height()
        ypos = self.y_info + height / 6.0
        if n > 0:
            ypos += n * self.y_width / 3.0
        measurement.setPos(self.x_info - width, ypos)
        label.setPos(self.x_info + self.x_width + self.right_offset, ypos)


    def add_static_text(self):
        """ Initialise the immutable text elements of the inspector panel """
        self.report_age.setPos(self.x_info, (self.y_info - self.top_offset) / 2)
        self.planet_value.setPos(self.x_info, 0)
        self.add_and_move_text_elements(self.gravity, 'Gravity', 0)
        self.add_and_move_text_elements(self.temperature, ' Temperature', 1)
        self.add_and_move_text_elements(self.radiation, 'Radiation', 2)
        delta_y = self.y_width / 17
        yp = self.y_minerals + delta_y
        ironium = self.scene.addSimpleText("Ironium", self.font)
        width = ironium.boundingRect().width() + self.left_offset
        ironium.moveBy(self.x_minerals - width, yp)
        yp += 5 * delta_y
        boranium = self.scene.addSimpleText("Boranium", self.font)
        width = boranium.boundingRect().width() + self.left_offset
        boranium.moveBy(self.x_minerals - width, yp)
        yp += 5 * delta_y
        germanium = self.scene.addSimpleText("Germanium", self.font)
        width = germanium.boundingRect().width() + self.left_offset
        germanium.moveBy(self.x_minerals - width, yp)
        kt = 0
        xp = self.x_minerals
        yp = self.y_minerals + self.y_width + self.bottom_offset
        for i in range(11):
            label = self.scene.addSimpleText(str(i * 500), self.font)
            kt += 500
            dx = label.boundingRect().width() / 2
            label.moveBy(xp - dx, yp)
            xp += self.x_width / 10
        label = self.scene.addSimpleText("kt", self.font)
        xp = label.boundingRect().width() + 3 * self.left_offset
        label.moveBy(self.x_minerals - xp, yp)


    def init_biome(self):
        """ Initialise the display of the planetary parameters """
        pen, brush = _setup_colors()
        dy = self.y_width / 12.0
        caret = QPolygonF()
        caret.append(QPointF(0, 0))
        caret.append(QPointF(dy, dy))
        caret.append(QPointF(0, dy + dy))
        caret.append(QPointF(-dy, dy))
        line = QLineF(0, dy, 40, dy)
        yp = self.y_info + dy
        for n in (0, 1, 2):
            xp = self.x_info + self.x_width * 0.5
            mark = caret.translated(xp, yp)
            rate = line.translated(xp, yp)
            self.rates.append(self.scene.addLine(rate, pen[n + 12]))
            self.biome.append(self.scene.addPolygon(mark, pen[n + 6], brush[n + 6]))
            yp += 4 * dy


    def init_minerals(self):
        """ Initialise the display of mineral deposits on a planet """
        pen, brush = _setup_colors()
        dy = self.y_width / 12.0
        caret = QPolygonF()
        caret.append(QPointF(0, 0))
        caret.append(QPointF(dy, dy))
        caret.append(QPointF(0, dy + dy))
        caret.append(QPointF(-dy, dy))
        delta_y = self.y_width / 17
        yp = self.y_minerals + 2 * delta_y
        for n in (0, 1, 2):
            xlen = self.x_width / 2
            xp = self.x_width
            show = False
            if xlen > self.x_width:
                show = True
                xlen = self.x_width
            box = QRectF(self.x_minerals, yp, xlen, 3 * delta_y)
            mark = caret.translated(xp, yp)
            self.s_conc.append(self.scene.addRect(box, pen[n + 3], brush[n + 3]))
            self.m_conc.append(self.scene.addPolygon(mark, pen[n + 9], brush[n + 9]))
            label = self.scene.addSimpleText(str(1000))
            label.setPos(self.x_minerals + self.x_offset, yp + self.text_offset)
            label.setPen(Pen.white)
            label.setVisible(show)
            self.s_text.append(label)
            yp += 5 * delta_y


    def update_minerals(self, planet):
        """ Update the display of mineral deposits """
        s_conc = []
        m_conc = []
        m_conc.append(planet.explored.crust.ironium / 100.0)
        m_conc.append(planet.explored.crust.boranium / 100.0)
        m_conc.append(planet.explored.crust.germanium / 100.0)
        s_conc.append(planet.explored.surface.ironium)
        s_conc.append(planet.explored.surface.boranium)
        s_conc.append(planet.explored.surface.germanium)
        delta_y = self.y_width / 17
        yp = self.y_minerals + 2 * delta_y
        for n in (0, 1, 2):
            caret = self.m_conc[n].polygon()
            dx = self.x_width * m_conc[n] - caret.first().x()
            caret.translate(self.x_minerals + dx, 0)
            self.m_conc[n].setPolygon(caret)
            show = False
            xlen = self.x_width * s_conc[n] / 5000.0
            if xlen > self.x_width:
                show = True
                xlen = self.x_width - 1
            self.s_conc[n].setRect(self.x_minerals, yp, xlen, 3 * delta_y)
            self.s_text[n].setVisible(show)
            self.s_text[n].setText(str(s_conc[n]))
            yp += 5 * delta_y


    def update_biome(self, planet):
        """ Update the display of the planetary parameters """
        data = []
        data.append(0.5 + math.log2(planet.gravity) / 6.0)
        data.append(0.5 + planet.temperature / 400.0)
        data.append(planet.radioactivity / 100.0)
        g = planet.gravity + planet.gravity_rate
        t = planet.temperature + planet.temperature_rate
        r = planet.radioactivity + planet.radioactivity_rate
        data.append(0.5 + math.log2(g) / 6.0 - data[0])
        data.append(0.5 + t / 400.0 - data[1])
        data.append(r / 100.0 - data[2])
        for n in (0, 1, 2):
            caret = self.biome[n].polygon()
            dx = self.x_width * data[n] - caret.first().x()
            caret.translate(self.x_info + dx, 0)
            line = self.rates[n].line()
            line.translate(self.x_info + dx, 0)
            line.setLength(self.x_width * data[3 + n])
            self.biome[n].setPolygon(caret)
            self.rates[n].setLine(line)
        g = int(planet.gravity * 100 + 0.5) / 100
        t = int(planet.temperature + 300.5) - 300
        r = int(planet.radioactivity + 0.5)
        self.gravity.setText(str(g) + "g")
        self.temperature.setText(str(t) + "\u00B0C")
        self.radiation.setText(str(r) + "mR")


    def update_text(self, year, planet):
        """ Update text elements of the inspector panel """
        age = year - planet.last_visit
        if age > 0:
            self.report_age.setText('Report is ' + str(age) + ' years old.')
        else:
            self.report_age.setText('Report is current.')
        val = round(100 * planet.value())
        self.planet_value.setText('Value: ' + str(val) + '%')
        if planet.colonists > 0:
            self.population.setText('Population: ' + str(planet.colonists))
        else:
            self.population.setText('Uninhabited')
        width = self.x_width - self.population.boundingRect().width()
        self.population.setPos(self.x_info + width, 0)


    def paint_backdrop(self, faction):
        """ Paint the background of the inspector panel """
        pen, brush = _setup_colors()
        delta_x = self.x_width / 10
        delta_y = self.y_width / 3
        info = QRectF(self.x_info, self.y_info, self.x_width, self.y_width)
        self.scene.addRect(info, Pen.black, Brush.black)
        xp = self.x_info + self.x_width
        yp = self.y_info + delta_y
        self.scene.addLine(self.x_info, yp, xp, yp, Pen.white_o)
        yp += delta_y
        self.scene.addLine(self.x_info, yp, xp, yp, Pen.white_o)
        minerals = QRectF(self.x_minerals, self.y_minerals, self.x_width, self.y_width)
        self.scene.addRect(minerals, Pen.black, Brush.black)
        xp = self.x_minerals
        yp = self.y_minerals + self.y_width
        for n in range(0, 10):
            xp += delta_x
            self.scene.addLine(xp, self.y_minerals, xp, yp, Pen.white_o)
        min_val = []
        max_val = []
        min_val.append(0.5 + math.log2(faction.min_gravity) / 6.0)
        min_val.append(0.5 + faction.min_temperatur / 400.0)
        min_val.append(faction.min_radioactivity / 100.0)
        max_val.append(0.5 + math.log2(faction.max_gravity) / 6.0)
        max_val.append(0.5 + faction.max_temperatur / 400.0)
        max_val.append(faction.max_radioactivity / 100.0)
        delta_y = self.y_width / 12
        yp = self.y_info + delta_y
        for n in (0, 1, 2):
            xp = self.x_info + self.x_width * min_val[n]
            xlen = self.x_width * (max_val[n] - min_val[n])
            box = QRectF(xp, yp, xlen, 2 * delta_y)
            self.scene.addRect(box, pen[n], brush[n])
            yp += 4 * delta_y

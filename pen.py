
""" This module provides a collection of pens to draw GUI elements """

from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt

import colours as COLOR



NOSHOW = QPen(Qt.PenStyle.NoPen)
BLUE_25 = QPen(COLOR.INSPECTOR_LIGHT_BLUE)
GREEN_25 = QPen(COLOR.INSPECTOR_LIGHT_GREEN)
RED_25 = QPen(COLOR.INSPECTOR_LIGHT_RED)
BLUE_25.setWidthF(2.5)
RED_25.setWidthF(2.5)
GREEN_25.setWidthF(2.5)
BLUE_I = QPen(COLOR.INSPECTOR_BLUE)
GREEN_I = QPen(COLOR.INSPECTOR_GREEN)
YELLOW_I = QPen(COLOR.INSPECTOR_YELLOW)
RED_I = QPen(COLOR.INSPECTOR_RED)
BLUE_P = QPen(COLOR.BACKGROUND_BLUE)
RED_P = QPen(COLOR.BACKGROUND_RED)
YELLOW_P = QPen(COLOR.BACKGROUND_YELLOW)
GREEN_P = QPen(COLOR.BACKGROUND_GREEN)
WHITE_L = QPen(COLOR.LABEL_WHITE)
WHITE_O = QPen(COLOR.OFF_WHITE)
RED_M = QPen(COLOR.MINEFIELD_RED)
RED_S = QPen(COLOR.SCANNER_RED)
RED_D = QPen(COLOR.DARK_RED)
YELLOW_S = QPen(COLOR.SCANNER_YELLOW)
WHITE = QPen(COLOR.WHITE)
BLACK = QPen(COLOR.BLACK)
BLUE = QPen(COLOR.BLUE)
BLUE_M = QPen(COLOR.MINEFIELD_BLUE)
BLUE_L = QPen(COLOR.LIGHT_BLUE)
BLUE_H = QPen(COLOR.HIGHLIGHT_BLUE)
GREEN = QPen(COLOR.GREEN)
GREEN_D = QPen(COLOR.DARK_GREEN)
YELLOW = QPen(COLOR.YELLOW)
YELLOW_M = QPen(COLOR.MINEFIELD_YELLOW)
YELLOW_D = QPen(COLOR.DARK_YELLOW)
RED = QPen(COLOR.RED)
RED_L = QPen(COLOR.HIGHLIGHT_RED)
BROWN = QPen(COLOR.DARK_BROWN)
NEUTRAL = QPen(COLOR.NEUTRAL)
WHITE_2 = QPen(COLOR.WHITE)
WHITE_08 = QPen(COLOR.WHITE)
BROWN.setWidthF(2.0)
WHITE_2.setWidthF(2.0)
WHITE_O.setWidth(2)
WHITE_08.setWidthF(0.8)
RED_M.setWidthF(0.4)
BLUE_M.setWidthF(0.4)
YELLOW_M.setWidthF(0.4)
BLACK_2 = QPen(COLOR.BLACK)
BLACK_2.setWidthF(2.0)

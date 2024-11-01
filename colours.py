
from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtCore import Qt



_black = QColor(0, 0, 0)
_blue = QColor(0, 0, 255)
_green = QColor(0, 255, 0)
_yellow = QColor(255, 255, 0)
_red = QColor(255, 0, 0)
_white = QColor(255, 255, 255)
_brown = QColor(181, 101, 29)
_neutral = QColor(40, 220, 40)

_scanner_yellow = QColor(255, 255, 0, 120)
_scanner_red = QColor(255, 120, 0, 220)
_label_white = QColor(255, 255, 255, 120)

_light_blue = QColor(0, 100, 255)
_light_red = QColor(255, 100, 100)
_dark_green = QColor(0, 100, 0)
_dark_yellow = QColor(100, 100, 0)
_dark_brown = QColor(128, 48, 0)

_minefield_red = QColor(255, 0, 0)
_minefield_yellow = QColor(255, 255, 0, 128)
_minefield_blue = QColor(0, 0, 255)



class Pen:

  noshow = QPen(Qt.PenStyle.NoPen)
  white_l = QPen(_label_white)
  red_m = QPen(_minefield_red)
  red_s = QPen(_scanner_red)
  yellow_s = QPen(_scanner_yellow)
  white = QPen(_white)
  black = QPen(_black)
  blue = QPen(_blue)
  blue_m = QPen(_minefield_blue)
  blue_l = QPen(_light_blue)
  green = QPen(_green)
  green_d = QPen(_dark_green)
  yellow = QPen(_yellow)
  yellow_m = QPen(_minefield_yellow)
  yellow_d = QPen(_dark_yellow)
  red = QPen(_red)
  red_l = QPen(_light_red)
  brown = QPen(_dark_brown)
  neutral = QPen(_neutral)
  white_2 = QPen(_white)
  white_08 = QPen(_white)
  brown.setWidthF(2.0)
  white_2.setWidthF(2.0)
  white_08.setWidthF(0.8)
  red_m.setWidthF(0.4)
  blue_m.setWidthF(0.4)
  yellow_m.setWidthF(0.4)


class Brush:

  white_l = QBrush(_label_white)
  white = QBrush(_white)
  black = QBrush(_black)
  blue = QBrush(_blue)
  blue_m = QBrush(_minefield_blue, Qt.BrushStyle.BDiagPattern)
  blue_l = QBrush(_light_blue)
  green = QBrush(_green)
  yellow = QBrush(_yellow)
  red = QBrush(_red)
  red_m = QBrush(_minefield_red, Qt.BrushStyle.FDiagPattern)
  brown = QBrush(_brown)
  neutral = QBrush(_neutral)
  red_s = QBrush(_scanner_red)
  yellow_s = QBrush(_scanner_yellow)
  yellow_m = QBrush(_minefield_yellow, Qt.BrushStyle.Dense6Pattern)

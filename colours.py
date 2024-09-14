
from PyQt6.QtGui import QColor, QPen, QBrush


_black = QColor(0, 0, 0)
_blue = QColor(0, 0, 255)
_green = QColor(0, 255, 0)
_yellow = QColor(255, 255, 0)
_red = QColor(255, 0, 0)
_white = QColor(255, 255, 255)
_brown = QColor(128, 48, 0)
_neutral = QColor(40, 220, 40)
    

class Pen:

  white = QPen(_white)
  black = QPen(_black)
  blue = QPen(_blue)
  green = QPen(_green)
  yellow = QPen(_yellow)
  red = QPen(_red)
  brown = QPen(_brown)
  neutral = QPen(_neutral)
  white_2 = QPen(_white)
  white_08 = QPen(_white)
  white_2.setWidthF(2.0)
  white_08.setWidthF(0.8)


class Brush:
  
  white = QBrush(_white)
  black = QBrush(_black)
  blue = QBrush(_blue)
  green = QBrush(_green)
  yellow = QBrush(_yellow)
  red = QBrush(_red)
  brown = QBrush(_brown)
  neutral = QBrush(_neutral)

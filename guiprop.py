
""" This module is used to configure visual elements of the star map """

from PyQt6.QtGui import QFont


FONTSIZE = 14
MAP_FONT = QFont('Courier', pointSize=FONTSIZE, weight=50)
INFO_FONT = QFont('Segoe', pointSize=16, weight=400)
CARGO_FONT = QFont('Segoe', pointSize=14, weight=800)

XSCALE = 0.75       # Change to resize the star map ...

# The following numbers denote screen coordinates.

H_VECTOR = 10
DH_VECTOR = 4
W_VECTOR = 6
F_RADIUS = 4
F_DIST = 8
FP_RADIUS = 8
WP_RADIUS = 3
WP_WIDTH = 2.0

DY_LABEL = 10
DY_POINTER = 20
D_RADIUS = 8
P_RADIUS = 8
O_RADIUS = 5
FLAG_HEIGHT = 25
FLAG_WIDTH = 10
FLAG_STEM = 2
CENTER_SIZE = 3
SCALE_LENGTH = 30
POINTER_SIZE = 20

MAP_FRAME = 200
PLANET_DISTANCE = 100
FLEET_HALO = 18.0
TIME_HORIZON = 5    # Applies to enemy fleets only ...

P_SNAP = 36         #  The old value (16) might be a bit too small ...

FP_WIDTH = {25: 2.8, 50: 2.0, 75: 1.8, 100: 1.8, 125: 1.4, 150: 1.4, 200: 1.2, 400: 1.0}


from PyQt6.QtGui import QFont



class GuiProps:

    fontsize = 14
    mapFont = QFont('Courier', pointSize=fontsize, weight=50)
    infoFont = QFont('Segoe', pointSize=16, weight=400)
    cargoFont = QFont('Segoe', pointSize=14, weight=800)

    Xscale = 0.75       # Change to resize the star map ...

    dy_label = 10
    dy_pointer = 20
    d_radius = 8
    p_radius = 8
    flag_height = 25
    flag_width = 10
    flag_stem = 2
    center_size = 3
    scale_length = 30
    pointer_size = 20

    map_frame = 200          # screen coordinates ...
    planet_distance = 100    # screen coordinates ...
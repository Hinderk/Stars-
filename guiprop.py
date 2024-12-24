
from PyQt6.QtGui import QFont



class GuiProps:

    fontsize = 14
    mapFont = QFont('Courier', pointSize=fontsize, weight=50)
    infoFont = QFont('Segoe', pointSize=16, weight=400)
    cargoFont = QFont('Segoe', pointSize=14, weight=800)

    Xscale = 0.75       # Change to resize the star map ...

    # The following numbers denote screen coordinates.

    h_vector = 10
    dh_vector = 4
    w_vector = 6
    f_radius = 4
    f_dist = 10
    fp_radius = 10

    dy_label = 10
    dy_pointer = 20
    d_radius = 8
    p_radius = 8
    o_radius = 5
    flag_height = 25
    flag_width = 10
    flag_stem = 2
    center_size = 3
    scale_length = 30
    pointer_size = 20

    map_frame = 200
    planet_distance = 100

    fp_width = 1.2

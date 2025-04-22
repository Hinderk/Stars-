
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
    f_dist = 8
    fp_radius = 8
    wp_radius = 3
    wp_width = 2.0

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
    fleet_halo = 15.0
    time_horizon = 5    # Applies to enemy fleets only ...
    
    p_snap = 16

    fp_width = {25: 2.8, 50: 2.0, 75: 1.8, 100: 1.8, 125: 1.4, 150: 1.4, 200: 1.2, 400: 1.0}


from PyQt5 import QtGui, QtCore, QtWidgets

##import stars_rc
import os



class PlanetInfo :

    def __init__( self, form ) :

        Button = QtWidgets.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Default' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtWidgets.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Surface' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtWidgets.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Minerals' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtWidgets.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Percent' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtWidgets.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/People' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtWidgets.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Cancel' )
        Button.setIcon( Icon )
        Button.setChecked( True )
        form.PlanetInfo.addWidget( Button )
        Button = QtWidgets.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Waypoint' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtWidgets.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Scanner' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )        
        self.RadarRange = QtWidgets.QSpinBox()
        self.RadarRange.setSuffix( '%' )
        self.RadarRange.setRange( 10, 100 )
        self.RadarRange.setValue( 100 )
        self.RadarRange.setSingleStep( 10 )
        self.RadarRange.setAlignment( QtCore.Qt.AlignRight )
        form.PlanetInfo.addWidget( self.RadarRange )

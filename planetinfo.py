
from PyQt4 import QtGui, QtCore

import sys
import os



class PlanetInfo :

    def __init__( self, form ) :

        Button = QtGui.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Default' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtGui.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Surface' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtGui.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Minerals' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtGui.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Percent' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtGui.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/People' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtGui.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Cancel' )
        Button.setIcon( Icon )
        Button.setChecked( True )
        form.PlanetInfo.addWidget( Button )
        Button = QtGui.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Waypoint' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )
        Button = QtGui.QToolButton()
        Button.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Scanner' )
        Button.setIcon( Icon )
        form.PlanetInfo.addWidget( Button )        
        self.RadarRange = QtGui.QSpinBox()
        self.RadarRange.setSuffix( '%' )
        self.RadarRange.setRange( 10, 100 )
        self.RadarRange.setValue( 100 )
        self.RadarRange.setSingleStep( 10 )
        self.RadarRange.setAlignment( QtCore.Qt.AlignRight )
        form.PlanetInfo.addWidget( self.RadarRange )
            
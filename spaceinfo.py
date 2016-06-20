
from PyQt4 import QtGui, QtCore

import sys
import os
import stars



class SpaceInfo( stars.Ui_GUI ) :

    def __init__( self, form ) :

        MineFilter = QtGui.QMenu()
        self.AllMines = MineFilter.addAction( 'All Mine Fields' )
        self.NoMines = MineFilter.addAction( 'No Mine Fields' )
        MineFilter.addSeparator()
        self.YourMines = MineFilter.addAction( 'Mine Fields of Yours' )
        self.FriendlyMines = MineFilter.addAction( 'Mine Fields of Friends' )
        self.NeutralMines = MineFilter.addAction( 'Mine Fields of Neutrals' )
        self.EnemyMines = MineFilter.addAction( 'Mine Fields of Enemies' )
        self.YourMines.setCheckable( True )
        self.FriendlyMines.setCheckable( True )
        self.NeutralMines.setCheckable( True )
        self.EnemyMines.setCheckable( True )
        Mines = QtGui.QToolButton()
        Mines.setCheckable( True )
        Mines.setPopupMode( Mines.DelayedPopup )
        Icon = QtGui.QIcon( ':/Toolbar/Mine' )
        Mines.setIcon( Icon )
        Mines.setMenu( MineFilter )
        form.SpaceInfo.addWidget( Mines )
    ##
        Paths = QtGui.QToolButton()
        Paths.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Paths' )
        Paths.setIcon( Icon )
        form.SpaceInfo.addWidget( Paths )
    ##
        Names = QtGui.QToolButton()
        Names.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Names' )
        Names.setIcon( Icon )
        form.SpaceInfo.addWidget( Names )
    ##
        Orbit = QtGui.QToolButton()
        Orbit.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Orbiting' )
        Orbit.setIcon( Icon )
        form.SpaceInfo.addWidget( Orbit )
    ##
        Idle = QtGui.QToolButton()
        Idle.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Waiting' )
        Idle.setIcon( Icon )
        form.SpaceInfo.addWidget( Idle )
    ##
        FriendFilter = QtGui.QMenu()
        self.AllFriends = FriendFilter.addAction( 'All Designs' )
        self.InvertFriends = FriendFilter.addAction( 'Invert Filter' )
        self.NoFriends = FriendFilter.addAction( 'No Designs' )
        FriendFilter.addSeparator()

########
        
## Friendly Designs will go here !
        
########
        
        Friends = QtGui.QToolButton()
        Friends.setCheckable( True )
        Friends.setPopupMode( Friends.DelayedPopup )
        Icon = QtGui.QIcon( ':/Toolbar/Friendlies' )
        Friends.setIcon( Icon )
        Friends.setMenu( FriendFilter )
        form.SpaceInfo.addWidget( Friends )
    ##
        FoeFilter = QtGui.QMenu()
        self.AllFoes = FoeFilter.addAction( 'All Designs' )
        self.InvertFoes = FoeFilter.addAction( 'Invert Filter' )
        self.NoFoes = FoeFilter.addAction( 'No Designs' )
        FoeFilter.addSeparator()
        self.ColonyShips = FoeFilter.addAction( 'Colony Ships' )
        self.Freighters = FoeFilter.addAction( 'Freighters' )
        self.Scouts = FoeFilter.addAction( 'Scouts' )
        self.Warships = FoeFilter.addAction( 'Warships' )
        self.UtilityShips = FoeFilter.addAction( 'Utility Ships' )
        self.Bombers = FoeFilter.addAction( 'Bombers' )
        self.MiningShips = FoeFilter.addAction( 'Mining Ships' )
        self.Tankers = FoeFilter.addAction( 'Fuel Transports' )
        self.ColonyShips.setCheckable( True ) 
        self.Freighters.setCheckable( True )
        self.Scouts.setCheckable( True )
        self.Warships.setCheckable( True )
        self.UtilityShips.setCheckable( True )
        self.Bombers.setCheckable( True )
        self.MiningShips.setCheckable( True )
        self.Tankers.setCheckable( True )
        Foes = QtGui.QToolButton()
        Foes.setCheckable( True )
        Foes.setPopupMode( Foes.DelayedPopup )
        Icon = QtGui.QIcon( ':/Toolbar/Foes' )
        Foes.setIcon( Icon )
        Foes.setMenu( FoeFilter )
        form.SpaceInfo.addWidget( Foes )
    ##
        ZoomLevel = QtGui.QMenu()
        self.Zoom25 = ZoomLevel.addAction( '25%' )
        self.Zoom38 = ZoomLevel.addAction( '38%' )
        self.Zoom50 = ZoomLevel.addAction( '50%' )
        self.Zoom75 = ZoomLevel.addAction( '75%' )
        self.Zoom100 = ZoomLevel.addAction( '100%' )
        self.Zoom125 = ZoomLevel.addAction( '125%' )
        self.Zoom150 = ZoomLevel.addAction( '150%' )
        self.Zoom200 = ZoomLevel.addAction( '200%' )
        self.Zoom400 = ZoomLevel.addAction( '400%' )
        self.Zoom25.setCheckable( True )
        self.Zoom38.setCheckable( True )
        self.Zoom50.setCheckable( True )
        self.Zoom75.setCheckable( True )
        self.Zoom100.setCheckable( True )
        self.Zoom125.setCheckable( True )
        self.Zoom150.setCheckable( True )
        self.Zoom200.setCheckable( True )
        self.Zoom400.setCheckable( True )
        Zoom = QtGui.QToolButton()
        Zoom.setCheckable( False )
        Zoom.setPopupMode( Zoom.InstantPopup )
        Icon = QtGui.QIcon( ':/Toolbar/Zoomlevel' )
        Zoom.setIcon( Icon )
        Zoom.setMenu( ZoomLevel )
        form.SpaceInfo.addWidget( Zoom )               
        
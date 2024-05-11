
from PyQt5 import QtGui, QtCore, QtWidgets
from stars import Stars

import sys
import os



class SpaceInfo :

    def __init__( self, form ) :

        MineFilter = QtWidgets.QMenu(form.SpaceInfo)
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
        Mines = QtWidgets.QToolButton(form.SpaceInfo)
        Mines.setToolTip( 'Show Minefields' )
        Mines.setCheckable( True )
        Mines.setPopupMode( Mines.DelayedPopup )
        Icon = QtGui.QIcon( ':/Toolbar/Mine' )
        Mines.setIcon( Icon )
        Mines.setMenu( MineFilter )
        form.SpaceInfo.addWidget( Mines )
    ##
        self.Paths = QtWidgets.QAction(form)
        self.Paths.setText( 'Set Waypoints' )
        self.Paths.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Paths' )
        self.Paths.setIcon( Icon )
        form.SpaceInfo.addAction( self.Paths )
    ##
        self.Names = QtWidgets.QAction(form)
        self.Names.setText( 'Show Names' )
        self.Names.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Names' )
        self.Names.setIcon( Icon )
        form.SpaceInfo.addAction( self.Names )
    ##
        self.Orbit = QtWidgets.QAction(form)
        self.Orbit.setText( 'Count Ships' )
        self.Orbit.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Orbiting' )
        self.Orbit.setIcon( Icon )
        form.SpaceInfo.addAction( self.Orbit )
    ##
        self.Idle = QtWidgets.QAction(form)
        self.Idle.setText( 'Show Idle Fleets' )
        self.Idle.setCheckable( True )
        Icon = QtGui.QIcon( ':/Toolbar/Waiting' )
        self.Idle.setIcon( Icon )
        form.SpaceInfo.addAction( self.Idle )
    ##
        self.FriendFilter = QtWidgets.QMenu(form.SpaceInfo)
        self.FriendlyDesigns = dict()
        Friends = QtWidgets.QToolButton(form.SpaceInfo)
        Friends.setCheckable( True )
        Friends.setPopupMode( Friends.DelayedPopup )
        Icon = QtGui.QIcon( ':/Toolbar/Friendlies' )
        Friends.setIcon( Icon )
        Friends.setMenu( self.FriendFilter )
        form.SpaceInfo.addWidget( Friends )
    ##
        self.FoeFilter = QtWidgets.QMenu(form.SpaceInfo)
        self.EnemyDesigns = dict()
        self.UpdateEnemyDesigns( [ 'Colony Ships', 'Freighters', 'Scouts', 'Warships', 'Utility Ships', 'Bombers', 'Mining Ships', 'Fuel Transports' ] )
        Foes = QtWidgets.QToolButton(form.SpaceInfo)
        Foes.setCheckable( True )
        Foes.setPopupMode( Foes.DelayedPopup )
        Icon = QtGui.QIcon( ':/Toolbar/Foes' )
        Foes.setIcon( Icon )
        Foes.setMenu( self.FoeFilter )
        form.SpaceInfo.addWidget( Foes )
    ##
        self.ZoomLevel = QtWidgets.QMenu(form.SpaceInfo)
        self.Zoom = dict()
        self.DefineZoomLevel( [ '25', '38', '50', '75', '100', '125', '150', '200', '400' ] )
        ChangeZoom = QtWidgets.QToolButton(form.SpaceInfo)
        ChangeZoom.setCheckable( False )
        ChangeZoom.setPopupMode( ChangeZoom.InstantPopup )
        Icon = QtGui.QIcon( ':/Toolbar/Zoomlevel' )
        ChangeZoom.setIcon( Icon )
        ChangeZoom.setMenu( self.ZoomLevel )
        form.SpaceInfo.addWidget( ChangeZoom )


    def UpdateFriendlyDesigns( self, DesignData ) :

        self.FriendFilter.clear()
        self.AllFriends = self.FriendFilter.addAction( 'All Designs' )
        self.InvertFriends = self.FriendFilter.addAction( 'Invert Filter' )
        self.NoFriends = self.FriendFilter.addAction( 'No Designs' )
        self.FriendFilter.addSeparator()
        self.FriendlyDesigns.clear()
        for NewDesign in DesignData :
            NewAction = self.FriendFilter.addAction( NewDesign )
            NewAction.setCheckable( True )
            self.FriendlyDesigns[ NewDesign ] = NewAction


    def UpdateEnemyDesigns( self, DesignData ) :

        self.FriendFilter.clear()
        self.AllFoes = self.FoeFilter.addAction( 'All Designs' )
        self.InvertFoes = self.FoeFilter.addAction( 'Invert Filter' )
        self.NoFoes = self.FoeFilter.addAction( 'No Designs' )
        self.FoeFilter.addSeparator()
        self.EnemyDesigns.clear()
        for NewDesign in DesignData :
            NewAction = self.FoeFilter.addAction( NewDesign )
            NewAction.setCheckable( True )
            self.EnemyDesigns[ NewDesign ] = NewAction


    def DefineZoomLevel( self, Level ) :

        self.ZoomLevel.clear()
        self.Zoom.clear()
        for NewLevel in Level :
            NewAction = self.ZoomLevel.addAction( NewLevel + '%' )
            NewAction.setCheckable( True )
            self.Zoom[ NewLevel ] = NewAction


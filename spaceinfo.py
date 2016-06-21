
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
        self.FriendFilter = QtGui.QMenu()
        self.FriendlyDesigns = dict()
        Friends = QtGui.QToolButton()
        Friends.setCheckable( True )
        Friends.setPopupMode( Friends.DelayedPopup )
        Icon = QtGui.QIcon( ':/Toolbar/Friendlies' )
        Friends.setIcon( Icon )
        Friends.setMenu( self.FriendFilter )
        form.SpaceInfo.addWidget( Friends )
    ##
        self.FoeFilter = QtGui.QMenu()
        self.EnemyDesigns = dict()
        self.UpdateEnemyDesigns( [ 'Colony Ships', 'Freighters', 'Scouts', 'Warships', 'Utility Ships', 'Bombers', 'Mining Ships', 'Fuel Transports' ] )
        Foes = QtGui.QToolButton()
        Foes.setCheckable( True )
        Foes.setPopupMode( Foes.DelayedPopup )
        Icon = QtGui.QIcon( ':/Toolbar/Foes' )
        Foes.setIcon( Icon )
        Foes.setMenu( self.FoeFilter )
        form.SpaceInfo.addWidget( Foes )
    ##
        self.ZoomLevel = QtGui.QMenu()
        self.Zoom = dict()
        self.DefineZoomLevel( [ '25', '38', '50', '75', '100', '125', '150', '200', '400' ] )
        ChangeZoom = QtGui.QToolButton()
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


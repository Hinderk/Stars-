
""" This module implements the available hull layouts """

from enum import Enum


class Layout(Enum):
    """ Hull layouts available for ship construction """
    MCS = 'Mini Colony-Ship'
    COS = 'Colony-Ship'
    MDM = 'Midget Miner'
    MML = 'Mini Mine-Layer'
    SCT = 'Scout'
    SFR = 'Small Freighter'
    MBO = 'Mini Bomber'
    MIM = 'Mini Miner'
    DTR = 'Destroyer'
    MFR = 'Medium Freighter'
    FTR = 'Fuel-Transport'
    PRV = 'Privateer'
    B17 = 'B-17 Bomber'
    FRI = 'Frigate'
    MIN = 'Miner'
    SFT = 'Super Fuel-Transport'
    LFR = 'Large Freighter'
    MMO = 'Mini Morph'
    ROG = 'Rogue'
    SBO = 'Stealth Bomber'
    CRU = 'Cruiser'
    BCR = 'Battle Cruiser'
    MOR = 'Meta Morph'
    AMI = 'Alien Miner'
    GAL = 'Galleon'
    MAM = 'Maxi Miner'
    BAT = 'Battleship'
    SUF = 'Super Freighter'
    UMI = 'Ultra Miner'
    B52 = 'B-52 Bomber'
    SML = 'Super Mine-Layer'
    DRN = 'Dreadnought'
    NUB = 'Nubian'


from enum import Enum

from layout import Layout as HL  # TODO: Implement the layout!


#  Name   En  We  Pr  Co  El  Bi   Weight Resources  Iro Bor Ger  Cargo  Fuel  Armor  Layout

class Hull(Enum):
    SFR = ['Small Freighter', 0, 0, 0, 0, 0, 0, 25, 20, 12, 0, 17, 70, 130, 25, HL.SFR]
    MFR = ['Medium Freighter', 0, 0, 0, 3, 0, 0, 60, 40, 20, 0, 19, 210, 450, 50, HL.MFR]
    LFR = ['Large Freighter', 0, 0, 0, 8, 0, 0, 125, 100, 35, 0, 21, 1200, 2600, 150, HL.LFR]
    SUF = ['Super Freighter', 0, 0, 0, 13, 0, 0, 175, 125, 45, 0, 21, 3000, 8000, 400, HL.SUF]
    SCT = ['Scout', 0, 0, 0, 0, 0, 0, 8, 10, 4, 2, 4, 0, 50, 20, HL.SCT] 
    FRI = ['Frigate', 0, 0, 0, 6, 0, 0, 8, 12, 4, 2, 4, 0, 125, 45, HL.FRI]
    DTR = ['Destroyer', 0, 0, 0, 3, 0, 0, 30, 35, 15, 3, 5, 0, 280, 200, HL.DTR]
    CRU = ['Cruiser', 0, 0, 0, 9, 0, 0, 90, 85, 40, 5, 8, 0, 600, 700, HL.CRU]
    BCR = ['Battle Cruiser', 0, 0, 0, 10, 0, 0, 120, 120, 55, 8, 12, 0, 1400, 1000, HL.BCR]
    BAT = ['Battleship', 0, 0, 0, 13, 0, 0, 222, 225, 120, 25, 20, 0, 2800, 2000, HL.BAT]
    DRN = ['Dreadnought', 0, 0, 0, 16, 0, 0, 250, 275, 140, 30, 25, 0, 4500, 4500, HL.DRN]
    PRV = ['Privateer', 0, 0, 0, 4, 0, 0, 65, 50, 50, 3, 2, 250, 650, 150, HL.PRV]
    ROG = ['Rogue', 0, 0, 0, 8, 0, 0, 75, 60, 80, 5, 5, 500, 2250, 450, HL.ROG]
    GAL = ['Galleon', 0, 0, 0, 11, 0, 0, 125, 105, 70, 5, 5, 1000, 2500, 900, HL.GAL]
    MCS = ['Mini Colony-Ship', 0, 0, 0, 0, 0, 0, 8, 3, 2, 0, 2, 10, 150, 10, HL.MCS]
    COS = ['Colony-Ship', 0, 0, 0, 0, 0, 0, 20, 20, 10, 0, 15, 25, 200, 20, HL.COS]
    MBO = ['Mini Bomber', 0, 0, 0, 1, 0, 0, 28, 35, 20, 5, 10, 0, 120, 50, HL.MBO]
    B17 = ['B-17 Bomber', 0, 0, 0, 6, 0, 0, 69, 150, 55, 10, 10, 0, 400, 175, HL.B17]
    SBO = ['Stealth Bomber', 0, 0, 0, 8, 0, 0, 70, 175, 55, 10, 15, 0, 750, 225, HL.SBO]
    B52 = ['B-52 Bomber', 0, 0, 0, 15, 0, 0, 110, 280, 90, 15, 10, 0, 750, 450, HL.B52]
    MDM = ['Midget Miner', 0, 0, 0, 0, 0, 0, 10, 20, 10, 0, 3, 0, 210, 100, HL.MDM]
    MIM = ['Mini Miner', 0, 0, 0, 2, 0, 0, 80, 50, 25, 0, 6, 0, 210, 130, HL.MIM]
    MIN = ['Miner', 0, 0, 0, 6, 0, 0, 110, 110, 32, 0, 6, 0, 500, 475, HL.MIN]
    MAM = ['Maxi Miner', 0, 0, 0, 11, 0, 0, 110, 140, 32, 0, 6, 0, 850, 1400, HL.MAM]
    UMI = ['Ultra Miner', 0, 0, 0, 14, 0, 0, 100, 130, 30, 0, 6, 0, 1300, 1500, HL.UMI]
    FTR = ['Fuel-Transport', 0, 0, 0, 4, 0, 0, 12, 50, 10, 0, 5, 0, 750, 5, HL.FTR]
    SFT = ['Super Fuel-Transport', 0, 0, 0, 7, 0, 0, 111, 70, 20, 0, 8, 0, 2250, 12, HL.SFT]
    MML = ['Mini Mine-Layer', 0, 0, 0, 0, 0, 0, 10, 20, 8, 2, 5, 0, 400, 60, HL.MML]
    SML = ['Super Mine-Layer', 0, 0, 0, 15, 0, 0, 30, 30, 20, 3, 9, 0, 2200, 1200, HL.SML]
    NUB = ['Nubian', 0, 0, 0, 26, 0, 0, 100, 150, 75, 12, 12, 0, 5000, 5000, HL.NUB]
    MMO = ['Mini Morph', 0, 0, 0, 8, 0, 0, 70, 100, 30, 8, 8, 150, 400, 250, HL.MMO]
    MOR = ['Meta Morph', 0, 0, 0, 10, 0, 0, 85, 120, 50, 12, 12, 300, 700, 500, HL.MOR]
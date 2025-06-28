
""" This module defines the various lesser traits a faction can exhibit. """

from enum import Enum


class Perks(Enum):
    """ List of perks factions may enjoy or endure """
    IFE = ['Improved Fuel Efficiency', 'This gives You the \'Fuel Mizer\' and \'Galaxy Scoop\' '
           'engines and increases Your starting Propulsion technology by 1 level. All engines '
           'use 15% less fuel.', 1]
    TTF = ['Total Terraforming', 'Allows You to terraform by investing solely in the field of '
           'Biotechnology. You may terraform a variable up to 30%. Terraforming costs 30% '
           'less.', 2]
    ARM = ['Advanced Remote Mining', 'Gives You three additional mining hulls and two new '
           'robots. You will start the game with two Midget-Miners. You can\'t pick \'Only '
           'Basic Remote Mining\' with this option.', 3]
    ISB = ['Improved Starbases', 'Gives You two new starbase designs. The \'Stardock\' '
           'allows You to build light ships. The \'Ultra Station\' is a formidable weapons '
           'platform. Your starbases cost 20% less & are 20% cloaked.', 4]
    GRE = ['Generalized Research', 'Your race takes a holistic approach to research. Only '
           'half of the resources dedicated to research will be applied to the current '
           'field of research; however, 15% of the total will be applied to all other '
           'fields.', 5]
    URE = ['Ultimate Recycling', 'When You scrap a fleet at a starbase, You recover 90% of '
           'the minerals and some of the resources. The resources are availabe for use '
           'the next year. Scrapping at a planet gives You half the starbase amount.', 6]
    MAL = ['Mineral Alchemy', 'Allows You to turn resources into minerals four times more '
           'efficiently than other races. This may be performed at any planet You own.', 7]
    NRS = ['No Ramscoop Engines', 'No engines which travel at Warp 5 or greater burning no '
           'fuel will be available. However, the \'Interspace-10\' drive can be developed. '
           'It travels at Warp 10 without taking damage.', 8]
    CHE = ['Cheap Engines', 'You can throw engines together at half cost; however, at speeds '
           'in excess of Warp 6, there is a 10% chance the engines won\'t engage. You start '
           'the game with Propulsion technology one level higher than You would otherwise.', 9]
    BRM = ['Only Basic Remote Mining', 'The only mining ship available to You will be the '
           '\'Mini-Miner\'. This trait overrides \'Advanced Remote Mining\'. Your maximum '
           'population per planet is increased by 10%.', 10]
    NAS = ['No Advanced Scanners', 'No planet penetrating scanners will be available to You. '
           'However, conventional scanners will have their range doubled.', 11]
    LSP = ['Low starting population', 'You will start the game with 30% fewer colonists.', 12]
    BET = ['Bleeding edge technology', 'Newly researched technology cost twice as much to '
           'build. As soon as You exceed all of the technology requirements by one level, '
           'the cost drops back to normal. Miniaturization occurs at 5% a level and pegs '
           'at 80%.', 13]
    RSH = ['Regenerating shields', 'All shields are 40% stronger than their listed rating. '
           'They regain 10% of maximum strength after every round of battle. However, Your '
           'armor will only have 50% of its rated strength.', 14]

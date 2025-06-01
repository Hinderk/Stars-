
""" This module implements the primary traits of any player faction """

from enum import Enum



class Traits(Enum):
    """ These are the possible primary traits of a faction """
    NO = ['', '', -1]
    HE = ['Hyper-Expansion', 'You must expand to survive. You are given a small and cheap '
          'colony hull and an engine which travels at Warp-6 using no fuel. Your species '
          'will grow at twice the growth rate You select on page 4 of the wizard. However, '
          'the maximum population for a given planet is cut in half. The completely '
          'flexible Meta-Morph hull will be available only to Your faction.', 0]
    ST = ['Super Stealth', 'You can sneak through enemy territory and execute stunning '
          'surprise attacks. You are given top-drawer cloaks and all Your ships have 75% '
          'cloaking built in. Cargo does not decrease Your cloaking abilities. The Stealth '
          'Bomber and the Rogue hull are at Your disposal, as are a scanner, a shield and '
          'armor with stealthy properties. Two scanners which allow You to steal minerals '
          'from enemy fleets and planets are also available. You may safely travel through '
          'mine fields at one warp speed faster than other factions.', 2]
    WM = ['War Monger', 'You rule the battlefield. Your colonists attack better, Your '
          'ships are faster in battle and You can build weapons 25% cheaper than other '
          'factions. You start the game with a knowledge of Tech-6 Weapons and Tech-1 in '
          'Energy and Propulsion. Unfortunately, Your faction doesn\'t understand the '
          'necessity of building any but the most basic planetary defenses or the '
          'utility of mine fields.', 5]
    CA = ['Claim Adjuster', 'You are an expert at fiddling with planetary environments. '
          'You start the game with Tech-6 in Biotechnology and a ship capable of '
          'terraforming planets from orbit. You can arm Your ships with bombs that degrade '
          'the habitability of enemy worlds. Terraforming costs You nothing and planets '
          'You leave revert to their original environments. Planets You own have up to a '
          '10% chance of permanently improving an environment variable by 1% per year.', 7]
    IS = ['Inner Strength', 'You are strong and hard to defeat. Your colonists repeal '
          'attacks better, Your ships recover faster, You have special battle devices that '
          'protect Your ships and can lay Speed Trap mine fields. You have a device that '
          'acts as both a shield and armor. Your peace loving people refuse to build smart '
          'bombs. Planetary defenses cost You 40% less, though weapons cost You 25% more. '
          'Your colonists are able to reproduce while being transported by Your fleets.', 9]
    SD = ['Space Demolition', 'You are an expert in laying mine fields. You have a vast '
          'array of mine types at Your disposal and two unique hull designs which are '
          'made for mine dispersal. Your mine fields act as scanners and You have the '
          'ability to detonate Your own Standard mine fields remotely. You may safely '
          'travel through enemy mine fields two warp speeds faster than the stated limits. '
          'You start the game with two mine laying ships and Tech-2 in Biotechnology and '
          'Propulsion.', 1]
    PP = ['Packet Physics', 'Your faction excels at accelerating mineral packets to '
          'distant planets. You start with a Warp-5 accelerator at Your home starbase '
          'and Tech-4 in Energy. You will eventually be able to fling packets at the '
          'mind numbing speed of Warp-13. You can fling smaller packets and all of '
          'Your packets have penetrating scanners embedded in them. You will start the '
          'game owning a second planet some distance away unless the size of the galaxy '
          'is tiny. Packets You fling that aren\'t fully caught have a chance of '
          'terraforming the target planet', 4]
    IT = ['Interstellar Traveller', 'Your faction excels at building stargates. You '
          'begin the game with Tech-5 in Propulsion and Construction. You start out with '
          'a second planet unless the size of the galaxy is tiny. Both these planets '
          'feature stargates. Eventually, You may build stargates which have unlimited '
          'capabilities. Stargates cost You 25% less to build. Your faction scans any '
          'enemy planet with a stargate automatically if that planet is within range of '
          'one of Your stargates. Exceeding the safety limits of stargates is less '
          'likely to kill Your ships.', 6]
    AR = ['Alternate Reality', 'Your species developed in an alternate plane. Your '
          'people cannot survive on planets and live in orbit on Your starbases which '
          'are 20% cheaper to build. You cannot build planetary installations, but '
          'Your people have an intrinsic ability to mine and scan for enemy fleets. '
          'You can mine Your own worlds remotely. If a starbase is destroyed, all '
          'Your colonists aboard are killed. The growth of the population is '
          'determined by the type of starbase which is orbiting Your planet. '
          'Eventually, You will be able to build the Death Star.', 8]
    JT = ['Jack of All Trades', 'Your faction does not specialise in a single area. '
          'You start the game with Tech-3 in all areas and an assortment of ships. '
          'Your scout, destroyer and frigate hulls integrate a penetrating scanner '
          'which grows more powerful as You research new levels in Electronics. Your '
          'worlds can sustain a population density that is 20% greater than usual.', 10]



class SecondaryTraits(Enum):
    """ List of secondary traits factions may enjoy or endure """
    NONE = 0         # No specific perks
    IFE = 1          # Improved fuel efficiency
    NRSE = 2         # No ramscoop engines
    TTF = 3          # Total terraforming
    CHE = 4          # Cheap engines
    ARM = 5          # Advanced remote mining
    OBRM = 6         # Only basis remote mining
    ISB = 7          # Improved starbases
    NAS = 8          # No advanced scanners
    GRE = 9          # Generalized research
    LSP = 10         # Low starting population
    URE = 11         # Ultimate Recycling
    BET = 12         # Bleeding edge technology
    MAL = 13         # Mineral alchemy
    RSH = 14         # Regenerating shields
    ROB = 15         # Steal freight
    HIDE = 16        # Improve ship cloaking

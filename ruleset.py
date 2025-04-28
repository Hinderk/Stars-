
import random
import math

from guiprop import GuiProps
from scanner import Model


# This class facilities the generation of a random "Stars!" universe ...

class Ruleset(random.Random):

    f_id0 = 0   # Define the index of the faction controlled by the player ...


    def minefield_decay(f_id):
        return 0.02


    def cloaking_ratio(cloaking, weight):
        cloak = cloaking / weight
        if cloak <= 100:
            c = cloak / 2
        else:
            cloak -= 100
            if cloak <= 200:
                c = 50 + cloak / 8
            else:
                cloak -= 200
                if cloak <= 312:
                    c = 75 + cloak / 24
                else:
                    cloak -= 312
                    if cloak <= 512:
                        c = 88 + cloak / 64
                    elif cloak < 768:
                        c = 96
                    elif cloak < 1000:
                        c = 97
                    else:
                        c = 98
        return c / 100


    name_list = ["Aarhus", "Abderhalden", "Aberdonia", "Abilunon", "Abkhazia",
              "Achaemenides", "Adachi", "Adelheid", "Admetos", "Adonis",
               "Aegina", "Agamemnon", "Agasthenes", "Aharon", "Akhmatova",
               "Albellus", "Algoa", "Anhui", "Antenor", "Anteros", "Apollo",
               "Arnenordheim", "Arrhenius", "Artemis", "Aurelia", "Barkhatova",
               "Belgorod", "Bellerophon", "Caldeira", "Calliope", "Cancello",
               "Cassini", "Cebriones", "Cesaro", "Chaonis", "Charybdis",
               "Chione", "Chodas", "Chromios", "Clusius", "Condruses",
               "Cygania", "Cyllarus", "Daedalus", "Damocles", "Danae",
               "Deineka", "Deiphobus", "Demeter", "Demophon", "Deucalion",
               "Diomedes", "Dione", "Dresda", "Durkheim", "Echemmon", "Echion",
               "Egeria", "Enid", "Ennomos", "Eos", "Epimetheus", "Eriepa",
               "Esipov", "Eumelos", "Faerra", "Feros", "Firneis", "Fortuna",
               "Fraethi", "Gaea", "Galanthus", "Galatea", "Galilea", "Ganesa",
               "Ganymed", "Garuda", "Garumna", "Gelria", "Ghoshal", "Giada",
               "Ginestra", "Ginevra", "Giomus", "Gethsemane", "Gromov", "Gyas",
               "Hadano", "Hakone", "Halaesus", "Halitherses", "Halleria",
               "Hamina", "Hamra", "Hapke", "Hecuba", "Helenos", "Hercynia",
               "Hesperia", "Hirai", "Hygiea", "Hypatia", "Icarion", "Idaios",
               "Iduna", "Ikeda", "Illyria", "Ilos", "Inari", "Ishtar",
               "Ithaka", "Jacobi", "Jindra", "Jitka", "Junttura", "Jyuro",
               "Kaburaki", "Kahnia", "Kainar", "Kaizuka", "Kanroku",
               "Kapaneus", "Karlstad", "Kaseda", "Kasuga", "Kimura",
               "Kiruna", "Klotho", "Klythios", "Komm", "Koronis",
               "Kressida", "Kron", "Krystosek", "Kudara", "Kypria",
               "Lagerros", "Landau", "Laupheim", "Lautaro", "Leukothea",
               "Liberia", "Liguria", "Liia", "Lingas", "Liriope",
               "Lotharos", "Lukion", "Lycomede", "Lyubov", "Magion",
               "Maichin", "Maisica", "Makhaon", "Makino", "Malhotra",
               "Mansurova", "Manulis", "Maresjev", "Matsuda", "Meduna",
               "Melanthios", "Melchior", "Memnon", "Menabrea", "Merionis",
               "Minerva", "Minox", "Mirrin", "Mitaka", "Mjolnir", "Moraes",
               "Naeve", "Nakai", "Nemiro", "Nephthys", "Niebuhr", "Nihondaira",
               "Nisyros", "Nocturna", "Nortia", "Novalis", "Obrant", "Odessa",
               "Ogarev", "Ogiria", "Oineus", "Okuda", "Oleyuria", "Orelskaya",
               "Orestes", "Oriani", "Orpheus", "Ortigara", "Osipovia",
               "Paeonia", "Palatia", "Palisana", "Parvamenon", "Pasertia",
               "Peleus", "Pelion", "Peneleos", "Penza", "Peraga", "Periphas",
               "Petronius", "Phaedra", "Phemios", "Piironen", "Pindarus",
               "Plescia", "Praetorius", "Praxedis", "Prieska", "Prometheus",
               "Prylis", "Pyrrha", "Ra-Shalom", "Rabelais", "Rakos", "Rentaro",
               "Rezia", "Rhodesia", "Rodari", "Roehla", "Rudra", "Ryzhov",
               "Saitama", "Sakharov", "Salopia", "Sapientia", "Saskia",
               "Saturna", "Segovia", "Seleucus", "Semphyra", "Serpieri",
               "Sethos", "Sibelius", "Sipiera", "Smirnova", "Sostero",
               "Spahr", "Spiraea", "Sthenelos", "Suleika", "Talthybius",
               "Tantalus", "Tataria", "Tauris", "Telesio", "Tercidina",
               "Terradas", "Thekla", "Themis", "Thereus", "Thessalia",
               "Thorenia", "Thrasymede", "Tirion", "Tirol", "Titania",
               "Tolosa", "Tuscia", "Tyndareus", "Tyr", "Utopia", "Vanadis",
               "Vangelis", "Vargas", "Varuna", "Velimir", "Veritas",
               "Vietoris", "Vitaris", "Waltari", "Weierstrass", "Wiesenthal",
               "Xenia", "Xenophon", "Yakutia", "Yasuda", "Yoshino", "Yugra",
               "Zanstra", "Zenbei", "Zernike", "Zykina", "Alcari", "Kailey",
               "Achernar", "Acrux", "Acubens", "Adhafera", "Adhara", "Agena",
               "Albali", "Albireo", "Alchibah", "Alcor", "Alcyone", "Aldebaran",
               "Alderamin", "Alfirk", "Algedi", "Algenib", "Algieba", "Algol",
               "Alhena", "Alioth", "Alkaid", "Alkalurops", "Alkes", "Almaak",
               "Al Na'ir", "Alnasl", "Alnilam", "Alnitak", "Al Niyat",
               "Alphard", "Alphecca", "Alpheratz", "Alrisha", "Alshain",
               "Altair", "Alterf", "Aludra", "Altais", "Alula", "Alya",
               "Ancha", "Ankaa", "Antares", "Arcturus", "Arkab", "Arneb",
               "Ascella", "Asellus", "Antilicus", "Aspidiske", "Asterope",
               "Atik", "Atlas", "Atria", "Avior", "Azha", "Baten Kaitos",
               "Becrux", "Beid", "Bellatrix", "Benetnasch", "Betelgeuse",
               "Biham", "Canopus", "Capella", "Caph", "Castor", "Cebalrai",
               "Celaeno", "Chara", "Cheleb", "Cynos", "Chort", "Cor Caroli",
               "Dabih", "Deneb", "Deneb Algedi", "Deneb Kaitos", "Denebola",
               "Diphda", "Dnoces", "Dschubba", "Dubhe", "Edasich", "Electra",
               "El Nath", "Eltanin", "Enif", "Errai", "Fomalhaut", "Furud",
               "Gacrux", "Giausar", "Gienah", "Girtab", "Gomeisa", "Graffias",
               "Grumium", "Hadar", "Hamal", "Homam", "Izar", "Kadalis",
               "Kadusar", "Kirtab", "Kaus", "Keid", "Kitalpha", "Kokab",
               "Kornephoros", "Lesath", "Maia", "Marfik", "Markab", "Matar",
               "Mebsuta", "Media", "Megrez", "Meissa", "Menkib", "Menkalinan",
               "Menkar", "Merope", "Mesarthim", "Miaplacidus", "Mimosa",
               "Mintaka", "Mira", "Mirak", "Mirfak", "Mirzam", "Mizar",
               "Mothallah", "Muhlifain", "Muliphen", "Muphrid", "Muscida",
               "Naos", "Nashira", "Navi", "Nekkar", "Nihal", "Nasl", "Nusakan",
               "Phact", "Phad", "Phecda", "Pherkad", "Pleione", "Polaris",
               "Pollux", "Porrima", "Procyon", "Propus", "Pulcherrima",
               "Rasalgethi", "Rasalhague", "Ras Elased", "Rastaban",
               "Regor", "Regulus", "Rigel", "Rigil Kent", "Rigil Kentaurus",
               "Rotanev", "Rukba", "Rukbat", "Sabik", "Sadalachbia",
               "Sadalbari", "Sadalmelik", "Sadalsuud", "Sadatoni", "Sadr",
               "Saiph", "Sargas", "Scheat", "Schedar", "Seginus", "Shaula",
               "Sheliak", "Sheratan", "Sirius", "Situla", "Skat", "Spica",
               "Sterope", "Sualocin", "Suhail", "Sulafat", "Syrma",
               "Talitha", "Tania", "Tiraph", "Tarazed", "Taygeta",
               "Tegmine", "Thuban", "Unkalhai", "Vega", "Vindematrix",
               "Wasat", "Wazn", "Wezen", "Yed", "Yildun", "Zaniah",
               "Zaurak", "Zavijava", "Zosma", "Zubenelgenubi",
               "Zubeneschamali", "Kitara", "Talis", "Sol", "Sikarra",
               "Golganis", "Targus", "Vione", "Kronac", "Draconis"]


    def __init__(self, seed=128):
        super(self.__class__, self).__init__(seed)
        self.seed = seed
        self.location = []
        self.planet_names = list(Ruleset.name_list)


    def _FindClosest(self, x0, y0):
        dist = 1e20
        for [x, y] in self.location:
            d = (x - x0) * (x - x0) + (y - y0) * (y - y0)
            if d < dist:
                dist = d
        return math.sqrt(dist)


    def Random(self, min_val, max_val, optimum):
        return self.triangular(min_val, max_val, optimum)


    def find_name(self):
        try:
            name = self.choice(self.planet_names)
            self.planet_names.remove(name)
            return name
        except:
            return None


    def find_position(self):
        rmin = GuiProps.planet_distance / GuiProps.xscale
        xlim = self.xmax()
        ylim = self.ymax()
        retries = 0
        while retries < 128:
            x = self.randrange(-xlim, xlim)
            y = self.randrange(-ylim, ylim)
            r = self._FindClosest(x, y)
            if r > self.rmin() and r > rmin:
                self.location.append([x, y])
                return [x, y]
        return None


    def first_year(self):
        return 2400


    def get_population_ceiling():
        return 400000                    # TODO: Species dependent model


    def first_scanner(self):
#    return Model.Scoper150
        return Model.Snooper500X

    def get_max_resources(self):
        return 100.0

    def get_min_resources(self):
        return 5.0

    def get_resources(self):
        return 70.0

    def planet_count():
        return 15

    def xmax(self):
        return 1000

    def ymax(self):
        return 1000

    def rmin(self):
        return 20


    def get_number_of_players(self):  # This must depend on the size of the star map
        return 4

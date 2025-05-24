
""" This module implements a class to encode ship designs """



class Design:

    """ This class is used to specicfy ship designs & properties """

    hull_design = {}
    design_counter = {}
    latest_index = 0

    # fID : foe identifier ...

    def __init__(self, f_id, hull):
        self.f_id = f_id
        self.index = (f_id, self.latest_index)
        self.hull = hull
        self.system = []
        name = hull.value[1]
        if (name,f_id) in self.design_counter:
            nr = self.design_counter[(name, f_id)]
            self.name = name + ' Mk ' + str(nr)
            self.design_counter[(name, f_id)] = nr + 1
        else:
            self.name = name + ' Mk 1'
            self.design_counter[(name, f_id)] = 1
        self.picture_index = hull.value[0]
        self.latest_index += 1
        Design.hull_design[self.index] = self


    def get_design_name(self):
        """ Return the name of the ship design """
        return self.hull.value[1]


    def get_picture_index(self):
        """ The returned index may be used to visualize the ship """
        return self.picture_index


    def compute_battle_rating(self):
        """ Compute the battle rating of the ship design """
        return 1

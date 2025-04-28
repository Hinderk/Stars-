
from hull import Hull


class Design:

    hull_design = dict()
    design_counter = dict()
    latest_index = 0

    def get_design(index):
        return Design.hull_design.get(index)

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
        return self.hull.value[1]

    def get_picture_index(self):
        return self.picture_index

    def compute_battle_rating(self):
        return 1

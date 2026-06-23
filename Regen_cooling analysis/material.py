class SS308L:

    def __init__(self):

        self.k = 16.0

        self.max_outer_wall_temp = 600.0

        self.max_inner_wall_temp = 1200.0

    def conductivity(self, T=None):

        return self.k

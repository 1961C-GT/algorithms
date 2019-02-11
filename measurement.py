class Measurement:
    def __init__(self, node1, node2, dist, err=0):
        self.node1 = node1
        self.node2 = node2
        self.dist = dist
        self.err = err
        self.cleared = False
        self.confidence = 1.0
        self.opinions = 1
        if self.err == 0:
            self.calc_error()

    def calc_error(self):
        self.err = self.dist * 0.01

    def __str__(self):
        return '{:12s} ->  {:12s}: {:.3f} • {:.3f}'.format(str(self.node1), str(self.node2), self.dist, self.confidence)

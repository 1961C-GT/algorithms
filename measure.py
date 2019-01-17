class Measurement:
    def __init__(self, node1, node2, dist, unc=0):
        self.node1 = node1
        self.node2 = node2
        self.dist = dist
        self.unc = unc
        if self.unc == 0:
            self.calcUncertainty()

    def calcUncertainty(self):
        self.unc = self.dist * 0.01

    def __str__(self):
        return str(self.node1) + " -> " + str(self.node2) + " : " + str(self.dist) + "+" + str(self.unc)

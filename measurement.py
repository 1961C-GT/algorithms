class Measurement:
    def __init__(self, node1, node2, dist, err=0):
        self.node1 = node1
        self.node2 = node2
        self.dist = dist
        self.err = err
        if self.err == 0:
            self.calcError()

    def calcError(self):
        self.err = self.dist * 0.01

    def __str__(self):
        return str(self.node1) + " -> " + str(self.node2) + ": " + str(self.dist) + " ± " + str(self.err)

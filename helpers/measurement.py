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

    def getResolvedNode(self):
        if self.isResolved():
            return False
        if self.node1.isResolved():
            return self.node1
        elif self.node2.isResolved():
            return self.node2
        return None

    def getUnResolvedNode(self):
        if self.isResolved():
            return False
        if self.node1.isResolved():
            return self.node2
        elif self.node2.isResolved():
            return self.node1
        return None

    def getNodePair(self):
        res_node = self.getResolvedNode()
        if res_node is None or res_node == False:
            return res_node
        tgt_node = None
        if res_node == self.node1:
            tgt_node = self.node2
        else:
            tgt_node = self.node1

        return (res_node, tgt_node)

    def isResolved(self):
        return self.node1.isResolved() and self.node2.isResolved()

    def __str__(self):
        return '{:12s} ->  {:12s}: {:.3f} • {:.3f}'.format(str(self.node1), str(self.node2), self.dist, self.confidence)

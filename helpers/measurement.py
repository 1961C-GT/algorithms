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

    def get_resolved_node(self):
        if self.is_resolved():
            return False
        if self.node1.is_resolved():
            return self.node1
        elif self.node2.is_resolved():
            return self.node2
        return None

    def get_unresolved_node(self):
        if self.is_resolved():
            return False
        if self.node1.is_resolved():
            return self.node2
        elif self.node2.is_resolved():
            return self.node1
        return None

    def get_node_pair(self):
        res_node = self.get_resolved_node()
        if res_node is None or res_node is False:
            return res_node
        if res_node == self.node1:
            tgt_node = self.node2
        else:
            tgt_node = self.node1
        return res_node, tgt_node

    def is_resolved(self):
        return self.node1.is_resolved() and self.node2.is_resolved()

    def __str__(self):
        return '{:12s} ->  {:12s}: {:.3f} . {:.3f}'.format(str(self.node1), str(self.node2), self.dist, self.confidence)

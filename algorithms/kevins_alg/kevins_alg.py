from algorithms.algorithm import Algorithm

# > python3 main.py node_defs.csv raw_data.csv kevins_alg


class kevins_alg(Algorithm):
    def __init__(self, nodes):
        super().__init__(nodes)

    def process(self, callback, canvas):

        # Print each measurement from the nodes
        for key, node in self.nodes.items():
            for m in node.get_measurements():
                print(m)

        # Done!
        callback()

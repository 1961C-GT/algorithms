from Algorithms.algorithm import Algorithm

# > python3 main.py node_defs.csv raw_data.csv example_alg

class example_alg(Algorithm):
    def __init__(self, node_arr):
        super().__init__(node_arr)

    def process(self, callback):
        for key,node in self.node_arr.items():
            for m in node.get_measurements():
                print(m)
        self.node_arr['A1'].set_position(50, 50)

        callback()

from algorithm import Algorithm

# > python3 main.py points.csv example_alg

class example_alg(Algorithm):
    def __init__(self, node_arr):
        super().__init__(node_arr)

    def process(self):
        for key,node in self.node_arr.items():
            for m in node.getMeasurements():
                print(m)
        self.node_arr['A1'].setPosition(50, 50)

from Algorithms.algorithm import Algorithm

# > python3 main.py node_defs.csv raw_data.csv example_alg

class example_alg(Algorithm):
    def __init__(self, node_arr):
        super().__init__(node_arr)

    def process(self, callback, canvas):
        # Example direct canvas interaction
        canvas.create_circle(100, 100, 10, fill="red")

        # Print each measurement from the nodes
        for key,node in self.node_arr.items():
            for m in node.get_measurements():
                print(m)

        # Set the position of one of the nodes
        self.node_arr['A1'].set_position(50, 50)

        # Done!
        callback()

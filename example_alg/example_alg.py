from algorithms.algorithm import Algorithm


# > python3 main.py random example_alg


class example_alg(Algorithm):
    def __init__(self, nodes):
        super().__init__(nodes)

    def process(self, callback):
        # Print each measurement from the nodes
        for key, node in self.nodes.items():
            for m in node.get_measurements():
                print(m)

        # Set the position of one of the nodes
        print(self.nodes)
        self.nodes['3'].set_position(50, 50)

        # canvas.connect_nodes_guess(self.nodes['1'], self.nodes['2'], text="test", color="red", dashed=False)
        # canvas.connect_nodes_guess(self.nodes['3'], self.nodes['2'])
        # canvas.circle_node_guess(self.nodes['2'], 300, text="Test Zone", dashed=True, fill="", outline="orange")
        # canvas.circle_area(1000, 1500, 150, text="Custom Area")

        # Done!
        callback()

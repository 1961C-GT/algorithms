from algorithms.algorithm import Algorithm

# > python3 main.py node_defs.csv raw_data.csv example_alg


class example_alg(Algorithm):
    def __init__(self, nodes):
        super().__init__(nodes)

    def process(self, callback, canvas):
        # Example direct canvas interaction
        # canvas.create_circle(100, 100, 10, fill="red")
        # canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
        # canvas.create_rectangle(50, 25, 150, 75, fill="blue")
        # canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

        # Print each measurement from the nodes
        for key, node in self.nodes.items():
            for m in node.get_measurements():
                print(m)

        # Set the position of one of the nodes
        print(self.nodes)
        self.nodes['3'].set_position(50, 50)

        canvas.connect_nodes_guess(self.nodes['1'], self.nodes['2'], text="test", color="red", dashed=False)
        canvas.circle_node_guess(self.nodes['2'], 300, text="Test Zone", dashed=True, fill="", outline="orange")

        # Done!
        callback()

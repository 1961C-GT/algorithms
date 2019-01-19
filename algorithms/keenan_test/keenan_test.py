from algorithms.algorithm import Algorithm
from algorithms.algorithm import Vector2
from algorithms.algorithm import Intersection
import math

# > python3 main.py random example_alg

class keenan_test(Algorithm):
    def __init__(self, nodes):
        super().__init__(nodes)

    def process(self, callback, canvas):
        # Print each measurement from the nodes
        for key, node in self.nodes.items():
            if node.is_base:
                print(node)
                real = node.get_real_position()
                node.set_position(real[0], real[1])
                for m in node.get_measurements():
                    print(m)



        base1 = self.nodes['1']
        base2 = self.nodes['2']

        print()

        # print('M0',base1.get_measurements()[1])
        # print('M0',base2.get_measurements()[1])

        P1 = base1.get_real_position_vec()
        P2 = base2.get_real_position_vec()
        r1 = base1.get_measurements()[1].dist
        canvas.circle_node_guess(base1, r1, outline="orange")
        r2 = base2.get_measurements()[1].dist
        canvas.circle_node_guess(base2, r2, outline="orange")
        (v1, v2) = Intersection(P1, P2, r1, r2)

        canvas.create_circle(v1.x, v1.y, 20, outline="", fill="red")


        self.nodes['3'].set_position_vec(v2)


        # Done!
        callback(render=True)

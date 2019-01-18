from algorithms.algorithm import Algorithm
from scipy.optimize import minimize
from scipy.spatial.distance import pdist
import math

# > python3 main.py <data set> drct_trng

# Implementation of https://www.alanzucconi.com/2017/03/13/positioning-and-trilateration/


def mse(x, base_nodes, node_id):
    mse = 0.0
    for base_node in base_nodes:
        distance = base_node.get_measurement(node_id).dist
        distance_calculated = float(
            math.sqrt(math.pow(base_node.x - x[0], 2) + math.pow(base_node.y - x[1], 2)))
        mse += math.pow(distance_calculated - distance, 2.0)
    return mse / len(base_nodes)


class drct_trng(Algorithm):
    def __init__(self, nodes):
        super().__init__(nodes)

    def process(self, callback, canvas):

        base_nodes = list(filter(lambda n: n.is_base, self.nodes.values()))
        for n in base_nodes:
            print("Base node: {n} @ {p}".format(n=n, p=n.get_position()))

        n1 = [m.node2 for m in base_nodes[0].get_measurements()]
        n2 = [m.node2 for m in base_nodes[1].get_measurements()]
        drct_trng_nodes = set(n1).intersection(n2)
        for n in drct_trng_nodes:
            print("DT node: {n}".format(n=n))
            result = minimize(
                mse,                        # The error function
                (10, 50),                     # The initial guess
                args=(base_nodes, n.id))    # Additional parameters for error func
            self.nodes[n.id].set_position(result.x[0], result.x[1])

        # Done!
        print("Done.")
        callback()

from algorithms.algorithm import Algorithm
from algorithms.algorithm import Vector2
from algorithms.algorithm import Intersection
from directTriangulation import DirectTriangulation, Cluster
import math


# > python3 main.py random example_alg


class multi_tri(Algorithm):
    def __init__(self, nodes):
        super().__init__(nodes)
        self.measure_list = []
        self.resolved_nodes = [nodes['1'], nodes['2']]  # Known

    def process(self, callback, canvas):
        ###### Steps:
        # 1) Generate a list of measurements, ensuring that no duplicates
        #    exist. If they do, average the values.
        # 2) Apply raw confidence score based on each measurement distance
        # 3) Calibrate measurements based on RSSI?
        # 4) Generate all guesses for all nodes using only measurements from
        #    the resolved nodes
        #    4.1) Get all measurements for which one of the nodes is a
        #         resolved node
        #    4.2) Get a list of pairs of measurements from the previous list
        #         for which each measurement orgniates from a resolved node
        #         and terminates at a single un-resolved node
        #    4.3) Use triangulation to form two guesses, and store them in
        #         the un-resolved node (using triangulation object)
        #    4.4) Repeat until all combinations are tried
        #    4.5) Remove guesses that exist outside the world-border
        # 5) Parse through each un-resolved node to resolve position (Need either
        #    1 direct triangulation object with a single guess, or greater than 1
        #    direct triangulation object. If not the case, jump to ~5)
        #    5.1) Go though each guess in the first triangulation object (key)
        #         5.1.1) Go though each other triangulation object and get
        #                one guess from each that is closest to the key guess
        #         5.1.2) Set guess cluster aside
        #         5.1.3) Go back to 5.1.1 until no more guesses
        #    5.2) Find the radius and center of each cluster (use quality)
        #    5.3) Pick the guess that has the smallest radius
        #    5.4) If that guess is larger than a cutoff radius, node is un-resolved.
        #         (Should we go to another ~ section?)
        #    5.5) Otherwise set location and move it to resolved
        # ~5) (Delay until after step 7) Case where exactly 1 direct triangulation
        #     exists, so we have to preform
        #     an educated guess
        #     ~5.1) Previous location exists
        #           ~5.1.1) Use the previous location as another guess and jump to 5.1)
        #     ~5.2) Previous location does not exist
        #           ~5.2.1) Calculate the distance between each guess and the center
        #                   of all resolved nodes
        #           ~5.2.2) Pick the guess that has the largest distance sum
        # 6) Remove measurements for which both nodes are resolved
        # 7) Go back to step 4) until no progress is made?
        # 8) If ~5 was used, preform and jump back to step 4)
        # 9) Done!


        clust = Cluster(title="Test!")
        clust.addPoints([Vector2(0, 0), Vector2(500, 100), Vector2(0, 200)])
        clust.display(canvas)

        self.reduceMeasureList()  # Step 1 / Step 3?
        self.applyRawConfidence()  # Step2

        self.printList(self.resolved_nodes, title='Resolved Nodes', verbose=True)
        self.printList(self.measure_list, title='Current Meas')


        # Loop coordination for step 4
        resolving = True
        old_resolved_length = 0
        while resolving is True:
            old_resolved_length = len(self.resolved_nodes)

            ############# Begin algorithm #############

            


            # Step 6) Remove measurements where both nodes are resolved
            for node1 in self.resolved_nodes:
                for node2 in self.resolved_nodes:
                    if node1 == node2:
                        continue
                    rm = self.getMeasureUsingNodes(node1, node2)
                    if rm:
                        self.measure_list.remove(rm)
                        print('Removed ' + str(rm))
            ###########################################

            # Loop coordination
            if len(self.resolved_nodes) == old_resolved_length:
                resolving = False
        # Done!
        callback(render=True)

    ################################ Steps ################################

    # Parse through all nodes and remove duplicates while generating the
    # measure_list variable
    def reduceMeasureList(self):
        self.measure_list = []
        # Print each measurement from the nodes
        for key, node in self.nodes.items():
            for m in node.get_measurements():
                curMeas = self.getMeasureUsingNodes(m.node1, m.node2)
                if curMeas:
                    self.measure_list.remove(curMeas)
                    m.dist = (curMeas.dist + m.dist) / 2
                    m.opinions = m.opinions + curMeas.opinions
                self.measure_list.append(m)

    # Apply basic confidences based on the distance between nodes and the
    # number of orgnial measurements used
    def applyRawConfidence(self):
        for m in self.measure_list:
            m.confidence = 0.5
            for x in range(m.opinions-1):
                m.confidence *= 1.1

    ############################### Helpers ###############################

    # Print the any list with style
    def printList(self, arb_list, title=None, verbose=False):
        if title is not None:
            print((' ' + title + '---').rjust(60, '-'))
            for n in arb_list:
                if verbose is True:
                    try:
                        print(('| ' + n.getAsString()).ljust(59) + '|')
                    except:
                        print(('| ' + str(n)).ljust(59) + '|')
                else:
                    print(('| ' + str(n)).ljust(59) + '|')
                    
            print(''.center(60, '-'))
        else:
            for n in arb_list:
                print(n)
    
    # Check to see if a measurement is in the measure_list
    def checkMeasureInMeasureList(self, meas):
        return meas in self.measure_list

    # Get all the measurements from the measure_list that involve the
    # given node
    def getMeasuresUsingNode(self, node):
        out = []
        for m in self.measure_list:
            if (m.node1 == node) or (m.node2 == node):
                out.append(m)
        if len(out) == 0:
            return False
        else:
            return out

    # Get the sing;e measurement from the measure_list that involves both
    # of the given nodes
    def getMeasureUsingNodes(self, node1, node2):
        for m in self.measure_list:
            if (m.node1 == node1 and m.node2 == node2) or (m.node1 == node2 and m.node2 == node1):
                return m
        return False

    # Get measures that have a certain confidence or better and involves 
    # the given node
    def getMeasuresWithConfidenceCutoffAndNode(self, confidence, node):
        con_list = self.getMeasuresWithConfidenceCutoff(confidence)
        if con_list:
            for m in con_list:
                if m.node1 != node and m.node2 != node:
                    con_list.remove(m)
            return con_list
        else:
            return False

    # Get all measures that have a certain confidence or better
    def getMeasuresWithConfidenceCutoff(self, confidence):
        out = []
        for m in self.measure_list:
            if m.confidence >= confidence:
                out.append(m)
        if len(out) == 0:
            return False
        else:
             return out


from algorithms.algorithm import Algorithm
from algorithms.helpers.direct_triangulation import DirectTriangulation, Cluster
import math


# > python3 main.py random multi_tri


class multi_tri(Algorithm):
    def __init__(self, nodes):
        super().__init__(nodes)
        self.measure_list = []
        self.resolved_nodes = [nodes['1'], nodes['2']]  # Known

        self.config = {
            'max_cluster_radius': 105,
            'min_guess_isolation': 250
        }

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
        #     exists, so we have to preform an educated guess
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


        # clust = Cluster(title="Test!")
        # clust.addPoints([Vector2(0, 0), Vector2(500, 100), Vector2(0, 200)])
        # clust.display(canvas)

        self.reduceMeasureList()  # Step 1 / Step 3?
        self.applyRawConfidence()  # Step2

        self.printList(self.measure_list, title='Current Meas')

        # Loop coordination for step 4
        resolving = True
        guessing = True
        guess_success = False
        old_resolved_length = 0
        counter = 0
        while guessing is True:
            resolving = True
            while resolving is True:
                guessing = False
                guess_success = False
                print("")
                print("")
                old_resolved_length = len(self.resolved_nodes)
                self.printList(self.resolved_nodes,
                            title='Resolved Nodes '+str(counter+1), verbose=True)

                ############# Begin algorithm #############
                # Step 6) Remove measurements where both nodes are resolved
                self.removeUnusedMeasures()

                # Step 4.1) Get meas for which one node is resolved
                active_meas_list = []
                for node in self.resolved_nodes:
                    m = self.getMeasuresUsingNode(node)
                    if m:
                        active_meas_list += m
                self.printList(active_meas_list, title=('Measure List '+str(counter+1)))

                # Step 4.2) Get a list of pairs of measurements from the previous
                #           list for which each measurement orgniates from a
                #           resolved node and terminates at a single un-resolved node
                meas_pairs = []
                unresolved_nodes = []
                # Loop 0 -> N-1 through the active_meas_list
                for m1_x in range(len(active_meas_list)-1):
                    m1 = active_meas_list[m1_x]
                    # Also loop x -> N through the active_meas_list
                    for m2_x in range(m1_x+1, len(active_meas_list)):
                        m2 = active_meas_list[m2_x]
                        # We now have every set of pairs of measures, unrepeated
                        # Get the pairs of nodes from the measures
                        m1_pair = m1.getNodePair()
                        m2_pair = m2.getNodePair()
                        # Continue if the pair is invalid (none or both are resolved)
                        if m1_pair is None or m2_pair is None or m1_pair == False or m2_pair == False:
                            continue
                        # If the resolved nodes are equal, or the target nodes are different,
                        # continue
                        if m1_pair[0] == m2_pair[0] or m1_pair[1] != m2_pair[1]:
                            continue
                        # Add the pair to the list
                        meas_pairs.append((m1, m2))
                        unresolved_nodes.append(m1_pair[1])


                # Step 4.3) Use triangulation to form two guesses, and store them in
                #           the un-resolved node (using triangulation object)
                for pair in meas_pairs:
                    # Get measures
                    m1 = pair[0]
                    m2 = pair[1]
                    dt = DirectTriangulation(m1, m2)  # Also removes "world border" guesses
                    dt.triangulate()
                    target = m1.getUnResolvedNode()
                    target.addTriangulation(dt)

                    # dt.display(canvas)

                # Step 5) Parse through each un-resolved node to resolve position (Need either
                #         1 direct triangulation object with a single guess, or greater than 1
                #         direct triangulation object. If not the case, jump to ~5)
                for node in unresolved_nodes:
                    # Skip nodes that we just resolved
                    if node in self.resolved_nodes:
                        continue
                    # print(node)
                    dts = node.getTriangulations()
                    # 1 direct triangulation object with 1 guess only
                    case1 = len(dts) == 1 and dts[0].getNumGuesses() == 1
                    # More than 1 direct triangulation object
                    case2 = len(dts) > 1
                    # 1 direct triangulation object with more than 1 guess
                    case3 = len(dts) == 1 and dts[0].getNumGuesses() > 1
                    # print(case1, "  ", case2)
                    if case1:  # Resolvable, assign and move on
                        loc = dts[0].getGuesses()[0]
                        node.set_position_vec(loc)
                        self.resolved_nodes.append(node)
                        node.displayTriangulations(canvas)
                    elif case2:
                        # Step 5.1) Loop through triangulations and generate
                        #           clusters
                        clusters = []
                        key_dt = dts[0]
                        # Loop through each key guess
                        for guess in key_dt.getGuesses():
                            # Loop through other triangulations
                            cluster = Cluster()
                            cluster.addPoint(guess)
                            for x in range(1, len(dts)):
                                # Add the cloest guess from each other triangulation)
                                guess_point = dts[x].getClosestGuess(guess)[0]
                                if guess_point is not None:
                                    cluster.addPoint(guess_point)
                            # If we have more than one guess, the cluster is valid
                            if cluster.getNumPoints() > 1:
                                clusters.append(cluster)

                        # Step 5.2-5.5 Resolution based on cluster
                        smallest_radius = math.inf
                        best_cluster = None
                        # Loop through clusters to find best one
                        for cluster in clusters:
                            radius = cluster.getRadius()
                            # Record the smallest cluster radius
                            cluster.display(canvas, ghost=True)
                            if radius < smallest_radius:
                                smallest_radius = radius
                                best_cluster = cluster
                        
                        if best_cluster is not None and best_cluster.getRadius() <= self.config['max_cluster_radius']:
                            # Resolved!!
                            best_cluster.display(canvas)
                            loc = best_cluster.getCenter()
                            for point in best_cluster.getPoints():
                                canvas.connect_nodes((loc.x, loc.y), (point.x, point.y))
                            node.set_position_vec(loc)
                            self.resolved_nodes.append(node)
                            node.displayTriangulations(canvas)

                    elif case3:
                        # We're gonna have to guess!
                        guessing = True
                        pass

                ###########################################

                # Loop coordination
                if len(self.resolved_nodes) == old_resolved_length:
                    resolving = False
                counter += 1

            # If we are not valid for guessing, move on
            if guessing and len(unresolved_nodes) > 0:
                guess_success = False

                # Step ~5) Educated guessing - Tier I
                if guess_success is False:

                    # Step ~5.1) Previous location exists - Not supported yet
                    # Step ~5.1.1) Use the previous location as another guess and jump to 5.1)
                    for node in unresolved_nodes:
                        # Try previous location
                        # If success, set guess_success to True
                        pass

                # Step ~5) Educated guessing - Tier II
                if guess_success is False:

                    # Step ~5.2) Raw educated guess
                    # Step ~5.2.1) Calculate the distance between each guess and the center of all resolved nodes
                    # Step ~5.2.2) Pick the guess that has the largest distance sum
                    guess_options = []
                    # Loop through the nodes that are not resolved
                    for node in unresolved_nodes:
                        unused_resolved_list = []
                        # Check to see if this node qualifies
                        if len(node.getTriangulations()) == 1 and node.getTriangulations()[0].getNumGuesses() == 2:
                            print(node, ' Tier II Guessing...')
                            # Get the triangulation, since there should only be one
                            dt = node.getTriangulations()[0]
                            # Get the guesses from the triangulation
                            guesses = dt.getGuesses()
                            # Go through each resolved node and gather the ones that this node doesn't use
                            # to triangulate with
                            for resolved_node in self.resolved_nodes:
                                if resolved_node != dt.res1 and resolved_node != dt.res2:
                                    unused_resolved_list.append(resolved_node)
                            # There are two guesses from the single triangulation- set up
                            # sums for each one
                            guess1_total = 0
                            guess2_total = 0
                            # Loop through the list we just generated
                            for unused_resolved in unused_resolved_list:
                                # Calculate distance from each node to the guess point and add it
                                # to the guess sum
                                offset = guesses[0] - unused_resolved.get_position_vec()
                                guess1_total += offset.magnitude()
                                offset = guesses[1] - unused_resolved.get_position_vec()
                                guess2_total += offset.magnitude()
                            # Attempt to see what the best guess is, based on the summed
                            # distance. The larger distance is more likely, since the closer
                            # one should have gotten a ping from someone.
                            if guess1_total > guess2_total:
                                # Guess 1 is the better guess. Assign the variables
                                best_guess = guesses[0]
                                other_guess = guesses[1]
                                best_guess_distance = guess1_total
                                worst_guess_distance = guess_2_total
                            else:
                                # Guess 2 is the better guess. Assign the variables
                                best_guess = guesses[1]
                                other_guess = guesses[0]
                                best_guess_distance = guess2_total
                                worst_guess_distance = guess1_total
                            # If this guess qualifies, add it to the list of options
                            if best_guess_distance > self.config['min_guess_isolation']:
                                guess_options.append([node, best_guess, best_guess_distance, worst_guess_distance])
                    # Go through each guess option and find the node solution that
                    # has the largest difference between the guess distances. The
                    # larger the distance, the more likely this guess is correct.
                    best_spread = -1
                    best_guess_option = None
                    for guess_option in guess_options:
                        # Calculate the spread
                        spread = math.fabs(guess_option[2] - guess_option[3])
                        if spread > best_spread:
                            best_spread = spread
                            best_guess_option = guess_option
                    # If we found a good guess, use it!
                    if best_guess_option is not None:
                        # Assign the node position
                        node = best_guess_option[0]
                        best_guess = best_guess_option[1]
                        node.set_position_vec(best_guess)
                        self.resolved_nodes.append(node)
                        # Display details to the screen
                        node.displayTriangulations(canvas)
                        canvas.circle_node_guess(node, 25, dashed=True, fill="", outline="red")
                        canvas.circle_position((other_guess.x, other_guess.y), 5, dashed=False, fill="red", outline="red")
                        canvas.connect_nodes((other_guess.x, other_guess.y), (node.x, node.y), dashed=True, color="red")
                        # Queue another calculation run
                        guess_success = True

                if guess_success is False:
                    # No tier guesses yielded results. We're done!
                    guessing = False
                else:
                    for node in unresolved_nodes:
                        node.triangulate_list = []
            else:
                guessing = False



        # Done!

        print("")
        print(('--- Results ').ljust(60, '-'))
        for key, value in self.nodes.items():
            value.printReport()

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

    # Remove measures that are between two nodes in the resolved_nodes list
    def removeUnusedMeasures(self):
        for node1 in self.resolved_nodes:
            for node2 in self.resolved_nodes:
                if node1 == node2:
                    continue
                rm = self.getMeasureUsingNodes(node1, node2)
                if rm:
                    self.measure_list.remove(rm)
                    print('Removed ' + str(rm))

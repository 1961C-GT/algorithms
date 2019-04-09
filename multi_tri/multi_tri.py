from algorithms.algorithm import Algorithm
from algorithms.helpers.measurement import Measurement
from algorithms.helpers.direct_triangulation import DirectTriangulation, Cluster
import math
import time


# > python3 main.py random multi_tri


class multi_tri(Algorithm):
    def __init__(self, nodes):
        super().__init__(nodes)
        self.measure_list = []
        self.backup_nodes = nodes
        self.resolved_nodes = [nodes['0'], nodes['1']]  # Known

        self.config = {
            'max_cluster_radius': 50,
            'min_guess_isolation': 250,
            'min_cluster_difference': 10
        }

    def process(self, callback, multi_pipe=None):
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
        # clust.add_points([Vector2(0, 0), Vector2(500, 100), Vector2(0, 200)])
        # clust.display(canvas)

        self.measure_list = []
        self.resolved_nodes = [self.backup_nodes['0'], self.backup_nodes['1']]  # Known

        self.reduce_measure_list()  # Step 1 / Step 3?
        self.apply_raw_confidence()  # Step2
        self.print_list(self.measure_list, title='Current Meas')

        self.piping = False
        self.multi_pipe = multi_pipe
        if self.multi_pipe is not None:
            self.piping = True
            # self.send_pipe_msg({
            #     "cmd": "clear_screen",
            #     "args": None
            # })
            # time.sleep(0.01)

        # Loop coordination for step 4
        guessing = True
        counter = 0
        while guessing is True:
            resolving = True
            while resolving is True:
                guessing = False
                print("")
                print("")
                old_resolved_length = len(self.resolved_nodes)
                self.print_list(self.resolved_nodes,
                                title='Resolved Nodes ' + str(counter + 1), verbose=True)

                ############# Begin algorithm #############
                # Step 6) Remove measurements where both nodes are resolved
                self.remove_unused_measures()

                # Step 4.1) Get meas for which one node is resolved
                active_meas_list = []
                for node in self.resolved_nodes:
                    m = self.get_measures_using_node(node)
                    if m:
                        active_meas_list += m
                self.print_list(active_meas_list, title=('Measure List ' + str(counter + 1)))

                # Step 4.2) Get a list of pairs of measurements from the previous
                #           list for which each measurement originates from a
                #           resolved node and terminates at a single un-resolved node
                meas_pairs = []
                unresolved_nodes = []
                # Loop 0 -> N-1 through the active_meas_list
                for m1_x in range(len(active_meas_list) - 1):
                    m1 = active_meas_list[m1_x]
                    # Also loop x -> N through the active_meas_list
                    for m2_x in range(m1_x + 1, len(active_meas_list)):
                        m2 = active_meas_list[m2_x]
                        # We now have every set of pairs of measures, unrepeated
                        # Get the pairs of nodes from the measures
                        m1_pair = m1.get_node_pair()
                        m2_pair = m2.get_node_pair()
                        # Continue if the pair is invalid (none or both are resolved)
                        if m1_pair is None or m2_pair is None or not m1_pair or not m2_pair:
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
                    # print(pair)
                    # Get measures
                    m1 = pair[0]
                    m2 = pair[1]
                    dt = DirectTriangulation(m1, m2, multi_pipe=self.multi_pipe)  # Also removes "world border" guesses
                    dt.triangulate()
                    target = m1.get_unresolved_node()
                    target.add_triangulation(dt)
                    dt.display()

                # Step 5) Parse through each un-resolved node to resolve position (Need either
                #         1 direct triangulation object with a single guess, or greater than 1
                #         direct triangulation object. If not the case, jump to ~5)
                for node in unresolved_nodes:
                    # Skip nodes that we just resolved
                    if node in self.resolved_nodes:
                        continue
                    # print(node)
                    dts = node.get_triangulations()
                    # print(dts)
                    # 1 direct triangulation object with 1 guess only
                    case1 = len(dts) == 1 and dts[0].get_num_guesses() == 1
                    # More than 1 direct triangulation object
                    case2 = len(dts) > 1
                    # 1 direct triangulation object with more than 1 guess
                    case3 = len(dts) == 1 and dts[0].get_num_guesses() > 1
                    # print(case1, "  ", case2)
                    if case1:  # Resolvable, assign and move on
                        print("CASE 1")
                        loc = dts[0].get_guesses()[0]
                        node.set_position_vec(loc)
                        self.resolved_nodes.append(node)
                        node.display_triangulations()
                    elif case2:
                        print("CASE 2")
                        # Step 5.1) Loop through triangulations and generate
                        #           clusters
                        clusters = []
                        key_dt = dts[0]
                        # Loop through each key guess
                        for guess in key_dt.get_guesses():
                            # Loop through other triangulations
                            cluster = Cluster(multi_pipe=self.multi_pipe)
                            cluster.add_point(guess)
                            for x in range(1, len(dts)):
                                # Add the cloest guess from each other triangulation)
                                guess_point = dts[x].get_closest_guess(guess)[0]
                                if guess_point is not None:
                                    cluster.add_point(guess_point)
                            # If we have more than one guess, the cluster is valid
                            if cluster.get_num_points() > 1:
                                clusters.append(cluster)
                        # Step 5.2-5.5 Resolution based on cluster
                        smallest_radius = math.inf
                        best_cluster = None
                        next_best_cluster = None
                        # Loop through clusters to find the best one
                        for cluster in clusters:
                            radius = cluster.get_radius()
                            # Record the smallest cluster radius
                            cluster.display(ghost=True)
                            if radius < smallest_radius:
                                smallest_radius = radius
                                best_cluster = cluster
                        smallest_radius = math.inf
                        next_best_cluster = None
                        # Loop through clusters to find the next best one
                        for cluster in clusters:
                            if cluster == best_cluster:
                                continue
                            radius = cluster.get_radius()
                            # Record the smallest cluster radius
                            cluster.display(ghost=True)
                            if radius < smallest_radius:
                                smallest_radius = radius
                                next_best_cluster = cluster
                        # Look at the two best clusters and see if they are too close in size.
                        # A super close size number could indicate that the three nodes used to 
                        # triangulate this one are in a line.
                        if next_best_cluster is not None and next_best_cluster != best_cluster:
                            r1 = next_best_cluster.get_radius()
                            r2 = best_cluster.get_radius()
                            if math.fabs(r1 - r2) < self.config['min_cluster_difference']:
                                # The cluster sizes are too simular!
                                # Make them two guesses and send it off to the educated guesser
                                print(node, ' Forcing Tier II Queue')
                                g1 = best_cluster.get_center()
                                g2 = next_best_cluster.get_center()
                                dt = node.get_triangulations()[0]  # Should this dt be picked so it includes the two cluster locations?
                                node.triangulate_list = []
                                node.add_triangulation(dt)
                                dt.guess_list = []
                                dt.directly_add_guess(g1)
                                dt.directly_add_guess(g2)
                                guessing = True
                                continue
                        if best_cluster is not None and best_cluster.get_radius() <= self.config['max_cluster_radius']:
                            # Resolved!!
                            best_cluster.display()
                            loc = best_cluster.get_center()
                            if self.multi_pipe is not None:
                                for point in best_cluster.get_points():
                                    # canvas.connect_nodes((loc.x, loc.y), (point.x, point.y))
                                    self.multi_pipe.send({
                                        "cmd":"connect_points",
                                        "args":{
                                            "pos1": (loc.x, loc.y),
                                            "pos2": (point.x, point.y)
                                        }
                                    })

                            node.set_position_vec(loc)
                            self.resolved_nodes.append(node)
                            node.display_triangulations()

                    elif case3:
                        print("CASE 3")
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
                        if len(node.get_triangulations()) == 1 and node.get_triangulations()[0].get_num_guesses() == 2:
                            print(node, ' Tier II Guessing...')
                            # Get the triangulation, since there should only be one
                            dt = node.get_triangulations()[0]
                            # Get the guesses from the triangulation
                            guesses = dt.get_guesses()
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
                                best_guess_distance = guess1_total
                                worst_guess_distance = guess2_total
                            else:
                                # Guess 2 is the better guess. Assign the variables
                                best_guess = guesses[1]
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
                        # Display
                        node.display_triangulations()
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

        # print("")
        # print('--- Results '.ljust(60, '-'))
        # for key, value in self.nodes.items():
            # value.print_report()

        for node in self.resolved_nodes:
            node.show()

        callback(render=True)

    ################################ Steps ################################

    # Parse through all nodes and remove duplicates while generating the
    # measure_list variable
    def reduce_measure_list(self):
        self.measure_list = []
        # Print each measurement from the nodes
        for key, node in self.nodes.items():
            for m in node.get_measurements():
                cur_meas: Measurement = self.get_measure_using_nodes(m.node1, m.node2)
                if cur_meas:
                    self.measure_list.remove(cur_meas)
                    m.dist = (cur_meas.dist + m.dist) / 2
                    m.opinions = m.opinions + cur_meas.opinions
                self.measure_list.append(m)

    # Apply basic confidences based on the distance between nodes and the
    # number of original measurements used
    def apply_raw_confidence(self):
        for m in self.measure_list:
            m.confidence = 0.5
            for x in range(m.opinions - 1):
                m.confidence *= 1.1

    ############################### Helpers ###############################

    def send_pipe_msg(self, msg):
        if self.piping:
            self.multi_pipe.send(msg)

    # Print the any list with style
    @staticmethod
    def print_list(arb_list, title=None, verbose=False):
        if title is not None:
            print((' ' + title + '---').rjust(60, '-'))
            for n in arb_list:
                if verbose is True:
                    try:
                        print(('| ' + n.to_string()).ljust(59) + '|')
                    except AttributeError:
                        print(('| ' + str(n)).ljust(59) + '|')
                else:
                    print(('| ' + str(n)).ljust(59) + '|')

            print(''.center(60, '-'))
        else:
            for n in arb_list:
                print(n)

    # Check to see if a measurement is in the measure_list
    def check_measure_in_measure_list(self, meas):
        return meas in self.measure_list

    # Get all the measurements from the measure_list that involve the
    # given node
    def get_measures_using_node(self, node):
        out = []
        for m in self.measure_list:
            if (m.node1 == node) or (m.node2 == node):
                out.append(m)
        if len(out) == 0:
            return False
        else:
            return out

    # Get the single measurement from the measure_list that involves both
    # of the given nodes
    def get_measure_using_nodes(self, node1, node2):
        for m in self.measure_list:
            if (m.node1 == node1 and m.node2 == node2) or (m.node1 == node2 and m.node2 == node1):
                return m
        return False

    # Get measures that have a certain confidence or better and involves 
    # the given node
    def get_measures_with_confidence_cutoff_and_node(self, confidence, node):
        con_list = self.get_measures_with_confidence_cutoff(confidence)
        if con_list:
            for m in con_list:
                if m.node1 != node and m.node2 != node:
                    con_list.remove(m)
            return con_list
        else:
            return False

    # Get all measures that have a certain confidence or better
    def get_measures_with_confidence_cutoff(self, confidence):
        out = []
        for m in self.measure_list:
            if m.confidence >= confidence:
                out.append(m)
        if len(out) == 0:
            return False
        else:
            return out

    # Remove measures that are between two nodes in the resolved_nodes list
    def remove_unused_measures(self):
        for node1 in self.resolved_nodes:
            for node2 in self.resolved_nodes:
                if node1 == node2:
                    continue
                rm = self.get_measure_using_nodes(node1, node2)
                if rm:
                    self.measure_list.remove(rm)
                    print('Removed ' + str(rm))

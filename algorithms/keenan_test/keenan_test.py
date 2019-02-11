from algorithms.algorithm import Algorithm
from algorithms.algorithm import Vector2
from algorithms.algorithm import Intersection
import math

# > python3 main.py random example_alg

class keenan_test(Algorithm):
    def __init__(self, nodes):
        super().__init__(nodes)

    def process(self, callback, canvas):
        self.generateCleanList()

        # for m in self.clean_list:
        #     print(m)


        base1 = self.nodes['1']
        base1.set_position_vec(base1.get_real_position_vec())
        base2 = self.nodes['2']
        base2.set_position_vec(base2.get_real_position_vec())


        self.resolved = [base1, base2]

        resolving = True
        counter = 0
        index_x = 0
        index_y = 0
        while resolving is True:

            known1 = self.resolved[index_y]
            known2 = self.resolved[index_x]

            if known1 != known2 and (known1.cleared == False and known2.cleared == False):
                meas_list_1 = self.getMeasListFromNode(known1)
                meas_list_2 = self.getMeasListFromNode(known2)

                comparable_meas = []
                for m1 in meas_list_1:
                    for m2 in meas_list_2:
                        if m2 == m1 or m1.cleared == True or m2.cleared == True:
                            continue
                        n1 = m1.node1
                        n2 = m1.node2
                        n3 = m2.node1
                        n4 = m2.node2
                        if n1 == known2 or n2 == known2 or n3 == known1 or n4 == known1:
                            continue

                        if n1 == known1:
                            target1 = n2
                        else:
                            target1 = n1

                        if n3 == known2:
                            target2 = n4
                        else:
                            target2 = n3
                        
                        if target1 != target2:
                            continue

                        comparable_meas.append({
                            'm1': m1,
                            'm2': m2
                        })
                
                if len(comparable_meas) != 0:
                    counter_sub = 0
                    for m_set in comparable_meas:
                        print(m_set)
                        m1 = m_set['m1']
                        m2 = m_set['m2']

                        if m1.node1 == known1:
                            target = m1.node2
                        elif m1.node2 == known1:
                            target = m1.node1

                        n1 = m1.node1
                        n2 = m1.node2
                        n3 = m2.node1
                        n4 = m2.node2

                        print()
                        print(
                            f'{counter}.{counter_sub} : Resolving using {known1} & {known2} -> {target}')
                        # print(f'{m1.dist} & {m2.dist}')

                        print(f'{n1} {n2} {n3} {n4}')

                        (v1, v2) = Intersection(
                            known1.get_position_vec(), known2.get_position_vec(), m1.dist, m2.dist)


                        if v1.y < 401.7544:
                            target.set_position_vec(v2)
                            self.resolved.append(target)
                        elif v2.y < 401.7544:
                            target.set_position_vec(v1)
                            self.resolved.append(target)
                        else:
                            canvas.circle_position((v1.x, v1.y), 15, outline="", fill="red", text=str(target))
                            canvas.circle_position((v2.x, v2.y), 15, outline="", fill="green", text=str(target))

                            canvas.connect_node_and_pos(known1, (v1.x, v1.y), color="red")
                            canvas.connect_node_and_pos(known2, (v1.x, v1.y), color="red")

                            canvas.connect_node_and_pos(known1, (v2.x, v2.y), color="green")
                            canvas.connect_node_and_pos(known2, (v2.x, v2.y), color="green")


                        m1.cleared = True
                        m2.cleared = True
                        counter_sub = counter_sub + 1

                # print(meas_list)            


            index_x = index_x + 1
            if index_x >= len(self.resolved):
                index_x = 0
                index_y = index_y + 1
                if index_y >= len(self.resolved):
                    index_y = 0
            counter = counter + 1
            if counter > 100:
                resolving = False



        # r1 = base1.get_measurements()[1].dist
        # canvas.circle_node_guess(base1, r1, outline="orange")
        # r2 = base2.get_measurements()[1].dist
        # canvas.circle_node_guess(base2, r2, outline="orange")
        # (v1, v2) = Intersection(P1, P2, r1, r2)

        # canvas.create_circle(v1.x, v1.y, 20, outline="", fill="red")
        # self.nodes['3'].set_position_vec(v2)


        # Done!
        callback(render=True)

    def generateCleanList(self):
        self.clean_list = []
        # Print each measurement from the nodes
        for key, node in self.nodes.items():
            if node.is_base or True:
                # print(node)
                real = node.get_real_position()
                # node.set_position(real[0], real[1])
                for m in node.get_measurements():
                    curMeas = self.getMeasInCleanList(m.node1, m.node2)
                    if curMeas:
                        self.clean_list.remove(curMeas)
                        m.dist = (curMeas.dist + m.dist) / 2
                    self.clean_list.append(m)

    def getMeasInCleanList(self, node1, node2):
        for m in self.clean_list:
            if (m.node1 == node1 and m.node2 == node2) or (m.node1 == node2 and m.node2 == node1):
                return m
        return False

    def getMeasListFromNode(self, node):
        out_list = []
        for m in self.clean_list:
            if m.node1 == node or m.node2 == node:
                out_list.append(m)
        return out_list

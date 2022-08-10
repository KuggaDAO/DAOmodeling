# this file aims to model member network
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class Net:
    def __init__(self, members, relations):
        self.members = members
        self.n_member = len(members)
        self.labels = []
        for member in members:
            self.labels.append(member.label)
        self.relations = relations
        return

    # draw relation graph
    def draw(self,relation_name):
        relation=self.relations[relation_name]
        if relation.directed:
            Graph=nx.DiGraph()
        else:
            Graph=nx.Graph()
        Graph.add_nodes_from(relation.labels)
        Graph.add_edges_from(relation.edges)

        pos=nx.circular_layout(Graph)
        nx.draw(Graph,pos=pos,with_labels=True)
        plt.show()
from Network.Net import Net
from Network.Member import Member
from Network.Relation import Relation

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

__all__ = ['Net', 'Member', 'Relation', 'draw_prefer_diff_minispantree']


def norm_2(vec):
    vec = np.array(vec)
    return np.sqrt(np.sum(
        vec * vec
    ))

#draw minisapntree to discribe members structure
def draw_prefer_diff_minispantree(members):
    labels = []
    for member in members:
        labels.append(member.label)

    prefer_diffs = []
    n_member = len(members)

    prefer_len = []
    for member in members:
        prefer_len.append(norm_2(member.preference))

    for i in range(n_member):
        for j in range(i + 1, n_member):
            difference = norm_2(
                members[i].preference -
                members[j].preference
            )
            prefer_diffs.append((labels[i], labels[j], difference))

    G = nx.Graph()
    G.add_nodes_from(labels)
    G.add_weighted_edges_from(prefer_diffs)

    G_minispantree = nx.minimum_spanning_tree(G)

    weight = nx.get_edge_attributes(G_minispantree, "weight")
    for key, value in weight.items():
        weight[key] = np.round(value, 3)

    pos = nx.drawing.nx_agraph.graphviz_layout(G_minispantree)
    nx.draw(G_minispantree, pos=pos, with_labels=True)
    nx.draw_networkx_edge_labels(G_minispantree, pos=pos, edge_labels=weight)

import numpy as np


class Relation:
    def __init__(self, rel_name, labels, value_matrix, threshold, directed=True):
        rel_name = rel_name
        self.labels = labels
        self.value_matrix = value_matrix
        self.threshold = threshold
        self.directed = directed
        self.set_bool_info()

    # set bool_matrix and edges
    def set_bool_info(self):
        # bool_matrix discribes the situation of value exceeding threshold
        self.bool_matrix = ((self.value_matrix - \
                             self.threshold * np.ones_like(self.value_matrix)) >= 0)

        # edges collects True relationship
        # to facilitate drawing directed or undirected graph
        self.edges = []
        n_label = len(self.labels)
        for i in range(n_label):
            j_start = 0 if self.directed else i
            for j in range(j_start, n_label):
                if i != j and self.bool_matrix[i, j]:
                    self.edges.append([
                        self.labels[i], self.labels[j]
                    ])

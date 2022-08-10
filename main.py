import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from Network import *

names = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve']
members = []
for i in range(5):
    members.append(Member(names[i]))


rel_name = 'trust'
matrix = np.random.rand(5, 5)
threshold = 0.5
trust_relation = Relation(rel_name, names, matrix, threshold)

print(matrix)

net = Net(members, {'trust': trust_relation})
net.draw('trust')

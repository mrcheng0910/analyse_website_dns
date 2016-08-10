# encoding:utf-8

import networkx as nx
import matplotlib.pyplot as plt
# G = nx.Graph()
#
# G.add_node(1)
# G.add_node('1')
# G.add_nodes_from([2,3])
#
# G.add_edge(1,2)
#
# edge = (1,3)
# G.add_edge(*edge)
#
# print G.nodes()
# print G.edges()
# print G.number_of_nodes()
# print G.number_of_edges()
# DG = nx.DiGraph()
# DG.add_weighted_edges_from([(1,2,0.15),(3,1,0.75)])
# edge = (4,5)
# DG.add_edge(*edge)
# print DG.in_degree(1,weight='weight')
# print DG.out_degree(1,weight='weight')
# print DG.degree(1,weight='weight')
# print DG.successors(1)
# print DG.predecessors(1)
# print DG.neighbors(1)
# print nx.connected_components(DG)

# nx.draw(DG)
# nx.draw(DG)

# plt.show()

import networkx as nx

G=nx.path_graph(10)

pos=nx.spring_layout(G)

nx.draw(G,pos)

x,y=pos[1]

import matplotlib.pyplot as plt

plt.text(x,y+0.1,s='baidu.com',horizontalalignment='left')
plt.show()
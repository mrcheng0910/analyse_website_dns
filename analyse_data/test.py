# encoding:utf-8

"""

dot - "hierarchical" or layered drawings of directed graphs. This is the default tool to use if edges have directionality.

neato - "spring model'' layouts.  This is the default tool to use if the graph is not too large (about 100 nodes) and you don't know anything else about it. Neato attempts to minimize a global energy function, which is equivalent to statistical multi-dimensional scaling.

fdp - "spring model'' layouts similar to those of neato, but does this by reducing forces rather than working with energy.

sfdp - multiscale version of fdp for the layout of large graphs.

twopi - radial layouts, after Graham Wills 97. Nodes are placed on concentric circles depending their distance from a given root node.

circo - circular layout, after Six and Tollis 99, Kauffman and Wiese 02. This is suitable for certain diagrams of multiple cyclic structures, such as certain telecommunications networks.

"""

from domain_collection import get_domain_collection, insert
# from collections import Counter, defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import random
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.generators.atlas import *
# from networkx.algorithms.isomorphism.isomorph import graph_could_be_isomorphic as isomorphic



def get_data(domain='baidu.com'):
    """
    """
    domain_collection = get_domain_collection('data_info')
    domain_pkts = domain_collection.find({'domain_name': domain})
    if domain_pkts.count() == 0:  # 不存在集合
        print "该集合无符合条件数据"
        return
    return  domain_pkts


def main():
    edges = []
    domain_pkts = get_data('163.com')
    for i in domain_pkts[0]['details']:
        for v in i['answers']:
            edges.append((v['domain_name'],v['dm_data']))
            # print v

    # print edges

    G = nx.Graph()
    G.add_edges_from(edges)

    # nx.draw(G)
    # plt.show()
    pos = graphviz_layout(G, prog="neato")
    C = nx.connected_component_subgraphs(G)

    for g in C:
        c = [random.random()] * nx.number_of_nodes(g)  # random color...
        nx.draw(g,
                pos,
                node_size=90,
                node_color=c,
                vmin=0.0,
                vmax=1.0,
                with_labels=True
                )
    plt.show()


if __name__ == '__main__':
    main()


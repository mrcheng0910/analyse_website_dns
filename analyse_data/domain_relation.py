# encoding:utf-8

"""
分析站点的域名之间的关联关系，不同关联关系使用不同颜色进行标记，并且保存图片
"""

from domain_collection import get_domain_collection
import networkx as nx
import matplotlib.pyplot as plt
import random
from networkx.drawing.nx_pydot import graphviz_layout


def get_data(domain='baidu.com'):
    """
    获取要查询站点的探测数据信息
    :param domain: 站点的域名
    :return: 相关探测数据
    """
    domain_collection = get_domain_collection('data_info')
    domain_pkts = domain_collection.find({'domain_name': domain})
    if domain_pkts.count() == 0:  # 不存在集合
        print "该集合无符合条件数据"
        return
    return  domain_pkts


def main():
    edges = []   # 图的所有边信息
    domain_name = 'taobao.com'
    domain_pkts = get_data(domain_name)

    for i in domain_pkts[0]['details']:
        for v in i['answers']:
            edges.append((v['domain_name'],v['dm_data']))

    plt.figure(1, figsize=(10, 8))
    G = nx.Graph()
    G.add_edges_from(edges)

    pos = graphviz_layout(G, prog="fdp") #neato fdp
    C = nx.connected_component_subgraphs(G)  # 获取图的子图，用来标记颜色

    for g in C:
        c = [random.random()] * nx.number_of_nodes(g)
        nx.draw(g,
                pos,
                node_size=90,
                node_color=c,
                vmin=0.0,
                vmax=1.0,
                with_labels=False
        )
    plt.savefig('./graph/'+domain_name+"_relation.png", dpi=75)
    plt.show()


if __name__ == '__main__':
    main()


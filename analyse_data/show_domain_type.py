# encoding:utf-8

"""
展示网站主域名/cname/ip的关联关系
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
    """
    无图例展示
    :return:
    """
    edges = []   # 图的所有边信息
    domain_name = 'jd.com'
    domain_pkts = get_data(domain_name)
    from collections import defaultdict
    node_dict = defaultdict(set)
    for i in domain_pkts[0]['details']:
        for v in i['answers']:
            if v['dm_type'] == 'CNAME':
                node_dict[v['domain_name']].add('main')
                node_dict[v['dm_data']].add('cname')
            else:
                node_dict[v['dm_data']].add('ip')
                node_dict[v['domain_name']].add('main')
            edges.append((v['domain_name'],v['dm_data']))
    node_cat ={}
    for i in node_dict:
        if 'ip' in list(node_dict[i]):
            node_cat[i]='ip'
        elif 'cname' in list(node_dict[i]):
            node_cat[i]='cname'
        else:
            node_cat[i]='main'

    plt.figure(1,figsize=(10,8))
    G=nx.Graph()
    G.add_edges_from(edges)

    for node in G.nodes():
        G.node[node]['category'] = node_cat[node]

    color_map = {'main': 'b', 'cname': 'c', 'ip': 'r'}
    pos = graphviz_layout(G, prog="neato")  # neato fdp
    # pos = nx.random_layout(G)
    nx.draw(G,
            pos,
            node_size=100,
            node_color=[color_map[G.node[node]['category']] for node in G],
            label="nihao"
            )
    plt.axis('off')
    plt.savefig('./graph/' + domain_name + "_type.png", dpi=75)
    plt.show()

def main1():
    """
    有图例，图例需要再进行更改
    :return:
    """
    edges = []
    node_main = []
    node_cname = []
    node_ip = []
    domain_name = 'jd.com'
    domain_pkts = get_data(domain_name)
    from collections import defaultdict
    node_dict = defaultdict(set)
    for i in domain_pkts[0]['details']:
        node_main.append(i['qry_name'])
        for v in i['answers']:
            if v['dm_type'] == 'CNAME':
                node_dict[v['domain_name']].add('main')
                node_dict[v['dm_data']].add('cname')
            else:
                node_dict[v['dm_data']].add('ip')
                node_dict[v['domain_name']].add('main')
            edges.append((v['domain_name'], v['dm_data']))

    for i in node_dict:

        if 'ip' in list(node_dict[i]):
            node_ip.append(i)
        elif 'cname' in list(node_dict[i]):
            node_cname.append(i)

    plt.figure(1, figsize=(8, 6))
    G = nx.Graph()
    G.add_edges_from(edges)
    node_size = 120
    pos = graphviz_layout(G, prog="neato")  # neato fdp
    nx.draw_networkx_nodes(G,pos=pos,node_size=node_size,nodelist=node_ip,node_color='red',label="IP")
    nx.draw_networkx_nodes(G, pos=pos,node_size=node_size, nodelist=node_cname, node_color='green', label="CNAME")
    nx.draw_networkx_nodes(G, pos=pos, node_size=160,nodelist=node_main, node_color='blue', label="Main")
    nx.draw_networkx_edges(G,pos=pos)
    plt.legend(loc='lower center',ncol=3, shadow=True,numpoints=1)
    plt.axis('off')
    plt.savefig('./graph/' + domain_name + "_type.png", dpi=75)
    plt.show()



if __name__ == '__main__':
    main1()


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


def get_ip_cname(data):
    """
    获取IP和CNAME和访问次数
    :return:
    """
    visit_total = 0
    edges  = []
    node_main = []
    from collections import defaultdict
    node_dict = defaultdict(set)
    for i in data:
        visit_total += i['visit_count']
        node_main.append(i['qry_name'])
        for v in i['answers']:
            if v['dm_type'] == 'CNAME':
                node_dict[v['domain_name']].add('main')
                node_dict[v['dm_data']].add('cname')
            else:
                node_dict[v['dm_data']].add('ip')
                node_dict[v['domain_name']].add('main')
            edges.append((v['domain_name'], v['dm_data']))
    node_cname = []
    node_ip = []
    for i in node_dict:

        if 'ip' in list(node_dict[i]):
            node_ip.append(i)
        elif 'cname' in list(node_dict[i]):
            node_cname.append(i)

    return node_cname,node_ip,visit_total,edges,node_main



def main():
    domain_name = 'baidu.com'
    domain_pkts = get_data(domain_name)
    node_cname, node_ip, visit_total, edges, node_main = get_ip_cname(domain_pkts[0]['details'])
    for i in domain_pkts[0]['details']:
        for v in i['answers']:
            edges.append((v['domain_name'],v['dm_data']))

    DG = nx.DiGraph()
    DG.add_edges_from(edges)

    # 分析域名直接解析为IP的node
    for node in DG:
        if node in node_main and DG.successors(node) in node_ip:
            print node

    # 分析cname关联的IP数量分布
    for node in DG:
        if node in node_cname and DG.successors(node) not in node_cname:  # 查找与ip直接连接的cname
            print "node",DG.out_degree(node),DG.in_degree(node),DG.degree(node)
    # 与cname关联的域名个数
    # for node in DG:
    #     if node in node_cname and DG.predecessors(node) not in node_cname:
    #         print len(DG.predecessors(node))

    for node in DG:
        if node in  node_main:
            if len(DG.successors(node)) ==3:
                print node
                print DG.successors(node)
    # print sorted(nx.degree(DG).values())

    print nx.degree_assortativity_coefficient(DG)
    average_degree = sum(nx.degree(DG).values())/(len(node_cname)+len(node_ip)+len(node_main))
    print average_degree
    print len(node_cname)+len(node_ip)+len(node_main)
    print len(edges)
    print nx.degree_histogram(DG)
    # print nx.degree_centrality(DG)
    # print nx.in_degree_centrality(DG)
    # print nx.out_degree_centrality(DG)
    # print nx.closeness_centrality(DG)
    # print nx.load_centrality(DG)

if __name__ == '__main__':
    main()


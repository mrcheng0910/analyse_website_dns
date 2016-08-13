# encoding:utf-8

"""
分析站点的域名之间的关联关系，不同关联关系使用不同颜色进行标记，并且保存图片
"""

from domain_collection import get_domain_collection
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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



def manage_data(domain_name):

    domain_pkts = get_data(domain_name)
    node_cname, node_ip, visit_total, edges, node_main = get_ip_cname(domain_pkts[0]['details'])
    for i in domain_pkts[0]['details']:
        for v in i['answers']:
            edges.append((v['domain_name'],v['dm_data']))

    DG = nx.DiGraph()
    DG.add_edges_from(edges)

    ass =  nx.degree_assortativity_coefficient(DG)
    nodes_count = len(node_cname)+len(node_ip)+len(node_main)
    edges_count = len(edges)
    average_degree = sum(nx.degree(DG).values())
    print domain_name,ass
    return nodes_count,edges_count, ass,average_degree


def main():

    domains = ['baidu.com','toutiao.com','ifeng.com','taobao.com','hitwh.edu.cn','163.com','jd.com','qq.com','baike.com','amazon.cn',
               'alibaba.com','alipay.com','360.cn','360.com']
    x1 = []
    y1 = []
    z1 =[]
    x2 = []
    y2 = []
    z2 = []
    for i in domains:
        nodes,edges,ass,av = manage_data(i)
        if ass<=0:
            x1.append(nodes)
            y1.append(edges)
            z1.append(av)
        else:
            x2.append(nodes)
            y2.append(edges)
            z2.append(av)
    # plt.subplot(111, projection='3d')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    print x1,y1,x2,y2,z1,z2
    ax.scatter(x1, y1, marker='^', c='r')
    ax.scatter(x2, y2,  marker='o', c='c')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')
    plt.show()

if __name__ == '__main__':
    main()


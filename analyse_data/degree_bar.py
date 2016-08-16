# encoding:utf-8

"""
计算有向网络出入度的分布特征和图的平均度大小
"""

from domain_collection import get_domain_collection
import networkx as nx
import matplotlib.pyplot as plt


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
    """
    处理数据函数
    :param domain_name:
    :return:
    """
    domain_pkts = get_data(domain_name)
    node_cname, node_ip, visit_total, edges, node_main = get_ip_cname(domain_pkts[0]['details'])
    for i in domain_pkts[0]['details']:
        for v in i['answers']:
            edges.append((v['domain_name'],v['dm_data']))

    DG = nx.DiGraph()
    DG.add_edges_from(edges)

    in_degree_val = DG.in_degree().values()
    out_degree_val = DG.out_degree().values()

    degree_val = DG.degree().values()
    print '度: ',sum(degree_val)
    print '平均度:', float(sum(degree_val))/DG.number_of_nodes()


    from collections import Counter
    from operator import itemgetter

    in_degree_dict = Counter(in_degree_val)
    out_degree_dict = Counter(out_degree_val)
    in_x,in_y,out_x,out_y = [],[],[],[]

    for i in sorted(in_degree_dict.items(), key=itemgetter(0)):
        in_x.append(i[0])
        in_y.append(i[1])

    for i in sorted(out_degree_dict.items(), key=itemgetter(0)):
        out_x.append(i[0])
        out_y.append(i[1])

    return in_x,in_y,out_x,out_y


def main():

    domain = 'taobao.com'
    in_x_label,in_y,out_x_label,out_y = manage_data(domain)

    fig = plt.figure(1,figsize=(8.5, 5),dpi=75)
    left = 0.09  # the left side of the subplots of the figure
    right = 0.96  # the right side of the subplots of the figure
    bottom = 0.1  # the bottom of the subplots of the figure
    top = 0.93  # the top of the subplots of the figure
    wspace = 0.2  # the amount of width reserved for blank space between subplots
    hspace = 0.2  # the amount of height reserved for white space between subplots
    plt.subplots_adjust(left,bottom,right,top,wspace,hspace)

    import numpy as np

    width = 0.5
    in_x = np.arange(len(in_x_label))
    out_x = np.arange(len(out_x_label))
    fig.add_subplot(121)
    plt.bar(in_x,[float(i)/sum(in_y) for i in in_y],width,align='center')
    plt.plot(in_x,[float(i)/sum(in_y) for i in in_y],'r--')
    x_min, x_max = in_x.min(), in_x.max()
    plt.xlim(x_min - 1, x_max + 1)
    plt.xticks(in_x, in_x_label)
    plt.ylabel('In-Degree P(k)')
    plt.xlabel('In-Degree k')


    fig.add_subplot(122)
    plt.bar(out_x, [float(i) / sum(out_y) for i in out_y], width, align='center')
    plt.plot(out_x,[float(i) / sum(out_y) for i in out_y],'r--')
    x_min, x_max = out_x.min(), out_x.max()
    plt.xlim(x_min - 1, x_max + 1)
    plt.xticks(out_x, out_x_label)
    plt.ylabel('Out-Degree P(k)')
    plt.xlabel('Out-Degree k')

    plt.savefig('./graph/degree_bar.png', dpi=75)
    plt.show()

if __name__ == '__main__':
    main()


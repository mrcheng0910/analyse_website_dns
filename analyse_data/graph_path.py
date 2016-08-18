# encoding:utf-8

"""
计算有向网络中域名解析的路径长度分布/最长路径/最短路径以及平均路径长度
"""

from domain_collection import get_domain_collection
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter


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
    edges  = []
    node_main = []
    from collections import defaultdict
    node_dict = defaultdict(set)
    for i in data:
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
        elif 'main' in list(node_dict[i]) and len(node_dict[i])==1:
            node_main.append(i)

    return node_cname,node_ip,edges,node_main


def manage_data(domain_name):
    """
    处理数据函数
    :param domain_name:
    :return:
    """
    domain_pkts = get_data(domain_name)
    node_cname, node_ip, edges, node_main = get_ip_cname(domain_pkts[0]['details'])

    DG = nx.DiGraph()
    DG.add_edges_from(edges)

    # 为各个节点添加类别，区分domain/cname/ip
    for i in node_ip:
        DG.node[i]['category']='ip'
    for i in node_cname:
        DG.node[i]['category']='cname'

    for i in node_main:
        DG.node[i]['category']='domain'

    path_length = []

    for w in nx.weakly_connected_component_subgraphs(DG):
        domains = []
        ips = []
        for i in w.nodes_iter(data=True):
            if i[1]['category'] == 'ip':
                ips.append(i[0])
            if i[1]['category'] == 'domain':
                domains.append(i[0])

        for domain in domains:
            for ip in ips:
                try:
                    # print nx.dijkstra_path(w,domain,ip) # show the path
                    path_length.append(nx.dijkstra_path_length(w,domain,ip))  # add the lenth of path
                except:  # if between the source node and the destination has no path
                    pass

    average_path =  float(sum(path_length))/len(path_length)
    print '平均长度', float(sum(path_length))/len(path_length)
    print '最长路径',max(path_length)
    print '最短路径',min(path_length)
    print '路径条数',len(path_length)

    # draw bar about the length of path distribution

    c = Counter(path_length)
    print c
    y =  c.values()
    x_labels = c.keys()
    width = 0.5

    x = range(len(x_labels))

    plt.figure(1,figsize=(8,6),dpi=75)

    plt.bar(x, y, width=width, align='center')

    plt.annotate('the minimum\n  path length',
                 xy=(x[0], y[0]),
                 xycoords='data',
                 xytext=(-40, 30), textcoords='offset points',
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                )

    plt.annotate('the maximum\n   path length',
                 xy=(x[len(x)-1], y[len(y)-1]),
                 xycoords='data',
                 xytext=(-40, 30), textcoords='offset points',
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                 )

    font = {'family': 'serif',
            'color': 'k',
            'weight': 'normal',
            'size': 14,
            }
    plt.text(x[len(x)-2], 400,
             'the average path\n   length: '+ str(round(average_path,2)),
             fontdict=font,
             bbox=dict(facecolor='k', alpha=0.3)
             )


    x_min, x_max = min(x), max(x)
    plt.xlim(x_min - 1, x_max + 1)
    plt.xticks(x, x_labels)
    plt.xlabel('Path Length')
    plt.ylabel('The numbers')

    plt.savefig('./graph/'+domain_name+'_graph_path.png', dpi=75)

    plt.show()


def main():

    domain = '163.com'
    manage_data(domain)


if __name__ == '__main__':
    main()


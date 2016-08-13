# encoding:utf-8

"""
分析网站的详细内容，包括嵌入的域名/cname/ip，簇，集合等信息，具体如下：
1. 域名个数
2. 解析总数
3. 平均解析次数
4. CNAME个数
5. CNAME分布
6. IP个数
7. IP解析分布
8. IP地理位置分布
9. CDN使用情况
10. 域名集合情况
11. 域名簇情况

"""

from domain_collection import get_domain_collection
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def get_data(domain='baidu.com'):
    """
    获取要查询站点的探测数据信息
    :param domain: 站点的域名
    :return: 相关探测数据
    """
    domain_collection = get_domain_collection('data_info')
    domain_pkt = domain_collection.find({'domain_name': domain})
    if domain_pkt.count() == 0:  # 不存在集合
        print "该集合无符合条件数据"
        return
    return  domain_pkt[0]


def manage_data(domain='163.com'):
    domain_pkt = get_data(domain)
    # 域名数量
    domain_count = len(domain_pkt['details'])
    # cname_count, cname数量
    # ip_count，IP数量
    # visit_total,访问次数
    # edges,图的边
    node_cname,node_ip,visit_total,edges,node_main = get_ip_cname(domain_pkt['details'])
    cname_count = len(node_cname)
    ip_count = len(node_ip)
    sub_graph_count = sub_graph(edges,node_main,node_ip,node_cname)
    print "总共访问次数",visit_total
    print "域名数量",domain_count
    print "cname数量",cname_count
    print "IP数量",ip_count
    print "生成集合数量",sub_graph_count
    draw_sub_graph(visit_total,domain_count,cname_count,ip_count,sub_graph_count)


def draw_sub_graph(visit_total,domain_count,cname_count,ip_count,sub_graph_count):

    N = 5
    ind = np.arange(1, N + 1)
    width = 0.7
    plt.figure(1, figsize=(8, 6))
    data = [domain_count,cname_count,ip_count,sub_graph_count,visit_total]
    plt.bar(ind, data, width, color='c', align='center')

    x_min, x_max = ind.min(), ind.max()
    plt.xlim(x_min - 1, x_max + 1)
    plt.ylabel('The numbers')
    plt.xlabel('Categories')
    plt.xticks(ind,('Domain','CNAME','IP','Sub_Graph','DNS Hits'))
    plt.yticks()
    # 设置legend
    for a, b in zip(ind, data):
        plt.text(a, b, str(b))

    plt.savefig('./graph/domain_overall.png', dpi=75)
    plt.show()



def sub_graph(edges,node_main,node_ip,node_cname):
    """
    得到子图的多少
    :param edges:
    :return:
    """
    from collections import Counter
    sub_graph_set = Counter()  # 子图含有不同结点的数量统计
    sub_graph_count = 0    # 生成集合的数量（子图）
    sub_graph_domain_count = Counter()    #  子图中含有不同域名的数量统计
    sub_graph_cname_count = Counter()
    sub_graph_ip_count = Counter()
    G = nx.Graph()
    G.add_edges_from(edges)
    C = nx.connected_component_subgraphs(G)  # 获取图的子图
    test = {'domain_count': [],
            'cname_count': [],
            'ip_count': []
            }
    for g in C:
        sub_graph_count += 1
        sub_graph_set[len(g.nodes())] += 1
        # print  list(set(g.nodes()).intersection(set(nodes_main)))
        test['domain_count'].append(len(list(set(g.nodes()).intersection(set(node_main)))))
        test['cname_count'].append(len(list(set(g.nodes()).intersection(set(node_cname)))))
        test['ip_count'].append(len(list(set(g.nodes()).intersection(set(node_ip)))))
        sub_graph_domain_count[len(list(set(g.nodes()).intersection(set(node_main))))] += 1
        sub_graph_cname_count[len(list(set(g.nodes()).intersection(set(node_cname))))] += 1
        sub_graph_ip_count[len(list(set(g.nodes()).intersection(set(node_ip))))] += 1
    # print sub_graph_set
    # print sub_graph_domain_count
    # print sub_graph_cname_count
    # print sub_graph_ip_count
    draw_graph(test)
    return sub_graph_count


def draw_graph(domain_data):
    """
    绘制站点的域名解析数据，包括各个簇的域名个数,cname个数，ip个数等
    :param domain_data: 字典，各个属性的数量
    :return:
    """
    domain_count = domain_data['domain_count']
    cname_count = domain_data['cname_count']
    ip_count = domain_data['ip_count']
    N = len(domain_count)
    ind = np.arange(1,N+1)
    width = 0.7
    plt.figure(1, figsize=(8, 6))
    p1 = plt.bar(ind, domain_count, width, align='center',color='r',bottom=[x+y for x, y in zip(ip_count, cname_count)])
    p2 = plt.bar(ind, cname_count, width, color='y',align='center',bottom=ip_count)
    p3 = plt.bar(ind,ip_count,width,color='c',align='center')
    # x居中设置
    x_min, x_max = ind.min(), ind.max()
    plt.xlim(x_min - 1, x_max + 1)
    plt.ylabel('the numbers')
    plt.xlabel('sequence number')
    plt.xticks(np.arange(1, N+1, 3))
    plt.yticks()
    # 设置legend
    plt.legend((p1[0], p2[0],p3[0]), ('Domain', 'CNAME', 'IP'),fontsize='11')

    plt.savefig('./graph/' + "domain_hist.png", dpi=75)
    plt.show()



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


if __name__ == '__main__':
    # main1()
    manage_data()

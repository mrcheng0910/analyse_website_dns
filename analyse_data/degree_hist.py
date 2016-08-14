# encoding:utf-8

"""
分析站点的域名之间的关联关系，不同关联关系使用不同颜色进行标记，并且保存图片
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

    domain_pkts = get_data(domain_name)
    node_cname, node_ip, visit_total, edges, node_main = get_ip_cname(domain_pkts[0]['details'])
    for i in domain_pkts[0]['details']:
        for v in i['answers']:
            edges.append((v['domain_name'],v['dm_data']))

    DG = nx.DiGraph()
    DG.add_edges_from(edges)

    in_degree_val = DG.in_degree().values()
    max_in_degree = max(in_degree_val)

    from collections import Counter
    in_degree_dict = Counter(in_degree_val)
    in_degree_hist = []
    for i in range(max_in_degree+1):
        print i
        if i in in_degree_dict.keys():
            in_degree_hist.append(in_degree_dict[i])
        else:
            in_degree_hist.append(0)
    print in_degree_hist
    return nx.degree_histogram(DG),in_degree_hist


def main():

    domain = 'ifeng.com'
    hist,hist1 = manage_data(domain)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    import numpy as np
    x= np.arange(len(hist))
    x1 = np.arange(len(hist1))
    ax.plot(x, [float(i)/sum(hist) for i in hist ],'b-')
    # ax.plot(x1,[float(i)/sum(hist1) for i in hist1],'r-')
    plt.show()

if __name__ == '__main__':
    main()


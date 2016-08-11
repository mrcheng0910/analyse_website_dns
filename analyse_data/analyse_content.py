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
from networkx.drawing.nx_pydot import graphviz_layout


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


def manage_data(domain='baidu.com'):
    visit_total = 0  # 总共访问次数
    domain_pkt = get_data(domain)
    # 域名数量
    domain_count = len(domain_pkt['details'])
    # cname_count, ip_count
    cname_count,ip_count = get_ip_cname(domain_pkt['details'])

    for i in domain_pkt['details']:
        visit_total += i['visit_count']

    print visit_total
    print domain_count
    print cname_count
    print ip_count


def get_ip_cname(data):
    """
    有图例，图例需要再进行更改
    :return:
    """
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
    node_cname = []
    node_ip = []
    for i in node_dict:

        if 'ip' in list(node_dict[i]):
            node_ip.append(i)
        elif 'cname' in list(node_dict[i]):
            node_cname.append(i)

    return len(node_cname),len(node_ip)


if __name__ == '__main__':
    # main1()
    manage_data()

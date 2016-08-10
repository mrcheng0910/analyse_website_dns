# encoding: utf-8

"""
@author: 程亚楠
@function: 统计各个探测包中探测域名的详细信息，并且将详细信息存入的数据库中
@create_date: 2016-7-31
"""

import socket
from domain_collection import get_domain_collection, insert
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from ip_location.ip2Region import Ip2Region

searcher = Ip2Region('./ip_location/ip2region.db')  # IP定位


def ip2region(ip=None):
    """
    得到IP的地理位置和运营商
    :param ip: 待查询IP
    :return
        city: ip所在城市，若城市为空，则为国家
        network_operator: 运营商，可能为空
    """
    if ip == "" or ip is None:
        return

    data = searcher.btreeSearch(ip)
    region = data['region']
    region = region.split('|')
    city = region[3]

    network_operator = region[4]
    if city == '0':
        city = region[0]

    return city,network_operator


def valid_ip(address):
    """
    是否为合法IP
    :param address: IP地址
    :return
        True: 合法
        False： 非法
    """
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


def get_data(domain=None, start_date=None, end_date=None):
    """
    通过域名和开始截止时间，获取域名的探测数据集
    :param domain: 查询的域名
    :param start_date: 开始日期
    :param end_date: 截止日期
    :return
        domain_pkts: 该域名的探测结果集合，若无则为None
    :exception
        域名不存在，返回None
        输入为空，返回None
    """
    if domain is None or start_date is None or end_date is None:  # 之一条件不符合，返回None
        return

    domain_collection = get_domain_collection(domain)
    if domain_collection.count() == 0:  # 域名不存在
        print "域名不存在"
        return
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(hours=24)
    domain_pkts = domain_collection.find({'visit_time': {'$lte': end_date, '$gte': start_date}})
    if domain_pkts.count() == 0:  # 不存在集合
        print "该集合无符合条件数据"
        return
    return  domain_pkts


def get_frequency_appeared_domain(domain_pkt = None):
    """
    获取该次探测包中域名出现的次数和出现的域名列表
    :param domain_pkt: 探测包
    :return
        appeared_domain: 域名出现的列表
        qry_counter: 域名出现的次数
    :exception
        domain_pkt为空，则返回None
    """

    if domain_pkt is None:
        print "探测包为空"
        return
    qry_counter = Counter()  # 保存域名出现的次数
    appeared_domain = set()  # 保存出现的域名,不重复
    dns_details = defaultdict(set)
    # dsn_details = Counter()

    for pkt in domain_pkt['details']:
        if len(pkt['dns']) > 1:   # 分析dns响应报文
            domain_name = pkt['dns']['qry_name']   # 解析的域名
            qry_counter[domain_name] += 1      # 在该报文中出现的次数
            appeared_domain.add(domain_name)    # 域名出现的次数

            for i in pkt['dns']['details']:       # 解析dns报文详细内容
                dns_details[domain_name].add(
                    (i['domain_name'], i['dm_data'])
                )

    return appeared_domain, qry_counter, dns_details


def cal_pkts_domain_num(domain=None, start_date=None, end_date=None):
    """
    计算多次探测某域名中，所有的域名解析数据中的域名数量，包括出现次数和出现频率
    :param domain: 待查询的域名
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return:
        pkts_count: 探测次数
        qry_counter_domains: 域名出现的次数
        pkts_appeared_domains: 每次探测出现的域名频率
    """
    pkts_appeared_domains = Counter()
    qry_counter_domains = Counter()
    dns_details_domains = defaultdict(set)
    pkts = get_data(domain, start_date, end_date)

    if pkts is None:
        return

    pkts_count = pkts.count()

    for pkt in pkts:
        appeared_domain, qry_counter,dns_details = get_frequency_appeared_domain(pkt)

        qry_counter_domains += qry_counter   # 解析的域名出现的总次数

        for i in appeared_domain:      # 出现的域名
            pkts_appeared_domains[i] += 1

        # print dns_details
        for v in dns_details:
            for i in dns_details[v]:
                dns_details_domains[v].add(i)

    return pkts_count,qry_counter_domains,pkts_appeared_domains, dns_details_domains


def main(domain_name,start_date,end_date):
    # domain_name = 'hitwh.edu.cn'
    # start_date = '2016-6-25'
    # end_date = '2016-8-3'
    results = {
        "domain_name": domain_name,    # 检测的网站名称
        "detected_geo": "威海",   # 探测点地理位置
        "dns": "223.5.5.5",   # dns的IP
        "dns_geo": "杭州",     #dns的地理位置
        "detected_network_operator": "联通",  # 探测点运营商
        "dns_network_operator": "阿里云",  # dns的运营商
        "details":[   # 解析详细内容
            {
                "qry_name": "",   # 解析的域名名称
                "visit_count": 0,  # 解析次数
                "answers":[       # 响应内容
                    {
                        "dm_type": "",   # 类型
                        "domain_name": "",  # 名称
                        "dm_data": "",    # 结果
                        "geo":"",    # 若dm_type为IP则显示，否则为空 #todo: 注意和dm_type对应，有的IP没有地理位置
                        "network_operator": ""  # 若dm_type为IP则显示，否则为空
                    }
                ]
            }
        ]

    }

    pkts_count, domain_frequency, domain_appeared,dns_details = cal_pkts_domain_num(domain_name, start_date, end_date)
    details = []
    for i in domain_appeared:
        if domain_appeared[i] >= pkts_count/2:  # pkts_count/2该方法需要待验证 todo:待验证是否正确
            visit_count = domain_frequency[i] / domain_appeared[i]
            tmp = {}
            answer = []
            if visit_count == 0:  # 如果为0,则设为1
                visit_count = 1
            tmp['qry_name'] = i
            tmp['visit_count'] = visit_count
            for v, y in dns_details[i]:
                if valid_ip(y.strip()):
                    city,op = ip2region(y)
                    answer.append({
                        "dm_type": "A",
                        "domain_name": v,
                        "dm_data": y,
                        "geo": city,
                        "network_operator": op
                    })
                else:
                    answer.append({
                        'dm_type': "CNAME",
                        "domain_name": v,
                        "dm_data": y
                    })
            tmp['answers'] = answer
            details.append(tmp)

    results['details'] = details
    insert('data_info',results)

if __name__ == '__main__':
    main('ifeng.com','2016-6-25','2016-8-6')
    searcher.close()
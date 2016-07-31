# encoding:utf-8
"""
@author: Cheng ya'nan
@function:
@date: 2016-7-31
@update:
"""
from models.domain_collection import get_domain_collection
import pymongo
from datetime import datetime,timedelta,date
import json
import collections
from collections import Counter, OrderedDict


def get_dm_content(domain,start_date,end_date):

    content = []
    visit_time = '2016-07-21 15:16:51.847000'
    visit_time = datetime.strptime(visit_time, "%Y-%m-%d %H:%M:%S.%f")
    domain_collection = get_domain_collection(domain)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    # end = datetime.utcnow()+ timedelta(hours=8)  # 当前时间，timedelta是为了成为北京时间
    end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(hours=24)

    domain_pkts = domain_collection.find({'visit_time': {'$lte': end_date,'$gte': start_date}})
    for pkt in domain_pkts:
        qry_domains = {}
        resp_domains = {}
        tmp = dict(visit_time="", pkt_count=0, qry_pkt=0, resp_pkt=0, qry_domain_count=0, resp_domain_count=0,
                   qry_domains=qry_domains, resp_domains=resp_domains)
        visit_time = pkt['visit_time'].strftime("%Y-%m-%d %H:%M:%S.%f")
        tmp['visit_time'] = visit_time
        tmp['pkt_count'] = pkt['pkt_count']
        for i in pkt['details']:
            if len(i['dns']) <= 1:
                tmp['qry_pkt'] += 1
                if qry_domains.has_key(i['dns']['qry_name']):
                    qry_domains[i['dns']['qry_name']] += 1
                else:
                    qry_domains[i['dns']['qry_name']] = 1
            else:
                tmp['resp_pkt'] += 1
                if resp_domains.has_key(i['dns']['qry_name']):
                    resp_domains[i['dns']['qry_name']] += 1
                else:
                    resp_domains[i['dns']['qry_name']] = 1

        tmp['qry_domains'] = collections.OrderedDict(sorted(qry_domains.items()))
        tmp['resp_domains'] = collections.OrderedDict(sorted(resp_domains.items()))
        tmp['qry_domain_count'] = len(qry_domains)
        tmp['resp_domain_count'] = len(resp_domains)
        content.append(tmp)
    return json.dumps(content)


def get_data(domain=None,start_date=None,end_date=None):
    """
    获取探测数据
    :return:
    """
    domain_collection = get_domain_collection(domain)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(hours=24)
    domain_pkts = domain_collection.find({'visit_time': {'$lte': end_date, '$gte': start_date}})
    return  domain_pkts


def get_pkt_appeared_domain(domain_pkt = None):
    """
    to get the  domain names of appeared and frequency number in the this detected pkt
    :param domain_pkt: the data of the pkt
    :return
        appeared_domain: the appeared domain name in the pkt
        qry_counter: the frequency number of the domain names in the pkt
    """

    if domain_pkt is None:
        return
    qry_counter = Counter()  # to save frequency number of the domain names
    appeared_domain = []  # save appeared domain name
    for pkt in domain_pkt['details']:
        if len(pkt['dns']) <= 1:
            domain_name = pkt['dns']['qry_name']
            qry_counter[domain_name] += 1
            appeared_domain.append(domain_name)

    appeared_domain = list(OrderedDict.fromkeys(appeared_domain))  # domain deduplicate
    return appeared_domain, qry_counter


def domain_pks(domain=None,start_date=None,end_date=None):

    pkts_appeared_domains = Counter()
    qry_counter_domains = Counter()
    pkts = get_data(domain, start_date, end_date)

    for pkt in pkts:
        appeared_domain, qry_counter = get_pkt_appeared_domain(pkt)
        qry_counter_domains += qry_counter
        for i in appeared_domain:
            pkts_appeared_domains[i] += 1
    print pkts.count()
    print qry_counter_domains
    print pkts_appeared_domains
    for i in pkts_appeared_domains:
        print pkts_appeared_domains[i]
    # for i in pkts_appeared_domains:
    #     if pkts_appeared_domains[i]>=10:
    #         print i,pkts_appeared_domains[i]


def main():
    domain = 'qq.com'
    start_date = '2016-7-28'
    end_date = '2016-7-31'
    domain_pks(domain,start_date,end_date)

if __name__ == '__main__':
    main()
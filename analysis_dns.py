#!/usr/bin/python
# encoding:utf-8
"""
从网卡捕获dns包数据，并且解析出各个字段内容
注意：需要从adminstrater权限运行
作者：程亚楠
时间：2016.6.11
"""

import pyshark
from db_manage import insert

def capture_dns(interface='eth0', timeout=30):
    """
    从网卡抓取dns包
    timeout: 抓包时间，默认为30s
    :return: capture dns包
    """
    capture = pyshark.LiveCapture(interface=interface,bpf_filter='udp and port 53')
    capture.sniff(timeout=timeout)
    return capture


def extract_pkt_dns(pkt_dns):
    """
    提取dns层各个字段内容
    :param pkt_dns:
    :return:
    """
    dns_query = {}
    dns_response = {}
    if pkt_dns.flags_response == '0':    # 查询报文
        # print "查询报文"
        # print pkt_dns._all_fields
        dns_query['qry_name'] = pkt_dns.qry_name
        # print dns_query
        return dns_query

    elif pkt_dns.flags_response == '1':   # 响应报文
        # print "响应报文"
        # print pkt_dns._all_fields
        # pkt_dns.pretty_print()
        try:
            dns_response['qry_name'] = pkt_dns.qry_name  # 查询的域名
        except AttributeError:
            print "qry_name error"
            print pkt_dns._all_fields
            dns_response['qry_name']=""
        try:
            dns_response['resp_ttl'] = pkt_dns.resp_ttl  # 生存时间
        except AttributeError:
            print 'resp_ttl error'
            dns_response['resp_ttl'] = 0

        try:
            dns_response['time'] = pkt_dns.time   # 相应时间
        except AttributeError:
            print 'time error'
            dns_response['time'] = 0


        try:
            dns_response['resp_len'] = int(pkt_dns.resp_len)  # 响应报文大小
        except AttributeError:
            print 'resp_len error'
            dns_response['resp_len'] = 0

        dns_response['count_answers'] = int(pkt_dns.count_answers)  # 回答个数
        dns_response['count_auth_rr'] = int(pkt_dns.count_auth_rr)
        try:
            dns_response['response_to'] = int(pkt_dns.response_to)  # 响应请求报文的包number
        except AttributeError:
            print 'resonse_to error'
            dns_response['response_to']= 0

        dns_response['details'] = extract_answers_details(pkt_dns, int(pkt_dns.count_answers),int(pkt_dns.count_auth_rr))
        # print dns_response
        return dns_response


def extract_answers_details(pkt_dns,count_answers,count_auth_rr):
    """
    提取回答报文中的详细信息
    :param pkt:
    :return:
    """
    answers_list = []

    pkt_str = pkt_dns.__str__()
    pkt_list = pkt_str.split('\n\t')
    if count_answers>0:
        answers_index = pkt_list.index('Answers')
        last_index = answers_index + 1 + count_answers
    else:
        # print pkt_list
        answers_index = pkt_list.index('Authoritative nameservers')
        last_index = answers_index + 1 + count_auth_rr

    for i in range(answers_index+1,last_index):
        answer_tmp = {}
        domain_last_index = pkt_list[i].find(':')
        domain_name = pkt_list[i][:domain_last_index]
        exc_domain = pkt_list[i][domain_last_index+1:].strip()
        exc_domain_list = exc_domain.split(',')

        try:

            dm_type = exc_domain_list[0].strip().split(' ')[1]
            dm_class = exc_domain_list[1].strip().split(' ')[1]
            dm_data= exc_domain_list[2].strip().split(' ')[1]
        except:
            pkt_dns.pretty_print()
            print pkt_dns._all_fields
        try:
            answer_tmp['domain_name'] = domain_name
            answer_tmp['dm_type'] = dm_type
            answer_tmp['dm_class'] = dm_class
            answer_tmp['dm_data'] = dm_data
        except:
            print "error"
            pkt_dns.pretty_print()

        answers_list.append(answer_tmp)

    return answers_list


def extract_pkt_ip(pkt_ip):
    """
    提取各个包中ip层字段内容，请求报文与响应报文格式相同
    :param pkt_ip:
    :return:
    """
    ip_layers = {}
    ip_layers['version'] = pkt_ip.version
    ip_layers['hdr_len'] = pkt_ip.hdr_len
    ip_layers['len'] = pkt_ip.len
    ip_layers['src_host'] = pkt_ip.src_host
    ip_layers['dst_host'] = pkt_ip.dst_host
    ip_layers['ttl'] = pkt_ip.ttl

    # print ip_layers
    return ip_layers


def extract_pkt_udp(pkt_udp):
    """
    提取各个包中udp层字段内容，请求报文与响应报文格式相同
    :param pkt_udp:
    :return:
    """
    udp_layers = {}
    udp_layers['src_port'] = pkt_udp.srcport
    udp_layers['dst_port'] = pkt_udp.dstport
    udp_layers['length'] = pkt_udp.length

    # print udp_layers
    return udp_layers


def extract_pkt_frame(pkt_frame):
    """
    提取frame中的字段内容
    :param pkt_frame:
    :return:
    """

    frame_layers = {}
    frame_layers['length'] = pkt_frame.len

    # print frame_layers
    return frame_layers

def extract_pkt_fields(pkt):
    """
    提取包捕获时间/包号/含有pkt个数
    :param pkt:
    :return:
    """
    pkt_fields = {}
    pkt_fields['sniff_time'] = pkt.sniff_time
    pkt_fields['number'] = pkt.number
    # pkt_fields['pkt_count'] = len(pkt)

    # print pkt_fields
    return pkt_fields


def extract_capture(web_site=None, timeout=20):
    """
    :param timeout:
    :return:
    """
    c = capture_dns(timeout=timeout)
    print len(c)
    pkt_count = len(c)
    detail = []

    for i in range(len(c)):
        pkt_detail = {}
        pkt = c[i]
        pkt_detail['pkt'] = extract_pkt_fields(pkt)
        pkt_detail['frame'] = extract_pkt_frame(pkt.frame_info)
        pkt_detail['ip'] = extract_pkt_ip(pkt.ip)
        pkt_detail['udp'] = extract_pkt_udp(pkt.udp)
        pkt_detail['dns'] = extract_pkt_dns(pkt.dns)
        detail.append(pkt_detail)

    insert(web_site,pkt_count=pkt_count,detail=detail)

# if __name__ == '__main__':

    # extract_capture(web_site='www.hitwh.com',timeout=20)
#encoding:utf-8

import pyshark

def capture_dns(interface='eth0', timeout=30):
    """
    从网卡抓取dns包
    timeout: 抓包时间，默认为30s
    :return: capture dns包
    """
    capture = pyshark.LiveCapture(interface=interface,only_summaries=True)
    capture.sniff(timeout=timeout)
    print 'total: ' + str(len(capture))
    # return capture


# capture_dns()
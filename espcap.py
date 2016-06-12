#!/usr/bin/env python

import os
# import signal
import sys
# import click
from datetime import datetime

import pyshark

supported_protocols = {}

# Get supported application protocols
def get_protocols():
    global supported_protocols
    fp = None
    if os.path.isfile('./protocols.list'):
        fp = open('./protocols.list')
    elif os.path.isfile('../conf/protocols.list'):
        fp = open('../conf/protocols.list')
    elif os.path.isfile('conf/protocols.list'):
        fp = open('conf/protocols.list')
    protocols = fp.readlines()
    for protocol in protocols:
        protocol = protocol.strip()
        supported_protocols[protocol] = 1

# Get application level protocol
def get_highest_protocol(packet):
    global supported_protocols
    if not supported_protocols:
        get_protocols()
    for layer in reversed(packet.layers):
        if layer.layer_name in supported_protocols:
            return layer.layer_name
    return 'wtf'

# Get the protocol layer fields
def get_layer_fields(layer):
    layer_fields = {}
    for field_name in layer.field_names:
        if len(field_name) > 0:
            layer_fields[field_name] = getattr(layer, field_name)
    return layer_fields

# Returns a dictionary containing the packet layer data
def get_layers(packet):
    n = len(packet.layers)
    highest_protocol = get_highest_protocol(packet)
    layers = {}

    # Link layer
    layers[packet.layers[0].layer_name] = get_layer_fields(packet.layers[0])
    layer_above_transport = 0

    # Get the rest of the layers
    for i in range(1,n):
        layer = packet.layers[i]

        # Network layer - ARP
        if layer.layer_name == 'arp':
            layers[layer.layer_name] = get_layer_fields(layer)
            return highest_protocol, layers

        # Network layer - IP or IPv6
        elif layer.layer_name == 'ip' or layer.layer_name == 'ipv6':
            layers[layer.layer_name] = get_layer_fields(layer)

        # Transport layer - TCP, UDP, ICMP, IGMP, IDMP, or ESP
        elif layer.layer_name == 'tcp' or layer.layer_name == 'udp' or layer.layer_name == 'icmp' or layer.layer_name == 'igmp' or layer.layer_name == 'idmp' or layer.layer_name == 'esp':
            layers[layer.layer_name] = get_layer_fields(layer)
            if highest_protocol == 'tcp' or highest_protocol == 'udp' or highest_protocol == 'icmp' or highest_protocol == 'esp':
                return highest_protocol, layers
            layer_above_transport = i+1
            break

        # Additional transport layer data
        else:
            layers[layer.layer_name] = get_layer_fields(layer)
            layers[packet.layers[i].layer_name]['envelope'] = packet.layers[i-1].layer_name

    for j in range(layer_above_transport,n):
        layer = packet.layers[j]

        # Application layer
        if layer.layer_name == highest_protocol:
            layers[layer.layer_name] = get_layer_fields(layer)

        # Additional application layer data
        else:
            layers[layer.layer_name] = get_layer_fields(layer)
            layers[layer.layer_name]['envelope'] = packet.layers[j-1].layer_name

    return highest_protocol, layers

# Dump raw packets to stdout
def dump_packets(capture, file_date_utc, count,url):
    pkt_no = 1
    for packet in capture:
        highest_protocol, layers = get_layers(packet)
        sniff_timestamp = float(packet.sniff_timestamp)
        print url
        print 'Packet no.', pkt_no
        # print '* protocol        -', highest_protocol
        print '* file date UTC   -', file_date_utc.strftime('%Y-%m-%dT%H:%M:%S+0000')
        print '* sniff date UTC  -', datetime.utcfromtimestamp(sniff_timestamp).strftime('%Y-%m-%dT%H:%M:%S+0000')
        # print '* sniff timestamp -', sniff_timestamp
        # print '* layers'
        # for key in layers:
        #     print '\t', key, layers[key]
        print
        pkt_no += 1
        if count > 0 and pkt_no > count:
            return

# Live capture function
def live_capture(nic, bpf, count,url):
    try:
        sniff_date_utc = datetime.utcnow()
        capture = pyshark.LiveCapture(interface=nic, bpf_filter=bpf)
        dump_packets(capture, sniff_date_utc, count,url)

    except Exception as e:
        print '[ERROR] ', e


def main(nic, bpf, count=10,url='http://www.baidu.com'):

    if nic != None:
        live_capture(nic, bpf, count,url)


if __name__ == '__main__':
    url = sys.argv[1]
    # print url
    main(nic='eth0',bpf='udp port 53',url=url)
    print 'Done'
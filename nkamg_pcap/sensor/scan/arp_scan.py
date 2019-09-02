#!/usr/bin/env python
# -.- coding: utf-8 -.-
# arp_scan.py

import logging
import urllib2 as urllib
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy.config, scapy.layers.l2, scapy.route, socket, math, errno
from scapy.all import load_module, sniff

def resolve_mac(mac):
    try:
        url = "http://macvendors.co/api/vendorname/"
        request = urllib.Request(url + mac, headers={'User-Agent': "API Browser"})
        response = urllib.urlopen(request)
        vendor = response.read()
        vendor = vendor.decode("utf-8")
        vendor = vendor[:25]
        return vendor
    except:
        return "N/A"

def scan_network():

    def long2net(arg):
        if (arg <= 0 or arg >= 0xFFFFFFFF):
            raise ValueError("illegal netmask value", hex(arg))
        return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))

    def to_CIDR_notation(bytes_network, bytes_netmask):
        network = scapy.utils.ltoa(bytes_network)
        netmask = long2net(bytes_netmask)
        net = "%s/%s" % (network, netmask)
        if netmask < 16:
            return None

        return net


    def scan_and_print_neighbors(net, interface, timeout=1):
        hostsList = []
        try:
            ans, unans = scapy.layers.l2.arping(net, iface=interface, timeout=timeout, verbose=False)
            for s, r in ans.res:
                mac = r.sprintf("%Ether.src%")
                mac_vendor = resolve_mac(mac)
                ip = r.sprintf("%ARP.psrc%")

                #line = r.sprintf("%Ether.src%  %ARP.psrc%")
                hostsList.append([ip, mac, mac_vendor])
                #try:
                #    hostname = socket.gethostbyaddr(r.psrc)
                #    print hostname
                #    line += "," + hostname[0]
                #    print line
                #except socket.herror:
                #    pass
        except socket.error as e:
            if e.errno == errno.EPERM:     # Operation not permitted
                exit()
            else:
                raise
        return hostsList

    for network, netmask, _, interface, address in scapy.config.conf.route.routes:

        # skip loopback network and default gw
        if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
            continue

        if netmask <= 0 or netmask == 0xFFFFFFFF:
            continue

        # Skip APIPA network (corresponds to the 169.254.0.0/16 address range)
        # See https://fr.wikipedia.org/wiki/Automatic_Private_Internet_Protocol_Addressing for more details
        if network == 2851995648:
            continue

        net = to_CIDR_notation(network, netmask)

        if interface != scapy.config.conf.iface:
            # see http://trac.secdev.org/scapy/ticket/537
            continue

        if net:
            return scan_and_print_neighbors(net, interface)

if __name__ == "__main__":
    #load_module('p0f')    
    #sniff(prn=prnp0f, count=100, filter="tcp")

    hosts = scan_network()
    i = 0
    for ip, mac, mac_vendor in hosts:
        print "[{}]:\t{}\t{}\t{}".format(i, ip, mac, mac_vendor)
        i += 1


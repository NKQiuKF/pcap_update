#!/usr/bin/env python
# -.- coding: utf-8 -.-
# whois_info.py 

import netaddr
from netaddr import IPAddress
import requests 


def ripelookup(ipaddr):
    typefilter = "inetnum"
    source = "ripe"

    print ("Starting RIPE lookup for IP address: %s" % ipaddr)
    if (IPAddress(ipaddr).is_unicast()):
        #try:
        #    payload = { "type-filter" : typefilter, "source" : source, "query-string" : ipaddr }
        #    url = "http://rest.db.ripe.net/search"
        #    headers={"Accept" : "application/json"}
        #    response = requests.get(url, params=payload, headers=headers)
        #    jsonresult = response.json() 
        #    attributelist = jsonresult['objects']['object'][0]['attributes']['attribute']
        #    for i in attributelist:
        #        if i['name'] == "netname":
        #            netname = i['value']
        #            if netname == "NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK":                    
        #                return []
        #        elif i['name'] == "country":
        #            country = i['value']
        #        elif i['name'] == "descr":
        #            descr = i['value']
        #        elif i['name'] == "inetnum":
        #            netrange = netaddr.IPRange(i['value'].partition(' - ')[0],i['value'].partition(' - ')[2])
        #except requests.exceptions.ConnectionError:
        #    print ("RIPE Connection Error")
        payload = { "type-filter" : typefilter, "source" : source, "query-string" : ipaddr }
        url = "http://rest.db.ripe.net/search"
        headers={"Accept" : "application/json"}
        response = requests.get(url, params=payload, headers=headers)
        print response
        jsonresult = response.json() 
        print jsonresult
        
        attributelist = jsonresult['objects']['object'][0]['attributes']['attribute']
        for i in attributelist:
            if i['name'] == "netname":
                netname = i['value']
                if netname == "NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK":                    
                    return []
            elif i['name'] == "country":
                country = i['value']
            elif i['name'] == "descr":
                descr = i['value']
            elif i['name'] == "inetnum":
                netrange = netaddr.IPRange(i['value'].partition(' - ')[0],i['value'].partition(' - ')[2])
    return([netrange, country, descr, netname])

if __name__ == "__main__":
    ip_addr = "222.30.51.81" #"111.161.78.250"
    whois = ripelookup(ip_addr)
    print whois


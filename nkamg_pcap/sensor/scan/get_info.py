#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import subprocess
import re

def location(ip):
    cmd = 'curl -s ip.chinaz.com/%s' %ip
    html = subprocess.check_output(cmd, shell = True)
    #print(html)
    domtree = etree.HTML(html)
    location = domtree.xpath(u'//*[@id="leftinfo"]/div[3]/div[2]/p[2]/span[4]/text()')
    return location[0].encode('utf-8')

    
def main(ip):
    print(location(ip))


if __name__ == '__main__':
    ip = '45.33.32.156'     # scanme.nmap.org
    main(ip)

# coding=utf-8

import subprocess
import os
import csv
from datetime import date
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
# customized lib
from info_class import Host, Port


class NmapScanner(object):
    '''

    This module provides interfaces to execute the nmap command and save interesting information as csv format.

    Usage:
        from nmap_scanner import NmapScanner
        scanner = NmapScanner(cmd)
        scanner.execute() || csv_file = scanner.execute(get_csv = True)

    '''
    def __init__(self, command):
        # nmap comman string
        self._cmd = command
        self._tmp_file = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + '~tmp~.xml'
        # xml etree
        self._tree = None
        # csv header and data
        self._headers = ['row_id', 'ip', 'os', 'port_id', 'port_protocol', 'port_state', 'port_service_name']
        self._data = None           # data matrix except row_id
        # timestamp to name the csv file
        self._date = date.today()
        self._csv_file = '..' + os.path.sep + 'data' + os.path.sep

    def execute(self, get_csv = False):
        self._date = date.today()
        self._scan_with_xml_output()
        self._get_csv()
        if get_csv:
            abs_path = os.path.abspath(self._csv_file)
            return abs_path

    def _get_csv(self):
        # init xml etree
        self._tree = ET.ElementTree(file = self._tmp_file)
        # extract useful data from xml and save them in variable: self._data
        self._extract_from_xml()
        # write self._data from memory to disk as csv file
        self._store_as_csv()

    def _scan_with_xml_output(self):
        if '-oX' not in self._cmd:
            self._cmd += ' -oX ' + self._tmp_file
        else:
            # TODO: may be send message to server
            exit('command error')
        subprocess.call(self._cmd, shell = True)
        return

    # -----------------------------------------------------------------------
    # pattern in xml file is like:
    # <host>
    #   <address addr="127.0.0.1" addrtype="ipv4"/>
    #   <ports>
    #       <port protocol="tcp" portid="22">
    #           <state state="open" reason="syn-ack" reason_ttl="0"/>
    #           <service name="ssh" method="table" conf="3"/>
    #       </port>
    #   </ports>
    #   <os>
    #       <osmatch name="FreeBSD 6.2-RELEASE">
    #       </osmatch>
    #   <os>
    # </host>
    # <host>
    # ...
    def _extract_from_xml(self):
        hosts_info = []
        for host_layer in self._tree.iter(tag = 'host'):
            host = Host()
            ip = host_layer.find('address').get('addr')
            host.ip = ip

            # extracting ports from xml file
            ports = []
            for port_layer in host_layer.iter('port'):
                port = Port()
                port.portid = port_layer.get('portid')
                port.protocol = port_layer.get('protocol')
                for port_detail_layer in port_layer:
                    if port_detail_layer.tag == 'state':
                        port.state = port_detail_layer.get('state')
                    elif port_detail_layer.tag == 'service':
                        port.name = port_detail_layer.get('name')
                ports.append(port)
            if not ports:
                ports = [Port()]
            host.ports = ports

            # extracting os info
            os = host_layer.find('os').find('osmatch').get('name')
            host.os = os

            hosts_info.extend(host.to_csv())
        self._data = hosts_info

    # extract yy-mm-dd-time in xml file as the name of the csv file
    def _store_as_csv(self):
        # add row_id without modifying primitive data matrix: self._data
        data_matrix = []
        for (row_id, line) in enumerate(self._data):
            line_with_num = [row_id]
            line_with_num.extend(line)
            data_matrix.append(line_with_num)
        nmap_meta = self._tree.getroot()
        time = nmap_meta.get('start')
        self._csv_file += self._date.isoformat() + '-' + time + '.csv'
        with open(self._csv_file, 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(self._headers)
            f_csv.writerows(data_matrix)
        return

    def _test(self, dest_file = None):
        if dest_file:
            self._tmp_file = dest_file 
        self._get_csv()
        return (self._csv_file, self._data)


def main():
    cmd = 'sudo nmap -O 127.0.0.1 scanme.nmap.org'
    s = NmapScanner(cmd)
    #s.execute()

    # testing without nmap scan
    csv_file, hosts_info = s._test()
    print('\nThis is the whole data list\n')
    print(hosts_info)
    print('\nThese are data in readable format\n')
    for host in hosts_info:
        print(host)
    print('\nThis is the content of csv file\n')
    with open(csv_file, 'r') as f:
        print(f.read())

    # remove the test file
    os.remove(csv_file)
    print('the csv file has been removed')
    return
    
if __name__ == '__main__':
    main()

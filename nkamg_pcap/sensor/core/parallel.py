#!/usr/bin/env python


import os
import struct
import threading
import time
import datetime
import re
import commands
import json
import socket
from scapy.all import srp, ARP, Ether, conf
import uuid
import binascii

from enums import BLOCK_MARKER
from settings import BLOCK_LENGTH
from settings import config
from settings import REGULAR_SENSOR_SLEEP_TIME, SHORT_SENSOR_SLEEP_TIME, SCAN_PERIOD
#from core.common import load_trails
#from core.settings import trails
#from core.settings import LOAD_TRAILS_RETRY_SLEEP_TIME
#from core.settings import TRAILS_FILE

def read_block(buffer, i):
    offset = i * BLOCK_LENGTH % config.CAPTURE_BUFFER # a loop buffer

    while True:
        if buffer[offset] == BLOCK_MARKER.END:
            return None

        while buffer[offset] == BLOCK_MARKER.WRITE:
            time.sleep(SHORT_SENSOR_SLEEP_TIME)

        buffer[offset] = BLOCK_MARKER.READ
        buffer.seek(offset + 1)

        length = struct.unpack("=H", buffer.read(2))[0]
        retval = buffer.read(length)

        if buffer[offset] == BLOCK_MARKER.READ:
            break

    buffer[offset] = BLOCK_MARKER.NOP
    return retval


def write_block(buffer, i, block, marker=None):
    offset = i * BLOCK_LENGTH % config.CAPTURE_BUFFER

    while buffer[offset] == BLOCK_MARKER.READ:
        time.sleep(SHORT_SENSOR_SLEEP_TIME)

    buffer[offset] = BLOCK_MARKER.WRITE
    buffer.seek(offset + 1)

    buffer.write(struct.pack("=H", len(block)))
    buffer.write(block)

    buffer[offset] = marker or BLOCK_MARKER.NOP


def worker(buffer, n, offset, mod, process_packet):
    """
    Worker process used in multiprocessing mode
    """

    #def update_timer():
    #    if (time.time() - os.stat(TRAILS_FILE).st_mtime) >= config.UPDATE_PERIOD:
    #        _ = None
    #        while True:
    #            _ = load_trails(True)
    #            if _:
    #                trails.clear()
    #                trails.update(_)
    #                break
    #            else:
    #                time.sleep(LOAD_TRAILS_RETRY_SLEEP_TIME)
    #    threading.Timer(config.UPDATE_PERIOD, update_timer).start()

    #update_timer()

    count = 0L
    while True:
        try:
            if (count % mod) == offset:
                if count >= n.value:
                    time.sleep(REGULAR_SENSOR_SLEEP_TIME)
                    continue

                content = read_block(buffer, count)

                if content is None:
                    break

                if len(content) < 12:
                    continue

                sec, usec, ip_offset = struct.unpack("=III", content[:12])
                packet = content[12:]
                process_packet(packet, sec, usec, ip_offset)

            count += 1

        except KeyboardInterrupt:
            break


def check_local_hosts():
    try:
        if config.LOG_SERVER:
            server_host, server_port = config.LOG_SERVER.split(':')
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            HOST_LIST = {}
            lan = '192.168.0.1/24'
            #get all ip-mac
            ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=lan), timeout=2, verbose=False)
            print(ans)
            print(unans)
            """
            config.LOG_SERVER = '192.168.59.136:8337'
            <Results: TCP:0 UDP:0 ICMP:0 Other:1>
            <Unanswered: TCP:0 UDP:0 ICMP:0 Other:255>
            """
            if ans:
                for snd, rcv in ans:
                    cur_mac = rcv.sprintf("%Ether.src%")
                    cur_ip = rcv.sprintf("%ARP.psrc%")
                    HOST_LIST[cur_ip] = cur_mac
                    print(cur_mac)      # 78:2b:cb:17:08:c8
                    print(cur_ip)       # 192.168.0.120
            try:
                status, ScanInfo = commands.getstatusoutput("nbtscan 192.168.0.1-255")
            except Exception as ex:
                print(ex)
            print ScanInfo      # sh: 1: nbtscan: not found

            LineInfo = ScanInfo.split('\n')
            for line in LineInfo:
                CPULine = []
                find_ip = re.search('^[0-9]',line)
                if find_ip:
                    CPULine.append([tk for tk in line.split(' ') if tk])
                if CPULine:
                    #print(len(CPULine[0]))
                    if CPULine[0][0] in HOST_LIST.keys():
                        CPULine[0][len(CPULine[0])-1] = HOST_LIST[CPULine[0][0]]
                    else:
                        HOST_LIST[CPULine[0][0]] = CPULine[0][1].decode("gbk") + " " + CPULine[0][len(CPULine[0])-1]
            #print HOST_LIST
            tmpMac = uuid.UUID(int=uuid.getnode()).hex[-12:]
            sensorMac = ":".join([tmpMac[e:e+2] for e in range(0,11,2)])
            json_string = "IP_MAC_HOST_PACKET "+ sensorMac + " " + json.dumps(HOST_LIST)
            print json_string       # IP_MAC_HOST_PACKET 18:03:73:40:08:2d {"192.168.0.120": "78:2b:cb:17:08:c8"}
            s.sendto(json_string, (server_host, int(server_port)))
                    
        else:
            time.sleep(REGULAR_SENSOR_SLEEP_TIME)
    except KeyboardInterrupt:
            return
    thread = threading.Timer(SCAN_PERIOD, check_local_hosts)
    thread.daemon = True
    thread.start()

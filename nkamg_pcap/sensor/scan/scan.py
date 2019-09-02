#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Specifying the host (host can be ip, a range of ip, the whole subnet, and domain), and some options to start scanning by using nmap.

Typical Usage:
    scan <host>             This command is equivalent to nmap command 'sudo nmap -O <host>'

Usage:
    scan <host> [options]
    scan -h|--help
    scan -V|--version

Options:
    -Pn                     equal to nmap command -Pn
    --version, -V           show version info
    --help, -h

The host can be composed with the following formats:
    192.168.0.1             scanning single ip
    192.168.0.1-20          scanning a range of ips from 1 to 20
    192.168.0.0/24          scanning the subnet
    scanme.nmap.org         scanning by domain

'''

import sys, getopt
import argparse
from src.nmap_scan import NmapScanner

__version__ = '0.1'

def get_args():
    parser = argparse.ArgumentParser()
    # specify hosts
    parser.add_argument('host', help = 'specify the host here', nargs = '+')
    # -Pn
    parser.add_argument('-Pn', help = 'equal to nmap option -Pn', action = 'store_true')
    parser.add_argument('--version', '-V', action = 'version', version = __version__)

    args = parser.parse_args()
    return args

def get_cmd(args):
    cmd = 'sudo '
    cmd += 'nmap -O '
    if args.Pn:
        cmd += '-Pn '
    cmd += ' '.join(args.host)
        
    return cmd

def scan(cmd, local = True):
    scanner = NmapScanner(cmd)
    if local:
        csv_file = scanner.execute(get_csv = True)
    return csv_file

def main():
    args = get_args()
    cmd = get_cmd(args)
    csv_file = scan(cmd)

if __name__ == '__main__':
    main()

# coding=utf-8
import os
import psutil


def get_disk_info():
    disk_info = {}
    disk = os.statvfs("/")
    disk_info['available'] = disk.f_bsize * disk.f_bavail / 1024 / 1024 / 1024
    disk_info['all'] = disk.f_bsize * disk.f_blocks / 1024 / 1024 / 1024
    disk_info['free'] = disk.f_bsize * disk.f_bfree / 1024 / 1024 / 1024
    disk_info['used'] = disk_info['all'] - disk_info['free']
    return disk_info


def get_CPU_info(interval=1):
    return psutil.cpu_percent(interval)


def get_memory_info():
    phy_mem = psutil.virtual_memory()
    memory_info = {'used': int(phy_mem.used / 1024 / 1024), 'all': int(phy_mem.total / 1024 / 1024)}
    return memory_info


def get_server_info():
    server_info = {'cpu': get_CPU_info(), 'mem': get_memory_info(), 'disk': get_disk_info()}
    return server_info


if __name__ == '__main__':
    get_server_info()

# coding=utf-8
import os
import signal
import socket
import SocketServer
import sys
import threading
import time
import traceback
import json

from common import check_sudo
from settings import config
from settings import CONDENSE_ON_INFO_KEYWORDS, CONDENSED_EVENTS_FLUSH_PERIOD
from settings import DEFAULT_ERROR_LOG_PERMISSIONS, DEFAULT_EVENT_LOG_PERMISSIONS
from settings import TIME_FORMAT
from settings import WHITELIST

import datetime

Packet_buffer = []
Last_send_time = datetime.datetime(2016, 01, 01)

_thread_data = threading.local()
IP_MAC_DICT_SS = {}
IP_MAC_IN_LOG = []


def create_log_directory():
    if not os.path.isdir(config.LOG_DIR):
        if check_sudo() is False:
            exit("[!] please run with sudo/Administrator privileges")
        os.makedirs(config.LOG_DIR)
    print("[i] using '%s' for log storage" % config.LOG_DIR)


def get_event_log_handle(sec, flags=os.O_APPEND | os.O_CREAT | os.O_WRONLY):
    localtime = time.localtime(sec)
    _ = os.path.join(config.LOG_DIR, "%d-%02d-%02d.log" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday))
    if _ != getattr(_thread_data, "event_log_path", None):
        if not os.path.exists(_):
            open(_, "w+").close()
            os.chmod(_, DEFAULT_EVENT_LOG_PERMISSIONS)
        _thread_data.event_log_path = _
        _thread_data.event_log_handle = os.open(_thread_data.event_log_path, flags)
    return _thread_data.event_log_handle


def get_error_log_handle(flags=os.O_APPEND | os.O_CREAT | os.O_WRONLY):
    if not hasattr(_thread_data, "error_log_handle"):
        _ = os.path.join(config.LOG_DIR, "error.log")
        if not os.path.exists(_):
            open(_, "w+").close()
            os.chmod(_, DEFAULT_ERROR_LOG_PERMISSIONS)
        _thread_data.error_log_path = _
        _thread_data.error_log_handle = os.open(_thread_data.error_log_path, flags)
    return _thread_data.error_log_handle


def safe_value(value):
    retval = str(value or '-')
    if any(_ in retval for _ in (' ', '"')):
        retval = "\"%s\"" % retval.replace('"', '""')
    return retval


def ip_mac_event(ip_mac_dict={}):
    if not ip_mac_dict:
        return
    try:
        remote_host, remote_port = config.LOG_SERVER.split(':')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        json_string = "IP_MAC_PACKET " + json.dumps(ip_mac_dict)
        s.sendto(json_string, (remote_host, int(remote_port)))
    except Exception, ex:
        print(str(ex))


def log_event(event_tuple, packet=None, skip_write=False, skip_condensing=False):
    global Packet_buffer
    global Last_send_time
    try:
        sec, usec, src_ip, src_port, dst_ip, dst_port, proto, trail_type, trail, \
        info, ref, HostInfo, DomainInfo, BrowserInfo = event_tuple[:14]
        # print sec
        if config.LOG_SERVER:
            server_host, server_port = config.LOG_SERVER.split(':')
        # catch server ip
        if not config.LOG_SERVER or not any(_ == server_host for _ in (src_ip, dst_ip)):
            # catch server ip
            if not skip_write:
                localtime = "%s.%06d" % (time.strftime(TIME_FORMAT, time.localtime(int(sec))), usec)
                if False:
                    if (sec - getattr(_thread_data, "condensed_events_flush_sec", 0)) > CONDENSED_EVENTS_FLUSH_PERIOD:
                        _thread_data.condensed_events_flush_sec = sec

                        for key in getattr(_thread_data, "condensed_events", []):
                            condensed = False
                            events = _thread_data.condensed_events[key]

                            first_event = events[0]
                            condensed_event = [_ for _ in first_event]

                            for i in xrange(1, len(events)):
                                current_event = events[i]
                                for j in xrange(3, 7):  # src_port, dst_ip, dst_port, proto
                                    if current_event[j] != condensed_event[j]:
                                        condensed = True
                                        if not isinstance(condensed_event[j], set):
                                            # condensed_event[j] = set((condensed_event[j],))
                                            condensed_event[j] = {condensed_event[j]}
                                        condensed_event[j].add(current_event[j])

                            if condensed:
                                for i in xrange(len(condensed_event)):
                                    if isinstance(condensed_event[i], set):
                                        condensed_event[i] = ','.join(str(_) for _ in sorted(condensed_event[i]))

                            log_event(condensed_event, skip_condensing=True)

                        _thread_data.condensed_events = {}

                    if any(_ in info for _ in CONDENSE_ON_INFO_KEYWORDS):
                        if not hasattr(_thread_data, "condensed_events"):
                            _thread_data.condensed_events = {}
                        key = (src_ip, trail)
                        if key not in _thread_data.condensed_events:
                            _thread_data.condensed_events[key] = []
                        _thread_data.condensed_events[key].append(event_tuple)
                        return

                event = "%s** %s** %s\n" % (safe_value(localtime), safe_value(config.SENSOR_NAME),
                                            "** ".join(safe_value(_) for _ in event_tuple[2:]))
                if not config.DISABLE_LOCAL_LOG_STORAGE:
                    handle = get_event_log_handle(sec)
                    os.write(handle, event)
                if config.LOG_SERVER:
                    remote_host, remote_port = config.LOG_SERVER.split(':')
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto("%s %s" % (sec, event), (remote_host, int(remote_port)))
                if config.DISABLE_LOCAL_LOG_STORAGE and not config.LOG_SERVER or config.console:
                    sys.stderr.write(event)
                    sys.stderr.flush()
            if config.plugin_functions:
                for _ in config.plugin_functions:
                    _(event_tuple, packet)
    except SystemError, ex:
        print(ex)
    except (OSError, IOError):
        if config.SHOW_DEBUG:
            traceback.print_exc()


def log_error(msg):
    try:
        handle = get_error_log_handle()
        os.write(handle, "%s %s\n" % (time.strftime(TIME_FORMAT, time.localtime()), msg))
    except (OSError, IOError):
        if config.SHOW_DEBUG:
            traceback.print_exc()


def set_sigterm_handler():
    def handler(signum, frame):
        log_error("SIGTERM")
        raise SystemExit

    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, handler)


if __name__ != "__main__":
    set_sigterm_handler()

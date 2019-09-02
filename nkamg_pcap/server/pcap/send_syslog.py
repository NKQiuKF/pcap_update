# !/usr/bin/env python
# ! -*- coding:utf-8 -*-
import os
import pandas as pd
import logging
import logging.handlers
import time
import datetime
import ConfigParser

# TODO:
# 1. 多个Sensor的情况，会有多个Sensor ID，目前是确定为monitor01. 后期出现
# 多Sensor的时候要，Sensor ID要修改成可变的
# 2. time固定在biz之后，写到header里面

config = ConfigParser.ConfigParser()
config.read("config.ini")

SYSLOG_IP = config.get("syslog", "syslog_ip")
SYSLOG_PORT = config.get("syslog", "syslog_port")
PATH_SYSLOG = config.get("directory", "path_temp")
SENSOR_ID = config.get("sensor", "sensor_id")
SPACE_STRING = ', '
VOLUME = 'Kbps'

logger = logging.getLogger()
fh = logging.handlers.SysLogHandler((SYSLOG_IP,
     int(SYSLOG_PORT)), logging.handlers.SysLogHandler.LOG_AUTH)
formatter = logging.Formatter\
    ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


ftp_path = os.path.join(PATH_SYSLOG, 'ftp.log')
http_path = os.path.join(PATH_SYSLOG, 'http.log')
dns_path = os.path.join(PATH_SYSLOG, 'dns.log')
conn_path = os.path.join(PATH_SYSLOG, 'conn.log')

def replace_str(str):
  if str is '-':
    return ''
  else:
    return str
def flow_calculation(d1, d2):
  return float("%.3f" % (d1 * 8 / (d2 * 1024)))

def send_device_syslog(msg):
  new_msg = 'id=' + str(SENSOR_ID) +", type=device, biz=office, " + 'time='
  d = datetime.datetime.fromtimestamp(msg.time)
  str_time = d.strftime("%Y-%m-%d %H:%M:%S")
  new_msg = new_msg + str_time + SPACE_STRING
  new_msg = new_msg + "orig_h=" + msg.orig_h + ", orig_p=" + str(msg.orig_h)
  new_msg = new_msg + ", proto=" + msg.proto + ", resp_h=" \
            + msg.resp_h + ", resp_p=" + str(msg.resp_p)
  print new_msg
  logger.warning(new_msg)

def send_traffic_syslog(df):
  # send traffic information to syslog server
  total_time = 30.0
  dt_head = df.head(1)
  total_flow_orig = df['orig_ip_bytes'].sum()
  total_flow_resp = df['resp_ip_bytes'].sum()
  total_sending_volumn = flow_calculation(total_flow_orig, total_time)
  total_receiving_volumn = flow_calculation(total_flow_resp, total_time)
  total = float(total_sending_volumn) + float(total_receiving_volumn)
  d = datetime.datetime.fromtimestamp(dt_head['time'])
  str_time = d.strftime("%Y-%m-%d %H:%M:%S")
  traffic_syslog_head = 'id=' + str(SENSOR_ID) + SPACE_STRING \
                        + "type=traffic" + SPACE_STRING \
                        + "biz=office, time=" + str_time
  df_tcp = df[df['proto'] == 'tcp']
  df_udp = df[df['proto'] == 'udp']
  df_icmp = df[df['proto'] == 'icmp']
  total_tcp_sending = df_tcp['orig_ip_bytes'].sum()
  total_tcp_receiving = df_tcp['resp_ip_bytes'].sum()
  total_udp_sending = df_udp['orig_ip_bytes'].sum()
  total_udp_receiving = df_udp['resp_ip_bytes'].sum()
  total_icmp_sending = df_icmp['orig_ip_bytes'].sum()
  total_icmp_receiving = df_icmp['resp_ip_bytes'].sum()

  tcp_s_volumn = flow_calculation(total_tcp_sending, total_time)
  tcp_r_volumn = flow_calculation(total_tcp_receiving, total_time)
  udp_s_volumn = flow_calculation(total_udp_sending, total_time)
  udp_r_volumn = flow_calculation(total_udp_receiving, total_time)
  icmp_s_volumn = flow_calculation(total_icmp_sending, total_time)
  icmp_r_volumn = flow_calculation(total_icmp_receiving, total_time)

  total_msg = "total=" + str(total) + VOLUME + SPACE_STRING
  total_msg = total_msg + "send=" + str(total_sending_volumn) + VOLUME + \
              SPACE_STRING + "recv=" + str(total_receiving_volumn) + VOLUME \
              + SPACE_STRING
  total_msg = total_msg + "tcp_send=" + str(tcp_s_volumn) + VOLUME \
              + SPACE_STRING + "udp_send=" + str(udp_s_volumn) + VOLUME \
              + SPACE_STRING + "icmp_send=" + str(icmp_s_volumn) + VOLUME \
              + SPACE_STRING
  total_msg = total_msg + "tcp_recv=" + str(tcp_r_volumn) + VOLUME \
              + SPACE_STRING + "udp_recv=" + str(udp_r_volumn) \
              + VOLUME + SPACE_STRING + "icmp_recv=" + str(icmp_r_volumn) \
              + VOLUME
  new_msg = traffic_syslog_head + SPACE_STRING + total_msg
  print(new_msg)
  logger.warning(new_msg)

def send_ftp_syslog(msg):
  new_msg_head = 'id=' + str(SENSOR_ID) + SPACE_STRING + \
                 'type=ftp, biz=office, time='
  d = datetime.datetime.fromtimestamp(msg.time)
  str_time = d.strftime("%Y-%m-%d %H:%M:%S")
  new_msg = new_msg_head + str_time + SPACE_STRING + 'orig_h=' \
            + str(msg.orig_h) + SPACE_STRING +'orig_p=' \
            + str(msg.orig_p) + SPACE_STRING + 'resp_h=' \
            + str(msg.resp_h) + SPACE_STRING + 'resp_p=' \
            + str(msg.resp_p)
  new_msg = new_msg + SPACE_STRING + 'user=' + str(msg.user) \
            + SPACE_STRING + 'password=hidden' + SPACE_STRING \
            + 'command=' + str(msg.cmd) + SPACE_STRING + 'arg=' \
            + str(msg.arg) + SPACE_STRING + 'mime_type=' \
            +str(msg.mime_type)
  new_msg = new_msg + SPACE_STRING + 'file_size=' + str(msg.file_size) \
            + SPACE_STRING + 'reply_code=' + str(msg.reply_code) \
            + SPACE_STRING + 'reply_msg=' + str(msg.reply_msg) \
            + SPACE_STRING + 'data_channel.passive='
  new_msg = new_msg + replace_str(str(msg.data_channel_passive)) \
            + SPACE_STRING + 'data_channel.resp_h=' \
            + replace_str(str(msg.data_channel_resp_h))\
            + SPACE_STRING + 'data_channel.resp_p=' \
            + replace_str(str(msg.data_channel_resp_p))
  print (new_msg)
  logger.warning(new_msg)

def send_dns_syslog(msg):
  new_msg_head = 'id=' + str(SENSOR_ID) + ', type=dns, biz=office, time='
  d = datetime.datetime.fromtimestamp(msg.time)
  str_time = d.strftime("%Y-%m-%d %H:%M:%S")
  new_msg = new_msg_head + str_time + SPACE_STRING + 'orig_h=' \
            + str(msg.orig_h) + SPACE_STRING +'orig_p=' \
            + str(msg.orig_p) + SPACE_STRING + 'resp_h=' \
            + str(msg.resp_h) + SPACE_STRING + 'resp_p=' \
            + str(msg.resp_p)
  new_msg = new_msg + SPACE_STRING + 'proto=' + str(msg.proto) \
            + SPACE_STRING + 'trans_id=' + str(msg.trans_id) \
            + SPACE_STRING + 'query=' + str(msg.query) \
            + SPACE_STRING + 'qclass=' +str(msg.qclass)
  new_msg = new_msg + SPACE_STRING + 'qclass_name=' + str(msg.qclass_name) \
            + SPACE_STRING + 'qtype=' + str(msg.qtype) \
            + SPACE_STRING + 'qtype_name=' + str(msg.qtype_name) \
            + SPACE_STRING + 'rcode=' + str(msg.rcode)
  new_msg = new_msg + SPACE_STRING + 'rcode_name=' \
            + replace_str(str(msg.rcode_name)) + SPACE_STRING + 'AA=' \
            + replace_str(str(msg.AA)) + SPACE_STRING \
            + 'TC=' + replace_str(str(msg.TC)) + SPACE_STRING + 'RD=' \
            + replace_str(str(msg.RD))
  new_msg = new_msg + SPACE_STRING + 'Z=' + replace_str(str(msg.Z)) \
            + SPACE_STRING + 'answer=' + replace_str(str(msg.answer)) \
            + SPACE_STRING + 'TTLs=' + replace_str(str(msg.TTLs)) \
            + SPACE_STRING + 'rejected=' + replace_str(str(msg.rejected))
  print (new_msg)
  logger.warning(new_msg)

def send_http_syslog(msg):
  new_msg = 'id=' + str(SENSOR_ID) + ", type=http, biz=office, time="
  d = datetime.datetime.fromtimestamp(msg.time)
  str_time = d.strftime("%Y-%m-%d %H:%M:%S")
  new_msg = new_msg + str_time + SPACE_STRING
  new_msg = new_msg + 'orig_h=' + msg.orig_h + ", orig_p=" + str(msg.orig_p)
  new_msg = new_msg + ", resp_h=" + msg.resp_h + ", resp_p=" \
            + str(msg.resp_p)+", host= "+str(msg.host) + ", method="\
            + str(msg.method)+", url="+str(msg.uri)
  print new_msg
  logger.warning(new_msg)

def get_bro_logs(pcap):
  os.chdir(PATH_SYSLOG)
  os.popen('bro -C -r ' + pcap)
  # reading ftp.log
  if os.path.exists(ftp_path):
    df_ftp = pd.read_csv("ftp.log", skiprows=8, skipfooter=1,
                         sep=r"\t", engine='python')
    df_ftp.columns = ['time', 'uid', 'orig_h',
                      'orig_p', 'resp_h', 'resp_p',
                      'user', 'password', 'cmd',
                      'arg', 'mime_type',
                      'file_size',
                      'reply_code',
                      'reply_msg',
                      'data_channel_passive',
                      'data_channel_orig_h',
                      'data_channel_resp_h',
                      'data_channel_resp_p',
                      'fuid']

  # reading http.log
  if os.path.exists(http_path):
    df_http = pd.read_csv("http.log", skiprows=8, skipfooter=1,
                          sep=r"\t", engine='python')
    df_http.drop(df_http.columns[19], axis=1, inplace=True)
    df_http.columns = ['time', 'id', 'orig_h',
                       'orig_p', 'resp_h',
                       'resp_p','trans_depth',
                       'method', 'host','uri',
                       'referrer', 'user_agent',
                       'request_body_len',
                       'response_body_len',
                       'status_code','status_msg',
                       'info_code', 'info_msg',
                       'filename','username',
                       'password', 'proxied',
                       'orig_fuids',
                       'orig_mime_types',
                       'resp_fuids',
                       'resp_mime_types']

  # reading dns.log
  if os.path.exists(dns_path):
    df_dns = pd.read_csv("dns.log", skiprows=8, skipfooter=1,
                         sep=r"\t", engine='python')
    df_dns.columns = ['time','uid','orig_h',
                      'orig_p','resp_h','resp_p',
                      'proto','trans_id','query',
                      'qclass','qclass_name',
                      'qtype','qtype_name','rcode',
                      'rcode_name','AA','TC',
                      'RD','RA','Z','answer',
                      'TTLs','rejected']

  # reading conn.log
  if os.path.exists(conn_path):
    df_conn = pd.read_csv("conn.log", skiprows=8, skipfooter=1,
                          sep=r"\t", engine='python')
    df_conn.drop(df_conn.columns[-1], axis=1, inplace=True)
    df_conn.columns = ['time', 'id', 'orig_h',
                       'orig_p', 'resp_h', 'resp_p',
                       'proto', 'service', 'duration',
                       'orig_bytes', 'resp_bytes',
                       'conn_state', 'local_orig',
                       'local_resp', 'missed_bytes',
                       'history orig_pkts',
                       'orig_ip_bytes',
                       'resp_pkts',
                       'resp_ip_bytes',
                       'tunnel_parents']
    df_conn = df_conn.drop_duplicates()
    df_conn.sort_values(['time'], ascending=True, inplace=True)

  if os.path.exists(conn_path) is False:
    df_conn = pd.DataFrame()

  if os.path.exists(ftp_path) is False:
    df_ftp = pd.DataFrame()

  if os.path.exists(http_path) is False:
    df_http = pd.DataFrame()

  if os.path.exists(dns_path) is False:
    df_dns = pd.DataFrame()
  return df_conn, df_ftp, df_http, df_dns



def main():
  # 1. find all pcap files
  # 2. use Bro to get conn.log, ftp.log, dns.log, http.log
  # 3. send device information to syslog server
  # 4. send traffic information to syslog server
  # 5. send dns information to syslog server
  os.chdir(PATH_SYSLOG)
  while True:
    path = os.listdir(PATH_SYSLOG)
    path = sorted(path)
    for f in path:
      if os.path.splitext(f)[-1] == '.pcap' and f is not '.state':
        # sending device info
        list_df = get_bro_logs(f)
        if os.path.exists(conn_path) and not list_df[0].empty:
          list_df[0].apply(send_device_syslog, axis=1)
          print('--' * 100)
          # sending traffic info
          send_traffic_syslog(list_df[0])
          print('--' * 100)
        # sending dns info
        if os.path.exists(dns_path) and not list_df[3].empty:
          list_df[3].apply(send_dns_syslog, axis=1)
          os.remove(dns_path)
          print('--' * 100)
        # sending http info
        if os.path.exists(http_path) and not list_df[2].empty:
          list_df[2].apply(send_http_syslog, axis=1)
          os.remove(http_path)
          print('--' * 100)
        # sending ftp info
        if os.path.exists(ftp_path) and not list_df[1].empty:
          list_df[1].apply(send_ftp_syslog, axis=1)
          os.remove(ftp_path)
          print('--' * 100)
        os.remove(f)
  fh.close()

if __name__ == '__main__':
  main()

#syslog说明文档

## 设备信息

1. id : 设备标识符
2. type : syslog类型，默认为device
3. biz : 部门信息
4. time : 连接建立的时间
5. orig_h : 连接发起者的网络地址
6. orig_p : 连接发起者的端口号
7. proto : 应用依赖的传输层协议类型
8. resp_h : 连接响应者的网络地址
9. resp_p :  连接响应者的端口号

**example:**

id=monitor01, type=device, biz=office, time=2017-10-25 00:00:03, orig_h=172.16.0.1, orig_p=172.16.0.1, proto=tcp, resp_h=192.168.5.20, resp_p=25

## 流量信息

1. id: 设备标识符
2. type : syslog类型，默认为traffic
3. biz: 部门信息
4. time : 连接建立的时间
5. total : 连接建立过程的总流量
6. send : 连接发起者发送的流量信息
7. recv : 连接发起者收到的流量信息
8. tcp_send : tcp连接中发起者发送的流量信息
9. udp_send : udp连接中发起者发送的流量信息
10. icmp_send : icmp轮询过程中发起者发送的流量信息
11. tcp_recv : tcp连接中发起者收到的流量信息
12. udp_recv : udp连接中发起者收到的流量信息 
13. icmp_recv : icmp轮询过程中收到的流量信息

**example :**

id=monitor01, type=traffic, biz=office, time=2017-10-25 00:00:33, total=4.453Kbps, send=2.316Kbps, recv=2.137Kbps, tcp_send=2.179Kbps, udp_send=0.108Kbps, icmp_send=0.03Kbps, tcp_recv=2.052Kbps, udp_recv=0.06Kbps, icmp_recv=0.025Kbps

## 文件传输

1. id: 设备标识符
2. type : syslog类型，默认为ftp
3. biz: 部门信息
4. time: 连接建立的时间
5. orig_h : 连接发起者的网络地址
6. orig_p : 连接发起者的端口号
7. resp_h : 连接响应者的网络地址
8. resp_p : 连接响应者的端口号
9. user : 当前ftp会话中用户名
10. password : 当前ftp会话的密码，默认值是hidden
11. command : 用户发送的命令
12. arg : 命令参数
13. mine_type : 如果是文件传输命令，则使用Libmagic的文件类型
14. file_size : 传输文件的大小
15. reply_code : 服务器对命令的回复代码
16. reply_msg : 服务器对命令的回复信息
17. data_channel.passive : 预期的ftp数据通道
18. data_channel.resp_h : ftp响应者的网络地址
19. data_channel.resp_p : ftp响应者的端口号

**example :**

id=monitor01, type=ftp, biz=office, time=2009-04-20 11:28:34, orig_h=192.150.11.111, orig_p=36296, resp_h=98.114.205.102, resp_p=8884, user=1, password=hidden, command=RETR, arg=ftp://98.114.205.102/./ssms.exe, mime_type=application/x-dosexec, file_size=0, reply_code=150, reply_msg=Opening BINARY mode data connection, data_channel.passive=, data_channel.resp_h=, data_channel.resp_p=



## 域名解析

1. id: 设备标识符
2. type : syslog类型，默认为dns
3. biz: 部门信息
4. time: 连接建立的时间
5. orig_h : 连接发起者的网络地址
6. orig_p : 连接发起者的端口号
7. resp_h : 连接响应者的网络地址
8. resp_p : 连接响应者的端口号
9. proto : dns依赖的传输层协议类型
10. trans_id : 生成dns查询的程序分配的16位标识符，也用于匹配未完成查询的响应
11. query : dns查询的结果 
12. qclass : 该值指定dns查询类
13. qclass_name : 查询类的描述性名称
14. qtype : 该值指定dns查询类型
15. qtype_name : 查询类型的描述性名称
16. rcode_count : dns响应中的响应代码值
17. rcode_name : 响应代码值的描述性名称
18. AA : 响应信息的授权位指定响应的名称，服务器返回的域名是正确的
19. TC : 截断位指定消息被截断
20. RD : 请求消息中的递归标识位指示客户端需要此查询的递归服务
21. Z : 在查询和响应中通常为零的保留字段
22. answer : 查询结果中的一组资源描述信息
23. TTLs : 应答字段描述的RRs高速缓存间隔
24. rejected : 标识服务器是否拒绝DNS查询请求

**example :**

id=monitor01, type=dns, biz=office, time=2017-10-25 00:02:26, orig_h=192.168.5.230, orig_p=64026, resp_h=224.0.0.252, resp_p=5355, proto=udp, trans_id=63064, query=desktop-9qllhc6, qclass=1, qclass_name=C_INTERNET, qtype=255, qtype_name=*, rcode=-, rcode_name=, AA=F, TC=F, RD=F, Z=0, answer=, TTLs=, rejected=F

## 网络连接请求

1. id: 设备标识符
2. type: syslog类型，默认为http
3. biz: 部门信息
4. time : 连接建立的时间
5. orig_h : 连接发起者的网络地址
6. orig_p : 连接发起者的端口号
7. resp_h : 连接响应者的网络地址
8. resp_p : 连接响应者的端口号
9. host : HOST请求的头部信息
10. method : http的请求方式
11. url : 请求使用的url
12. referrer : referrer的头部值
13. version : 请求版本的部分值
14. user_agent : 来自客户端user-agent的头部信息
15. request_body_len : 从客户端传输数据的实际未压缩内容的大小
16. response_body_len : 从服务器传输数据的实际未压缩内容大小
17. status_code : 服务器返回的状态码
18. status_msg : 服务器返回的状态信息
19. info_code : 上次服务器返回的1xx信息回复代码
20. info_msg :  上次服务器返回的1xx信息回复消息
21. tags : 发现各种属性的一系列指标，并与特定的请求/响应对相关联
22. username :  如果执行基本的授权请求，则需要用户名
23. password : 如果执行基本的授权请求，则需要密码
24. capture_password : 确定是否为此请求捕获密码
25. proxied : 如果请求被代理，所有头部信息都会显示
26. range_request  : 指示该请求是否可以承受响应内容包含206个部分
27. orig_fuids : 文件id的有序向量
28. orig_filenames : 来自客户端的有序的文件名向量
29. orig_mime_types : 一个有序的MIME类型的向量
30. resp_fuids : 文件id的有序向量。
31. resp_filenames : 来自服务器的有序的文件名向量
32. resp_mime_types : 一个有序的MIME类型的向量
33. current_enity : 当前实体
34. orig_mime_depth : HTTP请求消息正文中当前MIME的实体数目
35. resp_mime_depth : HTTP响应消息正文中当前MIME的实体数目
36. client_header_names : 由客户端发送的http头部名称向量，仅包含头部名称不包含值
37. server_header_names : 由服务器发送的http头部名称向量，仅包含头部名称不包含值
38. omniture : 表明服务器是否是真正的广告服务器
39. flash_version : 未能解析的flash版本号
40. cookie_vars : 从所有cookie中提取的变量名称
41. uri_vars : 来自URI的变量名称

**example :**

id=monitor01, type=http, biz=office, time=2017-10-25 00:06:02, orig_h=20.4.1.103, orig_p=52701, resp_h=192.168.5.141, resp_p=81, host= 192.168.5.141, method=POST, url=/cloudquery.php
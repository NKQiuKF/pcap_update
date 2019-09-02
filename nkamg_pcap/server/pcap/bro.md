# Bro支持的应用层协议说明文档

## 1. ftp.log

**协议说明:**

FTP 是File Transfer Protocol（[文件传输协议](https://baike.baidu.com/item/%E6%96%87%E4%BB%B6%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE)）的英文简称，而中文简称为“文传协议”。用于Internet上的[控制文件](https://baike.baidu.com/item/%E6%8E%A7%E5%88%B6%E6%96%87%E4%BB%B6)的双向传输。同时，它也是一个[应用程序](https://baike.baidu.com/item/%E5%BA%94%E7%94%A8%E7%A8%8B%E5%BA%8F)（Application）。基于不同的操作系统有不同的FTP应用程序，而所有这些应用程序都遵守同一种协议以传输文件。在FTP的使用当中，用户经常遇到两个概念："下载"（Download）和"上传"（Upload）。"下载"文件就是从远程主机拷贝文件至自己的计算机上；"上传"文件就是将文件从自己的计算机中拷贝至远程主机上。用Internet语言来说，用户可通过客户机程序向（从）远程主机上传（下载）文件。

| 字段                      |             含义             |
| :---------------------- | :------------------------: |
| 1. ts                   |          命令发出的时间           |
| 2. uid                  |           连接的标识符           |
| 3. id                   |          网络地址/端口号          |
| 4.user                  |        当前ftp会话中用户名         |
| 5. password             |   当前ftp会话的密码，默认值是hidden    |
| 6. command              |          用户发送的命令           |
| 7. arg                  |            命令参数            |
| 8. mine_type            | 如果是文件传输命令，则使用Libmagic的文件类型 |
| 9. file_size            |          传输文件的大小           |
| 10. reply_code          |        服务器对命令的回复代码         |
| 11. reply_msg           |        服务器对命令的回复信息         |
| 12.data_channel         |         预期的ftp数据通道         |
| 13. cwd                 |        会话现在所在的工作目录         |
| 14. cmdarg              |         正在等待响应的命令          |
| 15. pending_commands    |      已经发送但是未收到响应的命令队列      |
| 16. passive             |        指示会话正处于活跃的模式        |
| 17. capture_password    |        确定是否为此请求捕获密码        |
| 18. fuid                |          文件的唯一标识符          |
| 19. last_auth_requested |          最后的验证请求           |

**example :**

ts=1508945587.967300, uid=CX8sqk1JwQWsZYGWyk, id.orig_h=192.168.5.20, id.orig_p=41874, id.resp_h=192.168.5.77, id.resp_p=21,  user=eyou, password=<hidden>, command=PASV, arg=	-, mime_type=-, file_size=-, reply_code=227, reply_msg=Entering Passive Mode, data_channel= (192,168,5,77,20,206)	passive=T, data_channel.orig_h=192.168.5.20, 	data_channel.resp_h=192.168.5.77	data_channel.resp_p=5326 ,fuid=-

## 2. dns.log

**协议说明:**

DNS（Domain Name System，域名系统），因特网上作为域名和[IP地址](https://baike.baidu.com/item/IP%E5%9C%B0%E5%9D%80)相互映射的一个[分布式数据库](https://baike.baidu.com/item/%E5%88%86%E5%B8%83%E5%BC%8F%E6%95%B0%E6%8D%AE%E5%BA%93)，能够使用户更方便的访问[互联网](https://baike.baidu.com/item/%E4%BA%92%E8%81%94%E7%BD%91)，而不用去记住能够被机器直接读取的IP数串。通过[主机](https://baike.baidu.com/item/%E4%B8%BB%E6%9C%BA)名，最终得到该主机名对应的IP地址的过程叫做域名解析（或主机名解析）。DNS协议运行在[UDP](https://baike.baidu.com/item/UDP)协议之上，使用端口号53。

| 字段                |                含义                 |
| ----------------- | :-------------------------------: |
| 1. ts             |        dns协议信息最早出现在连接上的时间         |
| 2. uid            |          正在传输dns数据连接的标识符          |
| 3. id             |             网络地址/端口号              |
| 4. proto          |             连接的传输层协议              |
| 5. trans_id       | 生成dns查询的程序分配的16位标识符，也用于匹配未完成查询的响应 |
| 6. rtt            |           一次查询和响应的往返时间            |
| 7. query          |             dns查询的结果              |
| 8. qclass         |            该值指定dns查询类             |
| 9. qclass_name    |             查询类的描述性名称             |
| 10. qtype         |            该值指定dns查询类型            |
| 11. qtype_name    |            查询类型的描述性名称             |
| 12. rcode_count   |           dns响应中的响应代码值            |
| 13. rcode_name    |            响应代码值的描述性名称            |
| 14. AA            |   响应信息的授权位指定响应的名称，服务器返回的域名是正确的    |
| 15. TC            |            截断位指定消息被截断             |
| 16. RD            |    请求消息中的递归标识位指示客户端需要此查询的递归服务     |
| 17. Z             |         在查询和响应中通常为零的保留字段          |
| 18. answer        |          查询结果中的一组资源描述信息           |
| 19.TTLs           |         应答字段描述的RRs高速缓存间隔          |
| 20. rejected      |         标识服务器是否拒绝DNS查询请求          |
| 21. total_answers |         回复消息的应答部分中的资源记录总数         |
| 22. total_replies |      回复消息的应答、权限和其他部分中的资源记录总数      |
| 23. saw_query     |           是否查看完整的DNS查询            |
| 24. saw_reply     |           是否查看完整的DNS应答            |
| 25. auth          |             查询的权威性响应              |
| 26. addl          |              查询的其他响应              |

**example :**

ts=1508947205.209799, uid=CKMFTD26Xh69hGxKNk, id.orig_h=192.168.5.51, id.orig_p=137, 	id.resp_h=192.168.5.255, id.resp_p=137, proto=udp, trans_id=37358, query=WIN-OGOR7CDLG2M, qclass=1      qclass_name=C_INTERNET, qtype=32, qtype_name=NB, rcode=-, rcode_name=-, AA=F	, TC=F, RD=T, RA=F, 	Z=1, answer=-, TTLs=-, rejected=F

## 3. http.log

**协议说明:**

[超文本传输协议](https://baike.baidu.com/item/%E8%B6%85%E6%96%87%E6%9C%AC%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE)（HTTP，HyperText Transfer Protocol)是[互联网](https://baike.baidu.com/item/%E4%BA%92%E8%81%94%E7%BD%91)上应用最为广泛的一种[网络协议](https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E5%8D%8F%E8%AE%AE)。所有的[WWW](https://baike.baidu.com/item/WWW)文件都必须遵守这个标准。设计HTTP最初的目的是为了提供一种发布和接收[HTML](https://baike.baidu.com/item/HTML)页面的方法。

| 字段                      |              含义               |
| :---------------------- | :---------------------------: |
| 1. time                 |            请求发起的时间            |
| 2. uid                  |             连接标识符             |
| 3. id                   |           网络地址/端口号            |
| 4. trans_depth          |      表示此请求/响应事务连接中的流水线深度      |
| 5. method               |           http的请求方式           |
| 6. host                 |         HOST请求的头部信息值          |
| 7. url                  |           请求使用的url            |
| 8. referrer             |         referrer的头部值          |
| 9. version              |           请求版本的部分值            |
| 10. user_agent          |     来自客户端user-agent的头部信息      |
| 11. request_body_len    |      从客户端传输数据的实际未压缩内容的大小      |
| 12. response_body_len   |      从服务器传输数据的实际未压缩内容大小       |
| 13. status_code         |           服务器返回的状态码           |
| 14. status_msg          |          服务器返回的状态信息           |
| 15. info_code           |       上次服务器返回的1xx信息回复代码       |
| 16. info_msg            |       上次服务器返回的1xx信息回复消息       |
| 17. tags                |  发现各种属性的一系列指标，并与特定的请求/响应对相关联  |
| 18. username            |      如果执行基本的授权请求，则需要用户名       |
| 19. password            |       如果执行基本的授权请求，则需要密码       |
| 20. capture_password    |         确定是否为此请求捕获密码          |
| 21. proxied             |      如果请求被代理，所有头部信息都会显示       |
| 22. range_request       |    指示该请求是否可以承受响应内容包含206个部分    |
| 23. orig_fuids          |           文件id的有序向量           |
| 24. orig_filenames      |        来自客户端的有序的文件名向量         |
| 25. orig_mime_types     |        一个有序的MIME类型的向量         |
| 26. resp_fuids          |           文件id的有序向量           |
| 27. resp_filenames      |        来自服务器的有序的文件名向量         |
| 28. resp_mime_types     |        一个有序的MIME类型的向量         |
| 29. current_enity       |             当前实体              |
| 30. orig_mime_depth     |    HTTP请求消息正文中当前MIME的实体数目     |
| 31. resp_mime_depth     |    HTTP响应消息正文中当前MIME的实体数目     |
| 32. client_header_names | 由客户端发送的http头部名称向量，仅包含头部名称不包含值 |
| 33. server_header_names | 由服务器发送的http头部名称向量，仅包含头部名称不包含值 |
| 34. omniture            |       表明服务器是否是真正的广告服务器        |
| 35. flash_version       |         未能解析的flash版本号         |
| 36. cookie_vars         |       从所有cookie中提取的变量名称       |
| 37. uri_vars            |           URI的变量名称            |

**example :**

ts=1508947203.079291, uid=Cehzac1LiCz9Ov6tn4, id.orig_h=202.102.85.24, id.orig_p=65522, id.resp_h=192.168.5.45, id.resp_p=80, trans_depth=1, method=GET, host=www.tj.gov.cn	url=/tj/tj/lydt/201604/W020160407389463997395.jpg	, referrer=-, user_agent=Mozilla/4.0(compatible; MSIE 6.0; Starbird; ),  request_body_len=0, response_body_len=39739, status_code=200,status_msg=OK, info_code=-, info_msg=-, filename=-, tags=(empty), username=-, password=-, proxied=X-FORWARDED-FOR -> 221.12.123.74,X-FORWARDED-FOR -> 202.102.85.24, orig_fuids=-, orig_mime_types=-, 	resp_fuids=Fyjx6gdIGnuhdjSlh, resp_mime_types=image/jpeg

## 4. irc.log##

**协议说明:**

[IRC](https://baike.baidu.com/item/IRC/10410) 协议在使用 [TCP/IP](https://baike.baidu.com/item/TCP%2FIP/214077) [网络协议](https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E5%8D%8F%E8%AE%AE)的系统上开发，然而它并没有要求TCP/IP 是其唯一的运行环境。IRC 是一种文本协议，它仅要求用户有一简单端口程序能与服务器连接。

| 字段                |      含义       |
| :---------------- | :-----------: |
| 1. ts             |  当命令开始执行的时间戳  |
| 2. uid            |    连接的标识符     |
| 3. id             | 端点主机的网络地址和端口号 |
| 4. nick           |     连接的昵称     |
| 5.user            |   为连接建立的用户名   |
| 6. command        |   客户端给出的命令    |
| 7. value          |   客户端给出命令的值   |
| 8. addl           |  命令执行需要的其他值   |
| 9. dcc_file_name  |   请求的ddc文件名   |
| 10. dcc_file_size | 发送方指定dcc传输的大小 |
| 11. dcc_mime_type |  嗅探mime类型的文件  |
| 12. fuid          |   文件的唯一标识符    |

**Example:**



## 5. smtp.log##

**协议说明:**

SMTP（Simple Mail Transfer Protocol）即[简单邮件传输协议](https://baike.baidu.com/item/%E7%AE%80%E5%8D%95%E9%82%AE%E4%BB%B6%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE),它是一组用于由源地址到目的地址传送[邮件](https://baike.baidu.com/item/%E9%82%AE%E4%BB%B6)的规则，由它来控制信件的中转方式。[SMTP协议](https://baike.baidu.com/item/SMTP%E5%8D%8F%E8%AE%AE)属于[TCP/IP协议簇](https://baike.baidu.com/item/TCP%2FIP%E5%8D%8F%E8%AE%AE%E7%B0%87)，它帮助每台[计算机](https://baike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA)在发送或中转信件时找到下一个目的地。通过SMTP协议所指定的[服务器](https://baike.baidu.com/item/%E6%9C%8D%E5%8A%A1%E5%99%A8),就可以把E-mail寄到收信人的服务器上了。

| 字段                        |              含义              |
| ------------------------- | :--------------------------: |
| 1.ts                      |         数据第一次出现的时间戳          |
| 2. uid                    |           连接的唯一标识符           |
| 3. id                     |         端点的网络地址和端口号          |
| 4. trans_depth            | 在一个连接中传输多个消息的一个计数来表示此消息事务的深度 |
| 5. helo                   |          helo头部的内容           |
| 6. mailfrom               |        From头部的Email地址        |
| 7. rcptto                 |        Rcpt头部的Email地址        |
| 8. date                   |          Data头部的内容           |
| 9. from                   |          From头部的内容           |
| 10. to                    |           To头部的内容            |
| 11. cc                    |           CC头部的内容            |
| 12. reply_to              |         Replyto头部的内容         |
| 13. msg_id                |          MsgID头部的内容          |
| 14. in_reply_to           |       In-Reply-To头部的内容       |
| 15. subject               |         Subject头部的内容         |
| 16. x_originating         |    X-Originating-IP头部的内容     |
| 17. first_received        |         第一次收到的头部的内容          |
| 18. second_received       |         第二次收到的头部的内容          |
| 19. last_reply            |        服务器发送给客户端的最新消息        |
| 20. path                  |         从头部提取的信息传输路径         |
| 21. user_agent            |     来自客户端的User-Agent头部的值     |
| 22. tls                   |         表明连接会被切换到TLS         |
| 23. process_received_from |   表明是否应该处理Received:from的头部   |
| 24. has_client_activity   |     指示是否已经看到客户端的活动，但未做记录     |
| 25. entity                |           当前被发现的实体           |
| 26. fuids                 |       附加到消息的文件标识符的有序向量       |
| 27. is_webmail            |    指明信息是否是通过webmail界面发送的     |

**Example:**

ts=1508947153.398518 uid=ClYbBV1Auez5SSxB4j id.orig_h=172.16.0.1	id.orig_p=57678	id.resp_h=192.168.5.20, id.resp_p=25,trans_depth=1, helo=tj.gov.cn, mailfrom=<george@wmz.com>, rcptto=<zxyj@tj.gov.cn>, date=-, from=-, to=-, reply_to=-, msg_id=-, in_reply_to=-, subject=-, x_originating_ip=-, first_received=-, second_received=-, last_reply=421 semf01.mfg.siteprotect.com lost input connection, path=64.26.60.153,192.168.5.20,  user_agent=-, tls=F, fuids=(empty)

## 6. ssh.log##

**协议说明:**

SSH 为建立在应用层基础上的安全协议。SSH 是目前较可靠，专为[远程登录](https://baike.baidu.com/item/%E8%BF%9C%E7%A8%8B%E7%99%BB%E5%BD%95)会话和其他网络服务提供安全性的协议。利用 SSH 协议可以有效防止远程管理过程中的信息泄露问题。

| 字段                  |             含义              |
| ------------------- | :-------------------------: |
| 1. ts               |         ssh连接开始的时间          |
| 2. uid              |           连接的标识符            |
| 3. id               |        端点主机的网络地址和端口号        |
| 4. version          |        ssh的版本号(1或者2)        |
| 5. auth_success     | 授权结果(T表示成功，F表示失败，unset表示未知) |
| 6. auth_attempts    |           授权尝试的次数           |
| 7. direction        |            连接的方向            |
| 8. client           |          客户端版本号字串           |
| 9. server           |          服务器版本号字串           |
| 10. cipher_alg      |          当前使用的加密算法          |
| 11. mac_alg         |       当前使用的签名(MAC)算法        |
| 12. compression_alg |         当前正在使用的压缩算法         |
| 13. kex_alg         |        当前正在使用的密钥交换算法        |
| 14. host_key_alg    |         服务器主机密钥的算法          |
| 15. host_key        |          服务器的指纹密钥           |
| 16. logged          |             可选              |
| 17. capabilities    |             可选              |
| 18. analyzer_id     |             可选              |
| 19. remote_location |     添加与连接的“远程”主机相关的地理数据     |

**Example:**

ts=1508913692.909269, uid=CqVgjD3F1Q2Z2niBG9, id.orig_h=20.4.3.102, id.orig_p=54973, id_resp_h=192.168.5.3, id_resp_p=22,version=2, auth_success=-, direction=-, client=SSH-2.0-PuTTY_0_69_CN_Build, server=SSH-2.0-OpenSSH_5.3, cipher_alg=aes128-ctr, mac_alg=hmac-md5, compression_alg=none, kex_alg=diffie-hellman-group-exchange-sha256, host_key_alg=ssh-rsa, host_key=-



## 7. ssl.log##

**协议说明:**

| 字段                                       |                 含义                  |
| ---------------------------------------- | :---------------------------------: |
| 1. ts                                    |           第一次检测到ssl连接的时间            |
| 2. uid                                   |               连接的标识符                |
| 3. id                                    |            端点主机的网络地址和端口号            |
| 4. version_num                           |          服务器选择ssl/tls的版本数量          |
| 5. cipher                                |          服务器选择的ssl/tls密码套件          |
| 6. curve                                 |     使用ECDH / ECDHE时服务器选择的椭圆曲线。      |
| 7. server_name                           |       服务器名称指示符的值，指客户端请求的服务器名        |
| 8. session_id                            |       客户端提供的会话id用于会话恢复，不用于记录        |
| 9. resumed                               |        标志是否重用较早连接中交换的密钥来恢复会话        |
| 10. client_ticket_empty_session_seen     |     标志是否看到客户端使用一个空会话id发送一个非空的会话     |
| 11. client_key_exchange_seen             |         标志是否看到客户端发送一个密钥交换信息         |
| 12. server_appdata                       | 为了跟踪服务器是否已经为tls 1.3 发送了应用程序数据包，从而计数 |
| 13.client_appdata                        |   标志、跟踪客户端是否已经为tls 1.3 发送了应用程序数据包   |
| 14. last_alert                           |            连接期间的最后一次警报信息            |
| 15. next_protocol                        |       服务器选择的下一个协议用应用层的下一个协议扩展       |
| 16. analyzer_id                          |       分析器id用于与每个连接相互关联的分析器实例        |
| 17. established                          |           标志ssl会话是否被成功的创建           |
| 18. logged                               |           标志该记录是否已经被记录下来            |
| 19. delay_tokens                         |                                     |
| 20. cert_chain                           |        服务器提供的证书链用来验证其完整的签名链         |
| 21. cert_chain_fuids                     |        服务器提供证书的所有证书文件ID的有序向量        |
| 22. client_cert_chain                    |        客户端提供的证书链用于验证其完整的签名链         |
| 23. client_cert_chain_fuids              |        客户端提供证书的所有证书文件ID的有序向量        |
| 24. subject                              |          由服务器提供的X.509证书的主体          |
| 25. issuer                               |        对由服务器提供的X.509证书的签名者主体        |
| 26. client_subject                       |          客户端提供的X.509证书的主体           |
| 27.client_issuer                         |        对由客户端提供的X.509证书的签名者主体        |
| 28. server_depth                         |       当前从任意一方看到的证书数目，用于创建文件句柄       |
| 29. client_depth                         |                 可选                  |
| 30.last_originator_hearbeat_request_size |                 可选                  |
| 31.last_responder_hearbeat_request_size  |                 可选                  |
| 32. originator_heartbeats                |                 可选                  |
| 33. responder_heartbeats                 |                 可选                  |
| 34. heartbleed_detected                  |                 可选                  |
| 35. enc_appdata_packages                 |                 可选                  |
| 36. enc_appdata_bytes                    |                 可选                  |
| 37. validation_status                    |             该连接的证书验证结果              |
| 38. ocsp_status                          |            该连接的ocsp的验证结果            |
| 39. ocsp_response                        |           以字符串的形式进行ocsp响应           |
| 40. notary                               |                 可选                  |

**Example:**

ts=1508947208.327025, uid=C3MQyR138308kgbDF, id.orig_h=218.69.8.30, id.orig_p=64503, id.resp_h=192.168.5.21, id.resp_p=443,  version=TLSv10, cipher=TLS_RSA_WITH_RC4_128_SHA, curve=-, server_name=-, resumed=F, last_alert=-, next_protocol=-, established=T,cert_chain_fuids=FecsuE14p9XOgxPgod,FxkbGo3wNX7ILgOEI2, client_cert_chain_fuids=(empty), subject=CN=10.0.0.1,OU=vpn,O=SecWorld,L=Beijing,ST=BJ,C=CN,issuer=CN=gateway,OU=vpn,O=SecWorld,L=Beijing,ST=BJ,C=CN, client_subject=-, client_issuer=-




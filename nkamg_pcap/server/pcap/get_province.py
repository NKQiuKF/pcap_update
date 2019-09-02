#coding:utf-8

import requests
def get_province_code(ip):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    response = requests.get("http://ip.taobao.com/service/getIpInfo.php?ip="+ip,headers = headers)
    content = eval(response.text)
    province = content['data']['region']
    code_province = {"北京":"CN-01","天津":"CN-02","河北":"CN-03","山西":"CN-04","内蒙古":"CN-05","辽宁":"CN-06","吉林":"CN-07","黑龙江":"CN-08","上海":"CN-09","江苏":"CN-10","浙江":"CN-11","安徽":"CN-12","福建":"CN-13","江西":"CN-14","山东":"CN-15","河南":"CN-16","湖北":"CN-17","湖南":"CN-18","广东":"CN-19","广西":"CN-20","海南":"CN-21","重庆":"CN-22","四川":"CN-23","贵州":"CN-24","云南":"CN-25","西藏":"CN-26","陕西":"CN-27","甘肃":"CN-28","青海":"CN-29","宁夏":"CN-30","新疆":"CN-31","香港":"CN-32","台湾":"CN-33","澳门":"CN-34"}
    return code_province.get(province,province)
